# -*- coding: utf-8 -*-
"""
Used for different generics regression automation.

@author: ayalac
"""
import os
from os import path
from configparser import ConfigParser, ExtendedInterpolation
from datetime import datetime
from glob import glob
import random
import xml.etree.ElementTree as ET
import sys
from FileManager import get_next_line_in_file

class RegressionRunner:
    global vrun_setenv_cmd
    
    def __init__(self):
        self.init_path = os.environ["PATH"]
        self.config = self.load_vrc_config()
        gen = get_next_line_in_file()
        if (gen != ""):
            self.vrc_setenv_cmd =""
            self.set_path()
            self.set_env_path()
            self.vrun(gen.lower())
        
    # Setting paths into the environment variables
    def set_env_path(self):
        #  init path because we don't want to accumulate previous installation
        os.environ["PATH"] = self.init_path
        if sys.platform.startswith("linux"):

            self.vrc_setenv_cmd = self.vrc_path + self.config['GENERAL']["SCRIPT_VER"]

            qvip_path = self.qvip_path + self.config['GENERAL']['QVIP_VER'] + "/questa_mvc_core/linux_x86_64_gcc-7.4.0"

            vrun_setenv_cmd = self.questa_path + self.config['GENERAL']["VRUN_VER"] + "/questasim/bin" + ":"

            os.environ['LD_LIBRARY_PATH'] += ":" + qvip_path
            #os.environ['LD_LIBRARY_PATH'] += ":" + f"{self.py_path}"
            os.environ['VSIM_PATH'] = self.questa_path + self.config['GENERAL']["QUESTA_VER"] + "/questasim/bin/vsim "
            os.environ['VRUN_PATH'] = self.questa_path + self.config['GENERAL']["VRUN_VER"] + "/questasim/bin/vrun "
            os.environ['VIS_PATH']=self.visualizer_path+self.config['GENERAL']["VISUALIZER_VER"]+"/visualizer/bin/visualizer "
            os.environ['QUESTA_MVC_HOME'] = self.qvip_path + self.config['GENERAL']["QVIP_VER"]

            os.environ["PATH"] = vrun_setenv_cmd + os.environ["PATH"]

            if self.os_name == "rafael":
                os.environ['QRSH_CMD'] = f'qrsh -l nfq6 -now y -b y -N "vrc-vsim" -V -cwd -e /dev/null -o /dev/null env PATH={os.environ["PATH"]} env LD_LIBRARY_PATH={os.environ["LD_LIBRARY_PATH"]} '
                os.environ['VSIM_PATH'] += " -64 "
            elif self.os_name == "on_prem":
                os.environ['VSIM_PATH'] += " -64 "
                # os.environ['QRSH_CMD'] = f"sudo /usr/bin/Runapp.sh 2> /dev/null -c 8 -s "
                #temp!!!!!!!!
                os.environ['QRSH_CMD'] = f"export env PATH={os.environ['PATH']};export LD_LIBRARY_PATH=/Apps/mentor/questa/{config['GENERAL']['QUESTA_VER']}/questasim/gcc-7.4.0-linux_x86_64/lib:{os.environ['LD_LIBRARY_PATH']};"
                #os.environ['MODELSIM_TCL']="/Apps/mentor/questa/modelsim.tcl"
                #os.environ['VRUN_PATH'] +=  " -64 "
            elif self.os_name == "wild_west":
                os.environ['QRSH_CMD'] = f"export env PATH={os.environ['PATH']};export LD_LIBRARY_PATH=/Apps/mentor/questa/{self.config['GENERAL']['QUESTA_VER']}/questasim/gcc-7.4.0-linux_x86_64/lib:{os.environ['LD_LIBRARY_PATH']};"
                self.ui.app.setStyleSheet("""
                    QWidget {
                        font-size: 14px;
                    }
                """)
        elif sys.platform == "win32":
            os.environ['VIS_PATH'] = ""
            os.environ['VSIM_PATH'] = "vsim "
            os.environ['VRUN_PATH'] = "vrun "
            os.environ['QRSH_CMD'] = ""

            self.vrc_setenv_cmd = self.vrc_path + self.config['GENERAL']["SCRIPT_VER"]
            quest_dir = glob("C:\questasim*")
            try:
                os.environ["PATH"] += fr"{quest_dir[0]}\win64;"
            except IndexError:
                self.show_popup("ERROR", "you dont have questasim installation on your windows")

                #  Executes the vrun command and also generates the RMDB file

    # set the paths according to the different servers
    def set_path(self):
        if sys.platform.startswith("linux"):
            if os.path.exists("/ElcSoftware/misc/Python36TK/bin/python3"):
                self.os_name = "rafael"
            elif os.path.exists("/Projects/Firmver/Python/Python3.9.6/"):
                self.os_name = "on_prem"
            elif os.path.exists("/Enviroment/projects/Firmver/files/python368"):
                self.os_name = "wild_west"
        elif sys.platform == "win32":
            self.os_name = "windows"
        
        self.vrc_path =os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+ os.sep 
            
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
        elif self.os_name == "on_prem":
            self.visualizer_path = "/Apps/mentor/visualizer/"
            self.questa_path = "/Apps/mentor/questa/"
            self.qvip_path = "/Apps/mentor/qvip/"
            self.py_path = "/Projects/Firmver/Python/Python3.9.6/bin/python3.9"
        elif self.os_name == "windows":
            self.py_path = "python"
    

            
    #  read from self.config and write to gui
    def load_vrc_config(self):
        """
        Returns
        -------
        config : ConfigParser
            VRC config object.

        """
        config = ConfigParser(interpolation=ExtendedInterpolation())
        os.environ['LD_LIBRARY_PATH'] = "/usr/lib:/usr/openwin/lib:/usr/lib/X11"        
        vrc_config_path=path.join(os.getcwd(), "vrc.config")
        config.read(vrc_config_path)
        return config

    def vrun(self, gen=""):
        """
        Updates the config with the new generic, creates the regression's rmdb database and outputs to stdout the the vrun command to be executed
        from tcl.

        Parameters
        ----------
        gen : STRING, optional
            Name of the generic to use in regression. The default is "".

        Returns
        -------
        None.

        """
        date = datetime.now().strftime('VRMDATA_%Y-%m-%d_%H-%M-%S')
        
        # run the next regresstion with the vrun tool
        self.config['RUN_OPTIONS']["VRUN"]="1"
        self.config['RUN_OPTIONS']["QUESTASIM"]="0"
        self.config['RUN_OPTIONS']["VISUALIZER"]="0"
        
        #  execute vrun command
        vrun_cmd=""
        self.config['REG_OPTIONS']['GENERIC'] = f'-{gen}'
        
        if int((self.config['REG_OPTIONS']['GRID']) == 0 or self.os_name == "wild_west" or self.os_name == "on_prem"):
            vrun_cmd += os.environ['QRSH_CMD']

        if self.os_name == "on_prem":
            vrun_cmd +=os.environ['VRUN_PATH']
        vrun_cmd += f"vrun -rmdb {gen.upper()}_my.rmdb -vrmdata {date}_{gen.upper()}"
        vrun_cmd += f" -j {self.config['REG_OPTIONS']['JOBS']} "
        if bool(int(self.config['REG_OPTIONS']["RERUN"])) == 0 or bool(int(self.config['REG_OPTIONS']["DEBUG"])):
            vrun_cmd += " -nolocalrerun "
        if int(self.config['REG_OPTIONS']['COV_REPORT']) == 1:
            vrun_cmd +=f" -html -htmldir {date}_{gen.upper()}/vrunhtmlreport "

        vrun_cmd += f" -mseed {random.randint(1,1000000000)} " 

        vrun_cmd = f"{vrun_cmd}"
        
        self.save_config()
        
        self.create_my_rmdb(gen)

        print(vrun_cmd)

  
    def set_parameter(self, root, parameter, value):
        #  try- not al configuration defined as parameters in rmdb
        try:
            root.find(f'.//parameter[@name="{parameter}"]').text = value
        except AttributeError:
            pass
          
    def create_my_rmdb(self, gen):
        """
        Create the rmdb database for the regression run.

        Parameters
        ----------
        gen : STRING
            The generic that will be used in the regression run.

        Returns
        -------
        None.

        """
        #  read reg.rmdb in vrc path and configure my.rmdb according reg.rmdb & config file
        tree = ET.parse(os.path.join(self.vrc_setenv_cmd, "reg.rmdb"))  #
        root = tree.getroot()
        
        #  Iterate over all existing configuration in the config file
        for each_section in self.config.sections():
            for (each_key, each_val) in self.config.items(each_section):
                
                # set_parameter to my.rmdb
                self.set_parameter(root, each_key.upper(), each_val)

        self.set_parameter(root, "QRSH", os.environ['QRSH_CMD'])

        if int(self.config['REG_OPTIONS']['TRIAGE']) == 1:
            self.set_parameter(root, "triagefile", "(%DATADIR%)/triage.tdb")
            self.set_parameter(root, "triageoptions",f"-rulesfile {self.questa_path}{self.config['GENERAL']['QUESTA_VER']}/questasim/vm_src/uvm_generic_1.xform")
        
        if int(self.config['REG_OPTIONS']['DEBUG']) == 1:
            self.set_parameter(root, "DEBUGMODE", "1")
        
        if int(self.config['REG_OPTIONS']['TREND']) == 1:
            self.set_parameter(root, "trendfile", "(%DATADIR%)/trend.ucdb")

        if int(self.config['REG_OPTIONS']['SEND_MAIL']) == 1:
            self.set_parameter(root, "EMAIL_RECIPIENTS", "(%username%)@rafael.local")
            self.set_parameter(root, "EMAIL_SERVERS", "mw.rafael.local")
        
        if int(self.config['RUN_OPTIONS']["VISUALIZER"]) == 1:
            self.set_parameter(root, "VISUALIZER", "1")

        self.set_parameter(root,"MVC_HOME",os.environ['QUESTA_MVC_HOME'])

        #  create user rmdb
        tree.write(f'{gen.upper()}_my.rmdb')
        
        
    def save_config(self):
        """
        Dump the vrc config object.

        Returns
        -------
        None.

        """
        save_config_name = self.config['GENERAL']["CONFIG_NAME"]
        with open(save_config_name, 'w') as configfile:
            self.config.write(configfile)  

regRunner = RegressionRunner()
