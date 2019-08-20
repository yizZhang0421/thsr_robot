import cv2
import numpy as np
img=cv2.imread('test.jpg')
img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
img = cv2.fastNlMeansDenoising(img, None, 50.0, 7, 21)
ret1,img_ = cv2.threshold(img,1234, 255,cv2.THRESH_OTSU)
ret,img = cv2.threshold(img,ret1, 255,cv2.THRESH_BINARY_INV)

'''
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3, 1))
img=cv2.erode(img, kernel)
img = cv2.fastNlMeansDenoising(img, None, 70.0, 7, 21)

img = cv2.fastNlMeansDenoising(img, None, 70.0, 7, 21)
ret1,img_ = cv2.threshold(img,1234, 255,cv2.THRESH_OTSU)
ret,img = cv2.threshold(img,ret1, 255,cv2.THRESH_BINARY_INV)
'''
#cv2.imwrite('asd.jpg', img)

# find noise line and reverse it to fix structure
lines = cv2.HoughLinesP(image=img,rho=1,theta=np.pi/180, threshold=1,lines=np.array([]), minLineLength=8,maxLineGap=1)
a,b,c = lines.shape
x=[]
y=[]
tmp=img.copy()
for i in range(a):
    angle = np.rad2deg(np.arctan2(lines[i][0][3] - lines[i][0][1], lines[i][0][2] - lines[i][0][0]))
    if angle<=3 and angle>=-25:
        if lines[i][0][0]<img.shape[1]/2 and lines[i][0][1]<=img.shape[0]/2 and lines[i][0][2]<img.shape[1]/2 and lines[i][0][3]<=img.shape[0]/2:
            cv2.line(tmp, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (127, 127, 127), 2, cv2.LINE_AA)
            x.append(lines[i][0][0])
            y.append(lines[i][0][1])
            x.append(lines[i][0][2])
            y.append(lines[i][0][3])
        elif lines[i][0][0]>=img.shape[1]/2 and lines[i][0][1]<=img.shape[0]/3 and lines[i][0][2]>=img.shape[1]/2 and lines[i][0][3]<=img.shape[0]/3:
            cv2.line(tmp, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (127, 127, 127), 2, cv2.LINE_AA)
            x.append(lines[i][0][0])
            y.append(lines[i][0][1])
            x.append(lines[i][0][2])
            y.append(lines[i][0][3])
cv2.imshow('test', tmp)
cv2.waitKey(0)
cv2.destroyAllWindows()

# remove duplicate
lines=[[(x[i], y[i]), (x[i+1], y[i+1])] for i in range(0, len(x), 2)]
forbidden_index=[]
for i in range(len(lines)):
    for j in range(i+1, len(lines)):
        if lines[i][0][0]>=lines[j][0][0] and lines[i][1][0]<=lines[j][1][0]:
            i_y_center=lines[i][0][1]+int(round((lines[i][1][1]-lines[i][0][1]+1)/2))
            j_y_center=lines[j][0][1]+int(round((lines[j][1][1]-lines[j][0][1]+1)/2))
            if lines[i][0][0]>img.shape[1]/2 and lines[j][0][0]>img.shape[1]/2:
                forbidden_index.append(j if i_y_center <= j_y_center else i)
            elif lines[i][1][0]<img.shape[1]/2 and lines[j][1][0]<img.shape[1]/2:
                forbidden_index.append(j if i_y_center >= j_y_center else i)
x=[]
y=[]
for i in range(len(lines)):
    if i not in forbidden_index:
        x.append(lines[i][0][0])
        y.append(lines[i][0][1])
        x.append(lines[i][1][0])
        y.append(lines[i][1][1])
        


new_x=[i for i in range(img.shape[1])]
new_y=np.poly1d(np.polyfit(x, y, 3))(new_x)
tmp_fix=img.copy()
for x_, y_ in zip(new_x, new_y):
    y_=int(round(y_))
    color=255-img[y_][x_]
    if color==255:
        cv2.line(tmp_fix, (x_, y_), (x_, y_), (127, 127, 127), 2, cv2.LINE_AA)
    elif color==0:
        cv2.line(tmp_fix, (x_, y_), (x_, y_), (127, 127, 127), 2, cv2.LINE_AA)
    
cv2.imshow('test', tmp_fix)
cv2.waitKey(0)
cv2.destroyAllWindows()
#cv2.imwrite('asdasd.jpg', tmp_fix)

'''
new_x=[i for i in range(img.shape[1])]
new_y=np.poly1d(np.polyfit(x, y, 3))(new_x)
tmp=img.copy()
for x_, y_ in zip(new_x, new_y):
    y_=int(round(y_))
    color=255-img[y_][x_]
    if color==255:
        cv2.line(tmp, (x_, y_), (x_, y_), (255, 255, 255), 5, cv2.LINE_AA)
    elif color==0:
        cv2.line(tmp, (x_, y_), (x_, y_), (0, 0, 0), 5, cv2.LINE_AA)
cv2.imshow('test', tmp)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''

'''
自訂修正結構
當該點為白，計算白的高度範圍，在threshold內才需填黑，填黑直到黑或達threshold (上下同時擴展)
當該點為黑，填白直到白或達threshold
threshold試試看7
'''

new_x=[i for i in range(img.shape[1])]
new_y=np.poly1d(np.polyfit(x, y, 3))(new_x)
tmp=img.copy()
for x_, y_ in zip(new_x, new_y):
    y_=int(round(y_))
    color=img[y_][x_]
    # white height
    height=1
    if color==255:
        find_index=y_+1
        patient=0
        while find_index<img.shape[0]:
            if img[find_index][x_]!=color:
                patient+=1
                if patient<2 and x_<(img.shape[1]-img.shape[1]//4):
                    find_index+=1
                    continue
                else:
                    break
            else:
                patient=0
            height+=1
            find_index+=1
        find_index=y_-1
        patient=0
        while find_index>=0:
            if img[find_index][x_]!=color:
                patient+=1
                if patient<2:
                    find_index-=1
                    continue
                else:
                    break
            else:
                patient=0
            height+=1
            find_index-=1
    
    draw_range=3
    if color==255 and height<=7:
        for i in range(y_-draw_range, y_+draw_range+1):
            tmp[i][x_]=255-color
    elif color==0:
        for i in range(y_-draw_range, y_+draw_range+1):
            tmp[i][x_]=255-color
cv2.imshow('test', tmp)
cv2.waitKey(0)
cv2.destroyAllWindows()


tmp=255-tmp
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3))
aaa=cv2.dilate(tmp, kernel)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3))
aaa=cv2.erode(aaa, kernel)

cv2.imshow('test', aaa)
cv2.waitKey(0)
cv2.destroyAllWindows()
#cv2.imwrite('result.jpg', aaa)
