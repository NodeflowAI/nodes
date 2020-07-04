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

class QuantumDefault(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(QuantumDefault, self).__init__()

        TOKEN = 'e8ee3abd0bd2b8324e5e806a675313b5392e6a31b2aa537cb5f2e87b2995206aeca767a964a792b588679e063a4be6e4fc7e54cbbb6526b5f68007d1a2d8bf6a'

        nodeflow_main.createAttribute(node=n, name='Token', preset='String', socket=True, plug=True, dataType='str', dataAttr=TOKEN)

class QuantumDefaultAction(QAction):
    """Model Create"""
    def __init__(self, attrData, config):
        super(QuantumDefaultAction, self).__init__()

        from qiskit import IBMQ

        token = attrData.get('Token')

        IBMQ.save_account(token)

