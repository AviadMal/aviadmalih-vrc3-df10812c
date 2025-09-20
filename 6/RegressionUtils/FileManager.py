# -*- coding: utf-8 -*-
"""
Created on Sun Mar  2 20:40:58 2025

@author: ayalac
"""
import fcntl

def lock_file(file): # lock file to avoid dirty read/writes
    fcntl.flock(file, fcntl.LOCK_EX) # linux only (todo: add option for windows based on the system that's running the script)
        
def unlock_file(file):
    fcntl.flock(file, fcntl.LOCK_UN) # linux only (todo: add option for windows based on the system that's running the script)
        

def get_next_line_in_file(filename="generics_queue.txt", no_more_lines_msg=" No more generics in queue :)", file_doesnt_exits_msg="Oops! 'generics_queue.txt' doesn't exist."):
    """
     Get the next generic in the generics queue.   

    Returns
    -------
    STRING
        Next generics in regressions queue.

    """
    next_gen=""
    
    try:
        with open(filename, 'r+') as file:
            lock_file(file)
            lines = file.readlines()
            if lines:
                next_gen = lines[0].strip('\n')
                file.seek(0)
                file.truncate()
                if len(lines) > 1:
                    file.writelines(lines[1:])
            else:
                print(no_more_lines_msg)
            unlock_file(file)
    
    except FileNotFoundError:
        print(file_doesnt_exits_msg)
        return ""
    return next_gen
