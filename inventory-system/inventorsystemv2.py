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
mLHistoryList = []
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
        self.morningLoadVbox = QVBoxLayout(morningLoadContainer)
        morningLoadLabel = QLabel("MORNING LOAD")
        font = QFont("SansSerif", 15, QFont.Bold)
        morningLoadLabel.setFont(font)
        font = QFont("SansSerif", 10, QFont.DemiBold)
        chooseAgentBox = QHBoxLayout()
        agentLabel = QLabel("CHOOSE AGENT")
        agentLabel.setFont(font)
        self.agentComboBox = QComboBox()
        self.agentComboBox.addItems(agentNames)
        self.agentComboBox.currentTextChanged.connect( self.agent_changed )
        chooseAgentBox.addWidget(agentLabel)
        chooseAgentBox.addWidget(self.agentComboBox)

        #Defining elements of Description column
        chooseItemBox = QHBoxLayout()
        chooseItemLabel = QLabel("CHOOSE ITEM")
        chooseItemLabel.setFont(font)
        self.descriptionComboBox = QComboBox()
        self.descriptionComboBox.addItems(["ALFONSO 50cl", "ALFONSO 70cl"])
        self.descriptionComboBox.currentIndexChanged.connect( self.index_changed )
        itemIndex = self.descriptionComboBox.currentIndex()
        #self.descriptionComboBox.setEditable(True)
        self.descriptionComboBox.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)
        chooseItemBox.addWidget(chooseItemLabel)
        chooseItemBox.addWidget(self.descriptionComboBox)
        
        #Defining elements of row 1
        #stocksLabel = QLabel("Stocks")
        currentItemHeader = QLabel("DESCRIPTION")
        font = QFont("SansSerif", 10, QFont.Medium)
        self.currentItemLabel = QLabel(self.descriptionComboBox.currentText())
        stocksCaseLabel = QLabel("CASE")
        stocksPieceLabel = QLabel("PIECE")
        stocksPiecePerCaseLabel = QLabel("Piece per Case")
        currentItemHeader.setFont(font)
        stocksCaseLabel.setFont(font)
        stocksPieceLabel.setFont(font)
        stocksPiecePerCaseLabel.setFont(font)

        #Adding elements to row 2 of stocks
        
        self.descriptonCurrent = QLabel()
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
        self.claimIndex = 1
        self.currentAgent = QLabel(self.agentComboBox.currentText())

        self.caseInputLabel = QLabel("How many cases of "+self.descriptionComboBox.currentText()+" will "+self.agentComboBox.currentText()+" claim?")
        self.pieceInputLabel = QLabel("How many piece of "+self.descriptionComboBox.currentText()+" will "+self.agentComboBox.currentText()+" claim?")
        caseInputHBox = QHBoxLayout()
        caseInputHBox.addWidget(self.caseInputLabel)
        caseInputHBox.addWidget(self.caseInput)
        pieceInputHBox = QHBoxLayout()
        pieceInputHBox.addWidget(self.pieceInputLabel)
        pieceInputHBox.addWidget(self.pieceInput)
        self.morningLoadVbox.addWidget(morningLoadLabel)
        self.morningLoadVbox.addLayout(chooseAgentBox)
        

        self.currentAgent = QLabel(self.agentComboBox.currentText())
        #adding items to main grid
        self.morningLoadVbox.addLayout(chooseItemBox)
        self.morningLoadLayout = QGridLayout()
        self.morningLoadLayout.addWidget(currentItemHeader, 0, 0)
        self.morningLoadLayout.addWidget(stocksCaseLabel, 0, 1)
        self.morningLoadLayout.addWidget(stocksCaseLabel, 0, 1)
        self.morningLoadLayout.addWidget(stocksPieceLabel, 0, 2)
        self.morningLoadLayout.addWidget(stocksPiecePerCaseLabel, 0, 3)
        self.morningLoadLayout.addWidget(self.currentItemLabel, 1, 0)
        self.morningLoadLayout.addWidget(self.stocksCaseCurrent, 1, 1)  
        self.morningLoadLayout.addWidget(self.stocksPieceCurrent, 1, 2)
        self.morningLoadLayout.addWidget(self.stocksPiecePerCaseCurrent, 1, 3)
        #self.morningLoad.addWidget(self.agentName, 3, 0)
        self.morningLoadVbox.addLayout(self.morningLoadLayout)
        self.morningLoadVbox.addLayout(caseInputHBox)
        self.morningLoadVbox.addLayout(pieceInputHBox)
        self.morningLoadVbox.addWidget(self.loadBtn)
        

        """""""""
        self.morningLoadLayout.addWidget(claimedItemsLabel, 6, 0)
        self.morningLoadLayout.addWidget(claimedAgentLabel, 7, 0)
        self.morningLoadLayout.addWidget(claimedCaseLabel, 7, 1)
        self.morningLoadLayout.addWidget(claimedPieceLabel, 7, 2)
        self.morningLoadLayout.addWidget(claimedDescriptionLabel, 7, 3)
        """""""""

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

        #morning load history window
        mLHistoryContainer = QWidget()
        mLHistoryLayout = QVBoxLayout(mLHistoryContainer)
        columnTitles = ["Agent", "Description", "Case", "Piece"]
        mLHistoryLabel = QLabel("MORNING LOAD HISTORY")
        font = QFont("SansSerif", 15, QFont.Bold)
        mLHistoryLabel.setFont(font)
        mLHistoryLayout.addWidget(mLHistoryLabel)
        self.mLHistoryGrid = QGridLayout()
        for t in range(len(columnTitles)):
            font = QFont("SansSerif", 10, QFont.Medium)
            titleLabel = QLabel(columnTitles[t])
            titleLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
            titleLabel.setFont(font)
            self.mLHistoryGrid.addWidget(titleLabel, 0, t)
        mLHistoryLayout.addLayout(self.mLHistoryGrid)
        self.stacklayout.addWidget(mLHistoryContainer)



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
        self.caseInputLabel.setText("How many cases of "+self.descriptionComboBox.currentText()+" will "+self.agentComboBox.currentText()+" claim?")
        self.pieceInputLabel.setText("How many pieces of "+self.descriptionComboBox.currentText()+" will "+self.agentComboBox.currentText()+" claim?")
        self.currentItemLabel.setText(self.descriptionComboBox.currentText())
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
        font = QFont("SansSerif", 10, QFont.Normal)
        agentLabel.setFont(font)
        caseLabel.setFont(font)
        pieceLabel.setFont(font)
        descriptionLabel.setFont(font)
        self.mLHistoryGrid.addWidget(agentLabel, index, 0)
        self.mLHistoryGrid.addWidget(descriptionLabel, index, 1)
        self.mLHistoryGrid.addWidget(caseLabel, index, 2)
        self.mLHistoryGrid.addWidget(pieceLabel, index, 3)
        self.claimIndex += 1
        mLHistoryList.append([self.currentAgent.text(), str(int(self.caseInput.value())), str(int(self.pieceInput.value())), self.descriptionComboBox.currentText()])
        print(mLHistoryList)
        self.caseInput.setMaximum(int(self.stocksCaseCurrent.text()))
        if int(self.stocksCaseCurrent.text()) > 0:
            self.pieceInput.setMaximum(int(self.stocksPiecePerCaseCurrent.text()) - 1)
        else:
            self.pieceInput.setMaximum(int(self.stocksPieceCurrent.text()))

        #set values back to 0 after loading
        self.caseInput.setValue(0)
        self.pieceInput.setValue(0)

    def agent_changed(self, name):
        self.caseInputLabel.setText("How many cases of "+self.descriptionComboBox.currentText()+" will "+self.agentComboBox.currentText()+" claim?")
        self.pieceInputLabel.setText("How many pieces of "+self.descriptionComboBox.currentText()+" will "+self.agentComboBox.currentText()+" claim?")
        self.currentAgent.setText(name)

    

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()