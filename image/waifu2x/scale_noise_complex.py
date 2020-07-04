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

class ScaleNoiseComplex(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(ScaleNoiseComplex, self).__init__()

        nodeflow_main.createAttribute(node=n, name='Input', preset='Image', socket=True, plug=True, dataType='img', dataAttr='')
        nodeflow_main.createAttribute(node=n, name='Output', preset='Image', socket=True, plug=True, dataType='img', dataAttr='')
        nodeflow_main.createAttribute(node=n, name='Scale_Ratio', preset='Float', socket=True, plug=True, dataType='flt', dataAttr=2.0)
        nodeflow_main.createAttribute(node=n, name='Quality', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=5)
        nodeflow_main.createAttribute(node=n, name='TTA', preset='String', socket=True, plug=True, dataType='str', dataAttr='store_true')
        nodeflow_main.createAttribute(node=n, name='Batch_Size', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=16)
        nodeflow_main.createAttribute(node=n, name='Block_Size', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=128)
        nodeflow_main.createAttribute(node=n, name='Extension', preset='String', socket=True, plug=True, dataType='str', dataAttr='png')
        nodeflow_main.createAttribute(node=n, name='Arch', preset='String', socket=True, plug=True, dataType='str', dataAttr='VGG7')
        nodeflow_main.createAttribute(node=n, name='Method', preset='String', socket=True, plug=True, dataType='str', dataAttr='noise_scale')
        nodeflow_main.createAttribute(node=n, name='Noise_Level', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=1)
        nodeflow_main.createAttribute(node=n, name='Color', preset='String', socket=True, plug=True, dataType='str', dataAttr='rgb')
        nodeflow_main.createAttribute(node=n, name='TTA_Level', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=8)
        nodeflow_main.createAttribute(node=n, name='Width', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=0)
        nodeflow_main.createAttribute(node=n, name='Height', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=0)
        nodeflow_main.createAttribute(node=n, name='Shorter_Side', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=0)
        nodeflow_main.createAttribute(node=n, name='Longer_Side', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=0)
        nodeflow_main.createAttribute(node=n, name='Model_Dir', preset='String', socket=True, plug=True, dataType='str', dataAttr='')
        nodeflow_main.createAttribute(node=n, name='GPU', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=-1)


class ScaleNoiseComplexAction(QAction):
    """Model Create"""
    def __init__(self, attrData, config):
        super(ScaleNoiseComplexAction, self).__init__()

        INPUT = ' -i ' + attrData.get('Input')
        OUTPUT = ' -o ' + attrData.get('Output')
        QUALITY = ' -q ' + str(attrData.get('Quality'))
        MODEL = ' -d ' + attrData.get('Model_Dir')
        SCALE = ' -s ' + str(attrData.get('Scale_Ratio'))
        TAA = ' -t ' + attrData.get('TTA')
        BATCH = ' -b ' + str(attrData.get('Batch_Size'))
        BLOCK = ' -l ' + str(attrData.get('Block_Size'))
        EXT = ' -e ' + attrData.get('Extension')
        ARCH = ' -a ' + attrData.get('Arch')
        MOTHOD = ' -m ' + attrData.get('Method')
        NOISE = ' -n ' + str(attrData.get('Noise_Level'))
        COLOR = ' -c ' + attrData.get('Color')
        TTA_LEVEL = ' -T ' + str(attrData.get('TTA_Level'))
        WIDTH = ' -W ' + str(attrData.get('Width'))
        HEIGHT = ' -H ' + str(attrData.get('Height'))
        SHORTER = ' -S ' + str(attrData.get('Shorter_Side'))
        LONGER = ' -L ' + str(attrData.get('Longer_Side'))
        GPU = ' -g ' + str(attrData.get('GPU'))

        run = 'python C:/Code/nirvana/modules/waifu2x/waifu2x.py'+INPUT+OUTPUT+QUALITY+SCALE+BATCH+BLOCK+MOTHOD+NOISE+COLOR+TTA_LEVEL+WIDTH+HEIGHT+SHORTER+LONGER+ARCH+GPU

        print(run)
        os.system(run)
