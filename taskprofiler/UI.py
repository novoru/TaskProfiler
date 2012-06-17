#coding:utf-8

'''
Created on 2012/06/09
@author:        Noboru
Description:    Task Profiler User Interface Module using PyQt4
'''

import csv
import pickle
import sys
from PyQt4 import QtCore, QtGui

class StopWatchPanel(QtGui.QWidget):
    """
    ストップウォッチの表示と操作。
    """
    
    DEFAULT_SIZE = QtCore.QSize(270, 170)
    
    def __init__(self, parent = None, _labelText = "", _count = 0):
        QtGui.QWidget.__init__(self, parent = parent)
        self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.setFixedSize(self.DEFAULT_SIZE)
        self.label = QtGui.QLineEdit(QtCore.QString(_labelText))
        self.stopWatch = self.StopWatchWidget(self, _count)
        self.controllPanel = self.ControllPanel()
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.stopWatch)
        layout.addWidget(self.controllPanel)
        
        self.controllPanel.startButton.clicked.connect(self.stopWatch.startCountUp)
        self.controllPanel.stopButton.clicked.connect(self.stopWatch.stopCountUp)
        self.controllPanel.resetButton.clicked.connect(self.stopWatch.resetCount)
                
        self.setLayout(layout)
    
    def getState(self):
        state = self.stopWatch.getState()
        state["labelText"] = self.label.text()
        
        return state
        
    class ControllPanel(QtGui.QWidget):
        
        DEFAULT_SIZE    = QtCore.QSize(270,100)
        removeFunction  = None
        stopFunction    = None
        
        def __init__(self, parent = None):
            QtGui.QWidget.__init__(self, parent = parent)
            
            self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
            self.setFixedSize(self.DEFAULT_SIZE)
            
            self.startButton    = QtGui.QPushButton("START")
            self.stopButton     = QtGui.QPushButton("STOP")
            self.resetButton    = QtGui.QPushButton("RESET")
            self.removeButton   = QtGui.QPushButton("REMOVE")
            self.startButton.clicked.connect(self.stopOtherStopWatch)
            self.removeButton.clicked.connect(self.remove)
                   
            layout = QtGui.QHBoxLayout()
            layout.addWidget(self.startButton)
            layout.addWidget(self.stopButton)
            layout.addWidget(self.resetButton)
            layout.addWidget(self.removeButton)
            
            self.setLayout(layout)      

        def remove(self, event, _function = None):
            if self.removeFunction:
                self.removeFunction(self.parent())
                
            if _function:
                self.removeFunction = _function
        
        def stopOtherStopWatch(self, event, _function = None):
            if self.stopFunction:
                self.stopFunction(self.parent())
                
            if _function:
                self.stopFunction = _function
            
    class StopWatchWidget(QtGui.QWidget):
        
        INTERVAL    = 1000      #Unit: [ms]
        ONE_HOUR    = 3600      #Unit: [s]
        ONE_MINUTE  = 60        #Unit: [s]
        
        DEFAULT_SIZE    = QtCore.QSize(250,50)
        LCD_SIZE        = QtCore.QSize(200,200)
        
        count       = 0
        
        def __init__(self, parent = None, _count = 0):
            QtGui.QWidget.__init__(self, parent = parent)
            
            self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
            self.setFixedSize(self.DEFAULT_SIZE)
            self.timer = QtCore.QTimer(parent = self)
            self.timer.setInterval(self.INTERVAL)
            self.timer.timeout.connect(self.doCountUp)
            
            self.lcdNumber = QtGui.QLCDNumber(parent = self)
            self.lcdNumber.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
            #self.lcdNumber.setFixedSize(self.LCD_SIZE)
            #self.lcdNumber.setAutoFillBackground(False)
            self.lcdNumber.setSizePolicy(QtGui.QSizePolicy.Expanding,
                                          QtGui.QSizePolicy.Expanding)
            self.lcdNumber.setFrameStyle(QtGui.QFrame.NoFrame)
            self.lcdNumber.setSegmentStyle(QtGui.QLCDNumber.Flat)
            self.lcdNumber.setDigitCount(10)
            
            layout = QtGui.QVBoxLayout()
            layout.addWidget(self.lcdNumber)
            self.setLayout(layout)
            
            self.resetCount(_count)
            self.stopCountUp()
            
        def updateDisplay(self):
            time = self.convert24Hours()
            self.lcdNumber.display(time["hours"] + ":" + time["minutes"] + ":" + time["seconds"])
                    
        def resetCount(self, _count = 0):
            self.count = _count
            self.updateDisplay()
    
        def doCountUp(self):
            self.count += 1
            self.updateDisplay()
    
        def startCountUp(self):
            self.timer.start()
            self.lcdNumber.setFrameStyle(QtGui.QLCDNumber.Filled)
        
        def stopCountUp(self):
            self.timer.stop()
            self.lcdNumber.setFrameStyle(QtGui.QLCDNumber.NoFrame)
            
        def destructor(self):
            self.resetCount()
            self.stopCountUp()
            self.lcdNumber.display("")
    
        def convert24Hours(self):
            hours    = "00"
            minutes  = "00"
            seconds  = "00"
            
            mod     = 0
            
            PADDING_WIDTH = 2
            
            if self.count >= self.ONE_HOUR:
                hours   = str(self.count/self.ONE_HOUR).rjust(PADDING_WIDTH, "0")
                mod     = self.count%self.ONE_HOUR
                minutes = str(mod/self.ONE_MINUTE).rjust(PADDING_WIDTH, "0")
                seconds = str(mod%self.ONE_MINUTE).rjust(PADDING_WIDTH, "0")
            else:
                minutes = str(self.count/self.ONE_MINUTE).rjust(PADDING_WIDTH, "0")
                seconds = str(self.count%self.ONE_MINUTE).rjust(PADDING_WIDTH, "0")
                
            return {"hours":hours, "minutes":minutes, "seconds":seconds}

        def getState(self):
            return {"count":self.count}

class MainWindow(QtGui.QMainWindow):
    
    TITLE = "TaskProfiler"
    DEFAULT_GEOMETRY = QtCore.QRect(10,30,330,530)
    
    def __init__(self, parent = None):
        #QtGui.QMainWindow.__init__(self, parent = parent, flags = QtCore.Qt.WindowStaysOnTopHint)
        QtGui.QMainWindow.__init__(self, parent = parent)
        self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.setGeometry(self.DEFAULT_GEOMETRY)
        
        self.menuBar = self.MenuBar(self)
        self.setMenuBar(self.menuBar)
                
        self.mainPanel = QtGui.QWidget()
        self.mainPanelLayout = QtGui.QVBoxLayout()
        self.mainPanel.setLayout(self.mainPanelLayout)
                
        self.stopWatchArea = self.StopWatchArea(self)
        self.mainPanelLayout.addWidget(self.stopWatchArea)
        
        self.controllPanel = self.ControllPanel(self)
        self.mainPanelLayout.addWidget(self.controllPanel)
        
        #self.controllPanel.removeButton.clicked.connect(self.stopWatchArea.removeBottomStopWatch)
        
        self.setWindowTitle(self.TITLE)
        self.setCentralWidget(self.mainPanel)
        
        self.connect()
        
        self.stopWatchArea.addStopWatch()
        
        #デバッグ用のキーイベント
        self.keyPressEvent = self.debugKey
    
    def save(self, filePath):

        try:
            saveFile = open(filePath, 'w')
        except:
            return 
        
        state = self.stopWatchArea.getState()
        
        pickle.dump(state, saveFile)
        saveFile.close()
    
    def overwriteSave(self):
        pass
    
    def saveAs(self):
        self.save(QtGui.QFileDialog.getSaveFileName(self, caption = "Save File"))
        
    def load(self, filePath):
        
        loadFile = open(filePath, 'r')
        
        self.disConnet()
        self.stopWatchArea.removeAllStopWatch()
        self.mainPanelLayout.removeWidget(self.stopWatchArea)
        self.mainPanelLayout.removeWidget(self.controllPanel)
        
        self.stopWatchArea = None
        self.controllPanel = None
        
        state = pickle.load(loadFile)
                
        self.stopWatchArea = self.StopWatchArea(self, state)
        self.mainPanelLayout.addWidget(self.stopWatchArea)
        self.controllPanel = self.ControllPanel(self)
        self.mainPanelLayout.addWidget(self.controllPanel)
        self.connect()
    
    
    def openFile(self):
        self.load(QtGui.QFileDialog.getOpenFileName(self, caption = "Open File"))
    
    def new(self):
        
        msgBox = QtGui.QMessageBox()
        msgBox.setWindowTitle("Save")
        msgBox.setText("Do you want to save your changes?")
        msgBox.setStandardButtons(QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard | QtGui.QMessageBox.Cancel)
        msgBox.setDefaultButton(QtGui.QMessageBox.Cancel)
        msgBox.setIcon(QtGui.QMessageBox.Question)
        
        msg = msgBox.exec_()
        
        if msg == QtGui.QMessageBox.Save:
            self.saveAs()
        elif msg == QtGui.QMessageBox.Cancel:
            return 
        
        self.disConnet()
        self.stopWatchArea.removeAllStopWatch()
        self.mainPanelLayout.removeWidget(self.stopWatchArea)
        self.mainPanelLayout.removeWidget(self.controllPanel)
        
        self.stopWatchArea = None
        self.controllPanel = None
        
        self.stopWatchArea = self.StopWatchArea(self)
        self.mainPanelLayout.addWidget(self.stopWatchArea)
        self.controllPanel = self.ControllPanel(self)
        self.mainPanelLayout.addWidget(self.controllPanel)
        self.connect()
    
    def switchSynchronizeSetting(self):
        self.stopWatchArea.settings["synchronizeAllStopWatch"] = self.menuBar.editMenu.synchronizeStopWatchAction.isChecked()
        #self.menuBar.editMenu.synchronizeStopWatchAction.setChecked(self.menuBar.editMenu.synchronizeStopWatchAction.isChecked())
    
    def switchActive(self):
        BIT_MASK = 0xffffffff
        if self.menuBar.windowMenu.switchActiveWindowAction.isChecked():
            self.setWindowFlags(QtCore.Qt.WindowFlags(self.windowFlags().__int__() | (QtCore.Qt.WindowStaysOnTopHint.__int__())))
        else:
            self.setWindowFlags(QtCore.Qt.WindowFlags(self.windowFlags().__int__() & (BIT_MASK ^ QtCore.Qt.WindowStaysOnTopHint.__int__())))
        self.show()
    
    def export(self):
        filePath = QtGui.QFileDialog.getSaveFileName(self, caption = "Export CSV File")
        
        if not filePath:
            return
                
        try:
            exportFile = open(filePath,'w')
        except:
            msgBox = QtGui.QMessageBox()
            msgBox.setWindowTitle("Error")
            msgBox.setText("Export CSV Failed.")
            msgBox.setIcon(QtGui.QMessageBox.Warning)
            msgBox.exec_()
            return
        
        states   = self.stopWatchArea.getState().values()
        
        if not states:
            writer = csv.DictWriter(exportFile, "", extrasaction='ignore')
            writer.writerows("")
            exportFile.close()
            return 
        
        rows    = []
        parameters  = self.stopWatchArea.getState().values()[0].keys()
        header      = dict((val, val) for val in parameters)

        rows.append(header)
        [rows.append(state) for state in states]
        
        print rows
        
        writer = csv.DictWriter(exportFile, parameters, extrasaction='ignore')
        writer.writerows(rows)
        
        exportFile.close()

    def connect(self):
        self.controllPanel.addButton.clicked.connect(self.stopWatchArea.addStopWatch)
        self.menuBar.fileMenu.newFileAction.triggered.connect(self.new)
        self.menuBar.fileMenu.saveAsFileAction.triggered.connect(self.saveAs)
        self.menuBar.fileMenu.openFileAction.triggered.connect(self.openFile)
        self.menuBar.fileMenu.exportFileAction.triggered.connect(self.export)
        self.menuBar.editMenu.addStopWatchAction.triggered.connect(self.stopWatchArea.addStopWatch)
        self.menuBar.editMenu.removeStopWatchAction.triggered.connect(self.stopWatchArea.removeBottomStopWatch)
        self.menuBar.editMenu.synchronizeStopWatchAction.triggered.connect(self.switchSynchronizeSetting)
        self.menuBar.windowMenu.switchActiveWindowAction.triggered.connect(self.switchActive)
        
    def disConnet(self):
        self.controllPanel.addButton.clicked.disconnect(self.stopWatchArea.addStopWatch)
        self.menuBar.fileMenu.newFileAction.triggered.disconnect(self.new)
        self.menuBar.fileMenu.saveAsFileAction.triggered.disconnect(self.saveAs)
        self.menuBar.fileMenu.openFileAction.triggered.disconnect(self.openFile)
        self.menuBar.fileMenu.exportFileAction.triggered.disconnect(self.export)
        self.menuBar.editMenu.addStopWatchAction.triggered.disconnect(self.stopWatchArea.addStopWatch)
        self.menuBar.editMenu.removeStopWatchAction.triggered.disconnect(self.stopWatchArea.removeBottomStopWatch)
        self.menuBar.editMenu.synchronizeStopWatchAction.triggered.disconnect(self.switchSynchronizeSetting)
        self.menuBar.windowMenu.switchActiveWindowAction.triggered.disconnect(self.switchActive)
        
    
    def debugKey(self, event):
        key = event.text()
    
        if key == 'l':
            print "Load"
            self.load()
        if key == 'n':
            print "New"
            self.new()
                
    class StopWatchArea(QtGui.QScrollArea):
        
        stopWatchPanels = []
        SETTINGS_KEYS    = ["synchronizeAllStopWatch"]
        settings        = {key:"" for key in SETTINGS_KEYS}
        
        def __init__(self, parent = None, _state = None):
            QtGui.QScrollArea.__init__(self, parent = parent)
            
            self.base = QtGui.QWidget()
            self.base.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
                   
            self.layout = QtGui.QVBoxLayout(self)
            self.layout.setSizeConstraint(QtGui.QLayout.SetFixedSize)       #レイアウトに追加するウィジェットのサイズを固定にする。   
            
            self.base.setLayout(self.layout)
            self.setWidget(self.base)
            
            if _state:
                for key in sorted(_state.keys()):
                    self.addStopWatch(None, _state[key]["labelText"], _state[key]["count"])
        
        def addStopWatch(self, event = None, _labelText = "",  _count = 0):
            stopWatchPanel = StopWatchPanel(self, _labelText, _count)
            stopWatchPanel.controllPanel.remove(None, self.removeStopWatch)
            stopWatchPanel.controllPanel.stopOtherStopWatch(None, self.stopCountUpWithout)
            self.stopWatchPanels.append(stopWatchPanel)
            self.layout.addWidget(self.stopWatchPanels[-1])
                    
        def stopCountUpAll(self):
            [stopWatchPanel.stopWatch.stopCountUp() for stopWatchPanel in self.stopWatchPanels]
        
        def stopCountUpWithout(self, _stopWatch):
            if self.settings["synchronizeAllStopWatch"]:
                for stopWatchPanel in self.stopWatchPanels:
                    stopWatch = stopWatchPanel.stopWatch
                    if not(stopWatch == _stopWatch):
                        stopWatch.stopCountUp()
            
        def removeBottomStopWatch(self):
            if self.stopWatchPanels:
                stopWatchPanel = self.stopWatchPanels.pop()
                stopWatchPanel.stopWatch.destructor()
                self.layout.removeWidget(stopWatchPanel)
        
        def removeStopWatch(self, _stopWatch):
            for i, stopWatch in enumerate(self.stopWatchPanels):
                if stopWatch == _stopWatch:
                    removeStopWatch = self.stopWatchPanels.pop(i)
                    removeStopWatch.stopWatch.destructor()
                    self.layout.removeWidget(removeStopWatch)
                            
        def removeAllStopWatch(self):
            for i in range(len((self.stopWatchPanels))-1, -1, -1):
                removeStopWatch = self.stopWatchPanels.pop(i)
                removeStopWatch.stopWatch.destructor()
                self.layout.removeWidget(removeStopWatch)
        
        def getState(self):
            state = {}
            for i, stopWatchPanel in enumerate(self.stopWatchPanels):
                state[i] = stopWatchPanel.getState()
            
            return state
            
    class ControllPanel(QtGui.QWidget):
        def __init__(self, parent = None):
            QtGui.QWidget.__init__(self, parent = parent)
            
            self.layout = QtGui.QHBoxLayout()
            self.addButton = QtGui.QPushButton("Add")
            self.addButton.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
            self.layout.addWidget(self.addButton)
            
            """
            self.removeButton = QtGui.QPushButton("Remove")
            self.removeButton.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
            self.layout.addWidget(self.removeButton)
            """
            
            self.setLayout(self.layout)
            
    class MenuBar(QtGui.QMenuBar):
        
        def __init__(self, parent = None):
            QtGui.QMenuBar.__init__(self, parent = parent)
            
            self.fileMenu = self.FileMenu(self)
            self.addMenu(self.fileMenu)
            
            self.editMenu = self.EditMenu(self)
            self.addMenu(self.editMenu)            

            self.windowMenu = self.WindowMenu(self)
            self.addMenu(self.windowMenu)   
            
        class FileMenu(QtGui.QMenu):
            TITLE = "File"
            
            def __init__(self, parent = None):
                QtGui.QMenu.__init__(self, self.TITLE, parent = parent)

                self.newFileAction = QtGui.QAction("New", self)
                self.newFileAction.setShortcut("Alt+Shift+N")
                self.addAction(self.newFileAction)
                
                self.openFileAction = QtGui.QAction("Open File...", self)
                self.openFileAction.setShortcut("Ctrl+O")
                self.addAction(self.openFileAction)
                
                self.addSeparator()
    
                self.saveAsFileAction = QtGui.QAction("Save As...", self)
                self.saveAsFileAction.setShortcut("Ctrl+Shift+S")
                self.addAction(self.saveAsFileAction)
                
                self.addSeparator()
    
                self.exportFileAction = QtGui.QAction("Export...", self)
                self.exportFileAction.setShortcut("Ctrl+E")
                self.addAction(self.exportFileAction)
                
                self.addSeparator()
                            
                self.exitAction = QtGui.QAction("Exit", self)
                self.exitAction.setShortcut("Ctrl+Q")
                self.exitAction.setStatusTip("Exit application")
                self.exitAction.triggered.connect(QtGui.qApp.exit)
                self.addAction(self.exitAction)

        class EditMenu(QtGui.QMenu):
            TITLE = "Edit"
            
            def __init__(self, parent = None):
                QtGui.QMenu.__init__(self, self.TITLE, parent = parent)
                
                self.addStopWatchAction = QtGui.QAction("Add StopWatch", self)
                self.addStopWatchAction.setShortcut("Ctrl+N")
                self.addAction(self.addStopWatchAction)
                
                self.removeStopWatchAction = QtGui.QAction("Remove Bottom StopWatch", self)
                self.removeStopWatchAction.setShortcut("Ctrl+Shift+D")
                self.addAction(self.removeStopWatchAction)
                
                self.addSeparator()
                
                self.synchronizeStopWatchAction = QtGui.QAction("Synchronize All StopWatch", self)
                #self.settingAction.setShortcut("")
                self.synchronizeStopWatchAction.setCheckable(True)
                self.addAction(self.synchronizeStopWatchAction)

        class WindowMenu(QtGui.QMenu):
            TITLE = "Window"
            
            def __init__(self, parent = None):
                QtGui.QMenu.__init__(self, self.TITLE, parent = parent)
                
                self.switchActiveWindowAction = QtGui.QAction("Always TopLevel Window", self)
                self.switchActiveWindowAction.setCheckable(True)
                self.addAction(self.switchActiveWindowAction)


def main():
    app = QtGui.QApplication(sys.argv)
    
    mainWindow = MainWindow()
    mainWindow.show()
    
    app.exec_()

if __name__ == "__main__":
    main()