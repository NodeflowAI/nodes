from PyQt5.QtWidgets import QWidget, QAction
import os
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
CSV = config['ACTION']['CSV']

N = '\n'
T = '\t'
TT = '\t\t'
TTT = '\t\t\t'

class NoiseSimple(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(NoiseSimple, self).__init__()

        nodeflow_main.createAttribute(node=n, name='Input', preset='Image', socket=True, plug=True, dataType='img', dataAttr='')
        nodeflow_main.createAttribute(node=n, name='Output', preset='Image', socket=True, plug=True, dataType='img', dataAttr='')
        nodeflow_main.createAttribute(node=n, name='Quality', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=5)
        nodeflow_main.createAttribute(node=n, name='Noise_Level', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=1)
        nodeflow_main.createAttribute(node=n, name='Arch', preset='String', socket=True, plug=True, dataType='str', dataAttr='VGG7')
        nodeflow_main.createAttribute(node=n, name='Model_Dir', preset='String', socket=True, plug=True, dataType='str', dataAttr='')
        nodeflow_main.createAttribute(node=n, name='GPU', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=-1)


class NoiseSimpleAction(QAction):
    """Model Create"""
    def __init__(self, attrData, config):
        super(NoiseSimpleAction, self).__init__()

        INPUT = ' -i ' + attrData.get('Input')
        OUTPUT = ' -o ' + attrData.get('Output')
        QUALITY = ' -q ' + str(attrData.get('Quality'))
        MODEL = ' -d ' + attrData.get('Model_Dir')
        ARCH = ' -a ' + attrData.get('Arch')
        MOTHOD = ' -m noise'
        NOISE = ' -n ' + str(attrData.get('Noise_Level'))
        GPU = ' -g ' + str(attrData.get('GPU'))

        run = 'python C:/Code/nirvana/modules/waifu2x/waifu2x.py' + INPUT + OUTPUT + QUALITY + MOTHOD + NOISE + ARCH + GPU

        print(run)
        os.system(run)
