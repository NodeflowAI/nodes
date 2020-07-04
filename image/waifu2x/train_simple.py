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
CSV = config['ACTION']['CSV']

N = '\n'
T = '\t'
TT = '\t\t'
TTT = '\t\t\t'

class TrainSimple(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(TrainSimple, self).__init__()

        nodeflow_main.createAttribute(node=n, name='Dataset_Dir', preset='String', socket=True, plug=True, dataType='str', dataAttr='')
        nodeflow_main.createAttribute(node=n, name='Epoch', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=50)
        nodeflow_main.createAttribute(node=n, name='Inner_Epoch', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=4)
        nodeflow_main.createAttribute(node=n, name='Model_Name', preset='String', socket=True, plug=True, dataType='str', dataAttr='')
        nodeflow_main.createAttribute(node=n, name='Arch', preset='String', socket=True, plug=True, dataType='str', dataAttr='VGG7')
        nodeflow_main.createAttribute(node=n, name='Method', preset='String', socket=True, plug=True, dataType='str', dataAttr='scale')
        nodeflow_main.createAttribute(node=n, name='Noise_Level', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=1)
        nodeflow_main.createAttribute(node=n, name='GPU', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=-1)


class TrainSimpleAction(QAction):
    """Model Create"""
    def __init__(self, attrData, config):
        super(TrainSimpleAction, self).__init__()

        import os
        DD = ' -d ' + attrData.get('Dataset_Dir')
        EPO = ' -e ' + str(attrData.get('Epoch'))
        IE = ' -ie ' + str(attrData.get('Inner_Epoch'))
        MN = ' -mn ' + attrData.get('Model_Name')
        A = ' -a ' + str(attrData.get('Arch'))
        M = ' -m ' + str(attrData.get('Method'))
        NL = ' -nl ' + str(attrData.get('Noise_Level'))
        GPU = ' -g ' + str(attrData.get('GPU'))

        train = 'python C:/Code/nirvana/modules/waifu2x/pixpix_train.py'+DD+EPO+IE+MN+A+M+NL+GPU

        print(train)
        os.system(train)
