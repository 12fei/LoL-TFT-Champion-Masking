import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QMainWindow,QStylePainter,QApplication
import numpy as np
from mainwindow import MainWindow
from pyautogui import screenshot

class Mask(QMainWindow):
    def __init__(self, box,parent=None):
        QMainWindow.__init__(self, parent)
        self.resize(500, 500)
        self.box = box

    def paintEvent(self, event=None):
        painter = QStylePainter()
        painter.begin(self)

        painter.setOpacity(0.4)
        painter.setBrush(Qt.green)
        painter.setPen(QPen(Qt.green))   
        painter.drawRect(self.rect())
        self.setGeometry(self.box[0],self.box[1],self.box[2]-self.box[0],self.box[3]-self.box[1])
        
    def mousePressEvent(self, event):
        self.close()
        

activeBoxes = list()

class Controller:
    def __init__(self):
        self.Show_MainWindow()

    def Show_MainWindow(self):
        
        # Get 5 champions name's coordinates from screenshot
        img =  np.array(screenshot())

        self.box1 = [int(img.shape[1]*25/100),int(img.shape[0]*96/100),int(img.shape[1]*33/100),int(img.shape[0]*99/100)]
        self.box2 = [int(img.shape[1]*35/100),int(img.shape[0]*96/100),int(img.shape[1]*43/100),int(img.shape[0]*99/100)]
        self.box3 = [int(img.shape[1]*46/100),int(img.shape[0]*96/100),int(img.shape[1]*53/100),int(img.shape[0]*99/100)]
        self.box4 = [int(img.shape[1]*56/100),int(img.shape[0]*96/100),int(img.shape[1]*64/100),int(img.shape[0]*99/100)]
        self.box5 = [int(img.shape[1]*67/100),int(img.shape[0]*96/100),int(img.shape[1]*75/100),int(img.shape[0]*99/100)]
        
        self.ui = MainWindow()
        self.ui.worker.active.connect(self.run)
        self.ui.setWindowFlags(Qt.WindowStaysOnTopHint) # Main Window always top on
        
        self.ui.show()
        
    def run(self,maskChamps):
        # If masked boxes not in new mask list, delete box from active boxes and close mask.
        for box in activeBoxes:
            if box not in maskChamps:
                if box == self.box1:
                    self.ui2.close()
                    activeBoxes.remove(box)
                if box == self.box2:
                    self.ui3.close()
                    activeBoxes.remove(box)
                if box == self.box3:
                    self.ui4.close()
                    activeBoxes.remove(box)
                if box == self.box4:
                    self.ui5.close()
                    activeBoxes.remove(box)
                if box == self.box5:
                    self.ui6.close()
                    activeBoxes.remove(box)
                    
        # If mask box already masked, continue
        # Else, mask the box.
        for box in maskChamps:
            if box in activeBoxes:
                continue
            if box == self.box1:
                self.mask1()
                activeBoxes.append(box)
            if box == self.box2:
                self.mask2()
                activeBoxes.append(box)
            if box == self.box3:
                self.mask3()
                activeBoxes.append(box)
            if box == self.box4:
                self.mask4()
                activeBoxes.append(box)
            if box == self.box5:
                self.mask5()
                activeBoxes.append(box)
                
            

    def mask1(self):
        self.ui2 = Mask(self.box1)
        self.ui2.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.ui2.setAttribute(Qt.WA_NoSystemBackground, True)
        self.ui2.setAttribute(Qt.WA_TranslucentBackground, True)
        self.ui2.show()
        
    def mask2(self):
        self.ui3 = Mask(self.box2)
        self.ui3.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.ui3.setAttribute(Qt.WA_NoSystemBackground, True)
        self.ui3.setAttribute(Qt.WA_TranslucentBackground, True)
        self.ui3.show()
    
    def mask3(self):
        self.ui4 = Mask(self.box3)
        self.ui4.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.ui4.setAttribute(Qt.WA_NoSystemBackground, True)
        self.ui4.setAttribute(Qt.WA_TranslucentBackground, True)
        self.ui4.show()
    
    def mask4(self):
        self.ui5 = Mask(self.box4)
        self.ui5.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.ui5.setAttribute(Qt.WA_NoSystemBackground, True)
        self.ui5.setAttribute(Qt.WA_TranslucentBackground, True)
        self.ui5.show()
        
            
    def mask5(self):
        self.ui6 = Mask(self.box5)
        self.ui6.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.ui6.setAttribute(Qt.WA_NoSystemBackground, True)
        self.ui6.setAttribute(Qt.WA_TranslucentBackground, True)
        self.ui6.show()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    Controller = Controller()
    sys.exit(app.exec_())