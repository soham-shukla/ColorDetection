import argparse
import cv2
import numpy as np 
import pandas as pd

# image fetch

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help = "image path")
arg = vars(ap.parse_args())
path = arg["image"]
img = cv2.imread(path)



# image categorical data from csv file

index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)
clicked = False
xpos = ypos = 0
b = g = r = 0


# drawFunction calculates RGB values w/ a doubleclick

def drawFunction(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN or event == cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r, xpos, ypos, clicked
        clicked = True
        xpos = img.shape[1] // 2
        ypos = img.shape[0] - 1
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)

# distance calculation to find most accurate color_name

def getColorName(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))

        if d <= minimum:
            minimum = d
            colorName = csv.loc[i, "color_name"]

    return colorName

# window application
cv2.namedWindow('image')
cv2.setMouseCallback('image', drawFunction)

# runtime program

while (True):
    display = img.copy()
    if (clicked) :
        # generate rectange to show highlighted section on image
        cv2.rectangle(display, (xpos - 300,ypos), (xpos + 300,ypos - 40), (b,g,r), -1)

        # display text for colorName
        text = getColorName(r,g,b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
        cv2.putText(display, text, (xpos - 300,ypos), 3, 1, (0,0,0), 2, cv2.LINE_AA)

        clicked = False

    cv2.imshow("image", display)

    if cv2.waitKey(500) & 0xFF == 27:
        break

cv2.destroyAllWindows()