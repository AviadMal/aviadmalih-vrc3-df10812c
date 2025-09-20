import json
import sys
import os
from PySide2.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QCheckBox, QPushButton, QProgressBar, QTextEdit, QSizePolicy, QSpacerItem, QLineEdit, QMessageBox
)
from PySide2.QtCore import Qt, QThread, Signal, QTimer, QTime
import subprocess

class CompileThread(QThread):
    output = Signal(str)
    finished = Signal(int)
    def __init__(self, vendor, action):
        super().__init__()
        self.vendor = vendor
        self.action = action
    def run(self):
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../utils/compile_design.sh'))
        qrsh=f'/Projects/Firmver/scripts/qrsh -l nfq6 -now y -b y -cwd -N "vrc-vsim" env LD_LIBRARY_PATH={os.environ["LD_LIBRARY_PATH"]} '.split()
        if self.action=='compile':
            action_cmd=  "-c"
        elif self.action=='build & compile':
            action_cmd=  "-b -c"
        elif self.action=='build':
            action_cmd=  "-b"
        else:
            raise ValueError(f'Invalid action: {self.action}')    

        cmd = qrsh + [script_path, '-v', self.vendor ] + action_cmd.split()
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        for line in proc.stdout:
            self.output.emit(line)
        proc.wait()
        self.finished.emit(proc.returncode)
        

class CompileDesignGUI(QWidget):
    def __init__(self, config, config_path):
        super().__init__()
        # Output
        self.output = QTextEdit()
        self.config = config
        self.config_path = config_path
        self.first_error_line = None
        self.all_output_lines = []
        self.output_buffer = []  # Buffer for output lines
        self.output_update_timer = QTimer()
        self.output_update_timer.setInterval(100)  # עדכן כל 100ms
        self.output_update_timer.timeout.connect(self.flush_output_buffer)
        self.output_update_timer.start()
        self.setWindowTitle('Compile Design')
        self.setMinimumWidth(600)
        self.setStyleSheet('''
            QWidget {
                background: #f4f6fa;
                font-family: Arial, sans-serif;
                font-size: 13px;
            }
            QLabel#HeaderLabel {
                font-size: 20px;
                font-weight: bold;
                color: #1565c0;
                padding: 10px 0 20px 0;
            }
            QComboBox, QCheckBox, QPushButton, QProgressBar, QTextEdit {
                font-size: 13px;
            }
            QPushButton {
                background: #1976d2;
                color: white;
                border-radius: 6px;
                padding: 6px 18px;
            }
            QPushButton:disabled {
                background: #b0bec5;
                color: #ececec;
            }
            QProgressBar {
                height: 18px;
                border-radius: 6px;
            }
            QTextEdit {
                background: #fff;
                border: 1px solid #b0bec5;
                border-radius: 6px;
                padding: 8px;
            }
        ''')
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        # Header
        self.header = QLabel('Compile Design')
        self.header.setObjectName('HeaderLabel')
        self.header.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.header)
        # Vendor
        h_vendor = QHBoxLayout()
        h_vendor.addWidget(QLabel('Vendor:'))
        self.vendor_combo = QComboBox()
        self.vendor_combo.addItems(['vivado', 'quartus'])
        # Set default from config
        default_vendor = None
        if self.config.has_section('RUN_OPTIONS') and self.config.has_option('RUN_OPTIONS', 'vendor'):
            default_vendor = self.config.get('RUN_OPTIONS', 'vendor')
        if default_vendor and default_vendor in [self.vendor_combo.itemText(i) for i in range(self.vendor_combo.count())]:
            self.vendor_combo.setCurrentText(default_vendor)
        h_vendor.addWidget(self.vendor_combo)
        h_vendor.addStretch()
        layout.addLayout(h_vendor)
        
        # action
        h_action = QHBoxLayout()
        h_action.addWidget(QLabel('action:'))
        self.action_combo = QComboBox()
        default_action = 'build & compile'
        self.action_combo.addItems([default_action,'build', 'compile'])
        self.action_combo.setCurrentText(default_action)
        h_action.addWidget(self.action_combo)
        h_action.addStretch()
        layout.addLayout(h_action)
      
        # Progress
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)  # Indeterminate
        self.progress.setVisible(False)
        layout.addWidget(self.progress)
        # Output
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setMinimumHeight(220)
        self.output.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.output)
        # Status label
        self.status_label = QLabel('')
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet('font-weight: bold; font-size: 15px; color: #388e3c; padding: 8px;')
        self.status_label.setVisible(False)
        layout.addWidget(self.status_label)
        # OK/Close button
        self.ok_btn = QPushButton('OK')
        self.ok_btn.clicked.connect(self.on_ok)
        layout.addWidget(self.ok_btn)
        self.thread = None
        self.finished = False
        self.has_build_error = False
        # Search bar (hidden by default, shown on Ctrl+F)
        self.h_search = QHBoxLayout()
        self.search_line = QLineEdit()
        self.search_line.setPlaceholderText('Search output...')
        self.search_btn = QPushButton('Search')
        self.search_btn.clicked.connect(self.search_output)
        self.close_search_btn = QPushButton('X')
        self.close_search_btn.setFixedWidth(24)
        self.close_search_btn.clicked.connect(self.hide_search_bar)
        self.h_search.addWidget(self.search_line)
        self.h_search.addWidget(self.search_btn)
        self.h_search.addWidget(self.close_search_btn)
        self.search_bar_widget = QWidget()
        self.search_bar_widget.setLayout(self.h_search)
        self.search_bar_widget.setVisible(False)
        layout.addWidget(self.search_bar_widget)
        self.search_line.installEventFilter(self)
        #timer
        self.resize(300, 150)
        # רכיבים
        self.label = QLabel("00:00:00", self)
        self.label.setStyleSheet("font-size: 24px;")

        layout.addWidget(self.label)
 

        # timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        # start time
        self.time = QTime(0, 0, 0)


        
        # self.center_on_screen()  # Remove from __init__
    def keyPressEvent(self, event):
        # Show search bar on Ctrl+F
        if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_F:
            self.show_search_bar()
        else:
            super().keyPressEvent(event)

    def show_search_bar(self):
        self.search_bar_widget.setVisible(True)
        self.search_line.setFocus()
        self.search_line.selectAll()

    def hide_search_bar(self):
        self.search_bar_widget.setVisible(False)
        self.output.setFocus()

    def eventFilter(self, obj, event):
        # Hide search bar on Esc when search_line is focused
        if obj == self.search_line and event.type() == event.KeyPress:
            if event.key() == Qt.Key_Escape:
                self.hide_search_bar()
                return True
        return super().eventFilter(obj, event)

    def center_on_screen(self):
        screen = QApplication.primaryScreen()
        if screen:
            screen_geometry = screen.availableGeometry()
            x = screen_geometry.center().x() - self.width() // 2
            y = screen_geometry.center().y() - self.height() // 2
            self.move(x, y)


    def start_process(self):
        self.time = QTime(0, 0, 0)
        self.label.setText("00:00:00")
        self.timer.start(1000)  # כל שנייה

    def update_timer(self):
        self.time = self.time.addSecs(1)
        self.label.setText(self.time.toString("hh:mm:ss"))

    def end_process(self):
        self.timer.stop()


    def run_compile(self):
        self.ok_btn.setEnabled(False)
        self.progress.setVisible(True)
        self.status_label.setVisible(False)
        self.output.clear()
        self.all_output_lines = []
        self.first_error_shown = False
        self.first_error_line = None
        vendor = self.vendor_combo.currentText()
        action = self.action_combo.currentText()
        self.thread = CompileThread(vendor,action)
        self.thread.output.connect(self.append_output)
        self.thread.finished.connect(self.done)
        self.thread.start()
    
    def append_output(self, text):
        self.all_output_lines.append(text.rstrip('\n'))
        error_found = False
        html_line = None
        # Check for error indicators
        if text.startswith('ERRROR:') or text.startswith('Compile_design error:'):
            html_line = f'<span style="color:red; font-weight:bold;">{text.rstrip()}</span>'
            error_found = True
            if not self.first_error_shown:
                self.show_error_to_user(text.rstrip())
                self.first_error_shown = True
                self.first_error_line = text.rstrip()
        elif '** ERROR' in text:
            html_line = f'<span style="color:red; font-weight:bold;">{text.rstrip()}</span>'
            error_found = True
            if not self.first_error_shown:
                self.show_error_to_user(text.rstrip())
                self.first_error_shown = True
                self.first_error_line = text.rstrip()
        else:
            html_line = f'<span style="color:black;">{text.rstrip()}</span>'
        self.output_buffer.append(html_line + '<br>')
        if error_found:
            self.has_build_error = True
        if text.startswith("Compile_design summary: vopt libs are"):
            libs = text.split("Compile_design summary: vopt libs are", 1)[1].strip()
            if not self.config.has_section('OPT_VSIM_ARGS'):
                self.config.add_section('OPT_VSIM_ARGS')
            self.config.set('OPT_VSIM_ARGS', "VOPT_LIBRARIES_ARGS", libs)
            with open(self.config_path, 'w') as f:
                self.config.write(f)

    def flush_output_buffer(self):
        if self.output_buffer:
            html = ''.join(self.output_buffer)
            self.output.moveCursor(self.output.textCursor().End)
            self.output.insertHtml(html)
            self.output.moveCursor(self.output.textCursor().End)
            self.output_buffer.clear()

    def done(self, code):
        self.flush_output_buffer()  # Make sure all output is shown
        self.progress.setVisible(False)
        self.ok_btn.setEnabled(True)
        self.ok_btn.setText('Close')
        self.end_process()
        if self.has_build_error:
            self.status_label.setText('Build error')
            self.status_label.setStyleSheet('font-weight: bold; font-size: 15px; color: #c62828; padding: 8px;')
        else:
            self.status_label.setText('Build finished!')
            self.status_label.setStyleSheet('font-weight: bold; font-size: 15px; color: #388e3c; padding: 8px;')
        self.status_label.setVisible(True)
        self.finished = True
        

    def on_ok(self):
        # Save selected vendor to config
        self.start_process()
        selected_vendor = self.vendor_combo.currentText()
        if not self.config.has_section('RUN_OPTIONS'):
            self.config.add_section('RUN_OPTIONS')
        self.config.set('RUN_OPTIONS', 'vendor', selected_vendor)
        with open(self.config_path, 'w') as f:
            self.config.write(f)
        if self.finished:
            self.close()
        else:
            self.run_compile()
    
    def show_error_to_user(self, error_line):
        QMessageBox.critical(self, "compilation error", error_line)
    
    def search_output(self):
        text = self.search_line.text()
        if not text:
            return
        cursor = self.output.textCursor()
        document = self.output.document()
        found = document.find(text, 0)
        if found.isNull():
            QMessageBox.information(self, "Search", f'"{text}" was not found in the output.')
        else:
            self.output.setTextCursor(found)

if __name__ == '__main__':
    import sys
    from configparser import ConfigParser
    from PySide2.QtWidgets import QApplication

    if len(sys.argv) < 2:
        print("Usage: python compile_design_gui.py <config_path>")
        sys.exit(1)
    config_path = sys.argv[1]
    config = ConfigParser()
    config.read(config_path)

    app = QApplication(sys.argv)
    win = CompileDesignGUI(config, config_path)
    win.show()
    win.center_on_screen()
    sys.exit(app.exec_())
