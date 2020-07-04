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

class Conv2dLayer(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(Conv2dLayer, self).__init__()

        NAME = 'conv'
        TRAINABLE = True
        DTYPE = 'float32'
        FILTERS = 64
        KERNEL_SIZE = [3, 3]
        STRIDES = [1, 1]
        PADDING = 'same'
        DATA_FORMAT = 'channels_last'
        DILATION_RATE = [1, 1]
        ACTIVATION = 'relu'
        USE_BIAS = True
        KERNEL_INITIALIZER = None

        nodeflow_main.createAttribute(node=n, name='conv', preset='String', socket=True, plug=True, dataType='str', dataAttr='')
        nodeflow_main.createAttribute(node=n, name='trainable', preset='Bool', socket=True, plug=True, dataType='bool', dataAttr='True')
        nodeflow_main.createAttribute(node=n, name='dtype', preset='Float', socket=True, plug=True, dataType='str', dataAttr='float32')
        nodeflow_main.createAttribute(node=n, name='filters', preset='Integer', socket=True, plug=True, dataType='int', dataAttr='64')
        nodeflow_main.createAttribute(node=n, name='kernel', preset='Integer', socket=True, plug=True, dataType='int', dataAttr='3')
        nodeflow_main.createAttribute(node=n, name='kernel_size', preset='List', socket=True, plug=True, dataType='lst', dataAttr='[3, 3]')
        nodeflow_main.createAttribute(node=n, name='strides', preset='List', socket=True, plug=True, dataType='lst', dataAttr='[1, 1]')
        nodeflow_main.createAttribute(node=n, name='padding', preset='String', socket=True, plug=True, dataType='str', dataAttr='same')
        nodeflow_main.createAttribute(node=n, name='data_format', preset='String', socket=True, plug=True, dataType='str', dataAttr='channels_last')
        nodeflow_main.createAttribute(node=n, name='dilation', preset='Integer', socket=True, plug=True, dataType='int', dataAttr='1')
        nodeflow_main.createAttribute(node=n, name='dilation_rate', preset='List', socket=True, plug=True, dataType='lst', dataAttr='[1, 1]')
        nodeflow_main.createAttribute(node=n, name='activation', preset='String', socket=True, plug=True, dataType='str', dataAttr='relu')
        nodeflow_main.createAttribute(node=n, name='use_bias', preset='Bool', socket=True, plug=True, dataType='bool', dataAttr='True')
        nodeflow_main.createAttribute(node=n, name='kernel_initializer', preset='String', socket=True, plug=True, dataType='str', dataAttr='')

class ZerosLayerAction(QAction):
    """Model Train"""

    def __init__(self, attrData, config):
        super(ZerosLayerAction, self).__init__()

        print(attrData)