from PyQt5.QtWidgets import *
import sys
import re
class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()
 
    def setupUI(self):
        self.setGeometry(200,200,300,100)
        self.setWindowTitle("Upload file")
 
        self.OnOpenDocument_Button = QPushButton("파일 업로드")
        self.OnOpenDocument_Button.clicked.connect(self.FileUpload)
        self.label = QLabel()
 
        layout = QVBoxLayout()
        layout.addWidget(self.OnOpenDocument_Button)
        layout.addWidget(self.label)
 
        self.setLayout(layout)
 
    def FileUpload(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', "",
                                            "All Files(*);; txt File(*.txt)")
        list_n=fname[0].split('/')
        file_name=list_n[-1]
        if fname[0]:
            f = open(fname[0], 'r')
            filnes = f.read()
            filew=re.split("[, !?:;]+",filnes)
            print(filew)
        else:
            QMessageBox.about(self, "Warning", "파일을 선택하지 않았습니다.")
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()
