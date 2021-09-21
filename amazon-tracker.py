import re
import os
import requests
import smtplib
from bs4 import BeautifulSoup
from datetime import datetime

#add product links, if needed add multiple products seperated by comma 
product_url=['https://www.amazon.in/gp/product/B07G3YNLJB/ref=ewc_pr_img_1?smid=ARBEPCMT3FADX&psc=1','https://www.amazon.in/gp/product/B079TH8YZQ/ref=ewc_pr_img_1?smid=A1QFJV05H9TXZX&psc=1']

#add max-price in the same order as you gave above
max_price=['2500','2600']

# google 'my user agent' to get user agent of your device
headers={"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

def check_price(product_url,max_price):
    #URL=URL_input
    page=requests.get(product_url,headers=headers)
    soup=BeautifulSoup(page.content,'html.parser')
    
    title=soup.find(id='productTitle').get_text()
    price=soup.find(id='priceblock_ourprice').get_text()
    
    converted_price=float(re.sub('\,',"",price[1:])) #eliminate "," and currency
   
    if(converted_price<float(max_price)):
        send_mail(product_url)
        log_data(True,title.strip(),converted_price)
    else:
        log_data(False,title.strip(),converted_price)

def send_mail(product_url):
    server= smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    
    # generate 16 digit 'google 2 step verification' passcode for your email and pass it as second argument
    # Otherwise search 'allow less secure apps'
    # Any of the above method works fine
    server.login('n**************gmail.com','z**************h')
    
    # Email format
    subject="Price fell down!"
    body=product_url
    msg=f"Subject: {subject}\n\n{body}"
    
    # Specify 'from and to' email address
    server.sendmail('n****************gmail.com','m***************mail.com',msg)
    print('Email Sent')
    server.quit()

def log_data(affordable,title,current_price):
   # Log generation in root folder
   location = os.path.realpath(os.path.join(os.getcwd(),os.path.dirname(__file__)))
   now = datetime.now()
   date_time = now.strftime("%d/%m/%Y %H:%M:%S")
   
   line1 = "\n*****"
   line2 = f"\n[{date_time}] {title}------{current_price}"
   line3 = f"\t:) Price fell down, email notification sent!"
   line4 = f"\t:( No price change"
   
   with open(os.path.join(location,"amazon-price-log.txt"), "a") as text_file:
        if affordable:
            text_file.writelines([line1,line2,line3])
        else:
            text_file.writelines([line1,line2,line4])
   print("log created")



for p,q in zip(product_url,max_price):
    check_price(p,q)