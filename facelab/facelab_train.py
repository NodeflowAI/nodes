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

class FacelabTrain(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(FacelabTrain, self).__init__()

        BATCH_SIZE = 256
        EPOCHS = 60
        noise_dim = 100
        num_examples_to_generate = 16

        source_dir = 'C:/Nodeflow/input'
        output_dir = 'C:/Nodeflow/images/Output'

        nodeflow_main.createAttribute(node=n, name='Model_Name', preset='String', socket=True, plug=True, dataType='str', dataAttr='Tester')
        nodeflow_main.createAttribute(node=n, name='Model', preset='String', socket=True, plug=True, dataType='str', dataAttr='Quick96')
        nodeflow_main.createAttribute(node=n, name='Model_Dir', preset='String', socket=True, plug=True, dataType='str', dataAttr='C:/Nodeflow/models')

        nodeflow_main.createAttribute(node=n, name='Source_Dir', preset='String', socket=True, plug=True, dataType='str', dataAttr=source_dir)
        nodeflow_main.createAttribute(node=n, name='Dest_Dir', preset='String', socket=True, plug=True, dataType='str', dataAttr=output_dir)
        nodeflow_main.createAttribute(node=n, name='Pretraining_Data_Dir', preset='String', socket=True, plug=True, dataType='str', dataAttr='')
        nodeflow_main.createAttribute(node=n, name='Pretrained_Model_Dir', preset='String', socket=True, plug=True, dataType='str', dataAttr='')

        nodeflow_main.createAttribute(node=n, name='GPU', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=-1)

class FacelabTrainAction(QAction):
    """Model Create"""
    def __init__(self, attrData, config):
        super(FacelabTrainAction, self).__init__()

        NAME = ' --force-model-name ' + attrData.get('Model_Name')
        MOD = ' --model ' + attrData.get('Model')
        MOD_DIR = ' --model-dir ' + attrData.get('Model_Dir')
        SRC = ' --training-data-src-dir ' + attrData.get('Source_Dir')
        DST = ' --training-data-dst-dir ' + attrData.get('Dest_Dir')
        PRE_DATA = ' --pretraining-data-dir ' + attrData.get('Pretraining_Data_Dir')
        PRE_MODEL = ' --pretrained-model-dir ' + attrData.get('Pretrained_Model_Dir')
        GPU = ' --force-gpu-idxs ' + str(attrData.get('GPU'))

        try:
            run = 'python C:/Code/nirvana/modules/DeepFaceLab/main.py train'+NAME+MOD+MOD_DIR+SRC+DST+GPU
            print(run)
            os.system(run)
        except:
            pass