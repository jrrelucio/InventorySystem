import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QComboBox, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLineEdit, QDoubleSpinBox
from PyQt6.QtGui import QPalette, QColor

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)


stocksCaseValues = ["24", "41"]
stocksPieceValues = ["11", "5"]
stocksPiecePerCase = ["12", "6"]
agentNames = ["OMAR", "DENNIS", "RIGOR", "JOSHUA", "KENNETH"]
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventory System")

        mainLayout = QHBoxLayout()
        
        #initializing main box
        agentBox = QVBoxLayout()

        agentLabel = QLabel("Choose Agent Name")
        agentComboBox = QComboBox()
        agentButton = QPushButton("GO")
        agentComboBox.addItems(agentNames)
        agentComboBox.currentTextChanged.connect( self.agent_changed )
        agentBox.addWidget(agentLabel)
        agentBox.addWidget(agentComboBox)
        #agentBox.addWidget(agentButton)
        self.morningLoad = QGridLayout()
        
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
        #adding items to main grid
        self.morningLoad.addWidget(self.currentAgent, 0, 0)
        self.morningLoad.addWidget(descriptionLabel, 1, 0)
        #self.morningLoad.addWidget(stocksLabel, 0, 1)
        self.morningLoad.addWidget(stocksCaseLabel, 1, 1)
        self.morningLoad.addWidget(stocksPieceLabel, 1, 2)
        self.morningLoad.addWidget(stocksPiecePerCaseLabel, 1, 3)
        self.morningLoad.addWidget(self.descriptionComboBox, 2, 0)
        self.morningLoad.addWidget(self.stocksCaseCurrent, 2, 1)  
        self.morningLoad.addWidget(self.stocksPieceCurrent, 2, 2)
        self.morningLoad.addWidget(self.stocksPiecePerCaseCurrent, 2, 3)
        #self.morningLoad.addWidget(self.agentName, 3, 0)
        self.morningLoad.addWidget(self.caseInput, 3, 1)
        self.morningLoad.addWidget(self.pieceInput, 3, 2)
        self.morningLoad.addWidget(self.loadBtn, 3, 3)
        self.morningLoad.addWidget(claimedItemsLabel, 4, 0)
        self.morningLoad.addWidget(claimedAgentLabel, 5, 0)
        self.morningLoad.addWidget(claimedCaseLabel, 5, 1)
        self.morningLoad.addWidget(claimedPieceLabel, 5, 2)
        self.morningLoad.addWidget(claimedDescriptionLabel, 5, 3)
        #self.morningLoad.addWidget(totalLabel, 6,0)

        mainLayout.addLayout(agentBox)
        mainLayout.addLayout(self.morningLoad)
        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

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

        self.morningLoad.addWidget(agentLabel, index, 0)
        self.morningLoad.addWidget(caseLabel, index, 1)
        self.morningLoad.addWidget(pieceLabel, index, 2)
        self.morningLoad.addWidget(descriptionLabel, index, 3)
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