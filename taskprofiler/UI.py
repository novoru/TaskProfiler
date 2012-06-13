#coding:utf-8

'''
Created on 2012/06/09
@author:        Noboru
Description:    Task Profiler User Interface Module using PyQt4
'''

import sys
from PyQt4 import QtCore, QtGui

class StopWatchPanel(QtGui.QWidget):
    """
    ストップウォッチの表示と操作。
    """
    
    DEFAULT_SIZE = QtCore.QSize(270, 170)
    DEFAULT_TEXT = ""
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent = parent)
        self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.setFixedSize(self.DEFAULT_SIZE)
        self.label = QtGui.QLineEdit(self.DEFAULT_TEXT)
        self.stopWatch = self.StopWatchWidget()
        self.controllPanel = self.ControllPanel()
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.stopWatch)
        layout.addWidget(self.controllPanel)
        
        self.controllPanel.startButton.clicked.connect(self.stopWatch.startCountUp)
        self.controllPanel.stopButton.clicked.connect(self.stopWatch.stopCountUp)
        self.controllPanel.resetButton.clicked.connect(self.stopWatch.resetCount)
                
        self.setLayout(layout)
        
    class ControllPanel(QtGui.QWidget):
        
        DEFAULT_SIZE = QtCore.QSize(270,100)
        remove_function = None
        
        def __init__(self, parent = None):
            QtGui.QWidget.__init__(self, parent = parent)
            
            self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
            self.setFixedSize(self.DEFAULT_SIZE)
            
            self.startButton    = QtGui.QPushButton("START")
            self.stopButton     = QtGui.QPushButton("STOP")
            self.resetButton    = QtGui.QPushButton("RESET")
            self.removeButton   = QtGui.QPushButton("REMOVE")
            self.removeButton.clicked.connect(self.remove)
                   
            layout = QtGui.QHBoxLayout()
            layout.addWidget(self.startButton)
            layout.addWidget(self.stopButton)
            layout.addWidget(self.resetButton)
            layout.addWidget(self.removeButton)
            
            self.setLayout(layout)      

        def remove(self, event, _function = None):
            if _function:
                self.remove_function = _function
            
            if self.remove_function:
                self.remove_function(self.parent())
            

    class StopWatchWidget(QtGui.QWidget):
        
        INTERVAL    = 1000      #Unit: [ms]
        ONE_HOUR    = 3600      #Unit: [s]
        ONE_MINUTE  = 60        #Unit: [s]
        
        DEFAULT_SIZE = QtCore.QSize(250,50)
        LCD_SIZE = QtCore.QSize(200,200)
        
        def __init__(self, parent = None):
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
            
            self.resetCount()   
            self.stopCountUp()
            
        def updateDisplay(self):
            time = self.convert24Hours()
            self.lcdNumber.display(time["hours"] + ":" + time["minutes"] + ":" + time["seconds"])
                    
        def resetCount(self):
            self.count = 0
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

class MainWindow(QtGui.QMainWindow):
    
    TITLE = "TaskProfiler"
    DEFAULT_GEOMETRY = QtCore.QRect(10,30,330,800)
    
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent = parent, flags = QtCore.Qt.WindowStaysOnTopHint)
        self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.setGeometry(self.DEFAULT_GEOMETRY)
        
        self.mainPanel = QtGui.QWidget()
        self.mainPanelLayout = QtGui.QVBoxLayout()
        self.mainPanel.setLayout(self.mainPanelLayout)
                
        self.stopWatchArea = self.StopWatchArea(self)
        self.mainPanelLayout.addWidget(self.stopWatchArea)
        
        self.controllPanel = self.ControllPanel(self)
        self.mainPanelLayout.addWidget(self.controllPanel)
        
        self.controllPanel.addButton.clicked.connect(self.stopWatchArea.addStopWatch)
        #self.controllPanel.removeButton.clicked.connect(self.stopWatchArea.removeBottomStopWatch)
        
        self.setWindowTitle(self.TITLE)
        self.setCentralWidget(self.mainPanel)
        
        self.stopWatchArea.addStopWatch()
        
        #デバッグ用のキーイベント
        self.keyPressEvent = self.debugKey
        
    def debugKey(self, event):
        key = event.text()
        
        if key == 's':
            print "Stop"
            self.stopWatchArea.stopCountUpAllStopWatches()
        
    class StopWatchArea(QtGui.QScrollArea):
        
        stopWatchPanels = []
        
        def __init__(self, parent = None):
            QtGui.QScrollArea.__init__(self, parent = parent)
            
            self.base = QtGui.QWidget()
            self.base.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
                   
            self.layout = QtGui.QVBoxLayout(self)
            self.layout.setSizeConstraint(QtGui.QLayout.SetFixedSize)       #レイアウトに追加するウィジェットのサイズを固定にする。   
            
            self.base.setLayout(self.layout)
            self.setWidget(self.base)
        
        def addStopWatch(self):
            stopWatchPanel = StopWatchPanel(self)
            stopWatchPanel.controllPanel.remove(None, self.removeStopWatch)
            self.stopWatchPanels.append(stopWatchPanel)
            self.layout.addWidget(self.stopWatchPanels[-1])
        
        def stopCountUpAll(self):
            [stopWatchPanel.stopWatch.stopCountUp() for stopWatchPanel in self.stopWatchPanels]
        
        def stopCountUpWithout(self, _stopWatch):
            for stopWatchPanel in self.stopWatchPanels:
                stopWatch = stopWatchPanel.stopWatch
                if not(stopWatch == _stopWatch):
                    stopWatch.stopCountUp()
        
        def removeBottomStopWatch(self):
            print "hoge"
            if self.stopWatchPanels:
                stopWatchPanel = self.stopWatchPanels.pop()
                stopWatchPanel.stopWatch.destructor()
                self.layout.removeWidget(stopWatchPanel)
        
        def removeStopWatch(self, _stopWatch):
            if self.stopWatchPanels:
                for i, stopWatch in enumerate(self.stopWatchPanels):
                    if stopWatch == _stopWatch:
                        removeStopWatch = self.stopWatchPanels.pop(i)
                        removeStopWatch.stopWatch.destructor()
                        self.layout.removeWidget(removeStopWatch)
            
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


def main():
    app = QtGui.QApplication(sys.argv)
    
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec_()

if __name__ == "__main__":
    main()