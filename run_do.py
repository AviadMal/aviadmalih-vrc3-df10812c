"""codeded by shahafg"""
from configparser import ConfigParser, ExtendedInterpolation
import sys
import os
import fileinput
import argparse
from os import path
import subprocess
#from colorama import Fore
parser = argparse.ArgumentParser()

# define arguments for command line
parser.add_argument("--PRE_COMPILE", "-pre_c",default="none", help="set TB_NAME val")
parser.add_argument("--COMPILE_DESIGN", "-c_d",default="none", help="set TB_NAME val")
parser.add_argument("--COMPILE_VIPS", "-c_vips",default="none", help="set TB_NAME val")
parser.add_argument("--COMPILE_ENV", "-c_e",default="none", help="set TB_NAME val")
parser.add_argument("--POST_COMPILE", "-post_c",default="none", help="set TB_NAME val")
parser.add_argument("--OPTIMIZE", "-opt",default="none", help="set TB_NAME val")
parser.add_argument("--SIMULATION", "-sim",default="none", help="set TB_NAME val")
parser.add_argument("--QSIM_GUI", "-qgui",default="0", help="use '-qgui 1' if you run vrc from mentor gui")

# Read arguments from the command line
args = parser.parse_args()

config = ConfigParser(interpolation=ExtendedInterpolation())

if (path.exists("vrc.config")):
    config_path = 'vrc.config'

config.read(config_path)

# create dir's for user
if not path.exists("run"):
    os.mkdir("run")
if not path.exists("log"):
    os.mkdir("log")


#[GENERAL]
TB_NAME                     =  config['GENERAL']["TB_NAME"]
RMDBDIR                     =  config['GENERAL']["RMDBDIR"]
WORK_DIR                    =  config['GENERAL']["WORK_DIR"]
MODELSIMINI                 =  config['GENERAL']["MODELSIMINI"]
WAVE_SIZE_LIMIT             =  config['GENERAL']["WAVE_SIZE_LIMIT"]
#SCRIPT_PATH                 =  config['GENERAL']["SCRIPT_PATH"]

#[COMMANDS]
PRE_COMPILE_CMD             =  config['COMMANDS']["PRE_COMPILE_CMD"]
PRE_COMPILE_DESIGN_CMD      =  config['COMMANDS']["PRE_COMPILE_DESIGN_CMD"]
COMPILE_DESIGN_CMD          =  config['COMMANDS']["COMPILE_DESIGN_CMD"]
POST_COMPILE_DESIGN_CMD     =  config['COMMANDS']["POST_COMPILE_DESIGN_CMD"]
COMPILE_VIPS_CMD          	=  config['COMMANDS']["COMPILE_VIPS_CMD"]
PRE_COMPILE_ENV_CMD         =  config['COMMANDS']["PRE_COMPILE_ENV_CMD"]
COMPILE_ENV_CMD             =  config['COMMANDS']["COMPILE_ENV_CMD"]
POST_COMPILE_ENV_CMD        =  config['COMMANDS']["POST_COMPILE_ENV_CMD"]
POST_COMPILE_CMD            =  config['COMMANDS']["POST_COMPILE_CMD"]
WAVE_LOG_CMD                =  config['COMMANDS']["WAVE_LOG_CMD"]

#[OPT_VSIM_ARGS]
VOPT_LIBRARIES_ARGS         =  config['OPT_VSIM_ARGS']["VOPT_LIBRARIES_ARGS"]
VOPT_GENENV_LIBS            =  config['OPT_VSIM_ARGS']["VOPT_GENENV_LIBS"]
VOPT_DEFAULT_ARGS           =  config['OPT_VSIM_ARGS']["VOPT_DEFAULT_ARGS"]
VOPT_DEBUG_ARGS             =  config['OPT_VSIM_ARGS']["VOPT_DEBUG_ARGS"]
VOPT_CODECOV_ARGS           =  config['OPT_VSIM_ARGS']["VOPT_CODECOV_ARGS"]
VOPT_VISUAL_ARGS            =  config['OPT_VSIM_ARGS']["VOPT_VISUAL_ARGS"]
VSIM_DEFAULT_ARGS           =  config['OPT_VSIM_ARGS']["VSIM_DEFAULT_ARGS"]
VSIM_DEBUG_ARGS             =  config['OPT_VSIM_ARGS']["VSIM_DEBUG_ARGS"]
VSIM_CODECOV_ARGS           =  config['OPT_VSIM_ARGS']["VSIM_CODECOV_ARGS"]
VSIM_DPI_ARGS               =  config['OPT_VSIM_ARGS']["VSIM_DPI_ARGS"] # Added by Ayala
VSIM_VISUAL_ARGS            =  config['OPT_VSIM_ARGS']["VSIM_VISUAL_ARGS"]
MAIL_TXT_ARGS               =  config['OPT_VSIM_ARGS']["MAIL_TXT_ARGS"]
MAIL_HTML_ARGS              =  config['OPT_VSIM_ARGS']["MAIL_HTML_ARGS"]

#[RUN_OPTIONS]
TEST                        =  config['RUN_OPTIONS']["TEST"]
SEED                        =  config['RUN_OPTIONS']["SEED"]
WAVE                        =  config['RUN_OPTIONS']["WAVE"]
VERBOSITY                   =  config['RUN_OPTIONS']["VERBOSITY"]
CLEAR_WORK                  =  config['RUN_OPTIONS']["CLEAR_WORK"]
CLEAR_TRANSCRIPT            =  config['RUN_OPTIONS']["CLEAR_TRANSCRIPT"]
NEW_TRANSCRIPT              =  config['RUN_OPTIONS']["NEW_TRANSCRIPT"]
SAVE_WAVE                   =  config['RUN_OPTIONS']["SAVE_WAVE"]
FREE_LICENSE                =  config['RUN_OPTIONS']["FREE_LICENSE"]
VISUALIZER                  =  config['RUN_OPTIONS']["VISUALIZER"]
VRUN                        =  config['RUN_OPTIONS']["VRUN"]
QUESTASIM                   =  config['RUN_OPTIONS']["QUESTASIM"]
DEBUG_MODE                  =  config['RUN_OPTIONS']["DEBUG_MODE"]
CODECOV_MODE                =  config['RUN_OPTIONS']["CODECOV_MODE"]
GUI_MODE                  	=  int(config['RUN_OPTIONS']["GUI_MODE"])
BREAK                       =  int(config["RUN_OPTIONS"]["BREAK"]) # Added by Ayala
DEBUG_CONFIG_DB             =  int(config["RUN_OPTIONS"]["DEBUG_CONFIG_DB"]) # Added by Ayala

#[RUN_STAGES]
PRE_COMPILE                    =  config['RUN_STAGES']["PRE_COMPILE"]
COMPILE_DESIGN                 =  config['RUN_STAGES']["COMPILE_DESIGN"]
COMPILE_VIPS                   =  config['RUN_STAGES']["COMPILE_VIPS"]
COMPILE_ENV                    =  config['RUN_STAGES']["COMPILE_ENV"]
POST_COMPILE                   =  config['RUN_STAGES']["POST_COMPILE"]
OPTIMIZE                       =  config['RUN_STAGES']["OPTIMIZE"]
SIMULATION                     =  config['RUN_STAGES']["SIMULATION"]
RUN_TIME                       =  config['RUN_STAGES']["RUN_TIME"]

VOPT_NAME = "opt_test" #need to add to the config


# delete work cmd & set editor
if sys.platform.startswith("linux"):
    clear_work_cmd= "rm -rf " + WORK_DIR
    editor="gedit"

elif sys.platform == "win32":
    clear_work_cmd= "rmdir /s /q " + WORK_DIR
    editor=r"C:\Windows\Notepad"



run_list =[]

def compile_stage():

    com_list =[]
    if (int(PRE_COMPILE)==1 and PRE_COMPILE_CMD!=""):
        com_list.append(PRE_COMPILE_CMD)

    if (int(COMPILE_DESIGN)==1):
        com_list.append("#-----------compile design-------")
        if(PRE_COMPILE_DESIGN_CMD!=""):
            com_list.append(PRE_COMPILE_DESIGN_CMD)
        if(COMPILE_DESIGN_CMD!=""): 
            com_list.append(COMPILE_DESIGN_CMD)
        if(POST_COMPILE_DESIGN_CMD!=""): 
            com_list.append(POST_COMPILE_DESIGN_CMD)
   
    if (int(COMPILE_VIPS)==1):
        if(COMPILE_VIPS_CMD!=""):
            com_list.append("#-----------compile vips---------")
            com_list.append(f"set QUESTA_MVC_HOME {os.environ['QUESTA_MVC_HOME']}")
            com_list.append("set env_src ../src")
            com_list.append(COMPILE_VIPS_CMD)

    if (int(COMPILE_ENV)==1):
        com_list.append("#-----------compile env----------")
        com_list.append("set env_src ../src")
        if(PRE_COMPILE_ENV_CMD!=""):
            com_list.append(PRE_COMPILE_ENV_CMD)
        if(COMPILE_ENV_CMD!=""):
            com_list.append(COMPILE_ENV_CMD)
        if(POST_COMPILE_ENV_CMD!=""):
            com_list.append(POST_COMPILE_ENV_CMD)

    if (int(POST_COMPILE)==1 and POST_COMPILE_CMD!=""):
        com_list.append(POST_COMPILE_CMD)

    if int(COMPILE_DESIGN)==1 or int(COMPILE_VIPS)==1 or int(COMPILE_ENV)==1:
        run_list.append("#-----------compile-------------")
        com_do_cmd="do run/com.do"
        run_list.append(com_do_cmd)

    with open("run/com.do", 'w', encoding='UTF-8') as f:
        for line in com_list: # creating the run/last.do file - contain all the pre simulation commands(compiles & optimization etc.)
            f.write(f"{line} \n")

def optimizition_stage():
    vopt_args = VOPT_DEFAULT_ARGS

    if(int(VISUALIZER)==1):
        vopt_args += " " + VOPT_VISUAL_ARGS
    elif (int(DEBUG_MODE)==1):
        vopt_args += " " + VOPT_DEBUG_ARGS

    if int(CODECOV_MODE)==1:
        vopt_args += " " + VOPT_CODECOV_ARGS

    opt_cmd ="vopt " + TB_NAME + " " + VOPT_LIBRARIES_ARGS  + " "  + VOPT_GENENV_LIBS + " " + vopt_args + " -l log/vopt.log -o " + VOPT_NAME
    with open("run/opt.do", 'w', encoding='UTF-8') as f:
        f.write(f"{opt_cmd} \n")

    if int(OPTIMIZE)==1:
        run_list.append("#-----------optimize-------------")
        opt_do_cmd="do run/opt.do"
        run_list.append(opt_do_cmd)

def simulation_stage():
    vsim_args = VSIM_DEFAULT_ARGS
    break_flag = " +uvm_set_action=*,_ALL_,UVM_ERROR,UVM_DISPLAY|UVM_STOP" if BREAK==1 else ""
    debug_config_db_flag = " +UVM_CONFIG_DB_TRACE"  if DEBUG_CONFIG_DB==1 else ""
    
    if(int(VISUALIZER)==1):
        vsim_args += " " + VSIM_VISUAL_ARGS
    elif (int(DEBUG_MODE)==1):
        vsim_args += " " + VSIM_DEBUG_ARGS

    if int(CODECOV_MODE)==1:
        vsim_args+= " " + VSIM_CODECOV_ARGS

    # in VISUALIZER mode we need whole path
    if(int(VISUALIZER)==1):
        vsim_cmd= os.environ['VSIM_PATH']
        vsim_cmd+= " -visualizer=" +'"'+ "visualizer_top.bin" +'" ' 
    # in questa mode we need whole path
    else:
        vsim_cmd= "vsim "

    vsim_cmd+=set_argu("set StdArithNoWarnings   1")
    vsim_cmd+=set_argu("set NumericStdNoWarnings 1")
    vsim_cmd+=set_argu("run 0")
    vsim_cmd+=set_argu(f"do {WAVE}") 
    if(int(VISUALIZER)==0):
        vsim_cmd+=set_argu(WAVE_LOG_CMD) 
    vsim_cmd+=set_argu(RUN_TIME) 

    vsim_cmd+=  " " + vsim_args + " " + VSIM_DPI_ARGS + " " + VOPT_NAME + " -lib " + WORK_DIR +" +UVM_TESTNAME="+TEST +" -sv_seed "+ SEED + debug_config_db_flag +" +UVM_VERBOSITY="+VERBOSITY + break_flag + " -modelsimini "+MODELSIMINI+ " -l log/vsim.log" +f" -mvchome {os.environ['QUESTA_MVC_HOME']} "
    with open("run/sim.do", 'w', encoding='UTF-8') as f:
        f.write(f"{vsim_cmd} \n")

    if int(SIMULATION)==1:
        #only for user future use (full last run script)
        run_list.append("#-----------simulation-------------")
        sim_do_cmd="do run/sim.do \n"
        run_list.append(sim_do_cmd)

       
def set_argu(argu):
    return " -do " +'"'+argu+'" ' 

def clear_terminal():
    run_list.append("quit -sim ")
    if(args.QSIM_GUI == '1'):
        run_list.append(".main clear ")

def clear_work():
    if (int(CLEAR_WORK)==1 and os.path.exists(WORK_DIR)):
        run_list.append(clear_work_cmd)
        run_list.append(f"vlib {WORK_DIR}")
    elif not os.path.exists(WORK_DIR):
        run_list.append(f"vlib {WORK_DIR}")
    run_list.append(f"vmap work {WORK_DIR}")


def new_transcript():
    if (int(NEW_TRANSCRIPT) and os.path.exists("transcript.txt")):
        os.remove("transcript.txt")

def error_check():
    for line in fileinput.input("log/compile.log"):
        if line.startswith("# ** Error:")==True or line.startswith("# ** Error")==True or line.startswith("# ** Fatal:")==True or line.startswith("# ** Fatal")==True:
            print (Fore.RED,line)
            return True
    return False


if __name__ == "__main__": # main is the default module: by defualt: __name__==main
    #got flags from command line parsing
    if (args.PRE_COMPILE != "none"):
        PRE_COMPILE=args.PRE_COMPILE
    if (args.COMPILE_DESIGN != "none"):
        COMPILE_DESIGN=args.COMPILE_DESIGN
    if (args.COMPILE_VIPS != "none"):
        COMPILE_VIPS=args.COMPILE_VIPS
    if (args.COMPILE_ENV != "none"):
        COMPILE_ENV=args.COMPILE_ENV
    if (args.POST_COMPILE != "none"):
        POST_COMPILE=args.POST_COMPILE
    if (args.OPTIMIZE != "none"):
        OPTIMIZE=args.OPTIMIZE
    if (args.SIMULATION != "none"):
        SIMULATION=args.SIMULATION

    if os.path.exists("run/last.do"):
        os.remove("run/last.do")
    
    new_transcript()
    clear_terminal()
    clear_work()
    compile_stage()
    optimizition_stage()
    simulation_stage() 
    
    # creating the run/last.do file - contain all the pre simulation commands(compiles & optimization etc.)
    with open("run/last.do", 'a', encoding='UTF-8') as f:
        for line in run_list: # creating the run/last.do file - contain all the pre simulation commands(compiles & optimization etc.)
            f.write(f"{line} \n")
    if(args.QSIM_GUI == '0'):
        run_cmd= os.environ['QRSH_CMD']+os.environ['VSIM_PATH']
        
        if int(GUI_MODE)==1:
            if(int(VISUALIZER)==0):
                run_cmd+=" -gui "
        else:
            run_cmd+= " -c" # -c for batch mode (without it's gui mode)
        
        run_cmd += " -l log/compile.log -do " + '"'+ "run/last.do" + '"'
   
    
    
    if(args.QSIM_GUI == '0'):
        if(int(VISUALIZER)==1 or int(GUI_MODE)==0):
             os.system(run_cmd)
        else:
            subprocess.Popen(run_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, )
       
    else:
        print("do run/last.do")


 
