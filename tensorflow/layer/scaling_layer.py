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
N = '\n'
T = '\t'
TT = '\t\t'
TTT = '\t\t\t'

class ScalingLayer(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(ScalingLayer, self).__init__()

        NAME = 'VarianceScaling'
        SCALE = 1.0
        MODE = 'fan_avg'
        DISTROBUTION = 'uniform'
        SEED = None

        nodeflow_main.createAttribute(node=n, name='Model', preset='String', socket=True, plug=True, dataType='str', dataAttr='')
        nodeflow_main.createAttribute(node=n, name='VarianceScaling', preset='String', socket=True, plug=True, dataType='str', dataAttr='')
        nodeflow_main.createAttribute(node=n, name='scale', preset='Float', socket=True, plug=True, dataType='flt', dataAttr=SCALE)
        nodeflow_main.createAttribute(node=n, name='mode', preset='String', socket=True, plug=True, dataType='str', dataAttr='fan_avg')
        nodeflow_main.createAttribute(node=n, name='distribution', preset='String', socket=True, plug=True, dataType='str', dataAttr='uniform')
        nodeflow_main.createAttribute(node=n, name='seed', preset='String', socket=True, plug=True, dataType='str', dataAttr='None')
        nodeflow_main.createAttribute(node=n, name='bias_initializer', preset='String', socket=True, plug=True, dataType='str', dataAttr='')

class ScalingLayerAction(QAction):
    """Model Train"""
    def __init__(self, attrData, config):
        super(ScalingLayerAction, self).__init__()