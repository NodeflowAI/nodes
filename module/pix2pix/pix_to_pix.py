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

class PixToPix(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(PixToPix, self).__init__()

        nodeflow_main.createAttribute(node=n, name='Name', preset='String', socket=True, plug=True, dataType='str', dataAttr='label2city_1024p')
        nodeflow_main.createAttribute(node=n, name='Data_Root', preset='String', socket=True, plug=True, dataType='str', dataAttr='C:/Nodeflow/dataset/cityscapes')
        nodeflow_main.createAttribute(node=n, name='Checkpoint_Dir', preset='String', socket=True, plug=True, dataType='str', dataAttr='C:/Nodeflow/models')

        nodeflow_main.createAttribute(node=n, name='GPU', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=-1)


class PixToPixAction(QAction):
    """Model Create"""
    def __init__(self, attrData, config):
        super(PixToPixAction, self).__init__()

        NAME = ' -n  ' + attrData.get('Name')
        DR = ' -dr  ' + attrData.get('Data_Root')
        CPD = ' -cpd  ' + attrData.get('Checkpoint_Dir')
        GPU = ' -g  ' + str(attrData.get('GPU'))

        '''
        try:
            for IMG in IMAGES:
                run = 'python C:/Code/nirvana/modules/pix2pixHD/pixpix_test.py'+NAME+DR+GPU
                print(run)
                os.system(run)
        except:
            pass
        '''

        try:
            run = 'python C:/Code/nirvana/modules/pix2pixHD/pixpix_test.py'+NAME+DR+CPD+GPU+' --netG local --ngf 32 --resize_or_crop none'
            print(run)
            os.system(run)
        except:
            pass


