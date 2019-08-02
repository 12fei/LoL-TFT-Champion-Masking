from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QMainWindow,QCheckBox,QPushButton,QGridLayout,QWidget,QMessageBox,QHBoxLayout,QVBoxLayout
from worker import Worker
from threading import Thread

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle("TFT Champ Masking")
        self.selectedComps = []
        self.setupWidgets()
        
    def setupWidgets(self):
        self.thread = QThread()
        self.thread.start()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        
        self.centralWidget = QWidget(self)
        
        self.CBdict = dict()
        
        from worker import comps
        comps = list(comps.keys())
        sorting_type = [8,5,5,5] # Set row numbers for each column
        
        if sum(sorting_type) != len(comps):
            print("Invalid sorting type, automatically sorted.")
            sorting_type = []
            
            if len(comps)//5 == 0:
                sorting_type.append(len(comps))
            
            else:
                rowsPerColumn = 5 # If invalid sorting type, set automaticly
                for _ in range(len(comps)//rowsPerColumn):
                    sorting_type.append(len(comps)//rowsPerColumn)
                sorting_type.append(len(comps)%rowsPerColumn)
            
        
        for comp in comps:
            self.CBdict[comp] = QCheckBox(comp)
        
        
        grid = QGridLayout()
        
        
        # Add all checkboxes to grid and set signals
        column = 0
        compIndex = 0
        for totalRow in sorting_type:
            column += 1
            for row in range(totalRow):
                grid.addWidget(self.CBdict[comps[compIndex]],row,column)
                self.CBdict[comps[compIndex]].clicked.connect(lambda _,cb=self.CBdict[comps[compIndex]]: self.CBClicked(cb=cb))
                compIndex += 1
            
        self.startButton = QPushButton("Start")
        self.stopButton = QPushButton("Stop")
        self.stopButton.setEnabled(False)
        self.startButton.clicked.connect(self.startThread)
        self.stopButton.clicked.connect(self.stopThread)
        
        mainLayout = QVBoxLayout(self.centralWidget)
        startStopLayout = QHBoxLayout()
        startStopLayout.addWidget(self.startButton)
        startStopLayout.addWidget(self.stopButton)
        mainLayout.addLayout(grid)
        mainLayout.addLayout(startStopLayout)
        
        self.setCentralWidget(self.centralWidget)

    def CBClicked(self,cb):
        """ When checkbox clicked append/remove comp from worker class."""
        if cb.isChecked():
            self.selectedComps.append(cb.text())
        else:
            self.selectedComps.remove(cb.text())
        
        self.t3 = Thread(target = self.worker.reload_comps,args=(self.selectedComps,)) 
        self.t3.start()
        
    def startThread(self):
        if self.selectedComps == []:
            QMessageBox.warning(self, "Error", "No comps selected.")
            return
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        self.t1 = Thread(target = self.worker.run) 
        self.t1.start()
        
    def stopThread(self):
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        self.t2 = Thread(target = self.worker.stop) 
        self.t2.start()
        self.thread.quit()
        self.thread.wait()