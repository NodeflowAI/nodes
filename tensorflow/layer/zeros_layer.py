from PyQt5.QtWidgets import QWidget, QAction

# Action Settings
import configparser
config = configparser.ConfigParser()
config.read('config/action_settings.ini')
SEP = config['ACTION']['SEP']
ADD = config['ACTION']['ADD']
SUB = config['ACTION']['SUB']
DIV = config['ACTION']['DIV']
MUL = config['ACTION']['MUL']

class ZerosLayer(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(ZerosLayer, self).__init__()

        NAME = 'Zeros'
        KERNAL_REGULARIZER = None
        BIAS_REGULARIZER = None
        ACTIVITY_REGULARIZER = None
        KERNAL_CONSTRAINT = None
        BIAS_CONSTRAINT = None
        INBOUND_NODES = [[[nn, 0, 0, {}]]]

        nodeflow_main.createAttribute(node=n, name='Zeros', preset='String', socket=True, plug=True, dataType='str', dataAttr='')
        nodeflow_main.createAttribute(node=n, name='kernel_regularizer', preset='String', socket=True, plug=True, dataType='str', dataAttr='null')
        nodeflow_main.createAttribute(node=n, name='bias_regularizer', preset='String', socket=True, plug=True, dataType='str', dataAttr='null')
        nodeflow_main.createAttribute(node=n, name='activity_regularizer', preset='String', socket=True, plug=True, dataType='str', dataAttr='null')
        nodeflow_main.createAttribute(node=n, name='kernel_constraint', preset='String', socket=True, plug=True, dataType='str', dataAttr='null')
        nodeflow_main.createAttribute(node=n, name='bias_constraint', preset='String', socket=True, plug=True, dataType='str', dataAttr='null')
        nodeflow_main.createAttribute(node=n, name='bias_constraint', preset='String', socket=True, plug=True, dataType='str', dataExpr='[[[inbound, 0, 0, {}]]]')
        nodeflow_main.createAttribute(node=n, name='kernel_initializer', preset='String', socket=True, plug=True, dataType='str', dataAttr='')

class ZerosLayerAction(QAction):
    """Model Train"""

    def __init__(self, attrData, config):
        super(ZerosLayerAction, self).__init__()

        print(attrData)