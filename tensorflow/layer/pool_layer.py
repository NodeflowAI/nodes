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

class PoolLayer(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(PoolLayer, self).__init__()

        NAME = 'Pool'
        TRAINABLE = False
        DTYPE = 'float32'
        POOL = 2
        PADDING = 'valid'
        STRIDES = 2
        DATA_FORMAT = 'channels_last'
        INBOUND_NODES = [[[nn, 0, 0, {}]]]

        nodeflow_main.createAttribute(node=n, name='Pool', preset='String', socket=True, plug=True, dataType='str', dataAttr='')
        nodeflow_main.createAttribute(node=n, name='trainable', preset='Bool', socket=True, plug=True, dataType='bool', dataAttr='False')
        nodeflow_main.createAttribute(node=n, name='mdtypeode', preset='String', socket=True, plug=True, dataType='str', dataAttr='float32')
        nodeflow_main.createAttribute(node=n, name='pool', preset='Integer', socket=True, plug=True, dataType='int', dataAttr='2')
        nodeflow_main.createAttribute(node=n, name='pool_size', preset='List', socket=True, plug=True, dataType='lst', dataAttr='[2, 2]')
        nodeflow_main.createAttribute(node=n, name='padding', preset='String', socket=True, plug=True, dataType='str', dataAttr='valid')
        nodeflow_main.createAttribute(node=n, name='stride', preset='Integer', socket=True, plug=True, dataType='int', dataAttr='2')
        nodeflow_main.createAttribute(node=n, name='stride_size', preset='List', socket=True, plug=True, dataType='lst', dataAttr='[2, 2]')
        nodeflow_main.createAttribute(node=n, name='data_format', preset='String', socket=True, plug=True, dataType='str', dataAttr='channels_last')
        nodeflow_main.createAttribute(node=n, name='kernel_initializer', preset='String', socket=True, plug=True, dataType='str', dataAttr='')
