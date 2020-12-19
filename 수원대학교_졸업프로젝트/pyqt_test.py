import sys
from PyQt5.QtWidgets import *
def clicked_slot():
    print("clicke")

app=QApplication(sys.argv)
# label=QLabel("Hello, PyQt")
# label.show()

btn=QPushButton("hello")
btn.clicked.connect(clicked_slot)
print("before event")
btn.show()
print("before event2")
app.exec_()
print("after")