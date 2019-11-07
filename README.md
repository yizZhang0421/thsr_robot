# thsr_robot
利用網頁爬蟲自動訂高鐵票</br>
captcha code辨識率目前不高，約6成</br>
原因為使用預設tesseract 英文字元辨識</br>
*修改成使用自己訓練的CNN神經網路辨識模型將能大幅提高</br>


<h3>作法</h3>
![image](https://github.com/yizZhang0421/thsr_robot/raw/master/readme_image/origin.jpg "test")</br>
上圖為原圖，經過觀察，高鐵訂票系統圖形驗證碼皆為數字及大寫英文的組合，並有一條隨機的曲線貫穿並破壞字元結構。</br>
</br>
![image](https://github.com/yizZhang0421/thsr_robot/raw/master/readme_image/denoise.jpg)</br>
經過二值化及去噪會產生上圖，仍無法簡單辨識出結果。</br>
</br>
![image](https://github.com/yizZhang0421/thsr_robot/raw/master/readme_image/line.jpg)</br>
需要找到曲線才能修復字元結構，方法為找到最左側的點和最右側的點及其中點加上一點偏差，就能利用二次方程式畫出曲線。</br>
</br>
![image](https://github.com/yizZhang0421/thsr_robot/raw/master/readme_image/fix.jpg)</br>
利用該曲線可以修補字元。</br>
</br>
![image](https://github.com/yizZhang0421/thsr_robot/raw/master/readme_image/finish.jpg)</br>
再做一些膨脹及腐蝕的操作就可以開始執行OCR</br>
</br>
