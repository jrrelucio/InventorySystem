import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QStackedLayout, QScrollArea, QLabel, QComboBox, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QDoubleSpinBox, QFileDialog, QMessageBox
from PyQt6.QtGui import QPalette, QColor, QPixmap, QFont
import qtawesome as qta
import pandas as pd
import inventoryread as ir
from datetime import date

#initializing dataframes
df = pd.read_excel("current_stocks.xlsx")
df_initial_stocks = pd.read_excel("initial_stocks.xlsx")
df_history_ML = pd.read_excel('historyml.xlsx')
df_history_BL = pd.read_excel('historybl.xlsx')
df_agents = pd.read_excel("agents.xlsx")
stocksCaseValues = [str(x) for x in ir.get_all_case_values(df)]
stocksPieceValues = [str(x) for x in ir.get_all_piece_values(df)]
stocksPiecePerCase = [str(x) for x in  ir.get_all_ppc_values(df)]
stocksDescription = ir.get_all_description(df)
agentNames = list(df_agents['Agents'])
mLHistoryList = df_history_ML.values.tolist()
bLHistoryList = df_history_BL.values.tolist()

 
#implement save changes functionality to modify values on dataframe
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Warehouse Inventory")
        #self.setFixedSize(QSize(700, 400))
    
        pagelayout = QVBoxLayout()
        button_layout = QHBoxLayout()
        pagelayout.setContentsMargins(25, 25, 25, 25)
        button_layout.addStretch(1)
        self.stacklayout = QStackedLayout()

        pagelayout.addLayout(button_layout)
        pagelayout.addLayout(self.stacklayout)

        #PROPERTIES
        fontChoose = QFont("SansSerif", 12, QFont.DemiBold)
        fontTable = QFont("SansSerif", 12, QFont.Medium)
        fontButton = QFont("SansSerif", 10)
        fontTitle = QFont("SansSerif", 18, QFont.Bold)
        fontNormal = QFont("SansSerif", 10)

        btn_icon = qta.icon('fa5s.box-open')
        btn = QPushButton(btn_icon, "Inventory")
        btn.setFixedSize(200, 60)
        btn.setIconSize(QSize(20, 20))
        btn.setFont(fontButton)
        btn.pressed.connect(self.activate_tab_1)
        button_layout.addWidget(btn)
        #START OF INVENTORY WINDOW
        inventoryContainer = QWidget()
        self.inventoryVBLayout = QVBoxLayout(inventoryContainer)
        inventoryTitle = QLabel("INVENTORY")
        inventoryTitle.setFont(fontTitle)
        #self.inventoryTableContainer = QWidget()
        self.inventoryTableContainer = QWidget()
        self.inventoryTable = QGridLayout(self.inventoryTableContainer)
        self.scrollInventory = QScrollArea()
        self.scrollInventory.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollInventory.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollInventory.setWidgetResizable(True)
        self.scrollInventory.setWidget(self.inventoryTableContainer)
        self.columnTitles = ["Description", "Stocks (Case)", "Stocks (Piece)", "Piece per case", "Delivery (Case)", "Delivery (Piece)", "TOTAL (Case)", "TOTAL (Piece)"]
        for t in range(len(self.columnTitles)):
            title = QLabel(self.columnTitles[t])
            font = QFont("SansSerif", 10, QFont.Medium)
            title.setFont(font)
            self.inventoryTable.addWidget(title, 1, t)

        for i in range(2, len(stocksCaseValues)+ 2):
            self.inventoryTable.addWidget(QLabel(df_initial_stocks['Description'][i-2]), i, 0)
            self.inventoryTable.addWidget(QLabel(str(df_initial_stocks['Stocks (Case)'][i-2])), i, 1)
            self.inventoryTable.addWidget(QLabel(str(df_initial_stocks['Stocks (Piece)'][i-2])), i, 2)
            self.inventoryTable.addWidget(QLabel(str(df_initial_stocks['Piece per case'][i-2])), i, 3)
            self.inventoryTable.addWidget(QLabel(str(df_initial_stocks['Delivery (Case)'][i-2])), i, 4)
            self.inventoryTable.addWidget(QLabel(str(df_initial_stocks['Delivery (Piece)'][i-2])), i, 5)
            self.inventoryTable.addWidget(QLabel(str(df_initial_stocks['TOTAL (Case)'][i-2])), i, 6)
            self.inventoryTable.addWidget(QLabel(str(df_initial_stocks['TOTAL (Piece)'][i-2])), i, 7)

        #Delivery Section
        deliveryTitle = QLabel("DELIVERY")
        deliveryTitle.setFont(fontTitle)
        deliveryChooseItemBox = QHBoxLayout()
        deliveryChooseItemLabel = QLabel("Choose Item")
        deliveryChooseItemLabel.setFont(fontTable)
        self.delCIComboBox = QComboBox()
        self.delCIComboBox.addItems(stocksDescription)
        self.delCIComboBox.currentTextChanged.connect( self.del_index_changed )
        self.delCIComboBox.setMaximumWidth(200)
        
        casesDelivered = QLabel("Cases Delivered")
        piecesDelivered = QLabel("Pieces Delivered")
        casesDelivered.setFont(fontTable)
        piecesDelivered.setFont(fontTable)
        self.casesDeliveredInput = QDoubleSpinBox()
        self.casesDeliveredInput.setDecimals(0)
        self.piecesDeliveredInput = QDoubleSpinBox()
        self.piecesDeliveredInput.setDecimals(0)
        self.loadBtnDeliver = QPushButton(text="LOAD")
        self.loadBtnDeliver.setFont(fontButton)
        self.loadBtnDeliver.setFixedSize(64, 36)
        self.loadBtnDeliver.clicked.connect(self.update_delivery)

        deliveryChooseItemBox.addWidget(deliveryChooseItemLabel)
        deliveryChooseItemBox.addWidget(self.delCIComboBox)
        deliveryChooseItemBox.addWidget(casesDelivered)
        deliveryChooseItemBox.addWidget(self.casesDeliveredInput)
        deliveryChooseItemBox.addWidget(piecesDelivered)
        deliveryChooseItemBox.addWidget(self.piecesDeliveredInput)
        deliveryChooseItemBox.addWidget(self.loadBtnDeliver)
        deliveryChooseItemBox.addStretch(1)
        deliveryChooseItemBox.setSpacing(25)

        self.inventoryVBLayout.addWidget(inventoryTitle)
        self.inventoryVBLayout.addWidget(self.scrollInventory)
        self.inventoryVBLayout.addWidget(deliveryTitle)
        self.inventoryVBLayout.addLayout(deliveryChooseItemBox)
        self.stacklayout.addWidget(inventoryContainer)

        btn_icon = qta.icon('fa5s.sun')
        btn = QPushButton(btn_icon, "Morning Load")
        btn.setFixedSize(200, 60)
        btn.setIconSize(QSize(20, 20))
        btn.setFont(fontButton)
        btn.pressed.connect(self.activate_tab_2)
        button_layout.addWidget(btn)
        
        ###START OF MORNING LOAD WINDOW
        morningLoadContainer = QWidget()
        self.morningLoadVbox = QVBoxLayout(morningLoadContainer)
        morningLoadLabel = QLabel("MORNING LOAD")
        morningLoadLabel.setFont(fontTitle)
        chooseAgentBox = QHBoxLayout()
        agentLabel = QLabel("CHOOSE AGENT")
        agentLabel.setFont(fontChoose)
        self.agentComboBox = QComboBox()
        self.agentComboBox.addItems(agentNames)
        self.agentComboBox.currentTextChanged.connect( self.agent_changed )
        self.agentComboBox.setMaximumWidth(200)
        chooseAgentBox.addWidget(agentLabel)
        chooseAgentBox.addWidget(self.agentComboBox)
        chooseAgentBox.setSpacing(15)

        #Defining elements of Description column
        self.setFont(fontNormal)
        chooseItemBox = QHBoxLayout()
        chooseItemLabel = QLabel("CHOOSE ITEM")
        chooseItemLabel.setFont(fontChoose)
        self.descriptionComboBox = QComboBox()
        self.descriptionComboBox.addItems(stocksDescription)
        self.descriptionComboBox.currentIndexChanged.connect( self.index_changed )
        itemIndex = self.descriptionComboBox.currentIndex()
        self.descriptionComboBox.setMaximumWidth(200)
        chooseItemBox.addWidget(chooseItemLabel)
        chooseItemBox.addWidget(self.descriptionComboBox)
        
        #Defining elements of row 1
        #stocksLabel = QLabel("Stocks")
        currentItemHeader = QLabel("Description")
        
        stocksCaseLabel = QLabel("Case")
        stocksPieceLabel = QLabel("Piece")
        stocksPiecePerCaseLabel = QLabel("Piece per Case")
        currentItemHeader.setFont(fontTable)
        stocksCaseLabel.setFont(fontTable)
        stocksPieceLabel.setFont(fontTable)
        stocksPiecePerCaseLabel.setFont(fontTable)

        #Adding elements to row 2 of stocks
        self.currentItemLabel = QLabel(self.descriptionComboBox.currentText())
        self.currentItemLabel.setFont(fontNormal)  
        self.stocksCaseCurrent = QLabel(stocksCaseValues[itemIndex])
        self.stocksCaseCurrent.setFont(fontNormal)
        self.stocksPieceCurrent = QLabel(stocksPieceValues[itemIndex])
        self.stocksPieceCurrent.setFont(fontNormal)
        self.stocksPiecePerCaseCurrent = QLabel(stocksPiecePerCase[itemIndex])
        self.stocksPiecePerCaseCurrent.setFont(fontNormal)
        #ROW 3: Morning Load
        #morningloadAgent = QComboBox()
        #morningloadAgent.addItems(["NOEL", "OMAR"])
        #morningloadAgent.setEditable(True)
        self.caseInput = QDoubleSpinBox()
        self.caseInput.setDecimals(0)
        self.caseInput.setMaximumWidth(200)
        
        self.pieceInput = QDoubleSpinBox()
        self.pieceInput.setDecimals(0)
        self.pieceInput.setMaximumWidth(200)

        #setting maximum values of doublespinbox
        self.caseInput.setMaximum(int(self.stocksCaseCurrent.text()))
        self.caseInput.setMinimum(0)
        if int(self.stocksCaseCurrent.text()) > 0:
            self.pieceInput.setMaximum(int(self.stocksPiecePerCaseCurrent.text()) - 1)
        else:
            self.pieceInput.setMaximum(int(self.stocksPieceCurrent.text()))

        loadBox = QHBoxLayout()
        self.loadBtn = QPushButton(text="LOAD")
        self.loadBtn.setFont(fontButton)
        self.loadBtn.setFixedSize(64, 36)
        self.loadBtn.clicked.connect(self.update_stocks)
        loadBox.addStretch(1)
        loadBox.addWidget(self.loadBtn)

        self.claimIndex = len(mLHistoryList)

        self.caseInputLabel = QLabel("How many cases of "+self.descriptionComboBox.currentText()+" will "+self.agentComboBox.currentText()+" claim?")
        self.caseInputLabel.setFont(fontNormal)
        self.pieceInputLabel = QLabel("How many piece of "+self.descriptionComboBox.currentText()+" will "+self.agentComboBox.currentText()+" claim?")
        self.pieceInputLabel.setFont(fontNormal)
        caseInputHBox = QHBoxLayout()
        caseInputHBox.addWidget(self.caseInputLabel)
        caseInputHBox.addWidget(self.caseInput)
        pieceInputHBox = QHBoxLayout()
        pieceInputHBox.addWidget(self.pieceInputLabel)
        pieceInputHBox.addWidget(self.pieceInput)

        #adding items to main grid
        self.morningLoadLayout = QGridLayout()
        self.morningLoadLayout.setContentsMargins(65, 0, 0, 0)
        self.morningLoadLayout.addWidget(currentItemHeader, 0, 0)
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
        
        #Export Summary Button
        self.exportBox = QHBoxLayout()
        exportTitle = QLabel("GENERATE DAILY REPORT")
        exportTitle.setFont(fontChoose)
        self.exportBtn = QPushButton("EXPORT")
        self.exportBox.addWidget(exportTitle)
        self.exportBox.addWidget(self.exportBtn)
        self.exportBtn.clicked.connect(self.export_function)

        self.morningLoadVbox.addStretch(1)
        self.morningLoadVbox.addWidget(morningLoadLabel)
        self.morningLoadVbox.addLayout(chooseAgentBox)
        self.morningLoadVbox.addLayout(chooseItemBox)
        self.morningLoadVbox.addLayout(self.morningLoadLayout)
        self.morningLoadVbox.addLayout(caseInputHBox)
        self.morningLoadVbox.addLayout(pieceInputHBox)
        self.morningLoadVbox.addLayout(loadBox)
        self.morningLoadVbox.addStretch(1)
        self.morningLoadVbox.setSpacing(15)
        self.morningLoadVbox.setContentsMargins(50, 50, 50, 50)
        self.stacklayout.addWidget(morningLoadContainer)

        ###END OF MORNING LOAD WINDOW

        btn_icon = qta.icon('fa5s.moon')
        btn = QPushButton(btn_icon, "Backload")
        btn.setIconSize(QSize(20, 20))
        btn.setFont(fontButton)
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
        columnTitles = ["Description", "Case", "Piece", "Piece per case"]
        for i in range(len(columnTitles)):
            title = QLabel(columnTitles[i])
            title.setFont(fontTable)
            backloadGrid.addWidget(title, 0, i)
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
        self.returnIndex = len(bLHistoryList)
        self.loadBtnBL.setFont(fontButton)


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
        btn.setFont(fontButton)
        btn.setFixedSize(200, 60)
        btn.pressed.connect(self.activate_tab_4)
        button_layout.addWidget(btn)

        #morning load history window
        mLHistoryContainer = QWidget()
        mLHistoryLayout = QVBoxLayout(mLHistoryContainer)
        mLHistoryLayout.setContentsMargins(50, 50, 50, 50)
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

        for row in mLHistoryList:
            agentLabel = QLabel(row[0])
            descriptionLabel = QLabel(row[1])
            caseLabel = QLabel(str(row[2]))
            pieceLabel = QLabel(str(row[3]))
            font = QFont("SansSerif", 10, QFont.Normal)
            agentLabel.setFont(font)
            caseLabel.setFont(font)
            pieceLabel.setFont(font)
            descriptionLabel.setFont(font) 
            self.mLHistoryGrid.addWidget(agentLabel, self.claimIndex, 0)
            self.mLHistoryGrid.addWidget(descriptionLabel, self.claimIndex, 1)
            self.mLHistoryGrid.addWidget(caseLabel, self.claimIndex, 2)
            self.mLHistoryGrid.addWidget(pieceLabel, self.claimIndex, 3)
            self.claimIndex += 1
        
        mLHistoryGridScroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        mLHistoryGridScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        mLHistoryGridScroll.setWidgetResizable(True)
        
        mLHistoryGridScroll.setWidget(mLHistoryGridContainer)

        mLHistoryLayout.addWidget(mLHistoryGridScroll)
        self.stacklayout.addWidget(mLHistoryContainer)


        btn_icon = qta.icon('fa5s.clock')
        btn = QPushButton(btn_icon, "Backload History")
        btn.setIconSize(QSize(20, 20))
        btn.setFont(fontButton)
        btn.setFixedSize(200, 60)
        btn.pressed.connect(self.activate_tab_5)
        button_layout.addWidget(btn)
        button_layout.addStretch(1)
        button_layout.setSpacing(25)
        #backload history window
        bLHistoryContainer = QWidget()
        bLHistoryLayout = QVBoxLayout(bLHistoryContainer)
        bLHistoryLayout.setContentsMargins(50, 50, 50, 50)
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

        for row in bLHistoryList:
            agentLabel = QLabel(row[0])
            descriptionLabel = QLabel(row[1])
            caseLabel = QLabel(str(row[2]))
            pieceLabel = QLabel(str(row[3]))
            font = QFont("SansSerif", 10, QFont.Normal)
            agentLabel.setFont(font)
            caseLabel.setFont(font)
            pieceLabel.setFont(font)
            descriptionLabel.setFont(font)
            self.bLHistoryGrid.addWidget(agentLabel, self.returnIndex, 0)
            self.bLHistoryGrid.addWidget(descriptionLabel, self.returnIndex, 1)
            self.bLHistoryGrid.addWidget(caseLabel, self.returnIndex, 2)
            self.bLHistoryGrid.addWidget(pieceLabel, self.returnIndex, 3)
            self.returnIndex += 1

        bLHistoryGridScroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        bLHistoryGridScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        bLHistoryGridScroll.setWidgetResizable(True)
        bLHistoryGridScroll.setWidget(bLHistoryGridContainer)

        bLHistoryLayout.addWidget(bLHistoryGridScroll)
        bLHistoryLayout.addLayout(self.exportBox)
        self.stacklayout.addWidget(bLHistoryContainer)

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

    def del_index_changed(self, index):
        return

    def update_stocks(self):
        stocksCaseValue = int(self.stocksCaseCurrent.text())
        inputCaseValue = int(self.caseInput.value())
        stocksPieceValue = int(self.stocksPieceCurrent.text())
        inputPieceValue = int(self.pieceInput.value())
        piecePerCaseValue = int(self.stocksPiecePerCaseCurrent.text())
        if (stocksPieceValue - inputPieceValue) < 0:
            stocksPieceValue = int(piecePerCaseValue) + (stocksPieceValue - inputPieceValue)
            if  (stocksCaseValue - inputCaseValue - 1) > 0:
                print((stocksCaseValue - 1) + (stocksCaseValue - inputCaseValue))
                stocksCaseValue -= 1
            else:
                dlg = QMessageBox(self)
                dlg.setWindowTitle('Error!')
                dlg.setText("Invalid Input!")
                dlg.setStandardButtons(QMessageBox.StandardButton.Close)
                dlg.setIcon(QMessageBox.Icon.Warning)
                button = dlg.exec()
                return
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

    def update_delivery(self):
        index = self.delCIComboBox.currentIndex()
        caseInput = self.casesDeliveredInput.value()
        pieceInput = self.piecesDeliveredInput.value()
        ir.update_delivery(df_initial_stocks, index, caseInput, pieceInput)
        

        #render new table
        self.NewInventoryTableContainer = QWidget()
        self.InventoryTable = QGridLayout(self.NewInventoryTableContainer)
        self.columnTitles = ["Description", "Stocks (Case)", "Stocks (Piece)", "Piece per case", "Delivery (Case)", "Delivery (Piece)", "TOTAL (Case)", "TOTAL (Piece)"]
        for t in range(len(self.columnTitles)):
            title = QLabel(self.columnTitles[t])
            font = QFont("SansSerif", 10, QFont.Medium)
            title.setFont(font)
            self.inventoryTable.addWidget(title, 1, t)

        for i in range(2, len(stocksCaseValues)+ 2):
            self.inventoryTable.addWidget(QLabel(df_initial_stocks['Description'][i-2]), i, 0)
            self.inventoryTable.addWidget(QLabel(str(df_initial_stocks['Stocks (Case)'][i-2])), i, 1)
            self.inventoryTable.addWidget(QLabel(str(df_initial_stocks['Stocks (Piece)'][i-2])), i, 2)
            self.inventoryTable.addWidget(QLabel(str(df_initial_stocks['Piece per case'][i-2])), i, 3)
            self.inventoryTable.addWidget(QLabel(str(df_initial_stocks['Delivery (Case)'][i-2])), i, 4)
            self.inventoryTable.addWidget(QLabel(str(df_initial_stocks['Delivery (Piece)'][i-2])), i, 5)
            self.inventoryTable.addWidget(QLabel(str(df_initial_stocks['TOTAL (Case)'][i-2])), i, 6)
            self.inventoryTable.addWidget(QLabel(str(df_initial_stocks['TOTAL (Piece)'][i-2])), i, 7)

        self.inventoryVBLayout.replaceWidget(self.inventoryTableContainer, self.NewInventoryTableContainer)


    def agent_changed(self, name):
        self.caseInputLabel.setText("How many cases of "+self.descriptionComboBox.currentText()+" will "+self.agentComboBox.currentText()+" claim?")
        self.pieceInputLabel.setText("How many pieces of "+self.descriptionComboBox.currentText()+" will "+self.agentComboBox.currentText()+" claim?")

    def agent_changed_BL(self, name):
        self.caseInputLabelBL.setText("How many cases of "+self.chooseItemComboBoxBL.currentText()+" will "+self.agentComboBoxBL.currentText()+" return?")
        self.pieceInputLabelBL.setText("How many pieces of "+self.chooseItemComboBoxBL.currentText()+" will "+self.agentComboBoxBL.currentText()+" return?")

    def export_function(self):
        dir_name = QFileDialog.getSaveFileName(self, "Select a Directory", "summary.xlsx", "Excel Workbook (*.xlsx)")
        frames = [ir.create_description_df(stocksDescription), 
          ir.create_stocks_table(df_initial_stocks, "STOCKS"), 
          ir.load_table(df_history_ML, stocksDescription, "Morning Load"), 
          ir.load_table(df_history_BL, stocksDescription, "Backload"),
          ir.create_stocks_table(df, "BEGINNING")
          ]
        if dir_name[0] == '':
            return
        result = pd.merge(frames[0], frames[1], left_index=True, right_index=True)
        result = pd.merge(result, frames[2], left_index=True, right_index=True)
        result = pd.merge(result, frames[3], left_index=True, right_index=True)
        result = pd.merge(result, frames[4], left_index=True, right_index=True)
        result.to_excel(dir_name[0], sheet_name=str(date.today()))
        
        #insert file saved prompt
        self.exportBtn.setEnabled(False)
        savedLabel = QLabel("FILE SAVED SUCCESSFULLY")
        self.exportBox.addWidget(savedLabel)

        #save dataframes
        #mLHistoryList = []
        #bLHistoryList = []
        #ir.update_history_ml(mLHistoryList, "Morning Load")
        #ir.update_history_bl(bLHistoryList, "Backload")
        #ir.copy_current_to_initial(df)
        #empty out morning load history
        #empty out backload history
        #initial stocks = current stocks
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()