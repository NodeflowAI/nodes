from PyQt5.QtWidgets import QWidget, QAction
from tensorflow.keras.layers import Conv2D

# Action Settings
import configparser
config = configparser.ConfigParser()
config.read('config/action_settings.ini')
SEP = config['ACTION']['SEP']
ADD = config['ACTION']['ADD']
SUB = config['ACTION']['SUB']
DIV = config['ACTION']['DIV']
MUL = config['ACTION']['MUL']

class InputLayer(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(InputLayer, self).__init__()

        NAME = 'Input'
        INPUT_SIZE = 256
        SHAPE = 3
        BATCH_INPUT_SHAPE = [None, INPUT_SIZE, INPUT_SIZE, SHAPE]
        DTYPE = 'float32'
        SPARSE = False
        INBOUND_NODES = []

        nodeflow_main.createAttribute(node=n, name='Model_Name', preset='String', socket=True, plug=True, dataType='str', dataAttr='')
        nodeflow_main.createAttribute(node=n, name='Input_Size', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=INPUT_SIZE)
        nodeflow_main.createAttribute(node=n, name='Shape', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=SHAPE)
        nodeflow_main.createAttribute(node=n, name='batch_input_shape', preset='String', socket=True, plug=True, dataType='str', dataAttr='')
        nodeflow_main.createAttribute(node=n, name='dtype', preset='String', socket=True, plug=True, dataType='str', dataAttr='float32')
        nodeflow_main.createAttribute(node=n, name='sparse', preset='Bool', socket=True, plug=True, dataType='bool', dataAttr='False')
        nodeflow_main.createAttribute(node=n, name='inbound_nodes', preset='String', socket=True, plug=True, dataType='str', dataAttr='')

class InputLayerAction(QAction):
    """Model Train"""
    def __init__(self, attrData, config):
        super(InputLayerAction, self).__init__()

        L1_NUM_FILTERS = int(attrData.get('L1_Num_Filters'))
        L1_FILTER_SIZE = int(attrData.get('L1_Filter_Size'))
        L1_ACTIVATION = attrData.get('L1_Activation')


        model.add(Conv2D(L1_NUM_FILTERS, (L1_FILTER_SIZE, L1_FILTER_SIZE), input_shape=(INPUT_SIZE, INPUT_SIZE, SHAPE), activation=L1_ACTIVATION))