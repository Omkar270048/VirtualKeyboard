import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=1)
keys = [["Q","W","E","R","T","Y","U","I","O","P"],
        ["A","S","D","F","G","H","J","K","L",";"],
        ["Z","X","C","V","B","N","M",",",".","/"]]

finalText = ""

def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        overlayer = img.copy()
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), -1) #cv2.FILLED
        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
        alpha = 0.8
        img = cv2.addWeighted(overlayer, alpha, img, 1 - alpha, 0)

    return img

class Button():
    def __init__(self, pos, text, size=[85,85]):
        self.pos = pos
        self.size = size

        self.text = text

   # def draw(self, img):

       # return img

buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)
    img = drawAll(img, buttonList)

    if lmList:
        for button in buttonList:
            x,y = button.pos
            w,h = button.size
            if x < lmList[8][0] <x+w and y<lmList[8][1]<y+h:

                cv2.rectangle(img, button.pos, (x + w, y + h), (175,0,175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                l,_,_=detector.findDistance(8,12,img, draw=False)
                print(l)
                #when clicked
                if l<30:
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    finalText += button.text
                    sleep(0.5)

    overlayer = img.copy()
    cv2.rectangle(img, (50, 350), (700, 450), (175,0,175), cv2.FILLED)
    alpha = 0.8
    img = cv2.addWeighted(overlayer, alpha, img, 1 - alpha, 0)

    cv2.putText(img, finalText, (60, 430), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 4)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
