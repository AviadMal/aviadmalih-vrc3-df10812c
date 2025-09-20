# -*- coding: utf-8 -*-
"""
GUI helper class for generics.

@author: ayalac

"""
import re
from PySide2.QtWidgets import QDialog, QFileDialog, QTableWidgetItem, QListWidget
from gui.genericsWindow import Ui_genericsWindow
import os
import fcntl
class GenericsManager(QDialog, Ui_genericsWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setParent(parent)
        self.parent = parent
        self.setupUi(self) # set up the UI for the dialog
        self.genericsListWidget.setSelectionMode(QListWidget.MultiSelection) # allow user multiple selection out of list
        self.selectPushButton.clicked.connect(self.show_selected_items)
        self.defines_file=""
        self.generics_list=[] # set that the use chose
        self.all_generics_list=set()
        self.ui=parent.ui
        self.regressionGenericsTableWidget= self.ui.regressionGenericsTableWidget
        
    def show_selected_items(self):
        """
        Update the generics table according to what the user selected.

        Returns
        -------
        None.

        """
        selected_items = self.genericsListWidget.selectedItems()
        self.generics_list=[g.text() for g in selected_items]
        self.update_generics_table()
        self.close()
    
    def load_generics_sets(self, defines_file):
        """
        Open window with list of possible generics, user can select multiple generics using SHIFT and click

        Parameters
        ----------
        defines_file : STRING
            Path to defines file holding the generics.

        Returns
        -------
        all_generics_list : LIST
            All generic groups in file (e.g. "gen1", "gen2", "gen3")

        """
        self.show()
        all_generics_list = self.get_generics_sets_names(defines_file)
        self.genericsListWidget.clear()
        self.genericsListWidget.addItems(all_generics_list)
        return all_generics_list
        
    def get_generics_sets_names(self, defines_file):
        """
        Parse all possible generics from the given defines file.

        Parameters
        ----------
        defines_file : STRING
            Path to defines file that contains sets of generics.
            E.g. `ifdef GEN1

        Returns
        -------
        matches : LIST OF STRINGS
            Names of generics sets.
            E.g. [GEN1, GEN2, ... , GEN2]

        """
        pattern = r"\bifdef\s+(\w+)" # regular expression to match words starting with ifdef
        
        with open(defines_file, 'r') as file:
            content = file.read()
            
        # find all instances of words starting with `ifdef
        matches = re.findall(pattern, content)
        
        return matches
            
    def choose_defines_file(self): 
        """
        Opens a dialog for the user to choose a defines file from the file system.

        Returns
        -------
        STRING
            Defines file.
        STRING
            Full path of defines file.

        """
        dialog = QFileDialog(self)
        options = dialog.Options()
        options |= dialog.DontUseNativeDialog
        file, _ = dialog.getOpenFileName(self, "Open File", "../src/dv/env/", "SVH Files (*.svh)", options=options)

        if file:
            self.defines_file=file
            return os.path.basename(self.defines_file), self.defines_file
        else:
            self.clear_generics_table()
            return "[no file selected]", ""
        
    def clear_generics_table(self):
        """
        Clears the generics table from previous selecion.

        Returns
        -------
        None.

        """
        self.regressionGenericsTableWidget.setRowCount(0)
        with open('generics_queue.txt', 'w') as file:
                file.truncate()
                self.generics_list=[]
                
    def update_generics_table(self):
        """
        Updates the generics table according to the generics selected by the user.

        Returns
        -------
        None.

        """
        self.regressionGenericsTableWidget.setRowCount(len(self.generics_list))
        for i, gen in zip(range(len(self.generics_list)), self.generics_list):
            self.regressionGenericsTableWidget.setItem(i, 0, QTableWidgetItem(gen))
        if len(self.generics_list) == 0:
            self.parent.ui.clear_generics_table_button.setEnabled(False)
        else:
            self.parent.ui.clear_generics_table_button.setEnabled(True)
            
    def dump_generics_list(self):
        """
        Dumps the generics queue to a .txt file inside sim directory.

        Returns
        -------
        None.

        """
        with open('generics_queue.txt','w') as file:
            for gen in self.generics_list[1:]:
                file.write(gen + '\n')
                
