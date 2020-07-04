from threading import Thread
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
SPL = config['ACTION']['SPL']
NPZ = config['ACTION']['NPZ']
MOD = config['ACTION']['MOD']
JSN = config['ACTION']['JSN']
N = '\n'
T = '\t'

class CreateFunction(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(CreateFunction, self).__init__()

        name = nn+'Class_Name'

        nodeflow_main.createAttribute(node=n, name='Function_Name', preset='String', socket=True, plug=True, dataType='str', dataAttr='')

class CreateFunctionAction(QAction):
    """Main widget"""
    def __init__(self, attrData, config):
        super(CreateFunctionAction, self).__init__()

        FUNCTION_NAME = attrData.get('Function_Name')

        funt_init = 'def ' + FUNCTION_NAME + '():' + N
        func_action = T + 'print("' + FUNCTION_NAME + ' Function")' + N
        func_exec = FUNCTION_NAME + '()'

        funt_lines = funt_init + func_action + func_exec
        print(funt_lines)
        exec(funt_lines)
