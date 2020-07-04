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

class CycleganTrain(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(CycleganTrain, self).__init__()

        DATASETS = config.get('DATASETS')
        CHECKPOINTS = config.get('CHECKPOINTS')

        name = 'temp_cyclegan'
        dataroot = DATASETS+'mini'

        nodeflow_main.createAttribute(node=n, name='Name', preset='String', socket=True, plug=True, dataType='str', dataAttr=name)
        nodeflow_main.createAttribute(node=n, name='Data_Path', preset='String', socket=True, plug=True, dataType='str', dataAttr=dataroot)
        nodeflow_main.createAttribute(node=n, name='Checkpoint_Dir', preset='String', socket=True, plug=True, dataType='str', dataAttr=CHECKPOINTS)

        nodeflow_main.createAttribute(node=n, name='Epochs', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=1)
        nodeflow_main.createAttribute(node=n, name='Epochs_Decay', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=0)
        nodeflow_main.createAttribute(node=n, name='Save_Latest_Freq', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=10)
        nodeflow_main.createAttribute(node=n, name='Print_Freq', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=1)

        nodeflow_main.createAttribute(node=n, name='Display_ID', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=-1)
        nodeflow_main.createAttribute(node=n, name='GPU', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=0)

class CycleganTrainAction(QAction):
    """Model Create"""
    def __init__(self, attrData, config):
        super(CycleganTrainAction, self).__init__()

        NAME = ' --name ' + attrData.get('Name')
        DATA = ' --dataroot ' + attrData.get('Data_Path')
        CPD = ' --checkpoints_dir ' + attrData.get('Checkpoint_Dir')

        EPO = ' --n_epochs ' + str(attrData.get('Epochs'))
        EPO_D = ' --n_epochs_decay ' + str(attrData.get('Epochs_Decay'))
        SLF = ' --save_latest_freq ' + str(attrData.get('Save_Latest_Freq'))
        PF = ' --print_freq ' + str(attrData.get('Print_Freq'))

        DID = ' --display_id ' + str(attrData.get('Display_ID'))
        GPU = ' --gpu_ids ' + str(attrData.get('GPU'))

        command = 'python modules/PixGan/train.py --model cycle_gan'+NAME+DATA+CPD+EPO+EPO_D+SLF+PF+DID+GPU
        self.run(command)

    def run(self, command):
        try:
            print(command)
            exit_status = os.system(command)
            if exit_status > 0:
                exit(1)
        except:
            pass