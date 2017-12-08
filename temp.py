"""from PyQt5 import Qt
import sys
app = Qt.QApplication(sys.argv)
systemtray_icon = Qt.QSystemTrayIcon(app)
systemtray_icon.setIcon(Qt.QIcon("temperature.ico")) 
systemtray_icon.show()
systemtray_icon.showMessage("Biriyani", "Gotta love some biriyani")

"""

from win10toast import ToastNotifier
toaster = ToastNotifier()
toaster.show_toast("Biriyani",
              "I want some now",
              icon_path="\\temperature.ico",
              duration=10)

