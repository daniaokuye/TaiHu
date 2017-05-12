#coding:utf-8

import sys
from PyQt4 import QtGui
from texture import tex


class MyWindow(QtGui.QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.initUI()
     
    def initUI(self):

        self.EWIEdit = QtGui.QLineEdit()
        self.VerticalEdit = QtGui.QLineEdit()
        self.HorizontalEdit = QtGui.QLineEdit()
        
        EWIAction = QtGui.QPushButton('EWI')
        VerticalAction = QtGui.QPushButton('Vertical')
        HorizontalAction = QtGui.QPushButton('Horizontal')
        
        Action1 = QtGui.QPushButton('Angle 270',self)
        Action2 = QtGui.QPushButton('Angle 180',self)
        about= QtGui.QPushButton('about',self)
        
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.EWIEdit, 1, 0)
        grid.addWidget(EWIAction, 1, 1)

        grid.addWidget(self.VerticalEdit, 2, 0)
        grid.addWidget(VerticalAction, 2, 1)

        grid.addWidget(self.HorizontalEdit, 3, 0)
        grid.addWidget(HorizontalAction, 3, 1)

        self.setLayout(grid) 
        
        EWIAction.clicked.connect(self.openImg)
        VerticalAction.clicked.connect(self.openImg)
        HorizontalAction.clicked.connect(self.openImg)
        
        Action1.clicked.connect(self.on_about)
        Action2.clicked.connect(self.on_about)
        about.clicked.connect(self.on_about)

        self.setGeometry(300, 300, 350, 300)
        Action1.move(self.width()*0.15, self.height()*0.85)
        Action2.move(self.width()*0.55, self.height()*0.85)
        about.move(self.width()*0.3, self.height()*0.05)
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle('Horizontal')    
        self.show()

      
    def openImg(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 'd:\\python',"*.tif")
        b=filename.__str__()
        fname=b.encode("utf-8")
        sender=self.sender()
        t=sender.text()
        if t=='EWI':self.EWIEdit.setText(fname)
        elif t=='Vertical':self.VerticalEdit.setText(fname)
        else:self.HorizontalEdit.setText(fname)
        
        
    def on_about(self):
        sender=self.sender()
        t=sender.text()
        ewi=unicode(self.EWIEdit.text().toUtf8(), 'utf-8', 'ignore').encode('utf-8')
        if t=='Angle 270':
            V = unicode(self.VerticalEdit.text().toUtf8(), 'utf-8', 'ignore').encode('utf-8')
            if V==''or ewi =='':QtGui.QMessageBox.about(self, "About", 'please select directional fileter image and EWI')
            print ewi,'\n',V
            texture=tex(V,ewi)
            out=texture.out
            if out:QtGui.QMessageBox.about(self, "About", 'Done : '+out)
            
        elif t=='Angle 180':
            print repr(self.HorizontalEdit.text())
            H= unicode(self.HorizontalEdit.text().toUtf8(), 'utf-8', 'ignore').encode('utf-8')
            if H=='' or ewi =='':QtGui.QMessageBox.about(self, "About", 'please select directional fileter image and EWI')  
            print ewi,'\n',H
            texture=tex(H,ewi,False)
            out=texture.out
            if out:QtGui.QMessageBox.about(self, "About", 'Done : '+out)
            
        else:
            msg = "select Path of image:\n\n\t* EWI:  water index\n\t* Vertical: directional convolution with angle '270' \
                    \n\t* Horizontal:   directional convolution with angle '180'\nexecute with each image:\n \
                    \n\t* Angle 270:execute with EWI and Vertical\n\t* Angle 180:execute with EWI and Horizontal"
            QtGui.QMessageBox.about(self, "About", msg)        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = MyWindow()
    sys.exit(app.exec_())          
        
        
        