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

class FacelabUtil(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(FacelabUtil, self).__init__()

        BATCH_SIZE = 256
        EPOCHS = 60
        noise_dim = 100
        num_examples_to_generate = 16
        data_dir = "C:/Nodeflow/dataset/img_align_celeba"
        checkpoint_dir = 'C:/Nodeflow/checkpoints'
        output_dir = 'C:/Nodeflow/images/Output'
        phase = 'test'

        nodeflow_main.createAttribute(node=n, name='Input_Dir', preset='String', socket=True, plug=True, dataType='str', dataAttr=data_dir)
        nodeflow_main.createAttribute(node=n, name='Results_Dir', preset='String', socket=True, plug=True, dataType='str', dataAttr=data_dir)
        nodeflow_main.createAttribute(node=n, name='Checkpoint_Dir', preset='String', socket=True, plug=True, dataType='str', dataAttr=checkpoint_dir)
        nodeflow_main.createAttribute(node=n, name='Output_Dir', preset='String', socket=True, plug=True, dataType='str', dataAttr=output_dir)

        nodeflow_main.createAttribute(node=n, name='Epochs', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=EPOCHS)
        nodeflow_main.createAttribute(node=n, name='Batch_Size', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=BATCH_SIZE)
        nodeflow_main.createAttribute(node=n, name='Noise_Dim', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=noise_dim)
        nodeflow_main.createAttribute(node=n, name='Samples', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=num_examples_to_generate)

        nodeflow_main.createAttribute(node=n, name='GPU', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=-1)

class FacelabUtilAction(QAction):
    """Model Create"""
    def __init__(self, attrData, config):
        super(FacelabUtilAction, self).__init__()

        N = ' -n ' + attrData.get('Name')
        ID = ' --input-dir ' + attrData.get('Input_Dir')
        RD = ' -rd ' + attrData.get('Results_Dir')
        CPD = ' -cpd ' + attrData.get('Checkpoint_Dir')
        EPO = ' -epo ' + str(attrData.get('Epochs'))
        GPU = ' -g ' + str(attrData.get('GPU'))

        try:
            run = 'python C:/Code/nirvana/modules/DeepFaceLab/main.py util'
            print(run)
            os.system(run)
        except:
            pass