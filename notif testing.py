from PyQt5 import Qt
import sys
app = Qt.QApplication(sys.argv)
icon = Qt.QIcon("C:\\Users\\abdul\\Documents\\Python Scripts\\Green Lane Timetable Scraper git\\icons\\islamic3.png")
systemtray_icon = Qt.QSystemTrayIcon(app)
systemtray_icon.setIcon(icon) 
systemtray_icon.setToolTip("GLM Prayer Timetable")
systemtray_icon.show()
systemtray_icon.showMessage("Asr Start in 15 minutes", "You're welcome", icon)
print(systemtray_icon.isVisible())

while True:
    print("\o/")

"""
from win10toast import ToastNotifier
toaster = ToastNotifier()
toaster.show_toast()
"""
