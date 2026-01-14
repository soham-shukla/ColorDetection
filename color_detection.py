import argparse
import cv2
import numpy as np 
import pandas as pd

# image fetch

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help = "image path")
arg = vars(ap.parse_args())
path = arg["image"]
image = cv2.imread(path)

# image categorical data from csv file

index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)


# drawFunction calculates RGB values w/ a doubleclick

def drawFunction(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global r,g,b, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        r,g,b = image[x,y]
        r = int(r)
        g = int(g)
        b = int(b)

# distance calculation to find most accurate color_name

def getColorName(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))

        if d <= minimum:
            minimum = d
            colorName = csv.loc[i, "colorName"]
        return colorName
    
while True:
    cv2.imshow("currentImage", image)
    if clicked:
        # generate rectange to show highlighted section on image
        cv2.rectangle(image, (50,50), (100,100), (r,g,b), 10)

        # display text for colorName
        text = getColorName(r,g,b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
        cv2.putText(image, text, (75,75), 3, 1, (255,255,255), 2, cv2.LINE_AA)

        clicked = False


        if cv2.waitKey(50) & 0xFF == 27:
            break

cv2.destroyAllWindows()

# window application
cv2.namedWindow('currentImage')
cv2.setMouseCallback('currentImage', drawFunction())
