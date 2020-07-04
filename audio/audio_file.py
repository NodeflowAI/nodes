from PyQt5.QtWidgets import QWidget, QAction

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