import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
#pyside2-uic questa_sim_configurator_gui.ui -o questa_sim_configurator_gui.py
from PySide2.QtWidgets import QApplication, QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox, QTableWidgetItem
from PySide2.QtWidgets import *
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt, QTimer
import threading
from configparser import ConfigParser, ExtendedInterpolation
import xml.etree.ElementTree as ET
import shutil
from datetime import datetime
#  import os.path
import argparse
from os import path
import subprocess
import sys
import os
import ntpath
from glob import glob
import getpass
from utils import task
from functools import partial
import re
import random
from pathlib import Path
from gui.questasim_configurator_gui import Ui_MainWindow # Modified by Ayala
from DPI.dpi_manager import DPI_manager # Added by Ayala
from RegressionUtils.GenericsManager import GenericsManager # Added by Ayala
import utils
from RegressionUtils.FileManager import get_next_line_in_file
from gui.constants_gui import ConstantsDialog
from utils.parse_constants import update_all_vhdl_from_config

parser = argparse.ArgumentParser()
config = ConfigParser(interpolation=ExtendedInterpolation())
config_default = ConfigParser(interpolation=ExtendedInterpolation())
vrc_ver=os.path.basename(os.path.dirname(__file__))
commited = False

parser.add_argument("--QSIM_GUI", "-qgui",default="0", help="use '-qgui 1' if you run vrc from mentor gui")
parser.add_argument("--TOOL", "-t",default="questa", help="use '-t questa in QSIM_GUI we need to which tool call me questa/vrun")
parser.add_argument("--PIPELINE", "-p",default="0", help="use '-p 1' if you run vrc in pipeline mode")
parser.add_argument("--JOBS", "-j",default="NULL", help="use '-j 5' in vrun mode if you want 5 jobs to run")
parser.add_argument("--SEED", "-s",default="NULL", help="use '-s 98724974' when you want your seed to be 98724974 for exemple")
parser.add_argument("--TESTPLAN", "-tp",default="NULL", help="use '-tp testplan.xml' to deliver your test plan to vrc")
parser.add_argument("--TESTLIST", "-tl",default="NULL", help="use '-tl testlist.tl' to deliver your test list to vrc")
parser.add_argument("--BATCH", "-b",default="0", help="use '-b 1' to run vrc in batch mode and questa batch mode")
parser.add_argument("--BUILD_DESIGN", "-bd",default="0", help="use '-bd 1' to build design automatically - relevant only in batch mode")


def message_handler(mode, context, message):
    pass
def redirect_qt_messages():
    QtCore.qInstallMessageHandler(message_handler)
# Read arguments from the command line
args = parser.parse_args()

class main_gui_window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = config  # Make config available as an instance attribute
        self.ui = Ui_MainWindow()  # connect to the gui from the designer
        self._translate = QtCore.QCoreApplication.translate
        self.ui.setupUi(self)  # set up the gui

        # init path to use them over the code
        self.questa_path = None
        self.vrc_path = None
        self.qvip_path = None
        self.visualizer_path = None
        self.py_path = None
        self.config_path = None
        self.qsub = ""
        self.os_name = ""
        self.num_of_test_show = 0
        self.reg_test_line = []
        self.reg_seed_line = []
        self.reg_num_of_test_line = []
        self.test_frame = []
        self.abs_path_string=""
        self.file_path=""
        self.dpi_files_paths=set() # set of all DPI file paths
        # set paths according to the os
        self.init_path = os.environ["PATH"]

        # set the paths according to the different servers
        self.set_path()
        # gui upload
        self.gui_first_upload()
       

        self.ui.ok_cancel_buttun.accepted.connect(self.exec)
        self.ui.ok_cancel_buttun.rejected.connect(self.exit)

        # combo box
        self.ui.verbosity_combo_bt.activated.connect(self.get_verbosity)
        self.ui.questa_ver_combo_bt.activated.connect(self.get_questa_ver)
        self.ui.visualizer_ver_combo_bt.activated.connect(self.get_visualizer_ver)
        self.ui.vrun_ver_combo_bt.activated.connect(self.get_vrun_ver)
        self.ui.vrc_ver_combo_bt.activated.connect(self.vrc_ver_combo_bt)
        self.ui.qvip_ver_combo_bt.activated.connect(self.qvip_ver_combo_bt)


        self.ui.Dark.valueChanged.connect(self.set_stylesheet)

        # actions
        self.ui.actionLoadConfig.triggered.connect(self.config_name_push_bt)
        self.ui.actionSaveConfig.triggered.connect(self.save_config)
        self.ui.actionCangeDir.triggered.connect(self.chang_dir)
        self.ui.actionConstant_Override.triggered.connect(self.constant_override)
        self.ui.actionBuild_design.triggered.connect(self.build_design)
        self.ui.actionSuper_Env.triggered.connect(self.actionSuper_Env)
        self.ui.actionCreate_Env.triggered.connect(self.actionCreate_Env)
        self.ui.actionCreate_Project.triggered.connect(self.actionCreate_Project)
        self.ui.actionArtifactory.triggered.connect(self.actionArtifactory)
        self.ui.actionReport_Bugs_Featuers.triggered.connect(self.report_bugs_features)
        self.ui.actionCheck_Bugs.triggered.connect(self.check_bugs)
        self.ui.gitGraph.triggered.connect(self.gitGraph)
        self.ui.gitGraphDsigen.triggered.connect(self.gitGraphDsigen)
        self.ui.cloneRepo.triggered.connect(self.cloneRepo)
        self.ui.actionRUVM.triggered.connect(self.actionRUVM)

        # line connect
        # main tab
        self.ui.seed_line.textEdited.connect(self.seed_line)
        self.ui.test_line.textEdited.connect(self.test_line)
        self.ui.config_name_line.textEdited.connect(self.config_name_line)
        self.ui.run_time_line.textEdited.connect(self.run_time_line)

        # DPI tab buttons (Modified by Ayala)
        self.ui.add_dpi_button.clicked.connect(self.add_files_to_list)
        self.ui.clear_button.clicked.connect(self.remove_file_list)
        
        # advanced tab
        self.ui.tb_line.textEdited.connect(self.tb_line)
        self.ui.modelsimini_line.textEdited.connect(self.modelsimini_line)
        self.ui.testplan_line.textEdited.connect(self.testplan_line)
        self.ui.wave_line.textEdited.connect(self.wave_line)
        self.ui.work_dir_line.textEdited.connect(self.work_dir_line)

        self.ui.compile_design_line.textEdited.connect(self.compile_design_line)
        self.ui.compile_vips_line.textEdited.connect(self.compile_vips_line)
        self.ui.compile_env_line.textEdited.connect(self.compile_env_line)
        self.ui.post_compile_line.textEdited.connect(self.post_compile_line)
        self.ui.pre_compile_line.textEdited.connect(self.pre_compile_line)

        self.ui.opt_libs_line.textEdited.connect(self.opt_libs_line)
        self.ui.opt_genenv_line.textEdited.connect(self.opt_genenv_line)
        self.ui.opt_defualt_line.textEdited.connect(self.opt_defualt_line)
        self.ui.opt_debug_line.textEdited.connect(self.opt_debug_line)
        self.ui.opt_visualizer_line.textEdited.connect(self.opt_visualizer_line)
        self.ui.opt_codecov_line.textEdited.connect(self.opt_codecov_line)

        self.ui.vsim_codecov_line.textEdited.connect(self.vsim_codecov_line)
        self.ui.vsim_debug_line.textEdited.connect(self.vsim_debug_line)
        self.ui.vsim_defualt_line.textEdited.connect(self.vsim_defualt_line)
        self.ui.vsim_visualizer_line.textEdited.connect(self.vsim_visualizer_line)
        self.ui.vsim_dpi_textbox.textEdited.connect(self.vsim_dpi_line)

        # button connect
        self.ui.clear_work_bt.toggled.connect(self.clear_work_bt)
        self.ui.new_trans_bt.toggled.connect(self.new_trans_bt)
        self.ui.save_wave_bt.toggled.connect(self.save_wave_bt)
        self.ui.close_gui_bt.toggled.connect(self.close_gui_bt)

        # self.ui.TBD.toggled.connect(self.clear_work_bt)
        self.ui.visualizer_bt.toggled.connect(self.visualizer_bt)
        self.ui.questasim_bt.toggled.connect(self.questasim_bt)
        self.ui.vrun_bt.toggled.connect(self.vrun_bt)
        self.ui.debug_mode_bt.toggled.connect(self.debug_mode_bt)
        self.ui.code_cov_bt.toggled.connect(self.code_cov_bt)
        self.ui.gui_bt.toggled.connect(self.gui_bt)
        self.ui.dummy_dut_bt.toggled.connect(self.dummy_dut_bt)


        self.ui.pre_comp_bt.toggled.connect(self.pre_comp_bt)
        self.ui.comp_design_bt.toggled.connect(self.comp_design_bt)
        self.ui.compile_env_bt.toggled.connect(self.compile_env_bt)
        self.ui.comp_vips_bt.toggled.connect(self.comp_vips_bt)
        self.ui.comp_dpi_bt.toggled.connect(self.comp_dpi_bt)
        self.ui.post_compile_bt.toggled.connect(self.post_compile_bt)
        self.ui.opt_bt.toggled.connect(self.opt_bt)
        self.ui.simulate_bt.toggled.connect(self.simulate_bt)

        self.ui.test_bt.clicked.connect(self.test_bt)
        self.ui.tb_bt.clicked.connect(self.tb_bt)
        self.ui.config_name_push_bt.clicked.connect(self.config_name_push_bt)
        self.ui.load_tool_bt.clicked.connect(self.load_tool_bt)
        self.ui.libraries_push_bt.clicked.connect(self.libraries_push_bt)
        self.ui.compile_design_push_bt.clicked.connect(self.compile_design_push_bt)
        self.ui.compile_env_push_bt.clicked.connect(self.compile_env_push_bt)

        # reg connect
        
        self.ui.RankPushBut.clicked.connect(self.RankPushBut)
        self.ui.TestNamePushButton.clicked.connect(self.TestNamePushButton)
        self.ui.testplan_bt.clicked.connect(self.testplan_bt)
        self.ui.triage_bt.toggled.connect(self.triage_bt)
        self.ui.grid_bt.toggled.connect(self.grid_bt)
        self.ui.trend_bt.toggled.connect(self.trend_bt)
        self.ui.report_bt.toggled.connect(self.report_bt)
        self.ui.mail_bt.toggled.connect(self.mail_bt)
        self.ui.delete_vrmdata_bt.toggled.connect(self.delete_vrmdata_bt)
        self.ui.rerun_bt.toggled.connect(self.rerun_bt)
        self.ui.jobs_combo_bt.activated.connect(self.jobs_combo_bt)
        
        ########################### Added by Ayala
        # Generics
        self.genericsManager = GenericsManager(self)
        self.ui.add_generics_sets_button.clicked.connect(self.choose_generics_sets_button)
        self.ui.add_generics_sets_button.setEnabled(False)
        self.ui.clear_generics_table_button.setEnabled(False)
        self.ui.clear_generics_table_button.clicked.connect(self.clear_generics_table)
        self.ui.definesPushButton.clicked.connect(self.choose_defines_button)

        
        # DPI stuff
        self.dpi = DPI_manager(self.python_alias) # instantiate DPI manager
        self.ui.dpi_help_push_button.clicked.connect(self.dpi_help_push_button)
        self.ui.vsim_dpi_label.setToolTip("DPI simulation commands")
        self.ui.vsim_dpi_textbox.setToolTip("DPI simulation commands (e.g. -sv_lib mySharedObject)" if config['OPT_VSIM_ARGS']['VSIM_DPI_ARGS'] == "" else config['OPT_VSIM_ARGS']['VSIM_DPI_ARGS'])
        self.ui.dpi_load_template_push_button.clicked.connect(self.dpi_load_template_push_button)
        self.setAttribute(QtCore.Qt.WA_AlwaysShowToolTips, True)
        
        # Breakpoint
        self.ui.debug_break_cb.toggled.connect(self.debug_break_cb)
        self.ui.debug_config_db.toggled.connect(self.debug_config_db)
        ###########################
    
    def dpi_load_template_push_button(self):
        if sys.platform.startswith("linux"):
            file_path = f'{self.vrc_path}{vrc_ver}/DPI/pysv_template.py'
            os.system(f'xdg-open "{file_path}"')
            
    def dpi_help_push_button(self):
        if sys.platform.startswith("linux"):
            python_help_pdf_file_path = f'{self.vrc_path}{vrc_ver}/utils/Running_Python_Code_in_Systemverilog.pdf'
            os.system(f'xdg-open "{python_help_pdf_file_path}"') # maybe only works with linux
    
    def clear_generics_table(self):
        self.genericsManager.clear_generics_table()
        self.ui.clear_generics_table_button.setEnabled(False)
        
    def choose_defines_button(self):
        defines, define_path = self.genericsManager.choose_defines_file()
        self.ui.definesPushButton.setText(defines)
        self.ui.definesPushButton.setToolTip(define_path)
        if defines != "[no file selected]":
            self.ui.add_generics_sets_button.setEnabled(True)
            self.ui.clear_generics_table_button.setEnabled(False)
        
    def scrollArea4testlist(self):
        self.scrollArea = QScrollArea(self.ui.reg_modes_2)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 809, 415))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_scrollArea = QVBoxLayout(self.scrollAreaWidgetContents)
        self.ui.verticalLayout.addWidget(self.scrollArea)    

    
    def read_config(self):
        os.environ['LD_LIBRARY_PATH'] = "/usr/lib:/usr/openwin/lib:/usr/lib/X11"        
        # get config file from ver 4
        if sys.platform.startswith("linux"):
            default_config_path = f'{self.vrc_path}{vrc_ver}/default.config'
        elif sys.platform == "win32":
            default_config_path = fr'{self.vrc_path}{vrc_ver}\default.config'
        #  create new config file If there isn't one
        
        
        
        vrc_config_path=path.join(os.getcwd(), "vrc.config")
        configs_path=path.join(os.getcwd(),"configs", "run.config")
        if path.exists(vrc_config_path):
            config_path = vrc_config_path
        else:
            config_path = configs_path 
        if path.exists(config_path):
            config.read(config_path)
            if not config.has_option('GENERAL','SCRIPT_VER'):
                config.set('GENERAL','SCRIPT_VER',vrc_ver)
            config['GENERAL']["CONFIG_NAME"]="vrc.config"
            self.vrc_version()    
            config_default.read(default_config_path)
            # check all config variable is the same as default.config
            #  Iterate over all existing configuration in the config file
            for each_section in config_default.sections():
                for (each_key, each_val) in config_default.items(each_section):
                    if not config.has_option(each_section,each_key):
                        config.set(each_section,each_key,each_val)
                        #self.show_popup("config file error", f'your config file does not have : "{each_key}" \nin this section : "{each_section}" \nplease update your variables as in this file :  \n {default_config_path}')
                        #self.exit()
        else:
            config.read(default_config_path)
    #  read from config and write to gui
    def gui_first_upload(self):

       
       
        self.read_config()
        # Sending the versions of the tools to the gui according to the versions available on the server
        self.set_ver(self.questa_path, self.ui.questa_ver_combo_bt)
        self.set_ver(self.vrc_path, self.ui.vrc_ver_combo_bt)
        self.set_ver(self.qvip_path, self.ui.qvip_ver_combo_bt)
        self.set_ver(self.visualizer_path, self.ui.visualizer_ver_combo_bt)
        self.set_ver(self.questa_path, self.ui.vrun_ver_combo_bt)

        if args.QSIM_GUI=='1':
            if args.TOOL== "questa":
                self.delete_widget(self.ui.vrun_bt)
                self.delete_widget(self.ui.visualizer_bt)
                self.delete_widget(self.ui.load_tool_bt)
                config['RUN_OPTIONS']["VRUN"]="0"
                config['RUN_OPTIONS']["QUESTASIM"]="1"
                config['RUN_OPTIONS']["VISUALIZER"]="0"
            elif args.TOOL== "vrun" :
                self.delete_widget(self.ui.questasim_bt)
                self.delete_widget(self.ui.visualizer_bt)
                self.delete_widget(self.ui.load_tool_bt)
                config['RUN_OPTIONS']["VRUN"]="1"
                config['RUN_OPTIONS']["QUESTASIM"]="0"
                config['RUN_OPTIONS']["VISUALIZER"]="0"
        if args.TESTLIST != 'NULL':
            config['REG_OPTIONS']["TESTLIST"]=args.TESTLIST
        
        
        self.scrollArea4testlist()
        self.set_stylesheet()           
        self.set_win_title()
        self.set_vrc_icon()
        self.read_testlist_file()
        self.gui_update()

    # Search of the existing versions and Update of the gui
    def set_ver(self, pathto, ver_combo_bt):
        if pathto is not None:
            list_of_dir = glob(f"{pathto}*")
            list_of_dir.sort()
            
            if ver_combo_bt.objectName()=="visualizer_ver_combo_bt":
                tmp=[]
                for item in list_of_dir:
                    if os.path.exists(item + "/visualizer"):
                        tmp.append(item)
                list_of_dir=tmp
            for idx, current_path in enumerate(list_of_dir):
                if os.path.isdir(current_path) :  
                    ver_combo_bt.addItem("")
                    ver_combo_bt.setItemText(idx, self._translate("MainWindow", os.path.basename(os.path.normpath(current_path))))

    def set_vrc_icon(self):
        if sys.platform.startswith("linux"):
            icon = QtGui.QIcon(fr'{self.vrc_path}{vrc_ver}/vrc.png')  # Replace 'path_to_your_icon_file.ico' with the actual path
        elif sys.platform == "win32":
            icon = QtGui.QIcon(fr'{self.vrc_path}{vrc_ver}\vrc.png')  # Replace 'path_to_your_icon_file.ico' with the actual path
        self.setWindowIcon(icon)
    
    def set_win_title(self):
        full_path=os.getcwd()
        full_path=full_path.split("/")
        proj_name=""
        for idx, dir in enumerate(full_path):
            if dir == "verification":
                proj_name=full_path[idx-1] + " - "
        
        proj_name=proj_name.replace("_verif","")
        proj_name=proj_name.replace("_V1","")
        proj_name=proj_name.replace("FPGA_","")
        proj_name=proj_name.replace("IP_REPO_","")
        
        self.setWindowTitle(self._translate("MainWindow", proj_name + os.path.basename(os.path.normpath(os.getcwd()))))

    
    
    
    # set the paths according to the different servers
    def set_path(self):
        if sys.platform.startswith("linux"):
            if os.path.exists("/ElcSoftware/misc/Python36TK/bin/python3"):
                self.os_name = "rafael"
            elif os.path.exists("/Projects/Firmver/Python/Python3.9.6/"):
                self.os_name = "on_prem"
                # #?????????????????
                namespace_file = '/run/secrets/kubernetes.io/serviceaccount/namespace'
                if os.path.exists(namespace_file):
                    with open(namespace_file, 'r') as f:
                        namespace = f.read().strip()
                        if namespace == "rhpc":
                            self.os_name = "rhpc"
            elif os.path.exists("/Enviroment/projects/Firmver/files/python368"):
                self.os_name = "wild_west"
        elif sys.platform == "win32":
            self.os_name = "windows"
        
        self.vrc_path = os.path.dirname(os.path.dirname(__file__))+ os.sep 
        if self.os_name == "rafael":
            abs_path = self.init_path.split(':')
            for each_path in abs_path:
                if(each_path.startswith("/FP")):
                    abs_path=each_path.split(os.path.sep)[1:3]
            self.abs_path_string = f'/{abs_path[0]}/{abs_path[1]}/'
            second_abs_path = os.environ["REG"].split(os.path.sep)[1:3]
            self.second_abs_path_string = f'/{second_abs_path[0]}/{second_abs_path[1]}/'
            self.visualizer_path = self.abs_path_string + "applications/linux/mentorgraphics/questasim/"
            self.questa_path = self.abs_path_string + "applications/linux/mentorgraphics/questasim/"
            self.qvip_path = self.abs_path_string + "applications/linux/mentorgraphics/QVIP/"
            self.py_path = "export LD_LIBRARY_PATH=/FPGA/ecad/applications/linux/xilinx/DocNav:/FPGA/ecad/applications/linux/mentorgraphics/QVIP/2020.3/questa_mvc_core/linux_x86_64_gcc-7.4.0:/FPGA/ecad/applications/linux/xilinx/DocNav:/ElcSoftware/HPCgrid/sge6_2u2/lib/UNSUPPORTED-lx3.10.0-862.el7.x86_64-amd64:/usr/lib:/usr/openwin/lib:/usr/lib/X11:/ElcSoftware/Matlab/9.4/sys/os/glnxa64; /ElcSoftware/misc/Python36TK/bin/python3"
            self.python_alias = 'export PATH=$PATH\:/ElcSoftware/misc/cmake/cmake-3.22-prefix/bin; export D_LIBRARY_PATH=/FPGA/ecad/applications/linux/xilinx/DocNav:/FPGA/ecad/applications/linux/mentorgraphics/QVIP/2020.3/questa_mvc_core/linux_x86_64_gcc-7.4.0:/FPGA/ecad/applications/linux/xilinx/DocNav:/ElcSoftware/HPCgrid/sge6_2u2/lib/UNSUPPORTED-lx3.10.0-862.el7.x86_64-amd64:/usr/lib:/usr/openwin/lib:/usr/lib/X11:/ElcSoftware/Matlab/9.4/sys/os/glnxa64;/ElcSoftware/misc/Python36TK/bin/python3 '
            self.qldev_alias = 'qlogin -l dev'
        elif self.os_name == "wild_west":
            self.visualizer_path = "/Apps/mentor/visualizer/"
            self.questa_path = "/Apps/mentor/questa/"
            self.qvip_path = "/Apps/mentor/qvip/"
            self.py_path = "/Enviroment/projects/Firmver/files/python368/bin/python3"
            # self.python_alias = 'export /Enviroment/projects/Firmver/files/python368/bin/python3 '
        elif self.os_name == "on_prem" or self.os_name == "rhpc": #{D}
            self.visualizer_path = "/Apps/mentor/visualizer/"
            self.questa_path = "/Apps/mentor/questa/"
            self.qvip_path = "/Apps/mentor/qvip/"
            self.py_path = "/Projects/Firmver/Python/Python3.9.6/bin/python3.9"
            self.python_alias = "/Projects/Firmver/Python/Python3.9.6/bin/python3.9"
        elif self.os_name == "windows":
            self.py_path = "python"

    # Setting paths into the environment variables
    def set_env_path(self):
        global vrc_setenv_cmd
        #  init path because we don't want to accumulate previous installation
        os.environ["PATH"] = self.init_path
        if sys.platform.startswith("linux"):

            visualizer_setenv_cmd = self.visualizer_path + config['GENERAL']["VISUALIZER_VER"] + "/visualizer/bin" + ":"
            questa_setenv_cmd = self.questa_path + config['GENERAL']["QUESTA_VER"] + "/questasim/bin" + ":"
            vrun_setenv_cmd = self.questa_path + config['GENERAL']["VRUN_VER"] + "/questasim/bin" + ":"
            vrc_setenv_cmd = self.vrc_path + config['GENERAL']["SCRIPT_VER"]
            qvip_path = self.qvip_path + config['GENERAL']['QVIP_VER'] + "/questa_mvc_core/linux_x86_64_gcc-7.4.0"

            
            os.environ['LD_LIBRARY_PATH'] += ":" + qvip_path
            #os.environ['LD_LIBRARY_PATH'] += ":" + f"{self.py_path}"
            os.environ['VSIM_PATH'] = self.questa_path + config['GENERAL']["QUESTA_VER"] + "/questasim/bin/vsim "
            os.environ['VRUN_PATH'] = self.questa_path + config['GENERAL']["VRUN_VER"] + "/questasim/bin/vrun "
            os.environ['VIS_PATH']=self.visualizer_path+config['GENERAL']["VISUALIZER_VER"]+"/visualizer/bin/visualizer "
            os.environ['QUESTA_MVC_HOME'] = self.qvip_path + config['GENERAL']["QVIP_VER"]

            if int(config['RUN_OPTIONS']["QUESTASIM"]):
                os.environ["PATH"] = questa_setenv_cmd + os.environ["PATH"]
            elif int(config['RUN_OPTIONS']["VISUALIZER"]):
                os.environ["PATH"] = questa_setenv_cmd + visualizer_setenv_cmd + os.environ["PATH"]
            elif int(config['RUN_OPTIONS']["VRUN"]):
                os.environ["PATH"] = vrun_setenv_cmd + os.environ["PATH"]

            if self.os_name == "rafael":
                os.environ['QRSH_CMD'] = f'qrsh -l nfq6 -now y  -b y -N "vrc-vsim" -V -cwd -e /dev/null -o /dev/null env PATH={os.environ["PATH"]} env LD_LIBRARY_PATH={os.environ["LD_LIBRARY_PATH"]} '
                os.environ['VSIM_PATH'] += " -64 "
            elif self.os_name == "on_prem": #this is old!
                os.environ['VSIM_PATH'] += " -64 "
                os.environ['QRSH_CMD'] = f"sudo /usr/bin/Runapp.sh 2> /dev/null -c 2 -s " #{D}
                #os.environ['MODELSIM_TCL']="/Apps/mentor/questa/modelsim.tcl"
                #os.environ['VRUN_PATH'] +=  " -64 "
                
                #new {D}
            elif self.os_name == "rhpc":
                os.environ['LD_LIBRARY_PATH'] = "/Apps/mentor/questa/2021.3/questasim/gcc-7.4.0-linux_x86_64/lib"
                os.environ['VSIM_PATH'] += " -64 "
                os.environ['QRSH_CMD'] = f'/Projects/Firmver/scripts/qrsh -l nfq6 -now y -b y -cwd -N "vrc-vsim" env LD_LIBRARY_PATH={os.environ["LD_LIBRARY_PATH"]} '
            elif self.os_name == "wild_west":
                os.environ['QRSH_CMD'] = f"export env PATH={os.environ['PATH']};export LD_LIBRARY_PATH=/Apps/mentor/questa/{config['GENERAL']['QUESTA_VER']}/questasim/gcc-7.4.0-linux_x86_64/lib:{os.environ['LD_LIBRARY_PATH']};"

        elif sys.platform == "win32":
            os.environ['VIS_PATH'] = ""
            os.environ['VSIM_PATH'] = "vsim "
            os.environ['VRUN_PATH'] = "vrun "
            os.environ['QRSH_CMD'] = ""

            vrc_setenv_cmd = self.vrc_path + config['GENERAL']["SCRIPT_VER"]
            quest_dir = glob("C:\questasim*")
            try:
                os.environ["PATH"] += fr"{quest_dir[0]}\win64;"
            except IndexError:
                self.show_popup("ERROR", "you dont have questasim installation on your windows")

                #  Executes the vrun command and also generates the RMDB file


    def vrun(self, gen=""):
        #  create ucdb dir for all cudb's
        if not os.path.exists("ucdbs"):
            os.mkdir("ucdbs")

        date = datetime.now().strftime('VRMDATA_%Y-%m-%d_%H-%M-%S')
        if bool(int(config['REG_OPTIONS']["DELETE_PREV_VRMDATA"])):
            #  delete all trash file
            for filename in glob("VRMDATA*"):
                if os.path.isdir(filename) and filename is not date:
                    try:
                        shutil.rmtree(filename)
                    except OSError:
                        pass

        #  date- for vrmdata file name

        #  must delete prev vrmdata & work
        if os.path.exists(date):
            shutil.rmtree(date)
        if os.path.exists("work"):
            shutil.rmtree("work")

        
       
        #  execute vrun command
        vrun_cmd=""
            
        if (gen != ""):
            gen = "_" + gen
            config['REG_OPTIONS']['GENERIC'] = '-{}'.format(gen.lower())
        

        if int((config['REG_OPTIONS']['GRID']) == 0 or self.os_name == "wild_west" or self.os_name == "on_prem" or self.os_name =="rhpc") and args.QSIM_GUI == "0": #{D}
            vrun_cmd += os.environ['QRSH_CMD']
        
        self.create_my_rmdb()
        
        if self.os_name == "on_prem" and args.QSIM_GUI == "0":
            vrun_cmd +=os.environ['VRUN_PATH']
        vrun_cmd += f"{config['REG_OPTIONS']['REG_CMD']} -vrmdata {date}{gen.upper()} "
        vrun_cmd += f" -j {config['REG_OPTIONS']['JOBS']} "
        if bool(int(config['REG_OPTIONS']["RERUN"])) == 0 or bool(int(config['REG_OPTIONS']["DEBUG"])):
            vrun_cmd += " -nolocalrerun "
        if int(config['REG_OPTIONS']['COV_REPORT']) == 1:
            vrun_cmd +=f" -html -htmldir {date}{gen.upper()}/vrunhtmlreport "
        if args.QSIM_GUI == "0":
            vrun_cmd += f" -mseed {random.randint(1,1000000000)} " 
  
        if(args.PIPELINE == "1"):
            if("-gui" in vrun_cmd):
                vrun_cmd=vrun_cmd.replace("-gui","")
            os.system(vrun_cmd)
            self.exit()
        if (args.QSIM_GUI == "0"):
            vrun_cmd = f"{vrun_cmd} &"
            self.save_config() 
            subprocess.Popen(vrun_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, )
        else:
            if("-gui" in vrun_cmd):
                vrun_cmd=vrun_cmd.replace("-gui","")
            print(vrun_cmd)
            self.exit()
            
    def create_my_rmdb(self):
        #  read reg.rmdb in vrc path and configure my.rmdb according reg.rmdb & config file
        tree = ET.parse(os.path.join(vrc_setenv_cmd, "reg.rmdb"))  #
        root = tree.getroot()
        #  Iterate over all existing configuration in the config file
        for each_section in config.sections():
            for (each_key, each_val) in config.items(each_section):
                # set_parameter to my.rmdb
                self.set_parameter(root, each_key.upper(), each_val)

        self.set_parameter(root, "QRSH", os.environ['QRSH_CMD'])

        if int(config['REG_OPTIONS']['TRIAGE']) == 1:
            self.set_parameter(root, "triagefile", "(%DATADIR%)/triage.tdb")
            self.set_parameter(root, "triageoptions",f"-rulesfile {self.questa_path}{config['GENERAL']['QUESTA_VER']}/questasim/vm_src/uvm_generic_1.xform")
        
        if int(config['REG_OPTIONS']['DEBUG']) == 1:
            self.set_parameter(root, "DEBUGMODE", "1")
        
        if int(config['REG_OPTIONS']['TREND']) == 1:
            self.set_parameter(root, "trendfile", "(%DATADIR%)/trend.ucdb")

        if int(config['REG_OPTIONS']['SEND_MAIL']) == 1:
            self.set_parameter(root, "EMAIL_RECIPIENTS", "(%username%)@rafael.local")
            self.set_parameter(root, "EMAIL_SERVERS", "mw.rafael.local")
        
        if int(config['RUN_OPTIONS']["VISUALIZER"]) == 1:
            self.set_parameter(root, "VISUALIZER", "1")

        self.set_parameter(root,"MVC_HOME",os.environ['QUESTA_MVC_HOME'])

        #  create user rmdb
        tree.write('my.rmdb')

    def set_parameter(self, root, parameter, value):
        #  try- not al configuration defined as parameters in rmdb
        try:
            root.find(f'.//parameter[@name="{parameter}"]').text = value
        except AttributeError:
            pass
        
    def vrc_version(self):
        if config['GENERAL']['SCRIPT_VER'] != vrc_ver:
            if(args.QSIM_GUI=='1' and (config['GENERAL']["SCRIPT_VER"])<'5'):
                self.show_popup("WARNING" , "VRC version 4 and below does not support uploading VRC from questasim")
                config['GENERAL']["SCRIPT_VER"] = vrc_ver
                self.gui_update()
            else:
                if (path.exists(config['GENERAL']["CONFIG_NAME"])):
                    self.save_config()
                cmd=os.path.join(self.vrc_path+config['GENERAL']["SCRIPT_VER"], f"vrc.py")
                if (path.exists(cmd)):
                    cmd+=f" -qgui {args.QSIM_GUI} -t {args.TOOL} -p {args.PIPELINE} -j {args.JOBS} -s {args.SEED} -tp {args.TESTPLAN} -tl {args.TESTLIST} -b {args.BATCH} & "
                    cmd=self.py_path+" "+cmd
                    os.system(cmd)
                    self.exit()
                else:
                    config['GENERAL']['SCRIPT_VER'] = vrc_ver
                    self.gui_update()

    def set_dummy_dut(self):
         # Sync -dummy flag in COMPILE_ENV according to DUMMY_DUT
        dummy_flag = str(config['RUN_OPTIONS'].get("DUMMY_DUT", "0"))
        ce_val = config['COMMANDS'].get("COMPILE_ENV_CMD", "")
        if dummy_flag == "1":
            if "-dummy" not in ce_val.split():
                ce_val = (ce_val + " -dummy").strip()
        else:
            ce_val = " ".join([x for x in ce_val.split() if x != "-dummy"]).strip()
        config['COMMANDS']["COMPILE_ENV_CMD"] = ce_val
        self.ui.compile_env_line.setText(config['COMMANDS']["COMPILE_ENV_CMD"])

    def run_compile_design_headless(self):
        # Mimic the logic of CompileDesignGUI but without GUI
        print("run compile_design.sh")
        config_path = self.config['GENERAL']['CONFIG_NAME']
        config = self.config
        # Get vendor from config
        vendor = None
        if config.has_section('RUN_OPTIONS') and config.has_option('RUN_OPTIONS', 'vendor'):
            vendor = config.get('RUN_OPTIONS', 'vendor')
        if vendor is None:
            vendor = 'vivado'  # default
        qrsh=os.environ['QRSH_CMD'].split()
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'utils/compile_design.sh'))
        cmd = qrsh + [script_path, '-b', '-c', '-v', vendor]
        # Ensure the log directory exists
        log_dir = os.path.join(os.getcwd(), 'log')
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, 'fps.log')

        # Open the log file for writing
        with open(log_path, 'w') as log_file:
            # Start the compilation process
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)
            for line in proc.stdout:
                log_file.write(line)      # Write each line to the log file
                log_file.flush()          # Ensure the output is written immediately
                print(line, end='')       # Also print to console (optional)
                # Check for error indicators
                if line.startswith('ERRROR:') or line.startswith('Compile_design error:') or '** ERROR' in line:
                    print("Build error. Exiting.")
                    proc.terminate()
                    exit(1)
                # Save vopt libs summary to config if found
                if line.startswith("Compile_design summary: vopt libs are"):
                    libs = line.split("Compile_design summary: vopt libs are", 1)[1].strip()
                    if not config.has_section('OPT_VSIM_ARGS'):
                        config.add_section('OPT_VSIM_ARGS')
                    config.set('OPT_VSIM_ARGS', "VOPT_LIBRARIES_ARGS", libs)
                    with open(config_path, 'w') as f:
                        config.write(f)
            proc.wait()
        print("done to run compile_design.sh")


    def exec(self):
        

        # save generics list
        if args.PIPELINE != '1':
            self.genericsManager.dump_generics_list()
        
        if(args.BATCH == '1'):
            config['RUN_OPTIONS']["GUI_MODE"] ="0"
      
        

        #  delete all trash file
        for filename in glob("wlf*"):
            if not os.path.isdir(filename):
                os.remove(filename)

        self.set_env_path()

        config['REG_OPTIONS']["TESTPLAN"] = self.ui.testplan_line.text()
        config['RUN_OPTIONS']["TEST"] = self.ui.test_line.text()
        config['GENERAL']["TB_NAME"] = self.ui.tb_line.text()

        config['RUN_OPTIONS']['BREAK']= str(int(self.ui.debug_break_cb.isChecked()))
        config['RUN_OPTIONS']['DEBUG_CONFIG_DB']= str(int(self.ui.debug_config_db.isChecked()))
        self.set_dummy_dut()

        self.save_config()
        self.add_parser_config()
        if self.configuration_check():
            if int(config['RUN_STAGES']["COMPILE_DPI"]):
                # ---- Added by Ayala---
                try:
                    dpi_vsim_cmds = self.dpi.compile_dpi(dpi_files=[self.ui.dpi_list.item(x).data(Qt.UserRole) \
                                                                            for x in range(self.ui.dpi_list.count())], \
                                                                            prev_vrc_sv_lib_cmds=config['OPT_VSIM_ARGS']["VSIM_DPI_ARGS"]) 
                except FileNotFoundError as fnf_error:
                    self.show_popup("str_title", f"File was not found. Details: {fnf_error}")
                config['OPT_VSIM_ARGS']["VSIM_DPI_ARGS"]=""
                config['OPT_VSIM_ARGS']["VSIM_DPI_ARGS"] = dpi_vsim_cmds
                self.save_config() # save vrc.config
                self.ui.vsim_dpi_textbox.setText(dpi_vsim_cmds)
                self.ui.vsim_dpi_textbox.setToolTip(dpi_vsim_cmds)
                ## --------------------


            if args.PIPELINE == '1' or args.BUILD_DESIGN =='1':
                # self.read_config()
                print("# vrc version: ", config['GENERAL']["SCRIPT_VER"])
                self.run_compile_design_headless()
            if int(config['RUN_OPTIONS']["VRUN"]):
                #  if user choose ok close gui and vrun
                if self.create_testlist_file():
                    if args.PIPELINE == '1': #if in batch mode - read from generics_queue.txt file & get the next generic
                        gen = get_next_line_in_file().lower()
                        self.vrun(gen)
                    else:
                        gen=""
                        if len(self.genericsManager.generics_list) > 0:
                            gen = self.genericsManager.generics_list[0]
                        self.vrun(gen)
                    if bool(int(config['GENERAL']["CLOSE_GUI"])) or args.QSIM_GUI == '1':
                        w.close()
                        self.exit()
            elif int(config['RUN_OPTIONS']["QUESTASIM"]) or int(config['RUN_OPTIONS']["VISUALIZER"]):
                #  if user choose ok close gui and run run_do.py
                cmd = os.path.join(vrc_setenv_cmd, "run_do.py ")
                cmd = self.py_path + " " + cmd + "-qgui " + args.QSIM_GUI
                if(args.QSIM_GUI=='0'):
                    cmd += " &"
                os.system(cmd)
                if bool(int(config['GENERAL']["CLOSE_GUI"])) or args.QSIM_GUI == '1':
                    w.close()
                    self.exit()
                    
                
    
    def add_parser_config(self):
        if(args.PIPELINE == '1'):
            config['RUN_OPTIONS']["VRUN"]="1"
            config['RUN_OPTIONS']["QUESTASIM"]="0"
            config['RUN_OPTIONS']["VISUALIZER"]="0" 
            config['RUN_OPTIONS']["CLEAR_WORK"]="0" 
            # print("PIPELINE MODE!!!!")
        if(args.BATCH == '1'):
            config['RUN_OPTIONS']["VRUN"]="0"
            config['RUN_OPTIONS']["QUESTASIM"]="1"
            config['RUN_OPTIONS']["VISUALIZER"]="0" 
        if(args.JOBS != "NULL"):
            config['REG_OPTIONS']["JOBS"]=args.JOBS
        if(args.SEED != "NULL"):
            config['RUN_OPTIONS']["SEED"]=args.SEED
        if(args.TESTPLAN != "NULL"):
            config['REG_OPTIONS']["TESTPLAN"]=args.TESTPLAN
            

    def configuration_check(self):
        if bool(int(config['RUN_OPTIONS']["CLEAR_WORK"])) and (not (bool(int(config['RUN_STAGES']["COMPILE_DESIGN"])) and bool(int(config['RUN_STAGES']["COMPILE_VIPS"])) and bool(int(config['RUN_STAGES']["COMPILE_ENV"])) and bool(int(config['RUN_STAGES']["OPTIMIZE"])))):
            self.show_popup("WARNING" , "You can't both uncompile and delete work")
        elif(int(config['RUN_OPTIONS']["QUESTASIM"])+int(config['RUN_OPTIONS']["VISUALIZER"])+int(config['RUN_OPTIONS']["VRUN"])==0):
            self.show_popup("WARNING" , "Please select one of the tools: questasim , vrun , visualizer ")
        elif(int(config['RUN_OPTIONS']["VISUALIZER"]) and config['GENERAL']["QUESTA_VER"]!= config['GENERAL']["VISUALIZER_VER"]):
            self.show_popup("WARNING" , "On visualizer mode you must set questa version and visualizer version to the same version")
        elif(int(config['RUN_OPTIONS']["VRUN"]) and int(config['REG_OPTIONS']["GRID"])==0 and int(config['REG_OPTIONS']["JOBS"])>= 2):
            self.show_popup("WARNING" , "If you want to use more then 2 jobs in your regrresion you must to config grid to be 1")
        elif((int(config['RUN_OPTIONS']["QUESTASIM"]) or int(config['RUN_OPTIONS']["VISUALIZER"])) and config['RUN_OPTIONS']["TEST"]==""):
            self.show_popup("WARNING" , "Please choose test before runing")
        elif((int(config['RUN_OPTIONS']["QUESTASIM"]) or int(config['RUN_OPTIONS']["VISUALIZER"])) and config['GENERAL']["TB_NAME"]==""):
            self.show_popup("WARNING" , "Please choose tb before runing")
        elif((int(config['RUN_OPTIONS']["QUESTASIM"]) and int(config['RUN_OPTIONS']["VISUALIZER"]))):
            self.show_popup("WARNING" , "Please choose 1 tool questa or visualizer")
        elif(int(config['RUN_OPTIONS']["VRUN"]) and config['REG_OPTIONS']["TESTPLAN"]==""):
            self.show_popup("WARNING" , "Please choose testplan before runing")
        elif(int(config['RUN_OPTIONS']["VRUN"]) and (not path.exists(config['REG_OPTIONS']["TESTPLAN"]))):
            self.show_popup("WARNING" , "Your testplan doesn't exist in sim dir")
        elif(int(config['RUN_OPTIONS']["VRUN"]) and config['GENERAL']["QUESTA_VER"]!= config['GENERAL']["VRUN_VER"]):
            self.show_popup("WARNING" , "VRUN version must be the same as QUESTA version")
        elif(args.QSIM_GUI=='1' and config['RUN_STAGES']["COMPILE_DPI"]== '1'):
            self.show_popup("WARNING" , "you can't use compile dpi while vrc run from Questa GUI")
        else:
            return True
        return False

    def create_testlist_file(self):
        with open(config['REG_OPTIONS']["TESTLIST"], 'w', encoding='UTF-8') as f:
            for idx in range(len(self.reg_test_line)):
                if self.reg_test_line[idx] != None and self.reg_test_line[idx].text() !='':
                    if(not self.reg_num_of_test_line[idx].text().isdigit() or (not self.reg_seed_line[idx].text().isdigit() and self.reg_seed_line[idx].text() !='') ):
                        self.show_popup("ERROR","You must insert digit to seed / num_of_test in Test List")
                        return False
                    f.write(f"{self.reg_test_line[idx].text()} {self.reg_num_of_test_line[idx].text()} {self.reg_seed_line[idx].text()}\n")   
        
        for idx in range(len(self.reg_test_line)):
            if self.reg_test_line[idx] != None and self.reg_test_line[idx].text() !='':
                return True
        self.show_popup("ERROR","You must insert at least 1 test in Test List")
        return False  

    def read_testlist_file(self):
        if path.exists(config['REG_OPTIONS']["TESTLIST"]):
            with open(config['REG_OPTIONS']["TESTLIST"], 'r', encoding='UTF-8') as f:
                content = f.readlines()
                for i in range(len(content)):
                    tl_param=content[i].split()
                    if(len(tl_param)>1):
                        self.pushButton_add_test()
                        self.reg_test_line[i].setText(tl_param[0])
                        self.reg_num_of_test_line[i].setText(tl_param[1])
                        try:
                            self.reg_seed_line[i].setText(tl_param[2])
                        except IndexError:
                            pass

        self.pushButton_add_test()

    def set_stylesheet(self):
        
        bgr = "#e0e0e0"
        color=self.ui.Dark.value()

        if color == 100:
            bgr = "#222222"
        if color > 95:
            bgr = "#2B3A55"
        elif color>90:
            bgr = "#0A2647"
        elif color > 85:
            bgr = "#144272"
        elif color > 80:
            bgr = "#205295"
        elif color > 75:
            bgr = "#999090"
        elif color > 70:
            bgr = "#472183"
        elif color > 65:
            bgr = "#227C70"
        elif color > 60:
            bgr = "#460C68"
        elif color > 55:
            bgr = "#678983"
        elif color > 50:
            bgr = "#3D5656"
        elif color > 45:
            bgr = "#22A39F"
        elif color > 40:
            bgr = "#DAE2B6"
        elif color > 35:
            bgr = "#FFFBE9"
        elif color > 30:
            bgr = "#F0DBDB"
        elif color > 25:
            bgr = "#A5F1E9"
        elif color > 20:
            bgr = "#CFF5E7"
        elif color > 15:
            bgr = "#C8FFD4"
        elif color > 10:
            bgr = "#BCCEF8"
        elif color > 5:
            bgr = "#DFF6FF"
        elif color > 0:
            bgr = "#e0e0e0"

        if color > 50:
            r = 255
            g = 255
            b = 255
        else:
            r = 0
            g = 0
            b = 0

        config['GENERAL']["COLOR"]=str(color)
        # self.ui.MainGUI.setStyleSheet(f"background-color: rgb({int(b_r)}, {int(b_g)}, {int(b_b)});\n"
        if(color>5):
            self.ui.MainGUI.setStyleSheet(f"background-color: {bgr};\n"
            "\n"
            f"color: rgb({r}, {g}, {b});\n"
            "border-color: rgb(159, 159, 159);\n"
            "\n"
            "")
        else:
            self.ui.MainGUI.setStyleSheet("border-color: rgb(159, 159, 159);\n"
            "\n"
            "\n"
            "")

    def exit(self):
        exit()

    #  pop up massege 
    def show_popup(self, str_title, str):
        if(args.PIPELINE == "1" or args.BATCH == "1"):
            print(f"{str_title} : {str}")
            self.exit()
        msg = QMessageBox()
        msg.setWindowTitle(str_title)
        msg.setText(str)
        result = msg.exec_()


   
    

    def get_questa_dir_path(self, msg ):
        self.file_path=msg.bugs_combobox.currentText()
        msg.close()

    def get_verbosity(self, index):
        config['RUN_OPTIONS']["VERBOSITY"] = self.ui.verbosity_combo_bt.itemText(index)

    def get_questa_ver(self, index):
        config['GENERAL']["QUESTA_VER"] = self.ui.questa_ver_combo_bt.itemText(index)

    def get_visualizer_ver(self, index):
        config['GENERAL']["VISUALIZER_VER"] = self.ui.visualizer_ver_combo_bt.itemText(index)

    def get_vrun_ver(self, index):
        config['GENERAL']["VRUN_VER"] = self.ui.vrun_ver_combo_bt.itemText(index)

    def vrc_ver_combo_bt(self, index):
        config['GENERAL']["SCRIPT_VER"] = self.ui.vrc_ver_combo_bt.itemText(index)
        self.vrc_version()
            

    def qvip_ver_combo_bt(self, index):
        config['GENERAL']["QVIP_VER"] = self.ui.qvip_ver_combo_bt.itemText(index)


    def chang_dir(self):
        sim_dir = str(QFileDialog.getExistingDirectory(self, "Select Directory",))
        if (sim_dir != ""):
            os.chdir(sim_dir)
            self.set_win_title()
            self.gui_first_upload()

    def constant_override(self):
        import sys, os
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        dlg = ConstantsDialog(self.config, self)
        dlg.exec_()

    
    def build_design(self):
        update_all_vhdl_from_config(config)
        self.save_config()
        gui_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'gui/compile_design_gui.py'))
        config_name = config['GENERAL']["CONFIG_NAME"]
        proc = subprocess.Popen([sys.executable, gui_path, config_name])

        def check_proc():
            if proc.poll() is not None:  
                self.read_config()
                if(config['COMMANDS']["COMPILE_DESIGN_CMD"]!=""):
                    self.show_popup("WARNING","please delete COMPILE DESIGN command in Advenced tab its not nesecessary any more")
                if("xil_defaultlib.glbl" in config['OPT_VSIM_ARGS']["VOPT_DEFAULT_ARGS"]):
                    config['OPT_VSIM_ARGS']["VOPT_DEFAULT_ARGS"]=config['OPT_VSIM_ARGS']["VOPT_DEFAULT_ARGS"].replace("xil_defaultlib.glbl","")
                self.gui_update()
            else:
                
                QTimer.singleShot(1000, check_proc)

        
        QTimer.singleShot(1000, check_proc)
    
    def save_config(self):
        config['GENERAL']['PATH2VRC'] = self.vrc_path
        config['GENERAL']['PYTHON_VER'] = 'python3' # can be changed in the future..
        save_config_name = config['GENERAL']["CONFIG_NAME"]
        with open(save_config_name, 'w') as configfile:
            config.write(configfile)

    def actionSuper_Env(self):
        pass

    def gitGraph(self):
        if args.QSIM_GUI=='1':
            self.show_popup("VRC","please use gitGraph feature when you load vrc from terminal, not from questa tool")
        else:
            subprocess.Popen(f"/ElcSoftware/misc/Python36TK/bin/python3   {self.second_abs_path_string}scripts/git/git_graph/app.py", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, )

    def gitGraphDsigen(self):
        if args.QSIM_GUI=='1':
            self.show_popup("VRC","please use gitGraphDsigen feature when you load vrc from terminal, not from questa tool")
        else:
            root_dir = subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).strip().decode()
            design_dir=os.path.join(root_dir,"design")
            if path.exists(design_dir):
                cur_dir=os.getcwd()
                os.chdir(design_dir)
                subprocess.Popen(f"/ElcSoftware/misc/Python36TK/bin/python3   {self.second_abs_path_string}scripts/git/git_graph/app.py", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, )
                os.chdir(cur_dir)
            else:
                print(F"# ERROR: design path not exist: '{cur_dir}'")


    def cloneRepo(self):
        if args.QSIM_GUI=='1':
            self.show_popup("VRC","please use this cloneRepo for the first time when you load vrc from terminal, not from questa tool")
        else:
            if task.init_globals() == None:
                return
            repo_proj = Get_Proj_Repo()
            if repo_proj.exec_() == QDialog.Accepted:
                dir,project, repo_name = repo_proj.get_report()
                msg=self.wait_msg()
                os.chdir(dir)
                subprocess.call(['git', 'clone', '--recurse-submodules',f'ssh://dvdtfsp:22/tfs/ComputingSystems_Collection/{project}/_git/{repo_name}'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                msg.close()
                cur_path=os.getcwd()
                cur_path=path.join(cur_path,repo_name,"verification", "sim")
                if path.exists(cur_path):
                    os.chdir(cur_path)
                    config_path=os.path.join(cur_path, "vrc.config")
                    if path.exists(config_path ):
                        config.read(config_path)
                        self.gui_update()
                else:
                    print(f'# path: {cur_path} not exist')  

    def catch_seed_error(self):
        if int(config['RUN_OPTIONS']["VRUN"]):
            items = os.listdir(os.getcwd() )
            # Filter the items to get only directories that start with "VRMDATA_"
            vrdata_folders = [item for item in items if os.path.isdir(item) and item.startswith("VRMDATA_")]
            if(len(vrdata_folders)==0):
                print("# ERROR there is no VRMDATA* file") 
                return None, None
            tests_path=path.join(vrdata_folders[-1],"regression","simulation","psim")
            log=self.find_folders_by_name(tests_path,"vsim_regression.wlf","TEST ERROR")
            if log == "0":
                print(F"# ERROR there no test with error in this path:{tests_path} ")
                return None, None
            else:
                 log=path.dirname(log)
                 log=path.join(log,"execScript.log")
                 return self.get_seed(log)
        elif int(config['RUN_OPTIONS']["QUESTASIM"]) or int(config['RUN_OPTIONS']["VISUALIZER"]):
            vsim_log_file=path.join(os.getcwd(),"log", "vsim.log")
            return self.get_seed(vsim_log_file)

    def get_seed(self,search_file):
        re_seed=r"-sv_seed (\w+)"
        re_seed1=r"# Sv_Seed = (\w+)"
        re_testname="\+UVM_TESTNAME=(\w+)"
        if path.exists(search_file):
            with open(search_file, "r") as file:
                for line in file:
                    if(line.startswith("# vsim ")): 
                        match_seed = re.search(re_seed, line)
                        match_test = re.search(re_testname, line)
                        if match_test:
                            match_test = match_test.group(1)
                            print("# Report:", )
                            print("# Test Name:", match_test)
                        if match_seed:
                            match_seed = match_seed.group(1)
                            if(match_seed=="random"):
                                
                                continue
                            print("# Seed number:", match_seed)
                            return match_seed, match_test  # Assuming you want to stop searching after finding the first match
                    else:
                        match_seed = re.search(re_seed1, line)
                        if match_seed:
                            match_seed = match_seed.group(1)
                            print("# Seed number:", match_seed)
                            return match_seed, match_test  # Assuming you want to stop searching after finding the first match
                print(f"# Seed number not found in this file: {search_file}.")
                return None, None
        else:
            print(f"# can't find seed with error because this file: {search_file} not exist")
            return None, None


    def get_questa_dir_path(self, msg ):
        self.file_path=msg.bugs_combobox.currentText()
        msg.close() 
 
    def list_popup(self, list_dir,title):
        msg = QDialog()
        msg.setWindowTitle(f' {title} SCRIPT')
        msg.resize(40, 40)
        msg.title_label = QLabel(f'Please select the right "{title}" directory: ', msg)
        msg.bugs_combobox = QComboBox(msg)
        list_dir=[path.dirname(dir) for dir in list_dir]
        msg.bugs_combobox.addItems(list_dir)
        msg.submit_button = QPushButton('Insert', msg)
        msg.submit_button.clicked.connect(lambda state=1, x=msg:  self.get_questa_dir_path(x))
        layout = QVBoxLayout(msg)
        layout.addWidget(msg.title_label)
        layout.addWidget(msg.bugs_combobox)
        layout.addWidget(msg.submit_button)
        msg.exec_()



    def actionCreate_Env(self):
        if self.os_name == "rafael":
            cmd=self.second_abs_path_string+"scripts/create_env/create_env.tcl &"
            os.system(cmd)

    def actionCreate_Project(self):
        if self.os_name == "rafael":
            cmd=self.second_abs_path_string+"scripts/git/create_git_project/create_project.tcl &"
            os.system(cmd)

    def actionArtifactory(self):
        if self.os_name == "rafael":
            cmd=self.second_abs_path_string+"scripts/git/artifact/artifact.tcl &"
            os.system(cmd)

    def actionRUVM(self):
        if self.os_name == "rafael":
            cmd= self.abs_path_string + "applications/linux/mentorgraphics/questasim/"+ config['GENERAL']["QUESTA_VER"] + "/questasim/"
            RA="RA_"+config['GENERAL']["QUESTA_VER"]
            RUVM="RUVM_"+config['GENERAL']["QUESTA_VER"]
            if path.exists(cmd+RA):
                cmd+=RA+"/regassist -gui -project . &"
            elif path.exists(cmd+RUVM):
                cmd+=RUVM+"/vreguvm -gui  &"
            else:
                self.show_popup("RUVM","can't upload RUM")
                return 1
            os.system(cmd)

    def update_dpi_buttons_state(self):
        if self.ui.dpi_list.count() > 0:
            self.ui.clear_button.setEnabled(True)
            self.ui.comp_dpi_bt.setEnabled(True)
            self.ui.comp_dpi_bt.setToolTip("Compile DPI files")
            self.comp_dpi_bt() # update config
        else:
            self.ui.clear_button.setEnabled(False)
            self.ui.comp_dpi_bt.setChecked(False)
            self.comp_dpi_bt() # update config
            self.ui.comp_dpi_bt.setEnabled(False)
            self.ui.comp_dpi_bt.setToolTip("No DPI files have been selected")
            
    #config write from buttun
    def update_file_list_from_config( self, file_list_widget): 
         
        if 'DPI' in config:
            dpi_section = config['DPI']
            file_list_widget.clear()  
            
            for file_name, file_path in dpi_section.items():
                if os.path.isabs(file_path):
                    item = QListWidgetItem(file_name)
                    item.setToolTip(file_path)
                    item.setData(Qt.UserRole, file_path)
                    file_list_widget.addItem(item)
                else:
                    full_path = os.path.abspath(file_path)
                    item = QListWidgetItem(file_name)
                    item.setToolTip(file_path)
                    item.setData(Qt.UserRole, full_path)
                    file_list_widget.addItem(item)
        self.update_dpi_buttons_state()
  
    def clear_work_bt(self):
        config['RUN_OPTIONS']["CLEAR_WORK"]      =str(int(self.ui.clear_work_bt.isChecked()))#get the value of the check box

    def new_trans_bt(self):
        config['RUN_OPTIONS']["NEW_TRANSCRIPT"] = str(int(self.ui.new_trans_bt.isChecked()))

    def save_wave_bt(self):
        config['RUN_OPTIONS']["SAVE_WAVE"] = str(int(self.ui.save_wave_bt.isChecked()))

    def close_gui_bt(self):
        config['GENERAL']["CLOSE_GUI"] = str(int(self.ui.close_gui_bt.isChecked()))

    def visualizer_bt(self):
        config['RUN_OPTIONS']["VISUALIZER"] = str(int(self.ui.visualizer_bt.isChecked()))

    def questasim_bt(self):
        config['RUN_OPTIONS']["QUESTASIM"] = str(int(self.ui.questasim_bt.isChecked()))

    def vrun_bt(self):
        config['RUN_OPTIONS']["VRUN"] = str(int(self.ui.vrun_bt.isChecked()))

    def debug_mode_bt(self):
        config['RUN_OPTIONS']["DEBUG_MODE"] = str(int(self.ui.debug_mode_bt.isChecked()))

    def code_cov_bt(self):
        config['RUN_OPTIONS']["CODECOV_MODE"] = str(int(self.ui.code_cov_bt.isChecked()))

    def gui_bt(self):
        config['RUN_OPTIONS']["GUI_MODE"] = str(int(self.ui.gui_bt.isChecked()))

    def dummy_dut_bt(self):
        config['RUN_OPTIONS']["DUMMY_DUT"] = str(int(self.ui.dummy_dut_bt.isChecked()))

    def pre_comp_bt(self):
        config['RUN_STAGES']["PRE_COMPILE"] = str(int(self.ui.pre_comp_bt.isChecked()))

    def comp_design_bt(self):
        config['RUN_STAGES']["COMPILE_DESIGN"] = str(int(self.ui.comp_design_bt.isChecked()))

    def comp_vips_bt(self):
        config['RUN_STAGES']["COMPILE_VIPS"] = str(int(self.ui.comp_vips_bt.isChecked()))

    def comp_dpi_bt(self):
        config['RUN_STAGES']["COMPILE_DPI"] = str(int(self.ui.comp_dpi_bt.isChecked()))

    def compile_env_bt(self):
        config['RUN_STAGES']["COMPILE_ENV"] = str(int(self.ui.compile_env_bt.isChecked()))

    def post_compile_bt(self):
        config['RUN_STAGES']["POST_COMPILE"] = str(int(self.ui.post_compile_bt.isChecked()))

    def opt_bt(self):
        config['RUN_STAGES']["OPTIMIZE"] = str(int(self.ui.opt_bt.isChecked()))

    def simulate_bt(self):
        config['RUN_STAGES']["SIMULATION"] = str(int(self.ui.simulate_bt.isChecked()))

    def debug_break_cb(self):
        config['RUN_OPTIONS']['BREAK']=str(int(self.ui.debug_break_cb.isChecked()))
        
    def debug_config_db(self):
        config['RUN_OPTIONS']['DEBUG_CONFIG_DB']=str(int(self.ui.debug_config_db.isChecked()))
        
    def triage_bt(self):
        config['REG_OPTIONS']["TRIAGE"] = str(int(self.ui.triage_bt.isChecked()))

    def grid_bt(self):
        config['REG_OPTIONS']["GRID"] = str(int(self.ui.grid_bt.isChecked()))

    def trend_bt(self):
        config['REG_OPTIONS']["TREND"] = str(int(self.ui.trend_bt.isChecked()))

    def report_bt(self):
        config['REG_OPTIONS']["COV_REPORT"] = str(int(self.ui.report_bt.isChecked()))

    def mail_bt(self):
        config['REG_OPTIONS']["SEND_MAIL"] = str(int(self.ui.mail_bt.isChecked()))

    def delete_vrmdata_bt(self):
        config['REG_OPTIONS']["DELETE_PREV_VRMDATA"] = str(int(self.ui.delete_vrmdata_bt.isChecked()))

    def rerun_bt(self):
        config['REG_OPTIONS']["RERUN"] = str(int(self.ui.rerun_bt.isChecked()))

    def jobs_combo_bt(self, index):
        config['REG_OPTIONS']["JOBS"] = self.ui.jobs_combo_bt.itemText(index)

    def report_bugs_features(self):
        if args.QSIM_GUI=='1':
            self.show_popup("VRC","please use report_bugs feature for the first time when you load vrc from terminal, not from questa tool")
        else:
            GitUplode('').is_inside_repo()
            if task.init_globals() == None:
                return
            report_popup = ReportBugsFeaturesPopup()
            if report_popup.exec_() == QDialog.Accepted:
                title, message, report_type, member, project, area, iteration, repo_name = report_popup.get_report()
            
                seed,test_name=self.catch_seed_error()
            
                if(seed != None and test_name != None):
                    self.save_config()
                    git_popup = GitUplode(title)
                    if git_popup.exec_() == QDialog.Accepted:
                        task.add_task(title, message, report_type, member, project, area, iteration, repo_name,test_name,seed)
                        print("# complete")
                    else:
                        print("# aborted")
              
                


    def check_bugs(self):
        if args.QSIM_GUI=='1':
            self.show_popup("VRC","please use check_bugs feature when you load vrc from terminal, not from questa tool")
        else:
            if task.init_globals() == None:
                return
            bugs_popup = CheckBugsPopup()
            if bugs_popup.exec_() == QDialog.Accepted:
                bug_chosen=bugs_popup.bugs_combobox.currentText()
                if( "<vrc>"  in bug_chosen):
                    bug_chosen=bug_chosen.replace("  <vrc>","")
                    commit,test_name,seed=task.get_bug_description(bug_chosen)
                    task.pull_commit_by_bug(commit)
                    self.gui_first_upload()
                    config['RUN_OPTIONS']["TEST"]=test_name
                    config['RUN_OPTIONS']["SEED"]=seed
                    config['RUN_STAGES']["PRE_COMPILE"]="1"
                    config['RUN_STAGES']["COMPILE_DESIGN"]="1"
                    config['RUN_STAGES']["COMPILE_VIP"]="1"
                    config['RUN_STAGES']["COMPILE_ENV"]="1"
                    config['RUN_STAGES']["POST_CMPILE"]="1"
                    config['RUN_STAGES']["OPTIMIZE"]="1"
                    config['RUN_STAGES']["SIMULATION"]="1"
                    config['RUN_OPTIONS']["QUESTASIM"]="1"
                    config['RUN_OPTIONS']["VRUN"]="0"
                    config['RUN_OPTIONS']["VISUALIZER"]="0"
                    self.gui_update()
                    self.exec()
                else:
                    print("ERROR this bug not opened by vrc tool so you can't restore this bug")

    def pushButton_add_test(self):
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        frame_test_list = QtWidgets.QFrame(self.ui.reg_modes_2)
        frame_test_list.setGeometry(QtCore.QRect(20, 10, 781, 46))
        frame_test_list.setFrameShape(QtWidgets.QFrame.StyledPanel)
        frame_test_list.setFrameShadow(QtWidgets.QFrame.Raised)
        frame_test_list.setObjectName("frame_test_list")
        horizontalLayout = QtWidgets.QHBoxLayout(frame_test_list)
        horizontalLayout.setObjectName("horizontalLayout")
        pushButton_sub_test = QtWidgets.QPushButton(frame_test_list)
        pushButton_sub_test.setObjectName("pushButton_sub_test")
        horizontalLayout.addWidget(pushButton_sub_test)
        pushButton_add_test = QtWidgets.QPushButton(frame_test_list)
        pushButton_add_test.setObjectName("pushButton_add_test")
        horizontalLayout.addWidget(pushButton_add_test)
        reg_test_bt = QtWidgets.QPushButton(frame_test_list)
        reg_test_bt.setObjectName("reg_test_bt")
        horizontalLayout.addWidget(reg_test_bt)
        reg_test_line = QtWidgets.QLineEdit(frame_test_list)
        reg_test_line.setFont(font)
        reg_test_line.setObjectName(f"reg_test_line_{self.num_of_test_show}]")
        horizontalLayout.addWidget(reg_test_line)
        reg_num_of_test = QtWidgets.QLabel(frame_test_list)
        reg_num_of_test.setFont(font)
        reg_num_of_test.setObjectName("reg_num_of_test")
        horizontalLayout.addWidget(reg_num_of_test)
        reg_num_of_test_line = QtWidgets.QLineEdit(frame_test_list)
        reg_num_of_test_line.setFont(font)
        reg_num_of_test_line.setObjectName("reg_num_of_test_line")
        horizontalLayout.addWidget(reg_num_of_test_line)
        reg_seed = QtWidgets.QLabel(frame_test_list)
        reg_seed.setFont(font)
        reg_seed.setObjectName("reg_seed")
        horizontalLayout.addWidget(reg_seed)
        reg_seed_line = QtWidgets.QLineEdit(frame_test_list)
        reg_seed_line.setFont(font)
        reg_seed_line.setObjectName("reg_seed_line")
        horizontalLayout.addWidget(reg_seed_line)
        reg_test_bt.setText(self._translate("MainWindow", "Test"))
        reg_num_of_test.setText(self._translate("MainWindow", "Num of Test"))
        reg_seed.setText(self._translate("MainWindow", "Seed:"))
        pushButton_add_test.setText(self._translate("MainWindow", "+"))
        pushButton_sub_test.setText(self._translate("MainWindow", "-"))
        self.verticalLayout_scrollArea.addWidget(frame_test_list)
        self.reg_test_line.append(reg_test_line)
        self.reg_seed_line.append(reg_seed_line)
        self.test_frame.append(frame_test_list)
        self.reg_num_of_test_line.append(reg_num_of_test_line)
        pushButton_add_test.clicked.connect(self.pushButton_add_test)
        pushButton_sub_test.clicked.connect(lambda state=1, x=self.num_of_test_show: self.pushButton_sub_test(x))
        reg_test_bt.clicked.connect(lambda state=1, x=self.num_of_test_show: self.reg_test_bt(x))
        self.num_of_test_show = self.num_of_test_show + 1

    def reg_test_bt(self, idx):
        testlist_path = str(QFileDialog.getOpenFileName(self, "open_file", "../src/dv/tests/", '',options=QFileDialog.DontUseNativeDialog)[0])
        testlist_path = ntpath.basename(testlist_path)
        testlist_path = testlist_path.split(".", 1)
        file_name = str(testlist_path[0])
        if file_name != "":
            self.reg_test_line[idx].setText(file_name)

    def pushButton_sub_test(self, idx):
        if self.reg_test_line[idx] != None:
            self.delete_widget(self.test_frame[idx])
        self.reg_test_line[idx]=None

       
    
    def delete_widget(self,widget):
        childrens= widget.children()
        revers_childrens= reversed(childrens)

        for child in revers_childrens:
            child.deleteLater()
        
        widget.deleteLater()
          


    def RankPushBut(self):
        test_list=[]
        seed_list=[]
        self.show_popup("RANKING","please choose UCDB file to rank")
        merge_path = str(QFileDialog.getOpenFileName(self, "open_file", './ucdbs', '*.ucdb', options=QFileDialog.DontUseNativeDialog)[0])
        if merge_path == "":
            return
        rank_file=datetime.now().strftime('best_test_%Y-%m-%d_%H-%M-%S.txt')
        subprocess.call([self.questa_path + config['GENERAL']["QUESTA_VER"] + "/questasim/bin/vcover", 'ranktest', merge_path, '-log', "best_test.log" , "-rankfile" , rank_file], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        re_best_test_num = r"Total Contributing Tests      = (\d+)"
        with open("best_test.log", "r") as file:
            for line in file:
                match_best_test = re.search(re_best_test_num, line)
                if match_best_test:
                    re_best_test_num=match_best_test.group(1)
                    break
        with open(rank_file, "r", encoding='utf-8', errors='replace') as file:
            for line in file:
                re_test=r"UVM_TESTNAME=(\w+)"                      
                match_test = re.search(re_test, line)
                re_seed=r"{{SEED} {(\w+)}}"                      
                match_seed = re.search(re_seed, line)
                if match_test:
                    test_list.append(match_test.group(1))   
                if match_seed:
                    seed_list.append(match_seed.group(1))
                    if len(seed_list) == int(re_best_test_num):
                        break
        testlist_best_file = datetime.now().strftime('testlist_best_%Y-%m-%d_%H-%M-%S.tl')
        with open(testlist_best_file, 'w', encoding='UTF-8') as f:
            for id in range(len(test_list)):
                f.write(f"{test_list[id]} 1 ")  
                f.write(f"{seed_list[id]}\n") 
        for filename in glob("best_test*"):
            if not os.path.isdir(filename):
                os.remove(filename)
        self.load_testlist(testlist_best_file)
        
    def TestNamePushButton(self):
        testlist_path = str(QFileDialog.getOpenFileName(self, "open_file", './', '', options=QFileDialog.DontUseNativeDialog)[0])
        testlist_path = ntpath.basename(testlist_path)
        self.load_testlist(str(testlist_path))
        
    def load_testlist(self,file_name):
        if file_name != "":
            config['REG_OPTIONS']["TESTLIST"] = file_name
            self.ui.TestNamePushButton.setText(self._translate("MainWindow", config['REG_OPTIONS']["TESTLIST"], None))
            for id in range(len(self.test_frame)):
                self.pushButton_sub_test(id)
            self.num_of_test_show = 0
            self.test_frame = []
            self.reg_test_line = []
            self.reg_seed_line = []
            self.reg_num_of_test_line=[]
            self.read_testlist_file()
            self.gui_update()

    def testplan_bt(self):
        testplan_path = str(QFileDialog.getOpenFileName(self, "open_file", './', '*.xml', options=QFileDialog.DontUseNativeDialog)[0])
        testplan_path = ntpath.basename(testplan_path)
        file_name = str(testplan_path)
        if file_name != "":
            config['REG_OPTIONS']["TESTPLAN"] = file_name
            self.ui.testplan_line.setText(config['REG_OPTIONS']["TESTPLAN"])

    def test_bt(self):
        test_path = str(QFileDialog.getOpenFileName(self, "open_file", "../src/dv/tests/", '',options=QFileDialog.DontUseNativeDialog)[0])
        test_path = ntpath.basename(test_path)
        test_path = test_path.split(".", 1)
        file_name = str(test_path[0])
        if file_name != "":
            config['RUN_OPTIONS']["TEST"] = file_name
            self.ui.test_line.setText(config['RUN_OPTIONS']["TEST"])

    def tb_bt(self):
        tb_path = str(QFileDialog.getOpenFileName(self, "open_file", "../src/tb/", '', options=QFileDialog.DontUseNativeDialog)[0])
        tb_path = ntpath.basename(tb_path)
        tb_path = tb_path.split(".", 1)
        file_name = str(tb_path[0])
        if file_name != "":
            config['GENERAL']["TB_NAME"] = file_name
            self.ui.tb_line.setText(config['GENERAL']["TB_NAME"])

    def config_name_push_bt(self):
        config_path = str(QFileDialog.getOpenFileName(self, "open_file", './', '', options=QFileDialog.DontUseNativeDialog)[0])
        config.read(config_path)
        config_path = ntpath.basename(config_path)
        file_name = str(config_path)
        if file_name != "":
            config['GENERAL']["CONFIG_NAME"] = file_name
            self.gui_update()


    def load_tool_bt(self):
        self.set_env_path()
        if int(config['RUN_OPTIONS']["QUESTASIM"]):
            # subprocess.Popen(os.environ['QRSH_CMD'] + os.environ['VSIM_PATH'] + " -gui &", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT,)
            os.system(os.environ['QRSH_CMD'] + os.environ['VSIM_PATH'] + " -gui &")
            print(os.environ['QRSH_CMD'] + os.environ['VSIM_PATH'] + " -gui &")

        elif int(config['RUN_OPTIONS']["VRUN"]):
            subprocess.Popen(os.environ['QRSH_CMD'] + os.environ['VRUN_PATH'] + " -gui &", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT,)
        elif int(config['RUN_OPTIONS']["VISUALIZER"]):
            subprocess.Popen(os.environ['QRSH_CMD'] + os.environ['VIS_PATH'] + " &", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT,)
        else:
            self.show_popup("ERROR", "tool was not selected")

    def libraries_push_bt(self):
        file_name=self.find_folders_by_name("../../design/design_units/top/build/simulation","elaborate.do","QUESTA")
        if file_name == '0':
            file_name=self.find_folders_by_name("../../design_units","elaborate.do","QUESTA")
        if file_name == '0':
            file_name=self.find_folders_by_name("../../design","elaborate.do","QUESTA")
        if file_name == '0':
            self.show_popup("Warning",f"you dont have 'questa' dir in your design please insert elaborate.do file")
            libs_path = str(QFileDialog.getOpenFileName(self, "open_file", "../../design/design_units/top/build/simulation/", '*.do', options=QFileDialog.DontUseNativeDialog)[0])
            file_name = str(libs_path)
        if file_name != "":
            with open(file_name, 'r') as f:
                libs = f.read()
            if libs.find("-", libs.rfind("-L")+1) == -1:
                config['OPT_VSIM_ARGS']["VOPT_LIBRARIES_ARGS"] = libs[libs.find("-L"):]
            else:
                config['OPT_VSIM_ARGS']["VOPT_LIBRARIES_ARGS"] = libs[libs.find("-L"):libs.find("-", libs.rfind("-L")+1)]
            self.ui.opt_libs_line.setText(config['OPT_VSIM_ARGS']["VOPT_LIBRARIES_ARGS"]) 
			

    def find_files_with_pattern(self,root_path, pattern):
        matching_files = []
        for file in os.listdir(root_path):
            os.path.join(root_path, file)
            file_path=os.path.join(root_path, file)
            if pattern in file_path:
                matching_files.append(file_path)
        return matching_files
    
    def wait_msg(self):
        msg = QDialog()
        msg.setWindowTitle('WAIT')
        msg.title_label = QLabel('P l e a s e   W a i t . . . ', msg)
        layout = QVBoxLayout(msg)
        layout.addWidget(msg.title_label)
        msg.show()
        return msg

    def find_folders_by_name(self,root_path, do_name,title):
        file_name=''
        msg=self.wait_msg()
        matching_folder=[]
        for root, dirs, files in os.walk(root_path):
                if(do_name in files):
                    if(title == "QUESTA"):
                        if os.path.basename(root) == "questa":
                            do_path=path.join(root,do_name)
                            if os.path.exists(do_path):
                                matching_folder.append(do_path)
                    else:
                        do_path=path.join(root,do_name)
                        if os.path.exists(do_path):
                            matching_folder.append(do_path)
        msg.close()
        if(len(matching_folder)==0):
            file_name='0'
        elif(len(matching_folder)>1):
            file_name=self.list_popup(matching_folder,title)
            file_name=path.join(self.file_path,do_name)
        else:
            file_name=matching_folder[0]  
        return file_name 

    
    def find_folders_with_files(self,root_path):
        matching_folders = []
        for root, dirs, files in os.walk(root_path):
            if any(files):
                matching_folders.append(root)
        return matching_folders

    def compile_design_push_bt(self):
        file_name=self.find_folders_by_name("../../design_units/top/build/simulation","compile.do","QUESTA")
        if file_name == '0':
            file_name=self.find_folders_by_name("../../design_units","compile.do","QUESTA")
        if file_name == '0':
            file_name=self.find_folders_by_name("../../design","compile.do","QUESTA")
        if file_name == '0':
            self.show_popup("Warning",f"you dont have 'questa' dir in your design please insert compile.do file")
            libs_path = str(QFileDialog.getOpenFileName(self, "open_file", "../../design/design_units/top/build/simulation/", '*.do', options=QFileDialog.DontUseNativeDialog)[0])
            file_name = str(libs_path)
        if path.exists(file_name):
            relpath=os.path.relpath(os.path.dirname(file_name),os.getcwd())
            with open(file_name, 'r') as f:
                libs = f.read()
                libs="vlib questa_lib\n"+libs
                libs = f"set design_src {relpath}\n"+libs
                libs=libs.replace('"..',f'"$design_src/..')
                libs=libs.replace('"+incdir+..',f'"+incdir+$design_src/..')
                libs=libs.replace('"glbl.v"','"$design_src/glbl.v"')
                if "xil_defaultlib.glbl" not in config['OPT_VSIM_ARGS']["VOPT_DEFAULT_ARGS"]:
                    config['OPT_VSIM_ARGS']["VOPT_DEFAULT_ARGS"]+= " xil_defaultlib.glbl"
                with open("vrc_compile_design.do", 'w') as f1:
                    f1.write(libs)
            config['COMMANDS']["COMPILE_DESIGN_CMD"]=" do vrc_compile_design.do"
            self.gui_update()

    def compile_env_push_bt(self):
        src = os.getcwd()
        src=src.split("/")
        src[-1]="src"
        src="/".join(src)
        current_location = src
        folders_with_files = self.find_folders_with_files(current_location)

        patternes_to_search = ['_if.sv', '_pkg','wrapper.sv','tb.sv']
        matching_files = []
        for pattern in patternes_to_search:
            for folder in folders_with_files:
                matching_files.extend(self.find_files_with_pattern(folder, pattern))

        # Replace prefix with "env_src$" and sort the files
        matching_files = [file.replace(src, "$env_src", 1) for file in matching_files]
   
        matching_files.insert(0,"vlog -sv -permissive")

        matching_files = [file+"\\" for file in matching_files]
        matching_files[-1]=matching_files[-1][:-1]
        env_id=0
        test_id=0
        for i  in range (len(matching_files)):
            if("/env/" in matching_files[i]):
                env_id=i
            if("/tests/" in matching_files[i]):
                test_id=i
        if(env_id != 0 and test_id !=0 and test_id>env_id):
            matching_files.insert(test_id-1, matching_files.pop(env_id))
        

        with open("vrc_compile_env.do","w")as file:
            for line in matching_files:
                file.write(line+ "\n")
        config['COMMANDS']["COMPILE_ENV_CMD"]="do vrc_compile_env.do"
        self.gui_update()
        
    def choose_generics_sets_button(self):
        self.genericsManager.load_generics_sets(self.genericsManager.defines_file)
        # if len(self.genericsManager.genericsListWidget.selectedItems()) == 0:
        #     self.ui.clear_generics_table_button.setEnabled(False)
        # else:
        #     
        # self.ui.clear_generics_table_button.setEnabled(True)
        
    # config write from text line
    def seed_line(self):
        config['RUN_OPTIONS']["SEED"] = self.ui.seed_line.text()

    def test_line(self):
        config['RUN_OPTIONS']["TEST"] = self.ui.test_line.text()

    def config_name_line(self):
        config['GENERAL']["CONFIG_NAME"] = self.ui.config_name_line.text()

    def run_time_line(self):
        config['RUN_STAGES']["RUN_TIME"] = self.ui.run_time_line.text()

    def tb_line(self):
        config['GENERAL']["TB_NAME"] = self.ui.tb_line.text()

    def modelsimini_line(self):
        config['GENERAL']["MODELSIMINI"] = self.ui.modelsimini_line.text()

    def testplan_line(self):
        config['REG_OPTIONS']["TESTPLAN"] = self.ui.testplan_line.text()

    def wave_line(self):
        config['RUN_OPTIONS']["WAVE"] = self.ui.wave_line.text()

    def work_dir_line(self):
        config['GENERAL']["WORK_DIR"] = self.ui.work_dir_line.text()

    def compile_design_line(self):
        config['COMMANDS']["COMPILE_DESIGN_CMD"] = self.ui.compile_design_line.text()

    def compile_vips_line(self):
        config['COMMANDS']["COMPILE_VIPS_CMD"] = self.ui.compile_vips_line.text()


    def compile_env_line(self):
        config['COMMANDS']["COMPILE_ENV_CMD"] = self.ui.compile_env_line.text()

    def post_compile_line(self):
        config['COMMANDS']["POST_COMPILE_CMD"] = self.ui.post_compile_line.text()

    def pre_compile_line(self):
        config['COMMANDS']["PRE_COMPILE_CMD"] = self.ui.pre_compile_line.text()

    def opt_libs_line(self):
        config['OPT_VSIM_ARGS']["VOPT_LIBRARIES_ARGS"] = self.ui.opt_libs_line.text()
    
    def opt_genenv_line(self):
        config['OPT_VSIM_ARGS']["VOPT_GENENV_LIBS"] = self.ui.opt_genenv_line.text()

    def opt_defualt_line(self):
        config['OPT_VSIM_ARGS']["VOPT_DEFAULT_ARGS"] = self.ui.opt_defualt_line.text()

    def opt_debug_line(self):
        config['OPT_VSIM_ARGS']["VOPT_DEBUG_ARGS"] = self.ui.opt_debug_line.text()

    def opt_visualizer_line(self):
        config['OPT_VSIM_ARGS']["VOPT_VISUAL_ARGS"] = self.ui.opt_visualizer_line.text()

    def opt_codecov_line(self):
        config['OPT_VSIM_ARGS']["VOPT_CODECOV_ARGS"] = self.ui.opt_codecov_line.text()

    def vsim_codecov_line(self):
        config['OPT_VSIM_ARGS']["VSIM_CODECOV_ARGS"] = self.ui.vsim_codecov_line.text()

    def vsim_debug_line(self):
        config['OPT_VSIM_ARGS']["VSIM_DEBUG_ARGS"] = self.ui.vsim_debug_line.text()

    def vsim_dpi_line(self):
        config['OPT_VSIM_ARGS']["VSIM_DPI_ARGS"] = self.ui.vsim_dpi_textbox.text()
        self.ui.vsim_dpi_textbox.setToolTip("DPI simulation commands (e.g. -sv_lib mySharedObject)")

    def vsim_defualt_line(self):
        config['OPT_VSIM_ARGS']["VSIM_DEFAULT_ARGS"] = self.ui.vsim_defualt_line.text()

    def vsim_visualizer_line(self):
        config['OPT_VSIM_ARGS']["VSIM_VISUAL_ARGS"] = self.ui.vsim_visualizer_line.text()


    def try_connect_widget(self, widget , data):
        try:
            widget.setChecked(data)
        except RuntimeError:
            pass
    
    def add_files_to_list(self):
        file_names, _ = QFileDialog.getOpenFileNames(self, "Select Files",  "../src/dv/dpi/", "Python Files (*.py);;C Files (*.c)", options=QFileDialog.DontUseNativeDialog)
        # check if files are under the pysv framework
        try:
            self.dpi.check_files_is_valid(file_names)
            if file_names:
                existing_files = set(item.data(Qt.UserRole) for item in self.ui.dpi_list.findItems("*", Qt.MatchWildcard))
                dpi_section = config.setdefault('DPI', {})
    
                for file_path in file_names:
                    file_name = os.path.basename(file_path)
                    if file_path not in existing_files:
                        item = QListWidgetItem(file_name) 
                        item.setToolTip(file_path)
                        item.setData(Qt.UserRole, file_path)  
                        self.ui.dpi_list.addItem(item)
                        if 'dv/dpi' in file_path:
                            sim_path=os.getcwd()
                            relative_path = os.path.relpath(file_path, sim_path)
                            dpi_section[file_name] = relative_path
                        else:
                            dpi_section[file_name] = file_path
                        
                        
                        self.dpi_files_paths.add(file_path)
                is_overrides, err_msg = self.dpi.check_name_overrides(self.dpi_files_paths)
                if is_overrides == True:
                    self.ui.dpi_build_errors_label.setText(err_msg)
                else:
                    self.ui.dpi_build_errors_label.setText("")
                self.update_dpi_buttons_state()
        except FileNotFoundError:
            self.show_popup("Invalid file", "Python file must be under the correct framework (pysv)")
        

            
    def open_file_in_vscode(self, item):
        # open file in vscode
        file_path = item.data(Qt.UserRole)  # full path
        normalized_path = os.path.normpath(file_path)  # normal path
        try:
            if self.os_name == "rafael":
                editor = "gedit"
            else:
                editor = "code"
            subprocess.Popen([editor, normalized_path ])  # open vscode
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open file in VSCode: {e}")

    def remove_file_list(self):
        # delete list
        self.ui.dpi_list.clear()
        self.ui.dpi_build_errors_label.setText("")
        self.dpi_files_paths=set()
        if 'DPI' in config:
            config.remove_section('DPI')
            config['OPT_VSIM_ARGS']["VSIM_DPI_ARGS"] = ""
            self.ui.vsim_dpi_textbox.setText(config['OPT_VSIM_ARGS']["VSIM_DPI_ARGS"]) # update gui
            self.ui.vsim_dpi_textbox.setToolTip("DPI simulation commands (e.g. -sv_lib mySharedObject)") # update gui
            self.save_config() # save vrc.config
        self.update_dpi_buttons_state()
    def gui_update(self):

        
        self.ui.config_name_line.setText(config['GENERAL']["CONFIG_NAME"])
        self.ui.Dark.setValue(int((config['GENERAL']["COLOR"])))
        self.set_stylesheet()

        # main tab
        self.ui.test_line.setText(config['RUN_OPTIONS']["TEST"])
        self.ui.seed_line.setText(config['RUN_OPTIONS']["SEED"])

        self.ui.clear_work_bt.setChecked(bool(int(config['RUN_OPTIONS']["CLEAR_WORK"])))
        self.ui.new_trans_bt.setChecked(bool(int(config['RUN_OPTIONS']["NEW_TRANSCRIPT"])))
        self.ui.save_wave_bt.setChecked(bool(int(config['RUN_OPTIONS']["SAVE_WAVE"])))
        self.ui.close_gui_bt.setChecked(bool(int(config['GENERAL']["CLOSE_GUI"])))

        self.try_connect_widget(self.ui.visualizer_bt,bool(int(config['RUN_OPTIONS']["VISUALIZER"])))
        self.try_connect_widget(self.ui.questasim_bt,bool(int(config['RUN_OPTIONS']["QUESTASIM"])))
        self.try_connect_widget(self.ui.vrun_bt,bool(int(config['RUN_OPTIONS']["VRUN"])))
        self.ui.debug_mode_bt.setChecked(bool(int(config['RUN_OPTIONS']["DEBUG_MODE"])))
        self.ui.code_cov_bt.setChecked(bool(int(config['RUN_OPTIONS']["CODECOV_MODE"])))
        self.ui.gui_bt.setChecked(bool(int(config['RUN_OPTIONS']["GUI_MODE"])))
        self.ui.dummy_dut_bt.setChecked(bool(int(config['RUN_OPTIONS']["DUMMY_DUT"])))

        self.ui.pre_comp_bt.setChecked(bool(int(config['RUN_STAGES']["PRE_COMPILE"])))
        self.ui.comp_design_bt.setChecked(bool(int(config['RUN_STAGES']["COMPILE_DESIGN"])))
        self.ui.comp_vips_bt.setChecked(bool(int(config['RUN_STAGES']["COMPILE_VIPS"])))
        self.ui.comp_dpi_bt.setChecked(bool(int(config['RUN_STAGES']["COMPILE_DPI"])))
        self.ui.compile_env_bt.setChecked(bool(int(config['RUN_STAGES']["COMPILE_ENV"])))
        self.ui.run_time_line.setText(config['RUN_STAGES']["RUN_TIME"])
        self.ui.post_compile_bt.setChecked(bool(int(config['RUN_STAGES']["POST_COMPILE"])))
        self.ui.opt_bt.setChecked(bool(int(config['RUN_STAGES']["OPTIMIZE"])))
        self.ui.simulate_bt.setChecked(bool(int(config['RUN_STAGES']["SIMULATION"])))
        
        
        self.ui.debug_config_db.setChecked(bool(int(config['RUN_OPTIONS']['CONFIG_DB_INFO'])))  # added by Ayala
        self.ui.debug_break_cb.setChecked(bool(int(config['RUN_OPTIONS']['BREAK']))) # added by Ayala
        self.ui.verbosity_combo_bt.setCurrentText(config['RUN_OPTIONS']["VERBOSITY"])
        self.ui.questa_ver_combo_bt.setCurrentText(config['GENERAL']["QUESTA_VER"])
        self.ui.visualizer_ver_combo_bt.setCurrentText(config['GENERAL']["VISUALIZER_VER"])
        self.ui.vrun_ver_combo_bt.setCurrentText(config['GENERAL']["VRUN_VER"])
        self.ui.vrc_ver_combo_bt.setCurrentText(config['GENERAL']["SCRIPT_VER"])
        self.ui.qvip_ver_combo_bt.setCurrentText(config['GENERAL']["QVIP_VER"])

        # DPI tab - added by Ayala
        self.update_file_list_from_config(self.ui.dpi_list)
        #  advanced tab
        self.ui.tb_line.setText(config['GENERAL']["TB_NAME"])
        self.ui.modelsimini_line.setText(config['GENERAL']["MODELSIMINI"])
        self.ui.testplan_line.setText(config['REG_OPTIONS']["TESTPLAN"])
        self.ui.wave_line.setText(config['RUN_OPTIONS']["WAVE"])
        self.ui.work_dir_line.setText(config['GENERAL']["WORK_DIR"])

        self.ui.compile_design_line.setText(config['COMMANDS']["COMPILE_DESIGN_CMD"])
        self.ui.compile_vips_line.setText(config['COMMANDS']["COMPILE_VIPS_CMD"])
        self.ui.compile_env_line.setText(config['COMMANDS']["COMPILE_ENV_CMD"])
        self.ui.post_compile_line.setText(config['COMMANDS']["POST_COMPILE_CMD"])
        self.ui.pre_compile_line.setText(config['COMMANDS']["PRE_COMPILE_CMD"])

        self.ui.opt_libs_line.setText(config['OPT_VSIM_ARGS']["VOPT_LIBRARIES_ARGS"])
        self.ui.opt_genenv_line.setText(config['OPT_VSIM_ARGS']["VOPT_GENENV_LIBS"])
        self.ui.opt_defualt_line.setText(config['OPT_VSIM_ARGS']["VOPT_DEFAULT_ARGS"])
        self.ui.opt_debug_line.setText(config['OPT_VSIM_ARGS']["VOPT_DEBUG_ARGS"])
        self.ui.opt_visualizer_line.setText(config['OPT_VSIM_ARGS']["VOPT_VISUAL_ARGS"])
        self.ui.opt_codecov_line.setText(config['OPT_VSIM_ARGS']["VOPT_CODECOV_ARGS"])

        self.ui.vsim_codecov_line.setText(config['OPT_VSIM_ARGS']["VSIM_CODECOV_ARGS"])
        self.ui.vsim_debug_line.setText(config['OPT_VSIM_ARGS']["VSIM_DEBUG_ARGS"])
        self.ui.vsim_defualt_line.setText(config['OPT_VSIM_ARGS']["VSIM_DEFAULT_ARGS"])
        self.ui.vsim_visualizer_line.setText(config['OPT_VSIM_ARGS']["VSIM_VISUAL_ARGS"])        
        self.ui.vsim_dpi_textbox.setText(config['OPT_VSIM_ARGS']["VSIM_DPI_ARGS"])# Added by Ayala
        
        # self.ui.testlist_line.setText(config['REG_OPTIONS']["TESTLIST"])
        self.ui.testplan_line.setText(config['REG_OPTIONS']["TESTPLAN"])

        self.ui.jobs_combo_bt.setCurrentText(config['REG_OPTIONS']["JOBS"])
        self.ui.TestNamePushButton.setText(self._translate("MainWindow", config['REG_OPTIONS']["TESTLIST"]))
        self.ui.triage_bt.setChecked(bool(int(config['REG_OPTIONS']["TRIAGE"])))
        self.ui.grid_bt.setChecked(bool(int(config['REG_OPTIONS']["GRID"])))
        self.ui.trend_bt.setChecked(bool(int(config['REG_OPTIONS']["TREND"])))
        self.ui.report_bt.setChecked(bool(int(config['REG_OPTIONS']["COV_REPORT"])))
        self.ui.mail_bt.setChecked(bool(int(config['REG_OPTIONS']["SEND_MAIL"])))
        self.ui.delete_vrmdata_bt.setChecked(bool(int(config['REG_OPTIONS']["DELETE_PREV_VRMDATA"])))
        self.ui.rerun_bt.setChecked(bool(int(config['REG_OPTIONS']["RERUN"])))


        

class GitUplode(QDialog):
    def __init__(self, description):
        global commited
        commited = False
        super().__init__()
        self.setWindowTitle('Commit To Git')
        self.resize(300, 100)
        self.git_label = QLabel('Commit to all fills to git or take last commit:', self)
        self.new_commit_button = QPushButton('Commit All', self)
        self.new_commit_button.clicked.connect(partial(self.commit_changes, description))

        self.last_commit_button = QPushButton('Last Commit', self)
        self.last_commit_button.clicked.connect(self.accept)

        layout = QVBoxLayout(self)
        layout.addWidget(self.git_label)
        layout.addWidget(self.new_commit_button)
        layout.addWidget(self.last_commit_button)

    def commit_changes(self, description):
        script_dir=os.getcwd()
        try:
            root_dir = subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).strip().decode()
            
            if script_dir.startswith(root_dir):
                cur_dir=os.getcwd()
                os.chdir(root_dir)
                subprocess.call(['git', 'add', '*'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                commit_message = description
                #commit_message = "commited from python"
                subprocess.call(['git', 'commit', '-m', commit_message], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                #subprocess.call(['git','tag','-a','vrc1', '-m', commit_message], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                subprocess.call(['git', 'push'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                #subprocess.call(['git', 'push', "--tag"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                os.chdir(cur_dir)
                print('# Files Commited')
        except:
            pass
        self.accept()

    def is_inside_repo(self):
        try:
            subprocess.run(['git', 'rev-parse', '--is-inside-work-tree'],stdout=subprocess.DEVNULL,  check=True)
            global commited
            commited = True
        except subprocess.CalledProcessError:
            pass

class ColoredComboBoxDelegate(QtWidgets.QStyledItemDelegate):
    def paint(self, painter, option, index):
        # Get the color for the item
        color = index.data( Qt.UserRole)
        if color:
            option.palette.setColor(QtGui.QPalette.Text, QtGui.QColor(color))
        
        super().paint(painter, option, index)

class CheckBugsPopup(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Check Bugs')
        self.resize(300, 100)
        if task.init_globals() == None:
            self.reject
        
        self.title_label = QLabel('Select the bug you want to check:', self)
        font= QtGui.QFont()
        font.setPointSize(8)
        self.footer_label = QLabel('Explanation:\ngray=New , green=Active , orange=Resolved , <vrc>=open by vrc', self)
        self.footer_label.setFont(font)
        self.bugs_combobox = QComboBox(self)
        self.bugs_combobox.setItemDelegate(ColoredComboBoxDelegate())
        workitem , stateitem =task.get_bug_workitems()
        for i in range(len(workitem)):
            if(stateitem[i]=="Resolved"):
                self.bugs_combobox.addItem(workitem[i], QtGui.QColor("orange").name())
            elif(stateitem[i]=="New"):
                self.bugs_combobox.addItem(workitem[i], QtGui.QColor("gray").name())
            elif(stateitem[i]=="Active"):
                self.bugs_combobox.addItem(workitem[i], QtGui.QColor("green").name())
            else:
                print(f"# ERRORE state is invalid state={stateitem[i]}")
              
        self.submit_button = QPushButton('Submit', self)
        self.submit_button.clicked.connect(self.accept)

        layout = QVBoxLayout(self)
        layout.addWidget(self.title_label)
        layout.addWidget(self.bugs_combobox)
        layout.addWidget(self.footer_label)
        layout.addWidget(self.submit_button)

class ReportBugsFeaturesPopup(QDialog):
    def __init__(self):
        super().__init__()
        self.default_member='Please Choose Member'
        self.setWindowTitle('Report Bugs')
        self.resize(600, 300)


        self.title_label = QLabel('Title of the Bug or Change Request:', self)
        self.title_textbox = QLineEdit(self)

        self.message_label = QLabel('Please provide a description of the issue or feature request:', self)
        self.message_textbox = QTextEdit(self)
        self.message_textbox.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        if not commited:
            self.project_label = QLabel('Select the project to assign to:', self)
            self.project_combobox = QComboBox(self)
            self.project_combobox.addItems(task.get_projects())

            self.repo_label = QLabel('Select the repo to assign to:', self)
            self.repo_combobox = QComboBox(self)
            self.repo_combobox.addItems(task.get_repos(self.project_combobox.currentText()))
            self.project_combobox.currentIndexChanged.connect(lambda: self.update_repo())
        else:
            self.project_label = QLabel('Select the project to assign to:', self)
            self.project_combobox = QComboBox(self)
            project_name = []
            project_name.append(task.get_current_project_name())
            self.project_combobox.addItems(project_name)

        self.report_type_label = QLabel('Select the type of report:', self)
        self.report_type_combobox = QComboBox(self)
        self.report_type_combobox.addItems(['Bug', 'Change Request'])


        self.member_label = QLabel('Select the member to assign to:', self)
        self.member_combobox = QComboBox(self)
        self.member_combobox.addItems(self.add_default_member())
        self.project_combobox.currentIndexChanged.connect(lambda: self.update_members())


        self.area_label = QLabel('Select the area to assign to:', self)
        self.area_combobox = QComboBox(self)
        self.area_combobox.addItems(task.get_root_areas_list("SOC_Dev_Department"))
        self.project_combobox.currentIndexChanged.connect(lambda: self.update_area())
        self.member_combobox.currentIndexChanged.connect(lambda: self.update_area())

        

        self.iteration_label = QLabel('Select the iteration to assign to:', self)
        self.iteration_combobox = QComboBox(self)
        self.iteration_combobox.addItems(task.get_iterations("SOC_Dev_Department"))
        self.project_combobox.currentIndexChanged.connect(lambda: self.update_iteration())



        self.submit_button = QPushButton('Submit', self)
        self.submit_button.clicked.connect(lambda: self.check_members())

        layout = QVBoxLayout(self)
        layout.addWidget(self.title_label)
        layout.addWidget(self.title_textbox)
        layout.addWidget(self.message_label)
        layout.addWidget(self.message_textbox)
        layout.addWidget(self.report_type_label)
        layout.addWidget(self.report_type_combobox)
        layout.addWidget(self.project_label)
        layout.addWidget(self.project_combobox)
        layout.addWidget(self.member_label)
        layout.addWidget(self.member_combobox)
        layout.addWidget(self.area_label)
        layout.addWidget(self.area_combobox)
        layout.addWidget(self.iteration_label)
        layout.addWidget(self.iteration_combobox)
        if not commited:
            layout.addWidget(self.repo_label)
            layout.addWidget(self.repo_combobox)
        layout.addWidget(self.submit_button)

    def add_default_member(self):
        members=task.get_members("SOC_Dev_Department")
        members=sorted(members)
        members.insert(0,self.default_member)
        uniq_members=[]
        [uniq_members.append(name) for name in members if name not in uniq_members ]
        return uniq_members
    
    def check_members(self):
        if self.member_combobox.currentText() == self.default_member:
            main_gui_window.show_popup(main_gui_window,"MEMBERS ERROR",f'"{self.member_combobox.currentText()}" is not valid members')
        else:
            self.accept()
    def get_report(self):
        title = self.title_textbox.text()
        message = self.message_textbox.toPlainText()
        report_type = self.report_type_combobox.currentText()
        member = self.member_combobox.currentText()
        area = self.area_combobox.currentText()
        iteration = self.iteration_combobox.currentText()
        if not commited:
            project = self.project_combobox.currentText()
            repo_name = self.repo_combobox.currentText()
        else:
            project = task.get_current_project_name()
            repo_name = task.get_repo_name()
        return title, message, report_type, member, project, area, iteration, repo_name

    def update_members(self):
        self.member_combobox.clear()
        members=task.get_members(self.project_combobox.currentText())
        members=sorted(members)
        members.insert(0,self.default_member)   
        uniq_members=[]
        [uniq_members.append(name) for name in members if name not in uniq_members ]     
        self.member_combobox.addItems(uniq_members)

    def update_area(self):
        self.area_combobox.clear()
        self.area_combobox.addItems(task.get_area("SOC_Dev_Department",self.member_combobox.currentText()))

    def update_iteration(self):
        self.iteration_combobox.clear()
        self.iteration_combobox.addItems(task.get_iterations(self.area_combobox.currentText()))

    def update_repo(self):
        self.repo_combobox.clear()
        self.repo_combobox.addItems(task.get_repos(self.project_combobox.currentText()))

        
class Get_Proj_Repo(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('CLONE REPO')
        self.resize(600, 300)
        self._translate = QtCore.QCoreApplication.translate
 
        self.project_label = QLabel('Select project:', self)
        self.project_combobox = QComboBox(self)
        self.project_combobox.addItems(task.get_projects())

        self.repo_label = QLabel('Select repo:', self)
        self.repo_combobox = QComboBox(self)
        self.repo_combobox.addItems(task.get_repos(self.project_combobox.currentText()))
        self.project_combobox.currentIndexChanged.connect(lambda: self.update_repo())
        
        self.dir_lable = QLabel("Directory To Clone:", self)
        self.dir_line = QLabel(os.getcwd(), self)
        self.create_dir_bt = QPushButton("Select Other Directory To Clone")
        self.create_dir_bt.clicked.connect(lambda: self.create_dir())
        self.dir_lable1 = QLabel("", self)


        self.submit_button = QPushButton('Clone', self)
        self.submit_button.clicked.connect(self.accept)

        layout = QVBoxLayout(self)
        layout.addWidget(self.dir_lable)
        layout.addWidget(self.dir_line)
        layout.addWidget(self.create_dir_bt)
        layout.addWidget(self.project_label)
        layout.addWidget(self.project_combobox)
        layout.addWidget(self.repo_label)
        layout.addWidget(self.repo_combobox)
        layout.addWidget(self.dir_lable1)
        
        # layout.addWidget(self.lable)
        layout.addWidget(self.submit_button)


    def get_report(self):
        project = self.project_combobox.currentText()
        repo_name = self.repo_combobox.currentText()
        clone_dir = self.dir_line.text()
        return  clone_dir,project, repo_name

    def update_repo(self):
        self.repo_combobox.clear()
        self.repo_combobox.addItems(task.get_repos(self.project_combobox.currentText()))

    def create_dir(self):
        sim_dir = str(QFileDialog.getExistingDirectory(self, "Select Directory" , options=QFileDialog.DontUseNativeDialog))
        if (sim_dir != ""):
            self.dir_line.setText(sim_dir)



redirect_qt_messages()
app = QApplication(sys.argv)



app.setStyleSheet("""
    QWidget {
        font-size: 14px;
    }
""")
w = main_gui_window()
if(args.PIPELINE == "0" and args.BATCH == "0"):
    w.show()
    w.set_stylesheet()
    sys.exit(app.exec_())
else:
    w.exec()

