# -*- coding: utf-8 -*-
"""
Template for Python code under pysv framework

DataType options: Bit, Byte, ShortInt, Int, LongInt, UByte, UShortInt, UInt, ULongInt, Object, String, Void (void can be used only for return type).
"""
from pysv import sv, compile_lib, generate_sv_binding, DataType

@sv(arg1=DataType.Int, arg2=DataType.Int, return_type=DataType.String)
def my_func1(arg1, arg2):
    # imports
    
    # do something
    
    return 0

@sv(arg1=DataType.Int, arg2=DataType.Int, return_type=DataType.String)
def my_func2(arg1, arg2):
    # imports
    
    # do something
    
    return 0
# compile the a shared_lib into build folder    
try:
    lib_path = compile_lib([my_func1, my_func2], cwd="my_build")
except FileNotFoundError as e:
    if "cmake" in str(e):
        print("CMake is not installed on this system. Compile DPI cannot be performed.\nPlease install cmake and try again.\nDetails:", e)
    else:
        print("File not found error:", e)
    exit(1)

# generate SV binding
generate_sv_binding([my_func1, my_func2], filename="my_pkg.sv" , pkg_name="my_pkg")    
