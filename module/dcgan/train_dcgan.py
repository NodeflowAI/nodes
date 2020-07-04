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

class TrainDcgan(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(TrainDcgan, self).__init__()

        BATCH_SIZE = 256
        EPOCHS = 60
        noise_dim = 100
        num_examples_to_generate = 16
        data_dir = "C:/Nodeflow/dataset/img_align_celeba"
        checkpoint_dir = 'C:/Nodeflow/checkpoints'
        store_produce_image_dir = 'C:/Nodeflow/images/Output'

        nodeflow_main.createAttribute(node=n, name='Data_Dir', preset='String', socket=True, plug=True, dataType='str', dataAttr=data_dir)
        nodeflow_main.createAttribute(node=n, name='Checkpoint_Dir', preset='String', socket=True, plug=True, dataType='str', dataAttr=checkpoint_dir)
        nodeflow_main.createAttribute(node=n, name='Output_Dir', preset='String', socket=True, plug=True, dataType='str', dataAttr=store_produce_image_dir)

        nodeflow_main.createAttribute(node=n, name='Epochs', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=EPOCHS)
        nodeflow_main.createAttribute(node=n, name='Batch_Size', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=BATCH_SIZE)
        nodeflow_main.createAttribute(node=n, name='Noise_Dim', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=noise_dim)
        nodeflow_main.createAttribute(node=n, name='Samples', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=num_examples_to_generate)


class TrainDcganAction(QAction):
    """Model Create"""
    def __init__(self, attrData, config):
        super(TrainDcganAction, self).__init__()

        from modules.DCGAN import  train_dcgan_model

        DATA = attrData.get('Data_Dir')
        CHECKPOINT = attrData.get('Checkpoint_Dir')
        OUTPUT = attrData.get('Output_Dir')
        EPOCHS = str(attrData.get('Epochs'))
        BATCH_SIZE = str(attrData.get('Batch_Size'))
        NOISE = str(attrData.get('Noise_Dim'))
        SAMPLES = str(attrData.get('Samples'))

        train_dcgan_model.train_dcgan_main(DATA, BATCH_SIZE, EPOCHS, NOISE, SAMPLES, CHECKPOINT, OUTPUT)

