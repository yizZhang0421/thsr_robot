import cv2, pytesseract
import numpy as np
def ocr(img):
    img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret1,img_ = cv2.threshold(img,1234, 255,cv2.THRESH_OTSU)
    ret,img = cv2.threshold(img,ret1+5, 255,cv2.THRESH_BINARY)
    
    img = cv2.fastNlMeansDenoising(img, None, 50.0, 7, 50)
    ret1,img = cv2.threshold(img,1234, 255,cv2.THRESH_OTSU)

    def find_point(mat):
        start_index=0
        end_index=mat.shape[0]-1
        for i in range(mat.shape[0]):
            if np.all(mat[i]==0) and start_index==0:
                start_index=i
            elif np.all(mat[i]==0)==False and start_index!=0:
                end_index=i-1
                break
        return int(start_index+round((end_index-start_index+1)/2))
    
    left=img[:, :5]
    right=img[:, -5:]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3))
    left=cv2.erode(left, kernel)
    right=cv2.erode(right, kernel)
    ret, left=cv2.threshold(left,1234, 255,cv2.THRESH_OTSU)
    ret, right=cv2.threshold(right,1234, 255,cv2.THRESH_OTSU)
    
    left_point=find_point(left)
    right_point=find_point(right)
    new_x=[i for i in range(img.shape[1])]
    new_y=np.poly1d(np.polyfit([0, (img.shape[1]-1)/2, img.shape[1]-1], [left_point, right_point+((left_point-right_point)/2)-6, right_point], 2))(new_x)
    line_template=np.full(img.shape, 255)
    for x_, y_ in zip(new_x, new_y):
        y_=int(round(y_))
        color=255-img[y_][x_]
        if color==255:
            cv2.line(line_template, (x_, y_), (x_, y_), (0, 0, 0), 3, cv2.LINE_AA)
        elif color==0:
            cv2.line(line_template, (x_, y_), (x_, y_), (0, 0, 0), 3, cv2.LINE_AA)
    line_template=line_template.astype(np.uint8)
    
    for r in range(img.shape[0]):
        for c in range(img.shape[1]):
            if line_template[r][c]==0 and img[r][c]==0:
                img[r][c]=255
            elif line_template[r][c]==0 and img[r][c]==255:
                img[r][c]=0
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(1, 3))
    img=cv2.erode(img, kernel)
    img=cv2.dilate(img, kernel)
    img=cv2.dilate(img, kernel)
    img=cv2.erode(img, kernel)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3, 1))
    img=cv2.dilate(img, kernel)
    img=cv2.erode(img, kernel)
    
    h=200
    w=int(img.shape[1]*h/img.shape[0])
    img = cv2.resize(img, (w, h), interpolation=cv2.INTER_CUBIC)
    
    bordersize = 100
    img = cv2.copyMakeBorder(
        img,
        top=bordersize,
        bottom=bordersize,
        left=bordersize,
        right=bordersize,
        borderType=cv2.BORDER_CONSTANT,
        value=[255, 255, 255]
    )
    
    #cv2.imwrite('asd.jpg', img)
    result=pytesseract.image_to_string(img, config="-l eng -psm 7 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    result=result.replace(' ', '')
    return result
