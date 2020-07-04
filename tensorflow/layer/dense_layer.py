from PyQt5.QtWidgets import QWidget, QAction

from tensorflow.keras.layers import Dense

# Action Settings
import configparser
config = configparser.ConfigParser()
config.read('config/action_settings.ini')
SEP = config['ACTION']['SEP']
ADD = config['ACTION']['ADD']
SUB = config['ACTION']['SUB']
DIV = config['ACTION']['DIV']
MUL = config['ACTION']['MUL']

class DenseLayer(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(DenseLayer, self).__init__()

        NAME = 'Input'
        SIZE = 256
        SHAPE = 3

        UNITS = 1
        ACTIVATION = 'sigmoid'

        nodeflow_main.createAttribute(node=n, name='Model_Name', preset='String', socket=True, plug=True, dataType='str', dataAttr='')

        nodeflow_main.createAttribute(node=n, name='Units', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=UNITS)
        nodeflow_main.createAttribute(node=n, name='Activation', preset='String', socket=True, plug=True, dataType='str', dataAttr=ACTIVATION)


class DenseLayerAction(QAction):
    """Model Train"""
    def __init__(self, attrData, config):
        super(DenseLayerAction, self).__init__()

        MODEL = attrData.get('Model_Name')
        UNITS = attrData.get('Units')
        ACTIVATION = attrData.get('Activation')

        model = globals()[MODEL]
        model.add(Dense(units=UNITS, activation=ACTIVATION))