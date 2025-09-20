# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 18:18:43 2024

@author: ayalac
"""
import os
import re
import shutil
import time 
import subprocess
                
class DPI_manager:
    
    def __init__(self, python_alias):
        self.python_alias=python_alias
        self.dpi_dir='dpi'
        
    def check_files_is_valid(self, src_files=[]):
        """
        Check if given files are under Pysv framework.
        If not - throws an exeption.

        Parameters
        ----------
        src_files : string list, optional
            List of Python script paths. The default is [].

        Returns
        -------
        None.

        """
        for file in src_files:
            self.get_build_dir_and_package_name(file)
            
    def get_build_dir_and_package_name(self, script_path):
        """
        Returns Build directory and SystemVerilog package name that are declared inside given Python file.

        Parameters
        ----------
        script_path : string
            Path to Python file.

        Raises
        ------
        FileNotFoundError
            If Python file is invalid (i.e. not under Pysv framework), raise a file not found exception.

        Returns
        -------
        build_res : string
            Build directory name which will hold all the compilation artifacts.
        package_res : string
            SystemVerilog package name which has the API to the methods inside given Python file.

        """
        cwd_pattern= r'^lib_path.*?\bcwd\s*="\s*([^\s]*)"'                          # regular expression pattern to handle optional spaces around '=' for 'cwd='
        filename_pattern = r'^generate_sv_binding.*?\bfilename\s*="\s*([^\s]*)"'    # regular expression pattern to handle optional spaces around '=' for 'filename='
        build_res=""
        package_res=""
        with open(script_path, 'r') as script_file:
            for line in script_file:
                build_match = re.search(cwd_pattern, line)          # search for 'cwd=' patten in the file
                package_match = re.search(filename_pattern, line)   # search for 'filename=' patten in the file
                
                if build_match:
                    build_res = build_match.group(1)
                elif package_match:
                    package_res = package_match.group(1) # return build dir name and systemverilog package name
        if (build_res == "" or package_res == ""):
            raise FileNotFoundError("Invalid Python file !! Missing pysv framework usage !!")
        return build_res, package_res
    
    def execute_script(self, script_path):
        """
        Executes given Python file. 

        Parameters
        ----------
        script_path : string
            Path to Python file.

        Returns
        -------
        build_res : TYPE
            Build directory name which will hold all the compilation artifacts.
        package_res : TYPE
            Systemverilog package name which has the API to the methods inside given Python file.

        """
        curr_dir = os.getcwd()
        dpi_dir_path = os.path.join(curr_dir, self.dpi_dir)
        if not os.path.isdir(dpi_dir_path):
            os.mkdir(dpi_dir_path)
        os.chdir(dpi_dir_path)

        build_res, package_res = self.get_build_dir_and_package_name(script_path)
        build_dir_path = os.path.join(dpi_dir_path, build_res)
        package_path = os.path.join(dpi_dir_path, package_res)
        if os.path.isdir(build_dir_path):
            shutil.rmtree(build_dir_path)
        # execute python script and capture output
        

        exit_code = os.system(self.python_alias + script_path)


        if exit_code != 0:
            print(f"Command faild with exit code {exit_code}")
        else:
            print("Command succeeded")
        os.chdir(curr_dir)
        return build_res, package_res 


    
    def check_name_overrides(self, dpi_files=[]):
        """
        Check if given Python files have overriding Build directory names and/or Package names.

        Parameters
        ----------
        dpi_files : list of strings
            DPI files paths. The default is [].

        Returns
        -------
        bool
            True if there's an error, False if everything's good.
        error_str : TYPE
            Debug message for user.

        """
        dictionary_names = []
        error_str=""

        for dpi_file in dpi_files:
            build_res, package_res = self.get_build_dir_and_package_name(dpi_file)
            if (build_res or package_res) in dictionary_names:
                error_str = error_str + "\nChange name of build and/or package inside: \n" + \
                    dpi_file + "\nIt has the same build/package name as a different file inside the DPI list. \nPackages and/or build directories with the same name will be overwritten; for that reason they must have different names." \
                        + "\nbuild dir: " + build_res + "\npackage name: " + package_res
            dictionary_names.extend([build_res, package_res])
        if error_str=="":
            return False, error_str
        return True, error_str
    
    def compile_dpi(self, dpi_files, prev_vrc_sv_lib_cmds=""):
        """
        Executes given list of DPI files

        Parameters
        ----------
        dpi_files : list of strings 
            List of DPI file paths to be executed.
        prev_vrc_sv_lib_cmds : string, optional
            previous vsim sv_lib commands. The default is "".

        Returns
        -------
        string
            Updated sv_lib command for vsim for the new DPIs (e.g. -sv_lib {path_1}/libysv -sv_lib {path_2}/libpysv).

        """
        

        curr_dir = os.getcwd()
        vrc_sv_lib_commands = set(prev_vrc_sv_lib_cmds.split('-sv_lib'))
        vrc_sv_lib_commands = {f'-sv_lib {element.strip()}' for element in vrc_sv_lib_commands if element.strip()}
        for dpi_file in dpi_files:
            build_dir, package_name = self.execute_script(dpi_file) # generate shared objects and systemverilog packages
            
            # move package to DPI directory (truncate if already exists)
            if os.path.exists(os.path.dirname(dpi_file) + "/" + package_name):
                os.remove(os.path.dirname(dpi_file) + "/" + package_name)
            shutil.move(curr_dir + "/" + self.dpi_dir + "/"  + package_name, os.path.dirname(dpi_file))
            
            cmd = "-sv_lib " + curr_dir + "/" + self.dpi_dir + "/" + build_dir + "/libpysv" # concat for vsim command  + "/libpysv" # concat for vsim command
            vrc_sv_lib_commands.add(cmd)
        
        return ' '.join(vrc_sv_lib_commands)
