#!/usr/bin/python3

import datetime, time, os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

mail_host = "smtp.163.com"
mail_user = "houmin_wei@163.com"
mail_pass = "********"

sender = 'houmin_wei@163.com'
receivers = ['houmin.wei@pku.edu.cn']

def cal_week(date):
    start_date = '20200104'
    week_start = 9175
    start_sec = time.mktime(time.strptime(start_date, '%Y%m%d'))
    date_sec = time.mktime(time.strptime(date, '%Y%m%d'))
    week_delta = int((date_sec - start_sec)/(24*60*60*7))
    week_now = week_start + week_delta
    return week_now

def get_audio(date, path):
    week_now = cal_week(date)
    url = "https://audiocdn.economist.com/sites/default/files/AudioArchive/{year}/{date}/Issue_{week}_{date}_The_Economist_Full_edition.zip".format(year=date[0:4], date=date, week=week_now)
    print(url)
    cmd = "cd {path}/audio && wget {url} && cd -;".format(path=path, url=url)
    os.system(cmd)

def get_book(date, path):
    filename = path + "/ebook/te" + date
    #cmd = 'ebook-convert \"The Economist.recipe\" ' + filename + '.mobi --output-profile=kindle'
    cmd = 'ebook-convert \"The Economist.recipe\" ' + filename + '.epub'
    os.system(cmd)

def send_mail(date, path, sender, receivers):
    epubFile = path + "/ebook/te" + date + '.epub'
    epubApart = MIMEApplication(open(epubFile, 'rb').read())
    epubApart.add_header('Content-Disposition', 'attachment', filename=epubFile)

    message = MIMEMultipart()
    message.attach(epubApart)
    message['Subject'] = "The Economist " + date

    try:
        smtpObj = smtplib.SMTP(mail_host, 465)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("sending mail success!")
    except smtplib.SMTPException:
        print("Error: cannot send mail")

def operator(path):
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    date = tomorrow.strftime('%Y%m%d')
    print("===============================================")
    print("Fetch The Economist {date} begin...".format(date=date))
    get_book(date, path)
    #get_audio(date, path)
    #send_mail(date, path, sender, receivers)
    print("Fetch The Economist {date} end.".format(date=date))
    print("===============================================\n\n")


if __name__ == "__main__":
    operator("./")
