import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QStackedLayout, QStyle, QLabel, QComboBox, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLineEdit, QDoubleSpinBox, QTextEdit
from PyQt6.QtGui import QPalette, QColor, QPixmap, QFont
from layout_colorwidget import Color
import qtawesome as qta

stocksCaseValues = ["24", "41"]
stocksPieceValues = ["11", "5"]
stocksPiecePerCase = ["12", "6"]
agentNames = ["OMAR", "DENNIS", "RIGOR", "JOSHUA", "KENNETH"]
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Warehouse Inventory")
        #self.setFixedSize(QSize(700, 700))
    
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
        
        ###START OF MORNING LOAD WINDOW
        morningLoadContainer = QWidget()
        self.morningLoadLayout = QGridLayout(morningLoadContainer)
        morningLoadLabel = QLabel("MORNING LOAD")
        agentLabel = QLabel("CHOOSE AGENT")
        agentComboBox = QComboBox()
        agentComboBox.addItems(agentNames)
        agentComboBox.currentTextChanged.connect( self.agent_changed )

        #Defining elements of Description column
        descriptionLabel = QLabel("CHOOSE ITEM")
        self.descriptionComboBox = QComboBox()
        self.descriptionComboBox.addItems(["ALFONSO 50cl", "ALFONSO 70cl"])
        self.descriptionComboBox.currentIndexChanged.connect( self.index_changed )
        itemIndex = self.descriptionComboBox.currentIndex()
        #self.descriptionComboBox.setEditable(True)
        self.descriptionComboBox.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)
        
        #Defining elements of row 1
        #stocksLabel = QLabel("Stocks")
        stocksCaseLabel = QLabel("Case")
        stocksPieceLabel = QLabel("Piece")
        stocksPiecePerCaseLabel = QLabel("Piece per Case")

        #Adding elements to row 2 of stocks
        
        self.stocksCaseCurrent = QLabel(stocksCaseValues[itemIndex])
        self.stocksPieceCurrent = QLabel(stocksPieceValues[itemIndex])
        self.stocksPiecePerCaseCurrent = QLabel(stocksPiecePerCase[itemIndex])
        #ROW 3: Morning Load
        #morningloadAgent = QComboBox()
        #morningloadAgent.addItems(["NOEL", "OMAR"])
        #morningloadAgent.setEditable(True)
        self.caseInput = QDoubleSpinBox()
        self.caseInput.setDecimals(0)
        
        self.pieceInput = QDoubleSpinBox()
        self.pieceInput.setDecimals(0)

        #setting maximum values of doublespinbox
        self.caseInput.setMaximum(int(self.stocksCaseCurrent.text()))
        if int(self.stocksCaseCurrent.text()) > 0:
            self.pieceInput.setMaximum(int(self.stocksPiecePerCaseCurrent.text()) - 1)
        else:
            self.pieceInput.setMaximum(int(self.stocksPieceCurrent.text()))


        self.loadBtn = QPushButton(text="LOAD")
        self.loadBtn.clicked.connect(self.update_stocks)

        #Row 4, Claimed Items
        #Row 5, Description, Case 
        claimedAgentLabel = QLabel("Agent")
        claimedCaseLabel = QLabel("Case")
        claimedPieceLabel = QLabel("Piece")
        claimedDescriptionLabel = QLabel("Description")
        #add item on table after computing

        claimedItemsLabel = QLabel("Claimed Items")
        totalLabel = QLabel("Total")
        self.claimIndex = 6
        
        self.currentAgent = QLabel(agentComboBox.currentText())


        align_top = Qt.AlignmentFlag.AlignTop
        self.morningLoadLayout.addWidget(morningLoadLabel, 0,0, align_top)
        self.morningLoadLayout.addWidget(agentLabel, 0,1, align_top)
        self.morningLoadLayout.addWidget(agentComboBox, 0,2, align_top)
        

        self.currentAgent = QLabel(agentComboBox.currentText())
        #adding items to main grid
        self.morningLoadLayout.addWidget(self.currentAgent, 1, 0)
        self.morningLoadLayout.addWidget(descriptionLabel, 2, 0)
        #self.morningLoad.addWidget(stocksLabel, 0, 1)
        self.morningLoadLayout.addWidget(stocksCaseLabel, 2, 1)
        self.morningLoadLayout.addWidget(stocksPieceLabel, 2, 2)
        self.morningLoadLayout.addWidget(stocksPiecePerCaseLabel, 2, 3)
        self.morningLoadLayout.addWidget(self.descriptionComboBox, 3, 0)
        self.morningLoadLayout.addWidget(self.stocksCaseCurrent, 3, 1)  
        self.morningLoadLayout.addWidget(self.stocksPieceCurrent, 3, 2)
        self.morningLoadLayout.addWidget(self.stocksPiecePerCaseCurrent, 3, 3)
        #self.morningLoad.addWidget(self.agentName, 3, 0)
        self.morningLoadLayout.addWidget(self.caseInput, 4, 1)
        self.morningLoadLayout.addWidget(self.pieceInput, 4, 2)
        self.morningLoadLayout.addWidget(self.loadBtn, 4, 3)
        self.morningLoadLayout.addWidget(claimedItemsLabel, 5, 0)
        self.morningLoadLayout.addWidget(claimedAgentLabel, 6, 0)
        self.morningLoadLayout.addWidget(claimedCaseLabel, 6, 1)
        self.morningLoadLayout.addWidget(claimedPieceLabel, 6, 2)
        self.morningLoadLayout.addWidget(claimedDescriptionLabel, 6, 3)

        self.stacklayout.addWidget(morningLoadContainer)

        ###END OF MORNING LOAD WINDOW

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

    def index_changed(self, index):
        self.stocksCaseCurrent.setText(stocksCaseValues[index])
        self.stocksPieceCurrent.setText(stocksPieceValues[index])
        self.stocksPiecePerCaseCurrent.setText(stocksPiecePerCase[index])

        #setting maximum values of doublespinbox
        self.caseInput.setMaximum(int(self.stocksCaseCurrent.text()))
        if int(self.stocksCaseCurrent.text()) > 0:
            self.pieceInput.setMaximum(int(self.stocksPiecePerCaseCurrent.text()) - 1)
        else:
            self.pieceInput.setMaximum(int(self.stocksPieceCurrent.text()))

    def update_stocks(self):
        stocksCaseValue = int(self.stocksCaseCurrent.text())
        inputCaseValue = int(self.caseInput.value())
        stocksPieceValue = int(self.stocksPieceCurrent.text())
        inputPieceValue = int(self.pieceInput.value())
        piecePerCaseValue = int(self.stocksPiecePerCaseCurrent.text())
        if (stocksPieceValue - inputPieceValue) < 0:
            stocksPieceValue = int(piecePerCaseValue) + (stocksPieceValue - inputPieceValue)
            stocksCaseValue -= 1
        else:
            stocksPieceValue = stocksPieceValue - inputPieceValue
        stocksCaseValue -= inputCaseValue

        self.stocksCaseCurrent.setText(str(stocksCaseValue))
        self.stocksPieceCurrent.setText(str(stocksPieceValue))

        itemIndex = self.descriptionComboBox.currentIndex()
        stocksCaseValues[itemIndex] = str(stocksCaseValue)
        stocksPieceValues[itemIndex] = str(stocksPieceValue)
        print("Claimed Item Deducted")
        
        print("Add to table: ", self.currentAgent.text(), inputCaseValue, inputPieceValue)
        index = self.claimIndex
        agentLabel = QLabel(self.currentAgent.text())
        caseLabel = QLabel(str(int(self.caseInput.value())))
        pieceLabel = QLabel(str(int(self.pieceInput.value())))
        descriptionLabel = QLabel(self.descriptionComboBox.currentText())
        #FIX, Problem with this, what if the user switches items.
        #create Vlayouts per column of the table that is rendered everytime the stocks are updated
        #create renderClaimedTable(self)
        #claimedColumn1 = QVBoxLayout()
        #claimedColumn2 = QVBoxLayout()
        #claimedColumn3 = QVBoxLayout()
        #self.morningLoad.addWidget(claimedColumn1, 6, 0)
        #self.morningLoad.addWidget(claimedColumn2, 6, 2)
        #self.morningLoad.addWidget(claimedColumn3, 6, 1)

        self.morningLoadLayout.addWidget(agentLabel, index, 0)
        self.morningLoadLayout.addWidget(caseLabel, index, 1)
        self.morningLoadLayout.addWidget(pieceLabel, index, 2)
        self.morningLoadLayout.addWidget(descriptionLabel, index, 3)
        self.claimIndex += 1

        self.caseInput.setMaximum(int(self.stocksCaseCurrent.text()))
        if int(self.stocksCaseCurrent.text()) > 0:
            self.pieceInput.setMaximum(int(self.stocksPiecePerCaseCurrent.text()) - 1)
        else:
            self.pieceInput.setMaximum(int(self.stocksPieceCurrent.text()))

    def agent_changed(self, name):
        self.currentAgent.setText(name)

    

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()