from PyQt5.QtWidgets import QWidget, QAction
from PyQt5 import QtGui, QtCore
import sys
import ui_main
import numpy as np
import pyqtgraph
import SWHear
from playsound import playsound

# Action Settings
import configparser
config = configparser.ConfigParser()
config.read('config/action_settings.ini')
DOT = config['ACTION']['DOT']
SEP = config['ACTION']['SEP']
ADD = config['ACTION']['ADD']
SUB = config['ACTION']['SUB']
DIV = config['ACTION']['DIV']
MUL = config['ACTION']['MUL']
SPL = config['ACTION']['SPL']
NPZ = config['ACTION']['NPZ']
MOD = config['ACTION']['MOD']
JSN = config['ACTION']['JSN']
N = '\n'
T = '\t'
TT = '\t\t'
TTT = '\t\t\t'

class AudioFile(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(AudioFile, self).__init__()

        nodeflow_main.createAttribute(node=n, name='Audio_File', preset='String', socket=True, plug=True, dataType='str', dataAttr='')

class AudioFileAction(QAction):
    """Model Create"""
    def __init__(self, attrData, config):
        super(AudioFileAction, self).__init__()

        FILE = attrData.get('Audio_File')
        playsound(FILE)

class ExampleApp(QtGui.QMainWindow, ui_main.Ui_MainWindow):
    def __init__(self, parent=None):
        pyqtgraph.setConfigOption('background', 'w') #before loading widget
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)
        self.grFFT.plotItem.showGrid(True, True, 0.7)
        self.grPCM.plotItem.showGrid(True, True, 0.7)
        self.maxFFT=0
        self.maxPCM=0
        self.ear = SWHear.SWHear()
        self.ear.stream_start()

    def update(self):
        if not self.ear.data is None and not self.ear.fft is None:
            pcmMax=np.max(np.abs(self.ear.data))
            if pcmMax>self.maxPCM:
                self.maxPCM=pcmMax
                self.grPCM.plotItem.setRange(yRange=[-pcmMax,pcmMax])
            if np.max(self.ear.fft)>self.maxFFT:
                self.maxFFT=np.max(np.abs(self.ear.fft))
                self.grFFT.plotItem.setRange(yRange=[0,self.maxFFT])
            self.pbLevel.setValue(1000*pcmMax/self.maxPCM)
            pen=pyqtgraph.mkPen(color='b')
            self.grPCM.plot(self.ear.datax,self.ear.data,
                            pen=pen,clear=True)
            pen=pyqtgraph.mkPen(color='r')
            self.grFFT.plot(self.ear.fftx[:500],self.ear.fft[:500],
                            pen=pen,clear=True)
        QtCore.QTimer.singleShot(1, self.update) # QUICKLY repeat
