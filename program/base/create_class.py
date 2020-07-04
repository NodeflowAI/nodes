from threading import Thread
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

class CreateClass(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(CreateClass, self).__init__()

        name = nn+'Class_Name'

        nodeflow_main.createAttribute(node=n, name='Class_Name', preset='String', socket=True, plug=True, dataType='str', dataAttr='')
        nodeflow_main.createAttribute(node=n, name='Funtion_Name', preset='String', socket=True, plug=True, dataType='str', dataAttr='')


class CreateClassAction(QAction):
    """Main widget"""
    def __init__(self, attrData, config):
        super(CreateClassAction, self).__init__()

        CLASS_NAME = attrData.get('Class_Name')
        FUNCTION_NAME = attrData.get('Funtion_Name')

        class_import = 'from PyQt5.QtWidgets import QWidget' +N
        class_create = 'class ' + CLASS_NAME + '(QWidget):' +N
        class_init = T+ 'def __init__(self):' +N
        class_super = TT+ 'super(' + CLASS_NAME + ', self).__init__()' +N

        class_exec = CLASS_NAME + DOT + FUNCTION_NAME + '()'+ N

        class_lines = class_import + class_create + class_init + class_super
        main_exec = class_exec
        class_build = class_lines + main_exec

        print(class_build)
        exec(class_build)