# https://irs.thsrc.com.tw/IMINT
import requests as req
rs=req.session()
headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'irs.thsrc.com.tw',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
 }
main_page=rs.get(url='https://irs.thsrc.com.tw/IMINT', headers=headers)
from bs4 import BeautifulSoup
soup=BeautifulSoup(main_page.text, 'html.parser')
captcha_img=soup.find(name='img', attrs={'id': 'BookingS1Form_homeCaptcha_passCode'})
img_data=rs.get(url='https://irs.thsrc.com.tw'+captcha_img['src'], headers=headers)
import cv2
import numpy as np
img_data = np.fromstring(img_data.content, np.uint8)
img_data = cv2.imdecode(img_data, cv2.IMREAD_COLOR)
# cv2.imwrite('test.jpg', img_data)

'''
cv2.imshow('test', img_data)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''

#cv2.imwrite('D:/Desktop/test.jpg', img_data)
from captcha import ocr
captcha_code=ocr(img_data)
#print('輸入驗證碼: ')
#captcha_code=input()
data={
      'selectStartStation': '2',
      'selectDestinationStation': '1',
      'trainCon:trainRadioGroup': '0',
      'seatCon:seatRadioGroup': 'radio17',
      'bookingMethod': '0',
      'toTimeInputField': '2019/10/05',
      'toTimeTable': '1201A',
      'backTimeInputField': '2019/10/05',
      'ticketPanel:rows:0:ticketAmount': '1F',
      'ticketPanel:rows:1:ticketAmount': '0H',
      'ticketPanel:rows:2:ticketAmount': '0W',
      'ticketPanel:rows:3:ticketAmount': '0E',
      'ticketPanel:rows:4:ticketAmount': '0P',
      'homeCaptcha:securityCode': captcha_code
      }
submit_url=soup.find(name='form', attrs={'id': 'BookingS1Form'})
submit_url='https://irs.thsrc.com.tw/IMINT'+submit_url['action']
submit=rs.post(url=submit_url, headers=headers, data=data)
# choose first
data={
      'TrainQueryDataViewPanel:TrainGroup': 'radio17'
      }
soup=BeautifulSoup(submit.text, 'html.parser')
submit_url=soup.find(name='form', attrs={'id': 'BookingS2Form'})
submit_url='https://irs.thsrc.com.tw/IMINT'+submit_url['action']
submit=rs.post(url=submit_url, headers=headers, data=data)
# get ticket details
soup=BeautifulSoup(submit.text, 'html.parser')
book_info_table=soup.find_all(name='table', attrs={'class': 'table_simple'})[0]
columns=book_info_table.find_all(name='tr')[0]
value=book_info_table.find_all(name='tr')[1]
for th, td in zip(columns.findChildren(recursive=False), value.findChildren(recursive=False)):
    print(th.text, ':', td.text)

