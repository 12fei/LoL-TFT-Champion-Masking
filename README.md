# League Of Legends - Teamfight Tactics Champion Masking
Its masks selected champions like Gangplank<br>
![Masked Gankplank](https://github.com/tufanYavas/LoL-TFT-Champion-Masking/blob/master/images/maskedimg.png)

It works fine but is a little slow. Detects in one second. Because of using tesseract.

### Installation For Windows
- [Download](https://github.com/UB-Mannheim/tesseract/wiki) and install tesseract.
- Modify ```pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe``` line from ```worker.py``` as your tesseract path.
- ```pip install -r requirements.txt```
- Make window mode borderless in game settings.
![Game Mode Setting](https://github.com/tufanYavas/LoL-TFT-Champion-Masking/blob/master/images/borderlessoption.png)
- Make Hud Scale = 100 in game settings.
![Hud Scale Setting](https://github.com/tufanYavas/LoL-TFT-Champion-Masking/blob/master/images/hudscaleoption.jpg)

- ```python main.py```

### Create Special Comps
- Modify ```comp``` dictionary (from ```worker.py```) as you wish. Thats all.

Example:
```
comps = {"Shapeshifter+Wild":["Nidalee",
                              "Elise",
                              "Shyvana",
                              "Gnar",
                              "Swain",
                              "Warwick",
                              "Ahri",
                              "Nidalee",
                              "Rengar",
                              "Gnar"]}
```
![Special Comp](https://github.com/tufanYavas/LoL-TFT-Champion-Masking/blob/master/images/specialcomp.png)
