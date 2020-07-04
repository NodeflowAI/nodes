from PyQt5.QtWidgets import QWidget, QAction

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
CSV = config['ACTION']['CSV']

N = '\n'
T = '\t'
TT = '\t\t'
TTT = '\t\t\t'

class FacelabTrain(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(FacelabTrain, self).__init__()

        nodeflow_main.createAttribute(node=n, name='Default', preset='String', socket=True, plug=True, dataType='str', dataAttr='')

class FacelabTrainAction(QAction):
    """Model Create"""
    def __init__(self, attrData, config):
        super(FacelabTrainAction, self).__init__()