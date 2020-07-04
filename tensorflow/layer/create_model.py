from PyQt5.QtWidgets import QWidget, QAction
from tensorflow.keras.models import Sequential

# Action Settings
import configparser
config = configparser.ConfigParser()
config.read('config/action_settings.ini')
SEP = config['ACTION']['SEP']
ADD = config['ACTION']['ADD']
SUB = config['ACTION']['SUB']
DIV = config['ACTION']['DIV']
MUL = config['ACTION']['MUL']
SPL = config['ACTION']['SPL']
NPZ = config['ACTION']['NPZ']
MOD = config['ACTION']['MOD']
JSN = config['ACTION']['JSN']

class CreateModel(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(CreateModel, self).__init__()
        global nfm
        nfm = nodeflow_main

        global node
        node = n

        MODEL = 'test'
        nodeflow_main.createAttribute(node=n, name='Model_Name', preset='String', socket=True, plug=True, dataType='str', dataAttr=MODEL)
        nodeflow_main.createAttribute(node=n, name='Layers', preset='Integer', socket=False, plug=True, dataType='int', dataAttr=1)

class CreateModelUpdate(QAction):
    """Model Train"""
    def __init__(self, attrData, config):
        super(CreateModelUpdate, self).__init__()

        # Building the model
        LAYERS = int(attrData.get('Layers'))

        for layer in range(1, LAYERS + 1):
            nfm.createAttribute(node=node, name='Layer_' + str(layer), preset='String', socket=True, plug=True,
                                dataType='str', dataAttr='')


class CreateModelAction(QAction):
    """Model Train"""

    def __init__(self, attrData, config):
        super(CreateModelAction, self).__init__()

        # Building the model
        MODEL = attrData.get('Model_Name')
        LAYERS = int(attrData.get('Layers'))

        layer_data = []
        for layer in range(1, LAYERS + 1):
            layer_data.append(layer)

        print(layer_data)
        #exec(layer)
