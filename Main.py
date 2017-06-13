#coding:utf-8

import sys
from PyQt4 import QtGui
from texture import tex,postProcedure
import time

class MyWindow(QtGui.QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.fname='d:/'
        self.outFile={}
        self.initUI()
        self.pP=postProcedure()
        
        
    def initUI(self):

        self.EWIEdit = QtGui.QLineEdit()
        self.V_0_Edit = QtGui.QLineEdit()
        self.V_1_Edit = QtGui.QLineEdit()
        self.H_0_Edit = QtGui.QLineEdit()
        self.H_1_Edit = QtGui.QLineEdit()
        self.threshold = QtGui.QLineEdit()
        
        EWIAction = QtGui.QPushButton('EWI')
        V_0_Action = QtGui.QPushButton('270')
        H_0_Action = QtGui.QPushButton('180')
        V_1_Action = QtGui.QPushButton('90')
        H_1_Action = QtGui.QPushButton('0')
        self.ok_Action = QtGui.QPushButton('threshold ok')
        self.progressBar=QtGui.QProgressBar() 
        
        #Action1 = QtGui.QPushButton('Angle 270',self)
        #Action2 = QtGui.QPushButton('Angle 180',self)
        about= QtGui.QPushButton('about',self)
        execu = QtGui.QPushButton('execu',self)
        
        grid = QtGui.QGridLayout()
        grid.setSpacing(5)

        grid.addWidget(self.EWIEdit, 1, 0)
        grid.addWidget(EWIAction, 1, 1)

        grid.addWidget(self.V_0_Edit, 2, 0)
        grid.addWidget(V_0_Action, 2, 1)
        
        grid.addWidget(self.V_1_Edit, 3, 0)
        grid.addWidget(V_1_Action, 3, 1)
        
        grid.addWidget(self.H_0_Edit, 4, 0)
        grid.addWidget(H_0_Action, 4, 1)
        
        grid.addWidget(self.H_1_Edit, 5, 0)
        grid.addWidget(H_1_Action, 5, 1)
        
        grid.addWidget(self.threshold, 6, 0)
        grid.addWidget(self.ok_Action, 6, 1)
        
        grid.addWidget(self.progressBar,7,0,1,2)
        grid.addWidget(execu,8,0)
        grid.addWidget(about,8,1)
        self.setLayout(grid) 
        
        self.progressBar.setMinimum(0)    
        self.progressBar.setMaximum(4) 
        
        EWIAction.clicked.connect(self.openImg)
        V_0_Action.clicked.connect(self.openImg)
        H_0_Action.clicked.connect(self.openImg)
        V_1_Action.clicked.connect(self.openImg)
        H_1_Action.clicked.connect(self.openImg)
        
        # Action1.clicked.connect(self.on_about)
        # Action2.clicked.connect(self.on_about)
        about.clicked.connect(self.on_about)
        execu.clicked.connect(self.execute)

        self.setGeometry(300, 300, 370, 400)
        # Action1.move(self.width()*0.15, self.height()*0.85)
        # Action2.move(self.width()*0.55, self.height()*0.85)
        #execu.move(self.width()*0.55, self.height()*0.9)
        #about.move(self.width()*0.15, self.height()*0.9)
        self.setFixedSize(self.width(), self.height())
        
        self.setWindowTitle('method of remove')    
        self.show()

      
    def openImg(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file', self.fname,"*.tif")
        b=filename.__str__()
        self.fname=b.encode("utf-8")
        sender=self.sender()
        t=sender.text()
        if t=='EWI':self.EWIEdit.setText(self.fname)
        elif t=='270':self.V_0_Edit.setText(self.fname)
        elif t=='90':self.V_1_Edit.setText(self.fname)
        elif t=='0':self.H_1_Edit.setText(self.fname)
        else:self.H_0_Edit.setText(self.fname)
        
    def on_about(self):
        msg = "select Path of image:\n\n\t* EWI:  water index\n\t* Vertical: directional convolution with angle '270' \
                \n\t* Horizontal:   directional convolution with angle '180'\nexecute with each image:\n \
                \n\t* Angle 270:execute with EWI and Vertical\n\t* Angle 180:execute with EWI and Horizontal"
        QtGui.QMessageBox.about(self, "About", msg)

    def execute(self):
        dataFile={}
        dataFile['ewi']=unicode(self.EWIEdit.text().toUtf8(), 'utf-8', 'ignore').encode('utf-8')
        dataFile[270] = unicode(self.V_0_Edit.text().toUtf8(), 'utf-8', 'ignore').encode('utf-8')
        dataFile[180] = unicode(self.H_0_Edit.text().toUtf8(), 'utf-8', 'ignore').encode('utf-8')
        dataFile[90] = unicode(self.V_1_Edit.text().toUtf8(), 'utf-8', 'ignore').encode('utf-8')
        dataFile[0] = unicode(self.H_1_Edit.text().toUtf8(), 'utf-8', 'ignore').encode('utf-8')
        
        for v in dataFile.values():
            if v=='':
                QtGui.QMessageBox.about(self, "Warning", 'please select all directional fileter images and EWI')
                return 0
        QtGui.QMessageBox.about(self, "Assert", 'Please make sure all images properly selected ! ')        
        
        ewi=dataFile.pop('ewi')
        out=[]#save temp image resptively
             
        while(len(dataFile)):
            dir,file=dataFile.popitem()
            #texture=tex(file,ewi,dir)
            #out.append(texture.out)
            self.timeBar(4-len(dataFile))
        #self.pP.finalImage(out)
        self.ok_Action.clicked.connect(self.on_threshold)        
    
    def on_threshold(self):
        tsh=unicode(self.threshold.text().toUtf8(), 'utf-8', 'ignore').encode('utf-8')
        try:
            tsh=float(tsh)
        except:
            QtGui.QMessageBox.about(self, "waring", 'Please input a float number ! ')
            return 0
        print tsh
        self.pP.thres(tsh)
        
    def timeBar(self,step):
        self.progressBar.setValue(step)
        
        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = MyWindow()
    sys.exit(app.exec_())          
        
        
        