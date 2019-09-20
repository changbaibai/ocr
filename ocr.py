# -*- coding: utf-8 -*-
import random
import requests
import urllib.request, urllib.parse
import  io, sys, json, socket
import base64
from pynput.keyboard import Controller, Key, Listener
from PIL import ImageGrab
socket.setdefaulttimeout(30)
import pyperclip
from PyQt5.QtGui import QPixmap,QIcon,QPalette,QBrush
from PyQt5.QtWidgets import QWidget,QListWidget,QMessageBox, QApplication, QGroupBox, QPushButton, QLabel, QHBoxLayout,  QVBoxLayout, QGridLayout, QFormLayout, QLineEdit, QTextEdit
# 监听按压
def on_press(key):
    try:
        print("正在按压:", format(key.char))
    except AttributeError:
        print("正在按压:", format(key))
        if format(key)=='Key.enter':
            print(233)
    # 开始监听
def start_listen():
        with Listener(on_press=on_press) as listener:
            listener.join()
def get_pictrue(url):
    try:
        req = requests.get(url)
        photo = QPixmap()
        photo.loadFromData(req.content)
        return photo
    except:
        msg_box = QMessageBox(QMessageBox.Warning,"响应超时", "网络连接超时")
        msg_box.show()
        sys.exit(app.exec_())
class frame(QWidget):
    def __init__(self):
        super(frame,self).__init__()
        self.initUi()
    def initUi(self):
        self.createGridGroupBox()
        self.creatVboxGroupBox()
        self.creatFormGroupBox()
        self.setGeometry(300,300,300,150)
        mainLayout = QVBoxLayout()
        hboxLayout = QHBoxLayout()
        hboxLayout.addStretch()
        hboxLayout.addWidget(self.gridGroupBox)
        hboxLayout.addWidget(self.vboxGroupBox)
        mainLayout.addLayout(hboxLayout)
        mainLayout.addWidget(self.formGroupBox)
        self.setLayout(mainLayout)
    def createGridGroupBox(self):
        list=['https://gitee.com/changbaibai/picture/raw/master/00.png'
            ,'https://gitee.com/changbaibai/picture/raw/master/11.png'
              ,'https://gitee.com/changbaibai/picture/raw/master/22.png'
            ,'https://gitee.com/changbaibai/picture/raw/master/33.png'
               ,'https://gitee.com/changbaibai/picture/raw/master/44.png'
            ,'https://gitee.com/changbaibai/picture/raw/master/55.png'
            , 'https://gitee.com/changbaibai/picture/raw/master/66.png'
            , 'https://gitee.com/changbaibai/picture/raw/master/77.png'
            , 'https://gitee.com/changbaibai/picture/raw/master/88.png'
            , 'https://gitee.com/changbaibai/picture/raw/master/99.png'
            , 'https://gitee.com/changbaibai/picture/raw/master/01.png']
        num=random.randint(0,10)
        print(list[num])
        photo = get_pictrue(list[num])
        self.gridGroupBox = QGroupBox()
        layout = QGridLayout()
        imgeLabel = QLabel()
        pixMap = QPixmap(photo)
        imgeLabel.setPixmap(pixMap)
        imgeLabel.setScaledContents(True)
        layout.setSpacing(10)
        layout.addWidget(imgeLabel,0,0,5,5)
        layout.setColumnStretch(1,10)
        self.gridGroupBox.setLayout(layout)
        self.setWindowTitle('文字提取')
    def creatVboxGroupBox(self):
        self.vboxGroupBox = QGroupBox()
        layout = QVBoxLayout()
        self.setLayout(layout)
        nameLabel = QLabel("文字识别结果：")
        self.listFile = QListWidget()
        self.msg_box = QMessageBox()
        layout.addWidget(nameLabel)
        layout.addWidget(self.listFile)
        self.vboxGroupBox.setLayout(layout)
    def creatFormGroupBox(self):
        import urllib.request
        url = "https://gitee.com/changbaibai/picture/raw/master/gonggao.txt"
        headers = ("User-Agent",
                   "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
        opener = urllib.request.build_opener()
        opener.addheaders = [headers]
        textPage = opener.open(url).read()
        str = textPage
        s = str.strip().decode('utf-8')
        # textPage = urllib.request.urlopen("https://gitee.com/changbaibai/picture/raw/master/gonggao.txt")
        # s = textPage.read()
        self.formGroupBox = QGroupBox()
        layout = QFormLayout()
        performanceLabel = QLabel("使用帮助：")
        planEditor = QTextEdit()
        planEditor.setPlainText(s)
        layout.addRow(performanceLabel)
        layout.addRow(planEditor)
        #创建按钮2
        self.btn2=QPushButton('识别' )

        #为按钮2添加图标
        self.btn2.setIcon(QIcon(QPixmap('11.png')))
        self.btn2.setStyleSheet("QPushButton{color:black}"
                                  "QPushButton:hover{color:red}"
                                  "QPushButton{background-color: #009FCC}"
                                  "QPushButton{border:2px}"
                                  "QPushButton{border-radius:10px}"
                                  "QPushButton{padding:2px 4px}")
        ##点击信号与槽函数进行连接，这一步实现：在控制台输出被点击的按钮

        self.btn2.clicked.connect(lambda :self.whichbtn())

        self.btn2.clicked.connect(self.slotAdd)
        layout.addWidget(self.btn2)
        self.formGroupBox.setLayout(layout)

    def slotAdd(self):
        self.listFile.clear()
        f = open(r'H:\文字识别\cor\image\text1.txt', "r")
        content = f.read()
        pyperclip.copy(content)
        self.listFile.addItem(content)
        QApplication.processEvents()
    def whichbtn(self):
        # 输出被点击的按钮
        self.ocr_clipboard()



    # 识别逻辑
    def get_auth(self):
        apikey = 'ITOQAuZHCipDKPlXpbM2KyW7'
        secret_key = 'ewuoybwn1YfQE6vtvH8UFkaFYf3Soppk'
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s' % (
            apikey, secret_key)
        req = urllib.request.Request(host)
        req.add_header('Content-Type', 'application/json; charset=UTF-8')
        res = urllib.request.urlopen(req)
        content = res.read()
        if (content):
            o = json.loads(content.decode())
            return o['access_token']
        return None
    def ocr_clipboard(self):
        im = ImageGrab.grabclipboard()
        if im is None:
            self.msg_box = QMessageBox(QMessageBox.Warning, "提示", "《没有复制图片，__v_v__》")
            self.msg_box.show()
            return
        print('image size: %sx%s\n' % (im.size[0], im.size[1]))
        mf = io.BytesIO()
        im.save(mf, 'JPEG')
        mf.seek(0)
        buf = mf.read()
        b64 = base64.encodebytes(buf)
        access_token = self.get_auth()
        if access_token is not None:
            url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=%s' % access_token
            data = urllib.parse.urlencode({'image': b64}).encode()
            req = urllib.request.Request(url, method='POST')
            req.add_header('Content-Type', 'application/x-www-form-urlencoded')
            with urllib.request.urlopen(req, data) as p:
                res = p.read().decode('utf-8')
                o = json.loads(res)
                file_write_obj = open(r'H:\文字识别\cor\image\text1.txt', 'w')
                if o['words_result'] is not None:
                    for w in o['words_result']:
                        file_write_obj.writelines(w['words'])
                        file_write_obj.write('\n')
                        print(w['words'])
                    file_write_obj.close()
        else:
            self.msg_box = QMessageBox(QMessageBox.Warning, "错误", "操作超时，请重试！")
            self.msg_box.show()

if __name__ == '__main__':

    file_write_obj = open(r'H:\文字识别\cor\image\text1.txt', 'w')
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(r'H:\文字识别\cor\image\22.png'))
    ex = frame()
    palette = QPalette()
    photo=get_pictrue('https://gitee.com/changbaibai/picture/raw/master/5.png')
    palette.setBrush(QPalette.Background, QBrush(QPixmap(photo)))
    ex.setPalette(palette)
    ex.resize(800,400)
    ex.move(200,40)

    ex.show()
    
    sys.exit(app.exec_())





