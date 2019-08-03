from PyQt5.QtCore import QThread,pyqtSlot,pyqtSignal
from pyautogui import screenshot
import numpy as np
import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

comps = {"Assassin":["Kha'Zix","Pyke","Zed","Katarina","Evelynn","Rengar","Akali"],
         "Demon":["Varus","Elise","Morgana","Evelynn","Aatrox","Brand","Swain"],
         "Blademaster":["Fiora","Shen","Aatrox","Gangplank","Draven","Yasuo"],
         "Glacial":["Braum","Lissandra","Ashe","Volibear","Sejuani","Anivia"],
         "Noble":["Fiora","Garen","Vayne","Lucian","Leona","Kayle"],
         "Sorcerer":["Kassadin","Ahri","Lulu","Veigar","Morgana","Aurelion Sol","Karthus","Twisted Fate"],
         "Yordle":["Tristana","Lulu","Poppy","Veigar","Kennen","Gnar"],
         "Knight":["Draven","Garen","Mordekaiser","Poppy","Sejuani","Kayle"],
         
         "Brawler":["Warwick","Rek'Sai","Blitzcrank","Volibear","Cho'Gath"],
         "Imperial":["Darius","Katarina","Draven","Swain"],
         "Ranger":["Ashe","Vayne","Kindred","Varus"],
         "Ninja":["Shen","Zed","Kennen","Akali"],
         "Wild":["Warwick","Ahri","Nidalee","Rengar","Gnar"],
         
         "Gunslinger":["Tristana","Lucian","Graves","Gangplank","Miss Fortune"],
         "Elementalist":["Lissandra","Brand","Kennen","Anivia"],
         "Pirate":["Graves","Pyke","Gangplank","Miss Fortune","Twisted Fate"],
         "Shapeshifter":["Nidalee","Elise","Shyvana","Gnar","Swain"],
         "Void":["Kha'Zix","Kassadin","Rek'Sai","Cho'Gath"],
         
         "Dragon":["Aurelion Sol","Shyvana"],
         "Guardian":["Leona","Braum"],
         "Phantom":["Mordekaiser","Kindred","Karthus"],
         "Exile":["Yasuo"],
         "Robot":["Blitzcrank"]
         }

from difflib import SequenceMatcher

def similar(a, b):
    """Return similarity ratio of a and b"""
    if (a=="Varus" and b=="Darius") | (a=="Darius" and b=="Varus"):
        return 0
    return SequenceMatcher(None, a, b).ratio()

def crop(imgArray,box):
    """Crop image"""
    return imgArray[box[1]:box[3], box[0]:box[2]]

def isbox1inbox2(box1,box2):
    """box1 in box2?"""
    if (box2[0] <= box1[0] and box1[2] <= box2[2]) and (box2[1] <= box1[1] and box1[3] <= box2[3]):
        return True
    
def screenshot_to_text():
    ss = np.array(screenshot())
    
    #boxes of 5 champs
    xi,yi,xs,ys = int(ss.shape[1]*25/100),int(ss.shape[0]*96/100),int(ss.shape[1]*33/100),int(ss.shape[0]*99/100)
    xi2,yi2,xs2,ys2 = int(ss.shape[1]*35/100),int(ss.shape[0]*96/100),int(ss.shape[1]*43/100),int(ss.shape[0]*99/100)
    xi3,yi3,xs3,ys3 = int(ss.shape[1]*46/100),int(ss.shape[0]*96/100),int(ss.shape[1]*53/100),int(ss.shape[0]*99/100)
    xi4,yi4,xs4,ys4 = int(ss.shape[1]*56/100),int(ss.shape[0]*96/100),int(ss.shape[1]*64/100),int(ss.shape[0]*99/100)
    xi5,yi5,xs5,ys5 = int(ss.shape[1]*67/100),int(ss.shape[0]*96/100),int(ss.shape[1]*75/100),int(ss.shape[0]*99/100)
    
    img = crop(ss,[xi,yi,xs5,ys5])
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
# =============================================================================
#     cv2.imshow("",img)
#     k = cv2.waitKey(1) & 0xFF
#     if k == 27:
#         return
# =============================================================================
    boxes = [[xi,yi,xs,ys],
             [xi2,yi2,xs2,ys2],
             [xi3,yi3,xs3,ys3],
             [xi4,yi4,xs4,ys4],
             [xi5,yi5,xs5,ys5]]
    
    
    lower_red = np.array([60,117,62])
    upper_red = np.array([213,228,218])
    
    mask = cv2.inRange(img, lower_red, upper_red)
    res = cv2.bitwise_and(img, img, mask= mask)
    
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    ret,thresh1 = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
    mask = cv2.inRange(thresh1, 0, 0)
    text = pytesseract.image_to_boxes(mask,lang="tur")
    textList = text.split("\n")
    
    texts = [["",boxes[0]],["",boxes[1]],["",boxes[2]],["",boxes[3]],["",boxes[4]]]
    
    if textList == ['']:
        return None
    for i in textList:
        i = i.split()
        box1 = [xi+int(i[1]),
                ss.shape[0]-int(i[2]),
                xi+int(i[3]),
                ss.shape[0]-int(i[4])]
        
        for boxIndex,box2 in enumerate(boxes):
            if isbox1inbox2(box1,box2):
                texts[boxIndex][0]+=i[0]
    
    return texts

class Worker(QThread):
    active = pyqtSignal(list)

    def __init__(self):
        super(Worker, self).__init__()
        self.selectedComps = list()
        self._sleep = False
        
    def reload_comps(self,selectedComps):
        self.selectedComps = selectedComps
        
    @pyqtSlot()
    def run(self):
        self.running = True
        while self.running:
            texts = screenshot_to_text()
            if texts == None:continue
            maskChamps = list()
            for champFromText in texts:
                for comp in self.selectedComps:
                    #if read champ in selected comps emit maskChamps
                    similarRates = [similar(champ,champFromText[0]) for champ in comps[comp]]
                    maxRate = similarRates[np.argmax(similarRates)]
                    if maxRate > .667:
                        if champFromText[1] not in maskChamps:
                            maskChamps.append(champFromText[1])
                            print(champFromText[0],comps[comp][np.argmax(similarRates)])
            self.active.emit(maskChamps)
            
    def stop(self):
        self.running = False

