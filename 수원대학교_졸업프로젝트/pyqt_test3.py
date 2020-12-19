import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import time
from client import SearchClient
import re
form_class=uic.loadUiType("./ui/login.ui")[0]
form_class2=uic.loadUiType("./ui/scan_ready.ui")[0]
form_class3=uic.loadUiType("./ui/scan.ui")[0]
# form_class4=uic.loadUiType("./ui/insert.ui")[0]
serches=SearchClient()
class MyWindow(QMainWindow,form_class):
    def __init__(self):
        super().__init__()
        self.show()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.btn_clicked)
        self.pushButton_2.clicked.connect(self.exit_clicked)
        self.id=""
        self.pw=""
        SearchClient.connectServer(serches)
    
    def btn_clicked(self):
        self.id=self.lineEdit.text()
        self.pw=self.lineEdit_2.text()
        try:
            recv_data=SearchClient.send_DBinfo(serches,self.id,self.pw)
        except:
            QMessageBox.about(self, "message","로그인중 에러가 발생하였습니다. 다시 시도해주세요")
            return
        
        if recv_data==True:
            # QMessageBox.about(self, "login","로그인 중 ....")
            # try:
            self.label_3.setText("<span style=' font-size:18pt; font-weight:600; color:#005500;'>로그인 중......</span>")
            self.label.repaint()
            SearchClient.set_TXset(serches)
            SearchClient.send_TXset(serches)
            # except:
            #     self.label_3.setText("")
            #     self.label.repaint()
            #     SearchClient.Initialize_DB(serches)
            #     QMessageBox.about(self, "warning","로그인 정보 전송중 오류가 발생하였습니다.")
            #     return
            self.close()
            self.myWindow2 = MyWindow2()
            self.myWindow2.set_id(self.id)
            self.myWindow2.show()
        else:
            QMessageBox.about(self, "message","아이디 또는 비밀번호가 일치하지않습니다.")

    def exit_clicked(self):
        self.close()
        
class MyWindow2(QMainWindow,form_class2):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.btn_clicked)
        self.pushButton_2.clicked.connect(self.btn_clicked2)

        # self.set_id("kwon")
    
    def set_id(self,id):
        # print(self.textBrowser_2.getText())
        self.id=id
        
        try:
            self.textBrowser_2.setText(self.id)
        except:
            self.textBrowser_2.setText("ID 정보를 불러오지 못했습니다.")
       
    def btn_clicked(self):
        # QMessageBox.about(self, "message","clicked")
        SearchClient.select_in(serches)
        self.close()
        self.myWindow3 = MyWindow3()
        self.myWindow3.set_id(self.id)
        self.myWindow3.show()

    def btn_clicked2(self):
        # QMessageBox.about(self, "message","clicked")
        # self.close()
        try:
            SearchClient.insert_in(serches)
            self.myWindow4 = MyWindow4()
            self.myWindow4.show()
            print("ss2")
        except:
            print("ss")
    


    
        
class MyWindow3(QMainWindow,form_class3):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.btn_clicked)
        self.pushButton_2.clicked.connect(self.exit_clicked)
        self.pushButton_3.clicked.connect(self.down_clicked)
        self.pushButton_4.clicked.connect(self.back_clicked)
        self.check_num=0
        # self.set_id("kwon")
        
    def set_id(self,id):
        self.id=id
        self.textBrowser_2.setText(self.id)

    def btn_clicked(self):
        i=0
        # if self.check_num !=0:
        SearchClient.loop_check(serches)
        self.listWidget.clear()
        try:
            print("kwon1")
            SearchClient.input_keyword(serches,self.plainTextEdit.toPlainText())
            print("kwon2")
            SearchClient.startwork(serches)
            print("kwon3")
            SearchClient.getIds(serches)
            print("kwon4")
            SearchClient.send_fileid(serches)
            print("kwon5")
            files=SearchClient.get_file(serches)
            print("kwon16")
            while i<len(files):
                self.listWidget.addItem(files[i])
                i=i+1
            print("kwon122")
            self.check_num=self.check_num+1
            SearchClient.select_send(serches)
            print("kwon1226")
        except:
            QMessageBox.about(self, "message","검색중 에러가 발생하였습니다 다시 검색해주세요")
            SearchClient.loop_check(serches)

        
    def down_clicked(self):
        try:
            check_num=0
            check_num=SearchClient.down_file(serches)
            if check_num==0:
                QMessageBox.about(self, "Warning", "다운 받을 파일이 없습니다")
        except:
            QMessageBox.about(self, "message","다운로드 에러입니다 재다운로드 하거나 재검색 해주세요")
    
    def back_clicked(self):
        SearchClient.back_check(serches)
        self.close()
        self.myWindow2 = MyWindow2()
        self.myWindow2.set_id(self.id)
        self.myWindow2.show()

    def exit_clicked(self):
        SearchClient.loop_check2(serches)
        self.close()

class MyWindow4(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()
 
    def setupUI(self):
        try:
            self.setGeometry(200,200,300,100)
            self.setWindowTitle("Upload file")
    
            self.OnOpenDocument_Button = QPushButton("파일 업로드")
            self.OnOpenDocument_Button.clicked.connect(self.FileUpload)
            self.label = QLabel()
    
            layout = QVBoxLayout()
            layout.addWidget(self.OnOpenDocument_Button)
            layout.addWidget(self.label)
    
            self.setLayout(layout)
        except:
            print("sfkkw")
 
    def FileUpload(self):
        open_file = QFileDialog.getOpenFileName(self, 'Open file', "",
                                            "All Files(*);; txt File(*.txt)")
        print("뭐가안맞아")
        list_n=open_file[0].split('/')
        file_name=list_n[-1]
        if open_file[0]:
            # f = open(open_file[0], 'r')
            # file_content = f.read()
            # file_keyword=re.split("[, !?:;]+",file_content)
            SearchClient.file_insert(serches,file_name,open_file[0])
            self.close()
        else:
            QMessageBox.about(self, "Warning", "파일을 선택하지 않았습니다.")
    def closeEvent(self, event):
        SearchClient.insert_exit(serches)
        self.deleteLater()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    # myWindow2 = MyWindow2()
    myWindow.show()
    app.exec_()
