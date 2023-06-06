import sys
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QStackedLayout, QStyle, QLabel, QComboBox, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLineEdit, QDoubleSpinBox, QTextEdit
from PyQt6.QtGui import QPalette, QColor, QPixmap, QFont
from layout_colorwidget import Color
import qtawesome as qta

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Warehouse Inventory")
        self.setFixedSize(QSize(700, 700))
    
        pagelayout = QHBoxLayout()
        button_layout = QVBoxLayout()
        self.stacklayout = QStackedLayout()

        pagelayout.addLayout(button_layout)
        pagelayout.addLayout(self.stacklayout)

        btn_icon = qta.icon('fa5s.box-open')
        btn = QPushButton(btn_icon, "Inventory")
        btn.setFixedSize(200, 60)
        btn.setIconSize(QSize(20, 20))
        font = QFont("Sans-serif")
        btn.setFont(font)
        btn.pressed.connect(self.activate_tab_1)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(Color("red"))

        btn_icon = qta.icon('fa5s.sun')
        btn = QPushButton(btn_icon, "Morning Load")
        btn.setFixedSize(200, 60)
        btn.setIconSize(QSize(20, 20))
        font = QFont("Sans-serif")
        btn.setFont(font)
        btn.pressed.connect(self.activate_tab_2)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(Color("green"))

        btn_icon = qta.icon('fa5s.moon')
        btn = QPushButton(btn_icon, "Backload")
        btn.setIconSize(QSize(20, 20))
        font = QFont("Sans-serif")
        btn.setFont(font)
        btn.setFixedSize(200, 60)
        btn.pressed.connect(self.activate_tab_3)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(Color("yellow"))

        btn_icon = qta.icon('fa5s.clock')
        btn = QPushButton(btn_icon, "Morning Load History")
        btn.setIconSize(QSize(20, 20))
        font = QFont("Sans-serif")
        btn.setFont(font)
        btn.setFixedSize(200, 60)
        btn.pressed.connect(self.activate_tab_4)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(Color("blue"))

        btn_icon = qta.icon('fa5s.clock')
        btn = QPushButton(btn_icon, "Backload History")
        btn.setIconSize(QSize(20, 20))
        font = QFont("Sans-serif")
        btn.setFont(font)
        btn.setFixedSize(200, 60)
        btn.pressed.connect(self.activate_tab_5)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(Color("orange"))

        widget = QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)

    def activate_tab_1(self):
        self.stacklayout.setCurrentIndex(0)

    def activate_tab_2(self):
        self.stacklayout.setCurrentIndex(1)

    def activate_tab_3(self):
        self.stacklayout.setCurrentIndex(2)

    def activate_tab_4(self):
        self.stacklayout.setCurrentIndex(3)

    def activate_tab_5(self):
        self.stacklayout.setCurrentIndex(4)

    

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()