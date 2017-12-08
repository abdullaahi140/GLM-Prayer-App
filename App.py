from PyQt5 import QtGui, QtWidgets, QtCore
import glmscraper as glm
import template
import datetime
import sys

class Window(QtWidgets.QMainWindow, template.Ui_MainWindow):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("GLM Prayer Timetable")
        self.today()

    def page(self):
        self.date_label.setText(self.date.strftime("%A %#d %B %Y"))
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
        self.b_button.clicked.connect(self.yesterday)
        self.f_button.clicked.connect(self.tomorrow)


    def today(self):
        self.date = datetime.date.today()
        self.tt = glm.todaysDate.today()
        self.page()

    def yesterday(self):
        self.date -= datetime.timedelta(1)
        self.past_datenum = self.date.strftime("%#d")
        self.past_month = self.date.strftime("%B")
        self.tt = glm.todaysDate.currentdaydata(self.past_datenum,self.past_month)
        self.page()
        
    def tomorrow(self):
        self.date += datetime.timedelta(1)
        self.future_datenum = self.date.strftime("%#d")
        self.future_month = self.date.strftime("%B")
        self.tt = glm.todaysDate.currentdaydata(self.future_datenum,self.future_month)
        self.page()

def main():
    app = QtWidgets.QApplication(sys.argv)
    GUI = Window()
    GUI.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
