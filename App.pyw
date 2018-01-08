from PyQt5 import QtGui, QtWidgets, QtCore, uic
import sys
import subprocess
import multiprocessing  # decide on this or subprocess
import datetime
import csv
import glmscraper as glm
import notifications


class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi('template.ui', self)
        self.setWindowTitle("GLM Prayer Timetable")
        self.fileSettings.triggered.connect(self.show_dialog)
        self.fileQuit.triggered.connect(self.close_application)
        self.setWindowIcon(QtGui.QIcon(QtGui.QPixmap("icons\icons8_Right_1.png")))
        self.today()
        self.b_button.clicked.connect(self.yesterday)
        self.f_button.clicked.connect(self.tomorrow)

    def page(self,tt):
        self.date_label.setText(self.date.strftime("%A {} %B %Y".format(tt[1])))
        _translate = QtCore.QCoreApplication.translate
        self.t1_label.setText(_translate("GUI", "<html><head/><body><p align=\"right\">%s</p></body></html>" %tt[2]))
        self.t2_label.setText(_translate("GUI", "<html><head/><body><p align=\"right\">%s</p></body></html>" %tt[3]))
        self.t3_label.setText(_translate("GUI", "<html><head/><body><p align=\"right\">%s</p></body></html>" %tt[4]))
        self.t4_label.setText(_translate("GUI", "<html><head/><body><p align=\"right\">%s</p></body></html>" %tt[5]))
        self.t5_label.setText(_translate("GUI", "<html><head/><body><p align=\"right\">%s</p></body></html>" %tt[6]))
        self.t6_label.setText(_translate("GUI", "<html><head/><body><p align=\"right\">%s</p></body></html>" %tt[7]))
        self.t7_label.setText(_translate("GUI", "<html><head/><body><p align=\"right\">%s</p></body></html>" %tt[8]))
        self.t8_label.setText(_translate("GUI", "<html><head/><body><p align=\"right\">%s</p></body></html>" %tt[9]))
        self.t9_label.setText(_translate("GUI", "<html><head/><body><p align=\"right\">%s</p></body></html>" %tt[10]))
        self.t10_label.setText(_translate("GUI", "<html><head/><body><p align=\"right\">%s</p></body></html>" %tt[11]))

    def show_dialog(self):
        d = Dialog()
        x = d.exec_()
        if x == Dialog.Accepted:
            self.settings_file(d.comboBox.currentIndex(),  d.pushnotif_cb.isChecked(),
                                            d.emailnotif_cb.isChecked(), d.email_le.text())
            if d.comboBox.currentIndex() != 0:
                self.initiate_notifs(d.comboBox.currentIndex(),  d.pushnotif_cb.isChecked(),
                                            d.emailnotif_cb.isChecked(), d.email_le.text())
                                            # Gotta look into subprocess

    def settings_file(self,comboBox_index, push_bool, email_bool, email_address):
        rows = [comboBox_index, push_bool, email_bool, email_address]
        with open("settings.csv", "w") as csvfile:
            writecsv= csv.writer(csvfile, lineterminator= "\n")
            for i in rows:
                writecsv.writerow([i])

    def initiate_notifs(self,time_index,push_bool,email_bool, email_address):
        file = open("email_address.txt", "w")
        file.write(email_address)
        file.close()

        reminders_int_list = [None, 5, 10, 15]
        reminders_str_list = [None, "5 minutes", "10 mminutes", "15 minutes"]

        # sts = subprocess.call("pythonw notifications.pyw" + " " + str(reminders_int_list[time_index]) + " " + reminders_str_list[time_index] + " " + str(push_bool) + " " + str(email_bool))
        # print(sts.pid())
        # Carry on from here

        p = multiprocessing.Process(name="notifications", target=notifications.Notifications.start_notif, args=(reminders_int_list[time_index], reminders_str_list[time_index], push_bool, email_bool), daemon=True)
        p.start()
        print(p.pid)
        print(p)

    def yesterday(self):
        self.date -= datetime.timedelta(1)
        self.past_datenum = self.date.strftime("%#d")
        self.past_month = self.date.strftime("%B%Y")
        tt = glm.dateData.currentdaydata(self.past_datenum,self.past_month)
        self.tt_empty(tt,self.sender())

    def today(self):
        self.date = datetime.date.today()
        tt = glm.dateData.today()
        self.page(tt)

    def tomorrow(self):
        self.date += datetime.timedelta(1)
        self.future_datenum = self.date.strftime("%#d")
        self.future_month = self.date.strftime("%B%Y")
        tt = glm.dateData.currentdaydata(self.future_datenum,self.future_month)
        self.tt_empty(tt,self.sender())

    def tt_empty(self,tt,sender):
        if "1st" or "28th" or "29th" or "30th" in tt[1]:
            if sender.text() == "Backwards":
                i = -1
            elif sender.text() == "Forwards":
                i = 1

            temp_date = self.date + (datetime.timedelta(1) * i)
            temp_datenum = temp_date.strftime("%#d")
            temp_month = temp_date.strftime("%B%Y")
            temp_tt = glm.dateData.currentdaydata(temp_datenum,temp_month)

            if temp_tt is None:
                sender.setDisabled(True)
                self.page(tt)
            else:
                self.b_button.setEnabled(True)
                self.f_button.setEnabled(True)
                self.page(tt)

        else:
            self.b_button.setEnabled(True)
            self.f_button.setEnabled(True)
            self.page(tt)

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
        with open("settings.csv", "r") as csvfile:
            readcsv = csv.reader(csvfile)
            settings_list = [i for row in readcsv for i in row]

        self.comboBox.setCurrentIndex(int(settings_list[0]))
        if settings_list[1] == "True":
            self.pushnotif_cb.nextCheckState()
        if settings_list[2] == "True":
            self.emailnotif_cb.nextCheckState()
        if len(settings_list) == 4:
            self.email_le.setText(settings_list[3])


def main():
    app = QtWidgets.QApplication(sys.argv)
    GUI = Window()
    GUI.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
