from PyQt5 import QtGui, QtWidgets, QtCore, uic
import sys
import subprocess
import datetime
import json
import glmscraper as glm
import notifications
import psutil


class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi('home.ui', self)
        self.setWindowTitle("GLM Prayer Timetable")
        self.setWindowIcon(QtGui.QIcon("icons\\islamic3.png"))
        self.s_button.clicked.connect(self.show_dialog)
        self.dateincrement = 0
        self.current_day()
        self.time_until_prayer()
        self.b_button.clicked.connect(self.yesterday)
        self.f_button.clicked.connect(self.tomorrow)

    def keyPressEvent(self,event):
        if event.key() == QtCore.Qt.Key_Left:
            self.b_button.animateClick()
        if event.key() == QtCore.Qt.Key_Right:
            self.f_button.animateClick()

    def time_remaining(self):
        self.prayers_list = ["Fajr Start", "Fajr Jamat", "Sunrise", "Dhuhr Start", "Dhuhr Jamat", "Asr Start", "Asr Jamat", "Maghrib", "Isha Start", "Isha Jamat"]
        temp_tt, temp_date, temp_day, temp_month = glm.dateData.dt_grab_prayer_times(datetime.datetime.now(), self.dateincrement)
        datetime_tt = glm.dateData.dt_tt(temp_tt,temp_day,temp_month,hourformat="%I:%M %p",yearformat="%d%B%Y")[2:]

        self.timelist = []
        for i in datetime_tt:
            if (i - datetime.datetime.now()).total_seconds() > 0:
                self.timelist.append((i - datetime.timedelta(hours=datetime.datetime.now().hour, minutes=datetime.datetime.now().minute, seconds=datetime.datetime.now().second)))
            else:
                del self.prayers_list[0]

        if len(self.timelist) != 0:
            self.time_update = datetime.datetime.strftime(self.timelist[0], "%H:%M:%S")
        else:
            self.dateincrement += 1
            self.time_remaining()

    def time_until_prayer(self):
        self.time_remaining()
        labels = [self.timeleft_label, self.t11_label]
        texts = [("Time until " + self.prayers_list[0]), self.time_update]
        self.label_factory(labels, texts, "right")
        QtCore.QTimer.singleShot(1000, self.time_until_prayer)

    def page(self):
        self.date_label.setText(self.day.strftime("%A\n{} %B\n%Y".format(self.tt[1])))
        labels = [self.t1_label, self.t2_label, self.t3_label, self.t4_label, self.t5_label, self.t6_label,  self.t7_label, self.t8_label, self.t9_label, self.t10_label]
        self.label_factory(labels, self.tt[2:], "center")
    
    def label_factory(self, labels, texts, align):
        _translate = QtCore.QCoreApplication.translate
        for label, text in zip(labels, texts):
            label.setText(_translate("GUI", "<html><head/><body><p align=\"{}\">{}</p></body></html>".format(align, text)))

    def checktwofour(self):
        with open("settings.json", "r") as j:
            settings = json.load(j)

        if settings["24hour"] is True:
            self.am = False
            self.pm = True
        elif settings["24hour"] is False:
            self.am  = True
            self.pm = False

    def yesterday(self):
        self.tt, self.day = glm.dateData.dt_grab_prayer_times(self.day,dateincrement= -1,twelve=self.am,twofour=self.pm)[:2]
        self.tt_empty(self.sender())

    def current_day(self):
        self.checktwofour()
        self.tt, self.day = glm.dateData.dt_grab_prayer_times(datetime.datetime.today(),dateincrement=0,twelve=self.am,twofour=self.pm)[:2]
        self.page()

    def tomorrow(self):
        self.tt, self.day = glm.dateData.dt_grab_prayer_times(self.day,dateincrement=1,twelve=self.am,twofour=self.pm)[:2]
        self.tt_empty(self.sender())

    def tt_empty(self,sender):
        if "1st" in self.tt[1] or "28th" in self.tt[1] or "29th" in self.tt[1] or "30th" in self.tt[1]:
            if sender.objectName() == "b_button":
                temp_tt = glm.dateData.dt_grab_prayer_times(self.day,-1)[0]
            elif sender.objectName() == "f_button":
                temp_tt = glm.dateData.dt_grab_prayer_times(self.day,1)[0]

            if temp_tt is None:
                sender.setDisabled(True)
                self.page()
            else:
                self.b_button.setEnabled(True)
                self.f_button.setEnabled(True)
                self.page()
        else:
            self.b_button.setEnabled(True)
            self.f_button.setEnabled(True)
            self.page()

    def show_dialog(self):
        d = Dialog()
        if d.exec_() == Dialog.Accepted:
            self.settings_file(d.comboBox.currentIndex(),  d.pushnotif_cb.isChecked(), d.emailnotif_cb.isChecked(), d.email_le.text(), d.start_cb.isChecked(), d.jamat_cb.isChecked(), d.twofour_cb.isChecked())
        self.initiate_notifs(d.comboBox.currentIndex(),  d.pushnotif_cb.isChecked(), d.emailnotif_cb.isChecked(), d.email_le.text(), d.start_cb.isChecked(), d.jamat_cb.isChecked(), d.twofour_cb.isChecked())
        self.current_day()

    def settings_file(self, comboBox_index, push_bool, email_bool, email_address, start_bool, jamat_bool, twofour_bool):
        rows = [comboBox_index, push_bool, email_bool, email_address, start_bool, jamat_bool, twofour_bool]

        with open("settings.json", "r") as j:
            settings = json.load(j)
            dictkeys = [i for i in settings.keys()]
            for key, value in zip(dictkeys, rows):
                settings[key] = value

        with open("settings.json", "w") as j:
            json.dump(settings, j, indent=4)

    def initiate_notifs(self,time_index,push_bool,email_bool,email_address,start_bool,jamat_bool,twofour_bool):
        reminders_int_list = [None, 5, 10, 15]
        reminders_str_list = [None, "5{}minutes", "10{}minutes", "15{}minutes"]

        for proc in psutil.process_iter():
            try:
                if "notifications.pyw" in proc.cmdline():
                    proc.kill()
            except (psutil._exceptions.AccessDenied, IndexError):
                pass

        if time_index != 0:
            # print('pythonw "notifications.pyw"', str(reminders_int_list[time_index]), reminders_str_list[time_index], str(push_bool), str(email_bool), str(start_bool), str(jamat_bool))
            subprocess.Popen('pythonw "notifications.pyw"' + " " + str(reminders_int_list[time_index]) + " " + reminders_str_list[time_index] + " " + str(push_bool) + " " + str(email_bool) + " " + str(start_bool) + " " + str(jamat_bool))
            # notifications.Notifications.start_notif(str(reminders_int_list[time_index]), reminders_str_list[time_index], str(push_bool), str(email_bool), str(start_bool), str(jamat_bool))


class Dialog(QtWidgets.QDialog):

    def __init__(self):
        super(Dialog, self).__init__()
        uic.loadUi('dialog.ui', self)
        self.setWindowTitle("Settings")
        self.setWindowIcon(QtGui.QIcon("icons\\islamic3.png"))      
        self.comboBox.currentIndexChanged.connect(self.check_no_notifs)
        self.emailnotif_cb.stateChanged.connect(self.enable_le)
        self.restore_settings()
        self.check_no_notifs()

    def check_no_notifs(self):
        if self.comboBox.currentIndex() == 0:
            self.pushnotif_cb.setChecked(False)
            self.emailnotif_cb.setChecked(False)
            self.pushnotif_cb.setDisabled(True)
            self.emailnotif_cb.setDisabled(True)
            self.emailnotif_label.setStyleSheet("color: rgb(211, 211, 211);")
            self.pushnotif_label.setStyleSheet("color: rgb(211, 211, 211);")
        else:
            self.emailnotif_cb.setEnabled(True)
            self.pushnotif_cb.setEnabled(True)
            self.emailnotif_label.setStyleSheet("color: rgb(0, 0, 0);")
            self.pushnotif_label.setStyleSheet("color: rgb(0, 0, 0);")
        self.enable_le()

    def enable_le(self):
        if self.emailnotif_cb.isChecked() is True:
            self.email_le.setEnabled(True)
            self.emailadd_label.setStyleSheet("color: rgb(0, 0, 0);")      
        else:
            self.email_le.clear()
            self.email_le.setDisabled(True)
            self.emailadd_label.setStyleSheet("color: rgb(211, 211, 211);")

    def restore_settings(self):
        with open("settings.json", "r") as j:
            settings = json.load(j)

        self.comboBox.setCurrentIndex(settings["rmd_index"])
        if settings["push"] is True:
            self.pushnotif_cb.nextCheckState()
        if settings["email"] is True:
            self.emailnotif_cb.nextCheckState()
            self.email_le.setText(settings["emailaddress"])
        if settings["startpry"] is True:
            self.start_cb.nextCheckState()
        if settings["jamatpry"] is True:
            self.jamat_cb.nextCheckState()
        if settings["24hour"] is True:
            self.twofour_cb.nextCheckState()

def main():
    app = QtWidgets.QApplication(sys.argv)
    QtGui.QFontDatabase().addApplicationFont("Nunito//Nunito-Regular.ttf")
    GUI = Window()
    GUI.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
