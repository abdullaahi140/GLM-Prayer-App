import glmscraper as glm
import datetime
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
import os

class Notifications():

    def start_notif(queue,int_time,str_time,push,mail):
        queue.put(os.getpid())
        int_time,str_time,push,mail = sys.argv[1:]
        today_list, prayers_list = Notifications.remove_waste()
        while True:
            #time.sleep(60)
            if len(today_list) == 0:
                if Notifications.grab_list()[0][0].date() == datetime.date.today().replace(day = datetime.date.today().day + 1):
                    Notifications.start_notif()
                else:
                    pass
            elif (today_list[0] - datetime.datetime.now()).total_seconds() <= (int_time * 60):
                if mail is True:
                    Email.send_email(prayers_list[0], str_time)
                del today_list[0]
                del prayers_list[0]
            else:
                pass

    def remove_waste():
        today_list, prayers_list = Notifications.grab_list()
        k = 0
        for i in range(len(today_list)):
            if (today_list[k] - datetime.datetime.now()).total_seconds() <= 0:
                del today_list[k]
                del prayers_list[k]
            else:
                k += 1
        return today_list, prayers_list

    def grab_list():
        today = str(datetime.date.today())
        today_list = list(glm.todaysDate.today()[2:])
        prayers_list = ["Fajr Start", "Fajr Jamat", "Sunrise", "Dhuhr Start", "Dhuhr Jamat", "Asr Start", "Asr Jamat", "Maghrib", "Isha Start", "Isha Jamat"]
        k = 0
        for i in today_list:
            today_list[k] = today + " " + i
            today_list[k] = datetime.datetime.strptime(today_list[k],"%Y-%m-%d %I:%M%p")
            k += 1
        return today_list, prayers_list


class Email():

    def sender():
        SENDER_ADDRESS = "glmprayer@outlook.com"
        SENDER_PASSWORD = "makinganappishard123"
        return SENDER_ADDRESS, SENDER_PASSWORD

    def receiver():
        file = open("email_address.txt", "r")
        contact_email = file.read()
        file.close()
        return contact_email

    def msg_body(prayer,time):
        return ("""Dear Sir/Madam,\n\n{} prayer is coming shortly within {}.\n\nYours Truly,\nGLM Prayer Timetable App\n\nP.S. This is an automated email from GLM Prayer Timetable App.\nDO NOT SEND AN EMAIL TO THIS ADDRESS.\nIf you wish to no longer receive this emails please open the app and navigate to File > Settings > Deselect "Enable email notifications".""".format(prayer, time))

    def send_email(prayer,time):
        s = smtplib.SMTP(host="smtp-mail.outlook.com", port=587)
        s.starttls()
        s.login(Email.sender()[0], Email.sender()[1])

        msg = MIMEMultipart()
        msg["From"] = Email.sender()[0]
        msg["To"] = Email.receiver()
        msg["Subject"] = "{} is in {}".format(prayer, time)

        msg.attach(MIMEText(Email.msg_body(prayer=prayer, time=time), "plain"))  #CHANGE THIS
        s.send_message(msg)
        s.quit()


def main():
    sys.argv[2] = sys.argv[2].format(" ")
    #Notifications.start_notif(int(sys.argv[1]),sys.argv[2],sys.argv[3],sys.argv[4]) #Try this out
    print(sys.argv)


if __name__ == '__main__':
    main()
