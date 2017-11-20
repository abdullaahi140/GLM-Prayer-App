"""from PyQt5 import Qt
import sys
app = Qt.QApplication(sys.argv)
systemtray_icon = Qt.QSystemTrayIcon(app)
systemtray_icon.setIcon(Qt.QIcon("vscode-good.ico")) 
systemtray_icon.show()
systemtray_icon.showMessage("Biriyani", "Gotta love some biriyani")
"""
from win10toast import ToastNotifier
toaster = ToastNotifier()
toaster.show_toast("Biriyani",
              "I want some now",
              icon_path="vscode-good.ico",
              duration=10)