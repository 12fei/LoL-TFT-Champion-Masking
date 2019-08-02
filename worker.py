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

old_image_arrays = [0,0,0,0,0]
old_text = [0,0,0,0,0]
def screenshot_to_text():
    screenshotIm =  screenshot()
    img = np.array(screenshotIm) 
    
    #boxes of 5 champs
    xi,yi,xs,ys = int(img.shape[1]*25/100),int(img.shape[0]*96/100),int(img.shape[1]*33/100),int(img.shape[0]*99/100)
    xi2,yi2,xs2,ys2 = int(img.shape[1]*35/100),int(img.shape[0]*96/100),int(img.shape[1]*43/100),int(img.shape[0]*99/100)
    xi3,yi3,xs3,ys3 = int(img.shape[1]*46/100),int(img.shape[0]*96/100),int(img.shape[1]*53/100),int(img.shape[0]*99/100)
    xi4,yi4,xs4,ys4 = int(img.shape[1]*56/100),int(img.shape[0]*96/100),int(img.shape[1]*64/100),int(img.shape[0]*99/100)
    xi5,yi5,xs5,ys5 = int(img.shape[1]*67/100),int(img.shape[0]*96/100),int(img.shape[1]*75/100),int(img.shape[0]*99/100)
    
    boxes = [[xi,yi,xs,ys],
             [xi2,yi2,xs2,ys2],
             [xi3,yi3,xs3,ys3],
             [xi4,yi4,xs4,ys4],
             [xi5,yi5,xs5,ys5]]
    
    texts = list()
    
    for box in boxes:
        image = crop(img,box)
                
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # If before box's image same with new image, append before image's text and skip other steps
        if gray.tolist() == old_image_arrays[boxes.index(box)]:
            texts.append([old_text[boxes.index(box)],box])
            continue
        else:
            # Else, update old image array index by new array
            old_image_arrays[boxes.index(box)] = gray.tolist()
            
        #Clear noisy and read text via pytesseract
        ret,thresh = cv2.threshold(gray,127,255,1)
        
        text = pytesseract.image_to_string(thresh)
        
        texts.append([text,box])
        old_text[boxes.index(box)] = text
        
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

