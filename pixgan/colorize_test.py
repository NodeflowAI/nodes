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

class ColorizeTest(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(ColorizeTest, self).__init__()

        DATASETS = config.get('DATASETS')
        CHECKPOINTS = config.get('CHECKPOINTS')
        RESULTS = config.get('RESULTS')

        name = 'temp_color'
        dataroot = DATASETS+'mini_colorization'

        nodeflow_main.createAttribute(node=n, name='Name', preset='String', socket=True, plug=True, dataType='str', dataAttr=name)
        nodeflow_main.createAttribute(node=n, name='Data_Path', preset='String', socket=True, plug=True, dataType='str', dataAttr=dataroot)

        nodeflow_main.createAttribute(node=n, name='Checkpoints_Dir', preset='String', socket=True, plug=True, dataType='str', dataAttr=CHECKPOINTS)
        nodeflow_main.createAttribute(node=n, name='Results_Dir', preset='String', socket=True, plug=True, dataType='str', dataAttr=RESULTS)

        nodeflow_main.createAttribute(node=n, name='Aspect_Ratio', preset='Float', socket=True, plug=True, dataType='flt', dataAttr=1.0)

        nodeflow_main.createAttribute(node=n, name='Batch_Size', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=1)
        nodeflow_main.createAttribute(node=n, name='Num_Test', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=1)
        nodeflow_main.createAttribute(node=n, name='GPU', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=0)

class ColorizeTestAction(QAction):
    """Model Create"""
    def __init__(self, attrData, config):
        super(ColorizeTestAction, self).__init__()

        NAME = ' --name ' + attrData.get('Name')
        DATA = ' --dataroot ' + attrData.get('Data_Path')

        CPD = ' --checkpoints_dir ' + attrData.get('Checkpoints_Dir')
        RD = ' --results_dir ' + attrData.get('Results_Dir')

        AR = ' --aspect_ratio ' + str(attrData.get('Aspect_Ratio'))
        NUM = ' --num_test ' + str(attrData.get('Num_Test'))

        GPU = ' --gpu_ids ' + str(attrData.get('GPU'))

        command = 'python modules/PixGan/test.py --model colorization'+NAME+DATA+CPD+RD+AR+NUM+GPU
        self.run(command)

    def run(self, command):
        try:
            print(command)
            exit_status = os.system(command)
            if exit_status > 0:
                exit(1)
        except:
            pass