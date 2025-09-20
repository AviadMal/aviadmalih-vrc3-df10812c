import sys
import os
from PySide2.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QListWidgetItem,
    QLabel, QLineEdit, QMessageBox, QFileDialog, QFormLayout, QGroupBox, QInputDialog
)
from PySide2.QtCore import Qt
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from utils.parse_constants import parse_constants
from PySide2.QtGui import QIcon

class ConstantsDialog(QDialog):
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.setWindowTitle('VHDL Constants Editor')
        self.setMinimumWidth(600)
        self.config = config
        self.constants_by_path = {}  # {path: [{'name':..., 'value':...}, ...]}
        self.paths = []  # order of paths
        self.layout = QVBoxLayout(self)
        self.group = QGroupBox("Constants")
        self.group_layout = QVBoxLayout(self.group)
        self.label = QLabel("Constants and their values:")
        self.label.setAlignment(Qt.AlignCenter)
        self.group_layout.addWidget(self.label)

        # Icon-only toggle check all button at the top left
        icon_layout = QHBoxLayout()
        self.toggle_check_btn = QPushButton()
        self.toggle_check_btn.setIcon(QIcon.fromTheme("view-refresh"))  # Use a standard icon, can be replaced
        self.toggle_check_btn.setToolTip("Toggle check/uncheck all")
        self.toggle_check_btn.setFixedSize(28, 28)
        self.toggle_check_btn.setStyleSheet('background: none; border: none;')
        self.toggle_check_btn.clicked.connect(self.toggle_check_all_constants)
        icon_layout.addWidget(self.toggle_check_btn)
        icon_layout.addStretch()
        self.group_layout.addLayout(icon_layout)

        self.list_widget = QListWidget()
        self.group_layout.addWidget(self.list_widget)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add Constant (Add pkg file)")
        self.add_btn.clicked.connect(self.add_pkg_file)
        self.add_btn.setStyleSheet('')
        self.edit_btn = QPushButton("Edit Constant")
        self.edit_btn.clicked.connect(self.edit_constants)
        self.edit_btn.setStyleSheet('')
        self.delete_btn = QPushButton("Delete Selected")
        self.delete_btn.clicked.connect(self.delete_selected_constants)
        self.delete_btn.setStyleSheet('')
        self.ok_btn = QPushButton("OK")
        self.ok_btn.clicked.connect(self.accept)
        self.ok_btn.setStyleSheet('background: #1976d2; color: white; border-radius: 6px; padding: 6px 18px;')
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.ok_btn)
        self.group_layout.addLayout(btn_layout)
        self.layout.addWidget(self.group)
        self.layout.addStretch()
        self.load_from_config()

    def delete_selected_constants(self):
        # מחק את כל הקבועים שמסומנים ב-v (checkbox)
        checked_constants = set()
        idx = 0
        for path in self.paths:
            idx += 1  # דלג על כותרת path
            for c in self.constants_by_path[path]:
                item = self.list_widget.item(idx)
                if item and (item.flags() & Qt.ItemIsUserCheckable) and item.checkState() == Qt.Checked:
                    checked_constants.add((path, c['name']))
                idx += 1
        # מחק מהמבנה הפנימי
        paths_to_remove = []
        for path in list(self.constants_by_path.keys()):
            self.constants_by_path[path] = [
                c for c in self.constants_by_path[path]
                if (path, c['name']) not in checked_constants
            ]
            if not self.constants_by_path[path]:
                paths_to_remove.append(path)
        # הסר נתיבים ריקים
        for path in paths_to_remove:
            del self.constants_by_path[path]
            if path in self.paths:
                self.paths.remove(path)
        self.refresh_list()
        
    def load_from_config(self):
        self.constants_by_path = {}
        self.paths = []
        base_dir = os.getcwd()
        checked_constants = set()
        if self.config.has_section('CONSTANT'):
            items = list(self.config.items('CONSTANT'))
            current_path = None
            for key, value in items:
                if key.startswith('path'):
                    rel_path = value
                    abs_path = os.path.abspath(os.path.join(base_dir, rel_path))
                    current_path = abs_path
                    self.paths.append(current_path)
                    self.constants_by_path[current_path] = []
                else:
                    if current_path:
                        self.constants_by_path[current_path].append({'name': key, 'value': value})
                        # כל constant שמגיע מה-config (ולא path) ייכנס לסט של checked
                        checked_constants.add((current_path, key))
        self.refresh_list(checked_constants=checked_constants)

    def add_pkg_file(self):
        # שמור אילו קבועים מסומנים כרגע
        checked_constants = set()
        idx = 0
        for path in self.paths:
            idx += 1  # skip path header
            for c in self.constants_by_path[path]:
                item = self.list_widget.item(idx)
                if item and (item.flags() & Qt.ItemIsUserCheckable) and item.checkState() == Qt.Checked:
                    checked_constants.add((path, c['name']))
                idx += 1
        path, _ = QFileDialog.getOpenFileName(self, "Select VHDL Package", "", "VHDL Files (*.vhd *.vhdl)")
        if not path:
            return
        if path in self.constants_by_path:
            QMessageBox.information(self, "Already Added", "This pkg file is already in the list.")
            return
        constants = parse_constants(path)
        if not constants:
            QMessageBox.warning(self, "No constants", "No constants found in the selected file.")
            return
        self.paths.append(path)
        self.constants_by_path[path] = []
        for c in constants:
            self.constants_by_path[path].append({'name': c['name'], 'value': c['value'], 'new': True})
        self.refresh_list(checked_constants=checked_constants)

    def refresh_list(self, checked_constants=None):
        self.list_widget.clear()
        for path_idx, path in enumerate(self.paths):
            path_item = QListWidgetItem(f"pkg: {path}")
            path_item.setFlags(Qt.ItemIsEnabled)
            path_item.setBackground(Qt.lightGray)
            self.list_widget.addItem(path_item)
            for c in self.constants_by_path[path]:
                key_in_config = self.is_constant_in_config(path, c['name'])
                if key_in_config:
                    item = QListWidgetItem(f"✔ {c['name']}: {c['value']}")
                    item.setFlags(Qt.ItemIsEnabled)
                else:
                    item = QListWidgetItem(f"{c['name']}: {c['value']}")
                    item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                    # שמור v עבור קבועים שנבחרו
                    if checked_constants and (path, c['name']) in checked_constants:
                        item.setCheckState(Qt.Checked)
                    else:
                        item.setCheckState(Qt.Unchecked)
                self.list_widget.addItem(item)

    def is_constant_in_config(self, path, name):
        if not self.config.has_section('CONSTANT'):
            return False
        found = False
        items = list(self.config.items('CONSTANT'))
        current_path = None
        for key, value in items:
            if key.startswith('path'):
                current_path = value
            elif current_path == path and key == name:
                found = True
                break
        return found

    def edit_constants(self):
        # מצא את כל constants שמסומנים ב-✔ (כבר שמורים) או שסומנו ב-checkbox
        edit_items = []
        item_map = {}
        idx = 0
        checked_constants = set()
        for path in self.paths:
            idx += 1  # skip path header
            for c in self.constants_by_path[path]:
                item = self.list_widget.item(idx)
                is_saved = self.is_constant_in_config(path, c['name'])
                is_checked = item and (item.flags() & Qt.ItemIsUserCheckable) and item.checkState() == Qt.Checked
                if is_saved or is_checked:
                    edit_items.append((path, c['name'], c['value']))
                    item_map[(path, c['name'])] = (c, item)
                if is_checked:
                    checked_constants.add((path, c['name']))
                idx += 1
        if not edit_items:
            QMessageBox.information(self, "No constants to edit", "No constants available for editing.")
            return
        dlg = EditConstantsDialog(edit_items, self)
        if dlg.exec_() == QDialog.Accepted:
            updated = dlg.get_updated()
            for path, name, new_value in updated:
                c, item = item_map[(path, name)]
                c['value'] = new_value
                is_saved = self.is_constant_in_config(path, name)
                if is_saved:
                    item.setText(f"✔ {name}: {new_value}")
                else:
                    item.setText(f"{name}: {new_value}")

    def accept(self):
        if self.config.has_section('CONSTANT'):
            self.config.remove_section('CONSTANT')
        self.config.add_section('CONSTANT')
        path_counter = 1
        base_dir = os.getcwd()  # Use current working directory as base
        for path in self.paths:
            rel_path = os.path.relpath(path, base_dir)
            self.config.set('CONSTANT', f'path{path_counter}', rel_path)
            for c in self.constants_by_path[path]:
                self.config.set('CONSTANT', c['name'], c['value'])
            path_counter += 1
        super().accept()

    def get_selected_constants(self):
        result = {}
        for path in self.paths:
            for c in self.constants_by_path[path]:
                result[c['name']] = c['value']
        return result

    def toggle_check_all_constants(self):
        # בדוק אם כולם מסומנים
        all_checked = True
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item and (item.flags() & Qt.ItemIsUserCheckable):
                if item.checkState() != Qt.Checked:
                    all_checked = False
                    break
        # אם כולם מסומנים - ננקה, אחרת נסמן את כולם
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item and (item.flags() & Qt.ItemIsUserCheckable):
                item.setCheckState(Qt.Unchecked if all_checked else Qt.Checked)

class EditConstantsDialog(QDialog):
    def __init__(self, items, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Constants")
        self.resize(400, 400)
        layout = QFormLayout(self)
        self.edits = []
        for path, name, value in items:
            le = QLineEdit()
            le.setText(str(value))
            self.edits.append((path, name, le))
            layout.addRow(QLabel(f"{name} ({os.path.basename(path)})"), le)
        btn = QPushButton("OK")
        btn.clicked.connect(self.accept)
        layout.addRow(btn)
        self.setLayout(layout)
    def get_updated(self):
        return [(path, name, le.text()) for path, name, le in self.edits] 
