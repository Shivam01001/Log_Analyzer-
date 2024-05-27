import pprint
from dotenv import load_dotenv 
import os
import re
import pandas as pd

load_dotenv()

logfile = open("server.log","r")

pattern = r'((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'

ip_add_list = []  
failed_list = []
success_list = []
date_list = []
hr_list = []
min_list = []
sec_list = []

for log in logfile:
    ip_add = re.search(pattern,log)
    ip_add_list.append(ip_add.group())
    lst = log.split(" ")
    #print(lst)
    failed_list.append((int)(lst[-1]))
    success_list.append((int)(lst[-4]))
    datestr= (str)(lst[3])
    date= datestr.split(":") 
    date_list.append(date[0])
    hr_list.append(date[1]) 
    min_list.append(date[2])
    sec_list.append(date[3])  
    
df = pd.DataFrame(columns=['Date','Hours','Minute','Second','IP Adress','Success','Faild'])
df['Date'] = date_list
df['Hours'] = hr_list
df['Minute'] = min_list
df['Second'] = sec_list
df['IP Adress'] = ip_add_list
df['Success'] = success_list
df['Faild'] = failed_list

df.to_csv("Analyzed.csv")

#sending Csvfile in mail 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

#Setup server
smtp_port = 587
smtp_server = "smtp.gmail.com" 

email_from = os.getenv('email_from')
email_to = "panditshivam632@gmail.com"

pswd = os.getenv('pswd')


subject = "Anaylyzed log csv file"

def send_emails(email_to):
    body = """Here is your formated log file 
    Check out CSV analyzed file created by python log anayzer by Shivam Pandit"""
    
    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = subject
    msg.attach(MIMEText(body,'plain'))

    fileName = "Analyzed.csv"

    #Opening file in read binary mode
    attachment = open(fileName,"rb")
    #enacoding in base 64
    attachment_packet = MIMEBase('application','octet-stream')
    attachment_packet.set_payload((attachment).read())
    encoders.encode_base64(attachment_packet)
    attachment_packet.add_header('Content-Disposition',"attechment; filename: "+fileName)
    msg.attach(attachment_packet)
    #casting in string
    text =  msg.as_string()

    #Connecting to the server 
    print("Connecting to server....")
    TIE_server = smtplib.SMTP(smtp_server,smtp_port)
    TIE_server.starttls()
    TIE_server.login(email_from,pswd)
    print("Connected sucessfully...!")
    print()

    #sending mail
    print(f"Sending mail to: {email_to}")
    TIE_server.sendmail(email_from,email_to,text)
    print("Email sent sucessfully to:"+email_to)
    print()

    TIE_server.quit()

send_emails(email_to)