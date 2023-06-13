import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QStackedLayout, QScrollArea, QLabel, QComboBox, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLineEdit, QDoubleSpinBox, QTextEdit
from PyQt6.QtGui import QPalette, QColor, QPixmap, QFont
from layout_colorwidget import Color
import qtawesome as qta
import pandas as pd
import inventoryread as ir
df = pd.read_excel("current_stocks.xlsx")
df_history_ML = pd.read_excel('historyml.xlsx')
df_history_BL = pd.read_excel('historybl.xlsx')
stocksCaseValues = [str(x) for x in ir.get_all_case_values(df)]
stocksPieceValues = [str(x) for x in ir.get_all_piece_values(df)]
stocksPiecePerCase = [str(x) for x in  ir.get_all_ppc_values(df)]
stocksDescription = ir.get_all_description(df)
agentNames = ["NOEL", "OMAR", "RIGOR", "ENRICO", "ARNEL", "VICK", "MANNY", "ROMEL", "ELDIE", "JEROME", "DENNIS", "JERALD", "JOMAR", "MELVIN"]
mLHistoryList = df_history_ML.values.tolist()
print(mLHistoryList)
bLHistoryList = df_history_BL.values.tolist()
print(bLHistoryList)

#implement save changes functionality to modify values on dataframe
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Warehouse Inventory")
        self.setFixedSize(QSize(700, 400))
    
        pagelayout = QHBoxLayout()
        button_layout = QVBoxLayout()
        self.stacklayout = QStackedLayout()

        pagelayout.addLayout(button_layout)
        pagelayout.addLayout(self.stacklayout)

        btn_icon = qta.icon('fa5s.box-open')
        btn = QPushButton(btn_icon, "Inventory")
        btn.setFixedSize(200, 60)
        btn.setIconSize(QSize(20, 20))
        font = QFont("SansSerif")
        btn.setFont(font)
        btn.pressed.connect(self.activate_tab_1)
        button_layout.addWidget(btn)
        #START OF INVENTORY WINDOW
        inventoryContainer = QWidget()
        inventoryVBLayout = QVBoxLayout(inventoryContainer)
        inventoryTitle = QLabel("INVENTORY")
        fontTitle = QFont("SansSerif", 15, QFont.Bold)
        inventoryTitle.setFont(fontTitle)
        #self.inventoryTableContainer = QWidget()
        self.inventoryTableContainer = QWidget()
        self.inventoryTable = QGridLayout(self.inventoryTableContainer)
        scrollInventory = QScrollArea()
        scrollInventory.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scrollInventory.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scrollInventory.setWidgetResizable(True)
        scrollInventory.setWidget(self.inventoryTableContainer)
        self.columnTitles = ["DESCRIPTION", "CASE", "PIECE", "PIECE/CASE"]
        for t in range(len(self.columnTitles)):
            title = QLabel(self.columnTitles[t])
            font = QFont("SansSerif", 10, QFont.Medium)
            title.setFont(font)
            self.inventoryTable.addWidget(title, 0, t)

        for i in range(1, len(stocksCaseValues)+ 1):
            self.inventoryTable.addWidget(QLabel(stocksDescription[i-1]), i, 0)
            self.inventoryTable.addWidget(QLabel(stocksCaseValues[i-1]), i, 1)
            self.inventoryTable.addWidget(QLabel(stocksPieceValues[i-1]), i, 2)
            self.inventoryTable.addWidget(QLabel(stocksPiecePerCase[i-1]), i, 3)
        inventoryVBLayout.addWidget(inventoryTitle)
        inventoryVBLayout.addWidget(scrollInventory)
        self.stacklayout.addWidget(inventoryContainer)

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
        morningLoadLabel.setFont(fontTitle)
        fontChoose = QFont("SansSerif", 10, QFont.DemiBold)
        chooseAgentBox = QHBoxLayout()
        agentLabel = QLabel("CHOOSE AGENT")
        agentLabel.setFont(fontChoose)
        self.agentComboBox = QComboBox()
        self.agentComboBox.addItems(agentNames)
        self.agentComboBox.currentTextChanged.connect( self.agent_changed )
        chooseAgentBox.addWidget(agentLabel)
        chooseAgentBox.addWidget(self.agentComboBox)

        #Defining elements of Description column
        chooseItemBox = QHBoxLayout()
        chooseItemLabel = QLabel("CHOOSE ITEM")
        chooseItemLabel.setFont(fontChoose)
        self.descriptionComboBox = QComboBox()
        self.descriptionComboBox.addItems(stocksDescription)
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
        

        #adding items to main grid
        self.morningLoadVbox.addLayout(chooseItemBox)
        self.morningLoadLayout = QGridLayout()
        self.morningLoadLayout.addWidget(currentItemHeader, 0, 0)
        self.morningLoadLayout.addWidget(stocksCaseLabel, 0, 1)
        self.morningLoadLayout.addWidget(stocksCaseLabel, 0, 1)
        self.morningLoadLayout.addWidget(stocksPieceLabel, 0, 2)
        self.morningLoadLayout.addWidget(stocksPiecePerCaseLabel, 0, 3)
        self.morningLoadLayout.addWidget(self.currentItemLabel, 1, 0)
        self.currentItemLabel.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.morningLoadLayout.addWidget(self.stocksCaseCurrent, 1, 1)
        self.stocksCaseCurrent.setAlignment(Qt.AlignmentFlag.AlignTop)  
        self.morningLoadLayout.addWidget(self.stocksPieceCurrent, 1, 2)
        self.stocksPieceCurrent.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.morningLoadLayout.addWidget(self.stocksPiecePerCaseCurrent, 1, 3)
        self.stocksPiecePerCaseCurrent.setAlignment(Qt.AlignmentFlag.AlignTop)
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
        #START OF BACKLOAD WINDOW
        backloadContainer = QWidget()
        backloadLayout = QVBoxLayout(backloadContainer)
        backloadTitle = QLabel("BACKLOAD")
        backloadTitle.setFont(fontTitle)
        chooseAgentBoxBL = QHBoxLayout()
        chooseAgentLabelBL = QLabel("CHOOSE AGENT")
        chooseAgentLabelBL.setFont(fontChoose)
        self.agentComboBoxBL = QComboBox()
        self.agentComboBoxBL.addItems(agentNames)
        self.agentComboBoxBL.currentTextChanged.connect( self.agent_changed_BL )
        self.currentAgentBL = QLabel(self.agentComboBoxBL.currentText())
        chooseAgentBoxBL.addWidget(chooseAgentLabelBL)
        chooseAgentBoxBL.addWidget(self.agentComboBoxBL)
        chooseItemBoxBL = QHBoxLayout()
        chooseItemLabelBL = QLabel("CHOOSE ITEM")
        chooseItemLabelBL.setFont(fontChoose)
        self.chooseItemComboBoxBL = QComboBox()
        self.chooseItemComboBoxBL.addItems(stocksDescription)
        self.chooseItemComboBoxBL.currentIndexChanged.connect( self.index_changed_BL )
        chooseItemBoxBL.addWidget(chooseItemLabelBL)
        chooseItemBoxBL.addWidget(self.chooseItemComboBoxBL)
        #backloadGrid Section
        backloadGrid = QGridLayout()
        columnTitles = ["DESCRIPTION", "CASE", "PIECE", "PIECE PER CASE"]
        for i in range(len(columnTitles)):
            backloadGrid.addWidget(QLabel(columnTitles[i]), 0, i)
        self.currentItemBL = QLabel(self.chooseItemComboBoxBL.currentText())
        self.currentItemBL.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.stocksCaseCurrentBL = QLabel(stocksCaseValues[self.chooseItemComboBoxBL.currentIndex()])
        self.stocksCaseCurrentBL.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.stocksPieceCurrentBL = QLabel(stocksPieceValues[self.chooseItemComboBoxBL.currentIndex()])
        self.stocksPieceCurrentBL.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.stocksPPCCurrentBL = QLabel(stocksPiecePerCase[self.chooseItemComboBoxBL.currentIndex()])
        self.stocksPPCCurrentBL.setAlignment(Qt.AlignmentFlag.AlignTop)
        backloadGrid.addWidget(self.currentItemBL, 1, 0)
        backloadGrid.addWidget(self.stocksCaseCurrentBL, 1, 1)
        backloadGrid.addWidget(self.stocksPieceCurrentBL, 1, 2)
        backloadGrid.addWidget(self.stocksPPCCurrentBL, 1, 3)
        #caseInputBox Section
        caseInputBoxBL = QHBoxLayout()
        self.caseInputLabelBL = QLabel("How many cases of "+self.chooseItemComboBoxBL.currentText()+" will "+self.agentComboBoxBL.currentText()+" return?")
        self.caseInputBL = QDoubleSpinBox()
        self.caseInputBL.setDecimals(0)
        #pieceInputBox Section
        pieceInputBoxBL = QHBoxLayout()
        self.pieceInputLabelBL = QLabel("How many pieces of "+self.chooseItemComboBoxBL.currentText()+" will "+self.agentComboBoxBL.currentText()+" return?")
        self.pieceInputBL = QDoubleSpinBox()
        self.pieceInputBL.setDecimals(0)
        caseInputBoxBL.addWidget(self.caseInputLabelBL)
        caseInputBoxBL.addWidget(self.caseInputBL)
        pieceInputBoxBL.addWidget(self.pieceInputLabelBL)
        pieceInputBoxBL.addWidget(self.pieceInputBL)
        #setting maximum values of doublespinbox
        #self.caseInputBL.setMaximum(int(self.stocksCaseCurrentBL.text()))
        if int(self.stocksCaseCurrentBL.text()) > 0:
            self.pieceInputBL.setMaximum(int(self.stocksPPCCurrentBL.text()) - 1)
        #else:
        #    self.pieceInputBL.setMaximum(int(self.stocksPieceCurrentBL.text()))
        self.loadBtnBL = QPushButton(text="LOAD")
        self.loadBtnBL.clicked.connect(self.update_stocks_BL)
        self.returnIndex = 1
        font = QFont("SansSerif")
        self.loadBtnBL.setFont(font)


        backloadLayout.addWidget(backloadTitle)
        backloadLayout.addLayout(chooseAgentBoxBL)
        backloadLayout.addLayout(chooseItemBoxBL)
        backloadLayout.addLayout(backloadGrid)
        backloadLayout.addLayout(caseInputBoxBL)
        backloadLayout.addLayout(pieceInputBoxBL)
        backloadLayout.addWidget(self.loadBtnBL)
        self.stacklayout.addWidget(backloadContainer)

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
        self.columnTitles = ["Agent", "Description", "Case", "Piece"]
        mLHistoryLabel = QLabel("MORNING LOAD HISTORY")
        mLHistoryLabel.setFont(fontTitle)
        mLHistoryLayout.addWidget(mLHistoryLabel)
        mLHistoryGridScroll = QScrollArea()
        mLHistoryGridContainer = QWidget()
        self.mLHistoryGrid = QGridLayout(mLHistoryGridContainer)
        for t in range(len(self.columnTitles)):
            font = QFont("SansSerif", 10, QFont.Medium)
            titleLabel = QLabel(self.columnTitles[t])
            titleLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
            titleLabel.setFont(font)
            self.mLHistoryGrid.addWidget(titleLabel, 0, t)

        mLHistoryGridScroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        mLHistoryGridScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        mLHistoryGridScroll.setWidgetResizable(True)
        mLHistoryGridScroll.setWidget(mLHistoryGridContainer)

        mLHistoryLayout.addWidget(mLHistoryGridScroll)
        self.stacklayout.addWidget(mLHistoryContainer)


        btn_icon = qta.icon('fa5s.clock')
        btn = QPushButton(btn_icon, "Backload History")
        btn.setIconSize(QSize(20, 20))
        font = QFont("Sans-serif")
        btn.setFont(font)
        btn.setFixedSize(200, 60)
        btn.pressed.connect(self.activate_tab_5)
        button_layout.addWidget(btn)
        #backload history window
        bLHistoryContainer = QWidget()
        bLHistoryLayout = QVBoxLayout(bLHistoryContainer)
        self.columnTitles = ["Agent", "Description", "Case", "Piece"]
        bLHistoryLabel = QLabel("BACKLOAD HISTORY")
        bLHistoryLabel.setFont(fontTitle)
        bLHistoryLayout.addWidget(bLHistoryLabel)
        bLHistoryGridScroll = QScrollArea()
        bLHistoryGridContainer = QWidget()
        self.bLHistoryGrid = QGridLayout(bLHistoryGridContainer)
        for t in range(len(self.columnTitles)):
            font = QFont("SansSerif", 10, QFont.Medium)
            titleLabel = QLabel(self.columnTitles[t])
            titleLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
            titleLabel.setFont(font)
            self.bLHistoryGrid.addWidget(titleLabel, 0, t)

        bLHistoryGridScroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        bLHistoryGridScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        bLHistoryGridScroll.setWidgetResizable(True)
        bLHistoryGridScroll.setWidget(bLHistoryGridContainer)

        bLHistoryLayout.addWidget(bLHistoryGridScroll)
        self.stacklayout.addWidget(bLHistoryContainer)

        #scroll = QScrollArea()
        widget = QWidget()
        widget.setLayout(pagelayout)
        self.setGeometry(600, 100, 700, 400)
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

    def index_changed_BL(self, index):
        self.caseInputLabelBL.setText("How many cases of "+self.chooseItemComboBoxBL.currentText()+" will "+self.agentComboBoxBL.currentText()+" return?")
        self.pieceInputLabelBL.setText("How many pieces of "+self.chooseItemComboBoxBL.currentText()+" will "+self.agentComboBoxBL.currentText()+" return?")
        self.currentItemBL.setText(self.chooseItemComboBoxBL.currentText())
        self.stocksCaseCurrentBL.setText(stocksCaseValues[index])
        self.stocksPieceCurrentBL.setText(stocksPieceValues[index])
        self.stocksPPCCurrentBL.setText(stocksPiecePerCase[index])

        #setting maximum values of doublespinbox
        #self.caseInputBL.setMaximum(int(self.stocksCaseCurrentBL.text()))
        if int(self.stocksCaseCurrentBL.text()) > 0:
            self.pieceInputBL.setMaximum(int(self.stocksPPCCurrentBL.text()) - 1)
        #else:
        #    self.pieceInputBL.setMaximum(int(self.stocksPieceCurrentBL.text()))

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
        self.stocksCaseCurrentBL.setText(str(stocksCaseValue))
        self.stocksPieceCurrentBL.setText(str(stocksPieceValue))

        itemIndex = self.descriptionComboBox.currentIndex()
        #updating data on local list
        stocksCaseValues[itemIndex] = str(stocksCaseValue)
        stocksPieceValues[itemIndex] = str(stocksPieceValue)
        #updating data on excel file
        ir.update_stocks_df(df, itemIndex, stocksCaseValue, stocksPieceValue)
        print("Claimed Item Deducted")
        
        print("Add to table: ", self.agentComboBox.currentText(), inputCaseValue, inputPieceValue)
        index = self.claimIndex
        agentLabel = QLabel(self.agentComboBox.currentText())
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
        mLHistoryList.append([self.agentComboBox.currentText(), self.descriptionComboBox.currentText(), str(int(self.caseInput.value())), str(int(self.pieceInput.value()))])
        ir.update_history_ml(mLHistoryList, "Morning Load")
        self.caseInput.setMaximum(int(self.stocksCaseCurrent.text()))
        if int(self.stocksCaseCurrent.text()) > 0:
            self.pieceInput.setMaximum(int(self.stocksPiecePerCaseCurrent.text()) - 1)
        else:
            self.pieceInput.setMaximum(int(self.stocksPiecePerCaseCurrent.text()))

        #set values back to 0 after loading
        self.caseInput.setValue(0)
        self.pieceInput.setValue(0)

    def update_stocks_BL(self):
        stocksCaseValue = int(self.stocksCaseCurrentBL.text())
        inputCaseValue = int(self.caseInputBL.value())
        stocksPieceValue = int(self.stocksPieceCurrentBL.text())
        inputPieceValue = int(self.pieceInputBL.value())
        piecePerCaseValue = int(self.stocksPPCCurrentBL.text())
        if (stocksPieceValue + inputPieceValue) >= piecePerCaseValue:
            stocksPieceValue = (stocksPieceValue + inputPieceValue) - piecePerCaseValue
            stocksCaseValue += 1
        else:
            stocksPieceValue = stocksPieceValue + inputPieceValue
        stocksCaseValue += inputCaseValue

        self.stocksCaseCurrentBL.setText(str(stocksCaseValue))
        self.stocksPieceCurrentBL.setText(str(stocksPieceValue))
        self.stocksCaseCurrent.setText(str(stocksCaseValue))
        self.stocksPieceCurrent.setText(str(stocksPieceValue))

        itemIndex = self.chooseItemComboBoxBL.currentIndex()
        #updating data on local list
        stocksCaseValues[itemIndex] = str(stocksCaseValue)
        stocksPieceValues[itemIndex] = str(stocksPieceValue)
        #updating data on excel file
        ir.update_stocks_df(df, itemIndex, stocksCaseValue, stocksPieceValue)
        print("Claimed Item Deducted")
        
        print("Add to table: ", self.agentComboBoxBL.currentText(), inputCaseValue, inputPieceValue)
        index = self.returnIndex
        agentLabel = QLabel(self.agentComboBoxBL.currentText())
        caseLabel = QLabel(str(int(self.caseInputBL.value())))
        pieceLabel = QLabel(str(int(self.pieceInputBL.value())))
        descriptionLabel = QLabel(self.chooseItemComboBoxBL.currentText())
        font = QFont("SansSerif", 10, QFont.Normal)
        agentLabel.setFont(font)
        caseLabel.setFont(font)
        pieceLabel.setFont(font)
        descriptionLabel.setFont(font)
        self.bLHistoryGrid.addWidget(agentLabel, index, 0)
        self.bLHistoryGrid.addWidget(descriptionLabel, index, 1)
        self.bLHistoryGrid.addWidget(caseLabel, index, 2)
        self.bLHistoryGrid.addWidget(pieceLabel, index, 3)
        self.returnIndex += 1
        bLHistoryList.append([self.agentComboBoxBL.currentText(), self.chooseItemComboBoxBL.currentText(), str(int(self.caseInputBL.value())), str(int(self.pieceInputBL.value()))])
        ir.update_history_bl(bLHistoryList, "Backload")
        #self.caseInputBL.setMaximum(int(self.stocksCaseCurrentBL.text()))
        if int(self.stocksCaseCurrentBL.text()) > 0:
            self.pieceInputBL.setMaximum(int(self.stocksPPCCurrentBL.text()) - 1)
        #else:
        #    self.pieceInputBL.setMaximum(int(self.stocksPPCCurrentBL.text()))

        #set values back to 0 after loading
        self.caseInputBL.setValue(0)
        self.pieceInputBL.setValue(0)

    def agent_changed(self, name):
        self.caseInputLabel.setText("How many cases of "+self.descriptionComboBox.currentText()+" will "+self.agentComboBox.currentText()+" claim?")
        self.pieceInputLabel.setText("How many pieces of "+self.descriptionComboBox.currentText()+" will "+self.agentComboBox.currentText()+" claim?")

    def agent_changed_BL(self, name):
        self.caseInputLabelBL.setText("How many cases of "+self.chooseItemComboBoxBL.currentText()+" will "+self.agentComboBoxBL.currentText()+" return?")
        self.pieceInputLabelBL.setText("How many pieces of "+self.chooseItemComboBoxBL.currentText()+" will "+self.agentComboBoxBL.currentText()+" return?")

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()