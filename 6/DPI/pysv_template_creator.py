# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 18:46:29 2024

@author: ayalac
"""

import os

class pysvCreator:
    
    def get_template(self):
        with open('pysv_template.txt', 'r') as f:
            template = f.read()
            f.close()
            return template
        
    def create_pysv_template(self, filename="python_code.py"):
        with open(filename, 'w') as f:
            f.write(self.get_template())
            f.close()
            
            
            
p = pysvCreator()
p.create_pysv_template("fjfdkfdkfd.py")
