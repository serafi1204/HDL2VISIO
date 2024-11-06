from PyQt5 import QtCore, QtGui, QtWidgets
from lib.interpreter import VerilogInterpreter
import lib.drawing as draw
from lib.debug import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        self.Dialog = Dialog
        Dialog.setObjectName("Verilog2VISIO")
        Dialog.resize(635, 353)
        
        self.body = QtWidgets.QWidget(Dialog)
        self.body.setGeometry(QtCore.QRect(10, 10, 611, 331))
        self.body.setObjectName("body")
        
        self.container = QtWidgets.QHBoxLayout(self.body)
        self.container.setContentsMargins(0, 0, 0, 0)
        self.container.setObjectName("container")
        # open file
        self.fileView = QtWidgets.QVBoxLayout()
        self.fileView.setObjectName("fileView")
        self.buttenOpen = QtWidgets.QPushButton(self.body)
        self.buttenOpen.setObjectName("buttenOpen")
        self.buttenOpen.clicked.connect(self.btn_fun_FileLoad)
        self.fileView.addWidget(self.buttenOpen)
        self.fileList = QtWidgets.QTextBrowser(self.body)
        self.fileList.setObjectName("fileList")
        self.fileView.addWidget(self.fileList)
        self.container.addLayout(self.fileView)
        # read
        self.buttenRead = QtWidgets.QPushButton(self.body)
        self.buttenRead.setObjectName("buttenRead")
        self.container.addWidget(self.buttenRead)
        self.buttenRead.clicked.connect(self.readSourceCode)
        # checkbox
        self.groupbox = QtWidgets.QGroupBox(self.body)
        self.groupbox.setObjectName("groupbox")
        self.moduleView = QtWidgets.QVBoxLayout(self.groupbox)
        self.moduleView.setObjectName("moduleView")
        self.container.addWidget(self.groupbox, 0, QtCore.Qt.AlignTop)
        # draw
        self.buttenDraw = QtWidgets.QPushButton(self.body)
        self.buttenDraw.setObjectName("buttenDraw")
        self.container.addWidget(self.buttenDraw)
        self.buttenDraw.clicked.connect(self.drawing)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
        # vars
        self.files = []
        self.lib = {}
        self.checkBoxModules = []
        self.checkBoxs = []
        self.checkBoxLabels = []
        
    def btn_fun_FileLoad(self):        
        fname=QtWidgets.QFileDialog.getOpenFileNames(self.body,'','','Verilog(*.v)')

        if fname[0]:
            # update files
            for file in fname[0]:
                if (file not in self.files):
                    self.files.append(file)
            
            inner = ''
            for filename in self.files:
                inner += filename.split('/')[-1] + '\n'
            self.fileList.setText(QtCore.QCoreApplication.translate("Dialog", inner))
            
    def readSourceCode(self):
        vi = VerilogInterpreter()
        self.lib = vi.read(self.files)
        
        for module in self.lib:
            self.addCheckBox(module)
    
    def addCheckBox(self, module, deeps = 0):
        key = ' · '
        checkBox = QtWidgets.QCheckBox(self.groupbox)
        checkBox.setObjectName(f'{module.name}()')
        checkBox.setText(QtCore.QCoreApplication.translate("Dialog", key*deeps + f'{module.name}()'))
        self.moduleView.addWidget(checkBox, 0, QtCore.Qt.AlignTop)
        
        if (module.checked == True): checkBox.setCheckState(2)
        self.checkBoxModules.append(module)
        self.checkBoxs.append(checkBox)
        self.checkBoxLabels.append((deeps, f'{module.name}()'))
        
        deeps += 1
        for sub in module.submodule:
            self.addCheckBox(sub, deeps)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.buttenOpen.setText(_translate("Dialog", "open folder or file"))
        self.buttenRead.setText(_translate("Dialog", "Read"))
        self.buttenDraw.setText(_translate("Dialog", "Draw"))
        
    def updateCheckBox(self):
        for i, box in enumerate(self.checkBoxs):
            self.checkBoxModules[i].checked = True if box.checkState()==2 else False
            
    def drawing(self):
        self.updateCheckBox()
        
        for m in self.lib:
            if (m.checked == False): continue
            page = draw.Page.addPage()
            draw.DrawModule(page, m, self.alart)
            page.CenterDrawing()
            
    def alart(self):
        buttonReply = QtWidgets.QMessageBox.information(
            self.body, 'Verilog2VISIO', "Continue?", 
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No )
        if buttonReply == QtWidgets.QMessageBox.Yes:
            return 0
        else:
            return -1
            
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
