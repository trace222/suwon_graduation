import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class=uic.loadUiType("./ui/test.ui")[0]


class MyWindow(QMainWindow,form_class):
    def __init__(self):
        super().__init__()
        self.show()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.btn_clicked)
    def btn_clicked(self):
        plan=self.plainTextEdit.toPlainText()
        i=0
        value_l=[]
        valu=""
        while i<len(plan):
            if plan[i]=="\n":
                value_l.append(valu)
                self.listWidget.addItem(valu)
                valu=""
            else:
                valu=valu+plan[i]
            i=i+1
        value_l.append(valu)
        self.listWidget.addItem(valu)
        print(value_l)
        



    def exit_clicked(self):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    # myWindow2 = MyWindow2()
    
    app.exec_()
