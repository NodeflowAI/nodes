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

class ScaleSimple(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(ScaleSimple, self).__init__()

        nodeflow_main.createAttribute(node=n, name='Input', preset='Image', socket=True, plug=True, dataType='img', dataAttr='')
        nodeflow_main.createAttribute(node=n, name='Output', preset='Image', socket=True, plug=True, dataType='img', dataAttr='')
        nodeflow_main.createAttribute(node=n, name='Scale_Ratio', preset='Float', socket=True, plug=True, dataType='flt', dataAttr=2.0)
        nodeflow_main.createAttribute(node=n, name='Quality', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=5)
        nodeflow_main.createAttribute(node=n, name='Arch', preset='String', socket=True, plug=True, dataType='str', dataAttr='VGG7')
        nodeflow_main.createAttribute(node=n, name='Model_Dir', preset='String', socket=True, plug=True, dataType='str', dataAttr='')
        nodeflow_main.createAttribute(node=n, name='GPU', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=-1)

class ScaleSimpleAction(QAction):
    """Model Create"""
    def __init__(self, attrData, config):
        super(ScaleSimpleAction, self).__init__()

        IMAGES = attrData.get('Input')

        try:
            INPUT = ' -i ' + attrData.get('Input')
        except:
            pass

        OUTPUT = ' -o ' + attrData.get('Output')
        QUALITY = ' -q ' + str(attrData.get('Quality'))
        MODEL = ' -d ' + attrData.get('Model_Dir')
        SCALE = ' -s ' + str(attrData.get('Scale_Ratio'))
        ARCH = ' -a ' + attrData.get('Arch')
        MOTHOD = ' -m scale'
        GPU = ' -g ' + str(attrData.get('GPU'))

        try:
            for IMG in IMAGES:
                run = 'python C:/Code/nirvana/modules/waifu2x/waifu2x.py' + ' -i ' + IMG + ' -o ' + IMG + QUALITY + SCALE + MOTHOD + ARCH + GPU
                print(run)
                os.system(run)
        except:
            pass

        try:
            run = 'python C:/Code/nirvana/modules/waifu2x/waifu2x.py' + INPUT + OUTPUT + QUALITY + SCALE + MOTHOD + ARCH + GPU
            print(run)
            os.system(run)
        except:
            pass