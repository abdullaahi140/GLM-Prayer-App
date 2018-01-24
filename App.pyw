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
        uic.loadUi('template.ui', self)
        self.setWindowTitle("GLM Prayer Timetable")
        self.fileSettings.triggered.connect(self.show_dialog)
        self.fileQuit.triggered.connect(self.close_application)
        self.setWindowIcon(QtGui.QIcon(QtGui.QPixmap("icons\icons8_Right_1.png")))
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint) # Remove titlebar
        self.today()
        self.b_button.clicked.connect(self.yesterday)
        self.f_button.clicked.connect(self.tomorrow)

    def page(self):
        self.tt = self.checktwofour()

        self.date_label.setText(self.date.strftime("%A {} %B %Y".format(self.tt[1])))
        _translate = QtCore.QCoreApplication.translate
        self.t1_label.setText(_translate("GUI", "<html><head/><body><p align=\"right\">%s</p></body></html>" %self.tt[2]))
        self.t2_label.setText(_translate("GUI", "<html><head/><body><p align=\"right\">%s</p></body></html>" %self.tt[3]))
        self.t3_label.setText(_translate("GUI", "<html><head/><body><p align=\"right\">%s</p></body></html>" %self.tt[4]))
        self.t4_label.setText(_translate("GUI", "<html><head/><body><p align=\"right\">%s</p></body></html>" %self.tt[5]))
        self.t5_label.setText(_translate("GUI", "<html><head/><body><p align=\"right\">%s</p></body></html>" %self.tt[6]))
        self.t6_label.setText(_translate("GUI", "<html><head/><body><p align=\"right\">%s</p></body></html>" %self.tt[7]))
        self.t7_label.setText(_translate("GUI", "<html><head/><body><p align=\"right\">%s</p></body></html>" %self.tt[8]))
        self.t8_label.setText(_translate("GUI", "<html><head/><body><p align=\"right\">%s</p></body></html>" %self.tt[9]))
        self.t9_label.setText(_translate("GUI", "<html><head/><body><p align=\"right\">%s</p></body></html>" %self.tt[10]))
        self.t10_label.setText(_translate("GUI", "<html><head/><body><p align=\"right\">%s</p></body></html>" %self.tt[11]))

    def checktwofour(self):
        with open("settings.json", "r") as j:
            settings = json.load(j)

        if settings["24hour"] is True:
            self.tt = glm.dateData.dtobjectify([i.replace(" ", "") for i in self.tt], pm=True)
        elif settings["24hour"] is False:
            try:
                self.tt = glm.dateData.dtobjectify(self.tt, am=True, hourformat="%H:%M")
            except ValueError:
                pass
        return self.tt

    def yesterday(self):
        self.date -= datetime.timedelta(1)
        self.past_datenum = self.date.strftime("%#d")
        self.past_month = self.date.strftime("%B%Y")
        self.tt = glm.dateData.currentdaydata(self.past_datenum,self.past_month,am=True,pm=None)
        self.tt_empty(self.sender())

    def today(self):
        self.date = datetime.date.today()
        self.tt = glm.dateData.today(am=True,pm=None)
        self.page()

    def tomorrow(self):
        self.date += datetime.timedelta(1)
        self.future_datenum = self.date.strftime("%#d")
        self.future_month = self.date.strftime("%B%Y")
        self.tt = glm.dateData.currentdaydata(self.future_datenum,self.future_month,am=True,pm=None)
        self.tt_empty(self.sender())

    def tt_empty(self,sender):
        if "1st" in self.tt[1] or "28th" in self.tt[1] or "29th" in self.tt[1] or "30th" in self.tt[1] or "31th" in self.tt[1]:
            if sender.text() == "Backwards":
                i = -1
            elif sender.text() == "Forwards":
                i = 1

            temp_date = self.date + (datetime.timedelta(1) * i)
            temp_datenum = temp_date.strftime("%#d")
            temp_month = temp_date.strftime("%B%Y")
            temp_tt = glm.dateData.currentdaydata(temp_datenum,temp_month,am=True,pm=False)

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
        x = d.exec_()
        if x == Dialog.Accepted:
            self.settings_file(d.comboBox.currentIndex(),  d.pushnotif_cb.isChecked(), d.emailnotif_cb.isChecked(), d.email_le.text(), d.start_cb.isChecked(), d.jamat_cb.isChecked(), d.twofour_cb.isChecked())
        if d.comboBox.currentIndex() != 0:
            self.initiate_notifs(d.comboBox.currentIndex(),  d.pushnotif_cb.isChecked(), d.emailnotif_cb.isChecked(), d.email_le.text(), d.start_cb.isChecked(), d.jamat_cb.isChecked(), d.twofour_cb.isChecked())
        self.page()

    def settings_file(self, comboBox_index, push_bool, email_bool, email_address, start_bool, jamat_bool, twofour_bool):
        rows = [comboBox_index, push_bool, email_bool, email_address, start_bool, jamat_bool, twofour_bool]

        with open("settings.json", "r") as j:
            settings = json.load(j)
            dictkeys = [i for i in settings.keys()]
            for key, value in zip(dictkeys, rows):
                settings[key] = value

        with open("settings.json", "w") as j:
            json.dump(settings, j, indent=4)

    def initiate_notifs(self,time_index,push_bool,email_address,email_bool,start_bool,jamat_bool,twofour_bool):
        reminders_int_list = [None, 5, 10, 15]
        reminders_str_list = [None, "5{}minutes", "10{}minutes", "15{}minutes"]

        for proc in psutil.process_iter():
            try:
                if "notifications.pyw" in proc.cmdline():
                    proc.kill()
            except (psutil._exceptions.AccessDenied, IndexError):
                pass

        subprocess.Popen('pythonw "notifications.pyw"' + " " + str(reminders_int_list[time_index]) + " " + reminders_str_list[time_index] + " " + str(push_bool) + " " + str(email_bool) + " " + str(start_bool) + " " + str(jamat_bool))
        # notifications.Notifications.start_notif(str(reminders_int_list[time_index]), reminders_str_list[time_index], str(push_bool), str(email_bool), str(start_bool), str(jamat_bool))

    def close_application(self,event):
        sys.exit()


class Dialog(QtWidgets.QDialog):

    def __init__(self):
        super(Dialog, self).__init__()
        uic.loadUi('dialog.ui', self)
        self.setWindowTitle("Settings")
        self.comboBox.currentIndexChanged.connect(self.check_no_notifs)
        self.emailnotif_cb.stateChanged.connect(self.enable_le)
        self.restore_settings()

    def check_no_notifs(self):
        if self.comboBox.currentIndex() == 0:
            self.pushnotif_cb.nextCheckState()
            self.emailnotif_cb.nextCheckState()
            self.pushnotif_cb.setDisabled(True)
            self.emailnotif_cb.setDisabled(True)
            self.emailnotif_label.setStyleSheet("color: rgb(211, 211, 211);")
            self.pushnotif_label.setStyleSheet("color: rgb(211, 211, 211);")
        else:
            self.emailnotif_cb.setEnabled(True)
            self.pushnotif_cb.setEnabled(True)
            self.emailnotif_label.setStyleSheet("color: rgb(0, 0, 0);")
            self.pushnotif_label.setStyleSheet("color: rgb(0, 0, 0);")

    def enable_le(self):
        if self.emailnotif_cb.isChecked():
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
            self.email_le.setText(settings["emailadd"])
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
