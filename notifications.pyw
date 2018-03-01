import glmscraper as glm
import datetime
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from PyQt5 import Qt
import sys
import os


class Notifications():

    def start_notif(int_time,str_time,push,mail,start,jamat):
        int_time = int(int_time)
        str_time = str_time.format(" ")
        today_list, prayers_list = Notifications.grab_list() 
        while True:
            time.sleep(60)
            if len(today_list) == 0:
                if Notifications.grab_list()[0][0].date() == datetime.date.today().replace(day=datetime.date.today().day + 1):
                    Notifications.start_notif()
                else:
                    pass
            elif (today_list[0] - datetime.datetime.now()).total_seconds() <= (int_time * 60):
                if push == "True":
                    Push.win10push(prayers_list[0], str_time)
                if mail == "True":
                    Email.send_email(prayers_list[0], str_time)
                del today_list[0]
                del prayers_list[0]
            else:
                pass

    def grab_list():
        today_list, date, day, month  = glm.dateData.dt_grab_prayer_times(datetime.datetime.today())
        prayers_list = ["Fajr Start", "Fajr Jamat", "Sunrise", "Dhuhr Start", "Dhuhr Jamat", "Asr Start", "Asr Jamat", "Maghrib", "Isha Start", "Isha Jamat"]
        today_list = glm.dateData.dt_tt(today_list,day,month,hourformat="%I:%M %p",yearformat="%d%B%Y")[2:]
        k = 0
        for i in range(len(today_list)):
            if (today_list[k] - datetime.datetime.now()).total_seconds() <= 0:
                del today_list[k]
                del prayers_list[k]
            else:
                k += 1
        return today_list, prayers_list


class Push():

    def win10push(prayer,ptime):
        app = Qt.QApplication(sys.argv)
        icon = Qt.QIcon("icons\\islamic3.png")
        sys_tray = Qt.QSystemTrayIcon(app)
        sys_tray.setIcon(icon)
        sys_tray.setToolTip("GLM Prayer Timetable")
        sys_tray.show()
        sys_tray.showMessage("{} in {}".format(prayer,ptime), "GLM Prayer Timetable", icon, 10000)
        time.sleep(10)


class Email():

    def receiver_address():
        with open("settings.json", "r") as j:
            settings = json.load(j)
        return settings["emailaddress"]

    def msg_body(prayer,time):
        return ("""Dear Sir/Madam,\n\n{} prayer is coming shortly within {}.\n\nYours Truly,\nGLM Prayer Timetable App\n\nP.S. This is an automated email from GLM Prayer Timetable App.\nDO NOT SEND AN EMAIL TO THIS ADDRESS.\nIf you wish to no longer receive this emails please open the app and navigate to File > Settings > Deselect "Enable email notifications".""".format(prayer, time))

    def send_email(prayer,time):
        s = smtplib.SMTP(host="smtp-mail.outlook.com", port=587)
        s.starttls()
        s.login("glmprayer@outlook.com", "makinganappishard123")

        msg = MIMEMultipart()
        msg["From"] = "glmprayer@outlook.com"
        msg["To"] = Email.receiver_address()
        msg["Subject"] = "{} is in {}".format(prayer, time)

        msg.attach(MIMEText(Email.msg_body(prayer=prayer, time=time), "plain"))  #CHANGE THIS
        s.send_message(msg)
        s.quit()


if __name__ == '__main__':
    Notifications.start_notif(*sys.argv[1:])
    # Notifications.start_notif("23","5{}minutes","True","False",False,False)