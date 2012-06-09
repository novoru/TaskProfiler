#coding:utf-8

'''
Created on 2012/06/09

@author: Noboru
'''

import sys
from PyQt4 import QtCore, QtGui

class StopWatchPanel(QtGui.QWidget):
    """
    ストップウォッチの表示と操作。
    """
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent = parent)
        self.label = QtGui.QLineEdit("")
        self.stopWatch = self.StopWatchWidget()
        self.controllPanel = self.ControllPanel()
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.stopWatch)
        layout.addWidget(self.controllPanel)
        
        self.controllPanel.startButton.clicked.connect(self.stopWatch.startCountDown)
        self.controllPanel.stopButton.clicked.connect(self.stopWatch.stopCountDown)
        self.controllPanel.resetButton.clicked.connect(self.stopWatch.resetCount)
        #self.controllPanel.quitButton.clicked.connect()
        
        self.setLayout(layout)
        
    class ControllPanel(QtGui.QWidget):
        def __init__(self, parent = None):
            QtGui.QWidget.__init__(self, parent = parent)
            
            self.startButton    = QtGui.QPushButton("START")
            self.stopButton     = QtGui.QPushButton("STOP")
            self.resetButton    = QtGui.QPushButton("RESET")
            self.quitButton     = QtGui.QPushButton("QUIT")
            
            layout = QtGui.QHBoxLayout()
            layout.addWidget(self.startButton)
            layout.addWidget(self.stopButton)
            layout.addWidget(self.resetButton)
            #layout.addWidget(self.quitButton)
            self.setLayout(layout)

    class StopWatchWidget(QtGui.QWidget):
        
        INTERVAL    = 1000      #Unit: [ms]
        ONE_HOUR    = 3600      #Unit: [s]
        ONE_MINUTE  = 60        #Unit: [s]
        
        def __init__(self, parent = None):
            QtGui.QWidget.__init__(self, parent = parent)
            
            self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
            self.timer = QtCore.QTimer(parent = self)
            self.timer.setInterval(self.INTERVAL)
            self.timer.timeout.connect(self.doCountDown)
            
            self.lcdNumber = QtGui.QLCDNumber(parent = self)
            self.lcdNumber.setSizePolicy(QtGui.QSizePolicy.Expanding,
                                          QtGui.QSizePolicy.Expanding)
            self.lcdNumber.setFrameStyle(QtGui.QFrame.NoFrame)
            self.lcdNumber.setSegmentStyle(QtGui.QLCDNumber.Flat)
            self.lcdNumber.setDigitCount(10)
            
            layout = QtGui.QVBoxLayout()
            layout.addWidget(self.lcdNumber)
            self.setLayout(layout)
            
            self.resetCount()   
            
        def updateDisplay(self):
            time = self.convert24Hours()
            self.lcdNumber.display(time["hours"] + ":" + time["minutes"] + ":" + time["seconds"])
        
        def resetCount(self):
            self.count = 0
            self.updateDisplay()
    
        def doCountDown(self):
            self.count += 1
            self.updateDisplay()
    
        def startCountDown(self):
            self.timer.start()
        
        def stopCountDown(self):
            self.timer.stop()
    
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
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent = parent)
        
        base = QtGui.QWidget()
        layout = QtGui.QVBoxLayout()
        
        scrollArea = QtGui.QScrollArea()
        
        stopWatchPanel = StopWatchPanel()
        layout.addWidget(stopWatchPanel)
        stopWatchPanel2 = StopWatchPanel()
        layout.addWidget(stopWatchPanel2)
        stopWatchPanel3 = StopWatchPanel()
        layout.addWidget(stopWatchPanel3)
        stopWatchPanel4 = StopWatchPanel()
        layout.addWidget(stopWatchPanel4)
        
        base.setLayout(layout)
        scrollArea.setWidget(base)
        self.setWindowTitle("TaskProfiler")
        self.setCentralWidget(scrollArea)


def main():
    app = QtGui.QApplication(sys.argv)
    
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec_()

if __name__ == "__main__":
    main()