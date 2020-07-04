from PyQt5.QtWidgets import QWidget, QAction

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Activation, Dense, Flatten, Reshape, Dropout, Conv2DTranspose
from tensorflow.keras.callbacks import ModelCheckpoint
import numpy as np

# Action Settings
import configparser
config = configparser.ConfigParser()
config.read('config/action_settings.ini')
SEP = config['ACTION']['SEP']
ADD = config['ACTION']['ADD']
SUB = config['ACTION']['SUB']
DIV = config['ACTION']['DIV']
MUL = config['ACTION']['MUL']
SPL = config['ACTION']['SPL']
NPZ = config['ACTION']['NPZ']
MOD = config['ACTION']['MOD']
JSN = config['ACTION']['JSN']

class ReconModelCreate(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(ReconModelCreate, self).__init__()

        DATASET = config.get('DATASET')
        MODEL = config.get('MODEL')

        name = nn+'Model_Name'

        EPOCHS = 60
        BATCH_SIZE = 100
        OPTIMIZER = 'adam'
        LOSS = 'mse'
        MONITOR = 'val_loss'
        VERBOSE = 1

        nodeflow_main.createAttribute(node=n, name='Model_Name', preset='String', socket=True, plug=False, dataType='str', dataAttr='')

        nodeflow_main.createAttribute(node=n, name='Optimizer', preset='String', socket=True, plug=False, dataType='str', dataAttr=OPTIMIZER)
        nodeflow_main.createAttribute(node=n, name='Loss_Function', preset='String', socket=True, plug=False, dataType='str', dataAttr=LOSS)
        nodeflow_main.createAttribute(node=n, name='Monitor', preset='String', socket=True, plug=False, dataType='str', dataAttr=MONITOR)
        nodeflow_main.createAttribute(node=n, name='Verbose', preset='Integer', socket=True, plug=False, dataType='int', dataAttr=VERBOSE)
        nodeflow_main.createAttribute(node=n, name='Model_Epochs', preset='Integer', socket=True, plug=False, dataType='int', dataAttr=EPOCHS)
        nodeflow_main.createAttribute(node=n, name='Training_Epochs', preset='Integer', socket=True, plug=False, dataType='int', dataAttr=EPOCHS)
        nodeflow_main.createAttribute(node=n, name='Model_Batch_Size', preset='Integer', socket=True, plug=False, dataType='int', dataAttr=BATCH_SIZE)
        nodeflow_main.createAttribute(node=n, name='Training_Batch_Size', preset='Integer', socket=True, plug=False, dataType='int', dataAttr=BATCH_SIZE)

        nodeflow_main.createAttribute(node=n, name='Dataset_Path', preset='Path', socket=True, plug=True, dataType='str', dataExpr=SPL + DATASET + SPL + ADD + name + ADD + NPZ)
        nodeflow_main.createAttribute(node=n, name='Model_Path', preset='Path', socket=True, plug=True, dataType='str', dataExpr=SPL + MODEL + SPL + ADD + name + ADD + MOD)

class ModelCreateAction(QAction):
    """Model Create"""
    def __init__(self, attrData, config):
        super(ModelCreateAction, self).__init__()

        # loading previously created data
        print("Loading previously created data...")

        npz_file = attrData.get('Dataset_Path')
        mod_file = attrData.get('Model_Path')

        data = np.load(npz_file)

        monitor = attrData.get('Monitor')
        verbose = attrData.get('Verbose')

        model_batch_size = int(attrData.get('Model_Batch_Size'))
        model_epochs = int(attrData.get('Model_Epochs'))

        optimizer = attrData.get('Optimizer')
        loss = attrData.get('Loss_Function')


        self.dataX = "x_test"
        self.dataY = "y_test"


        input_dim = data["x_test"].shape[1:]
        output_dim = data["y_test"].shape[1:]

        # Building the model
        model = Sequential()

        # convolution layers
        model.add(Conv2D(1, (1, 1), data_format="channels_last", input_shape=input_dim))
        model.add(Conv2D(2, (3, 3)))
        model.add(Conv2D(3, (4, 4)))
        model.add(Dropout(.05))

        # Transpose convolution layers (Deconvolution)
        model.add(Conv2DTranspose(3, (3, 3)))
        model.add(Conv2DTranspose(2, (5, 5)))
        model.add(Conv2DTranspose(1, (8, 8)))
        model.add(Dropout(.1))

        # Fully connected layers
        model.add(Flatten())
        model.add(Dense(np.prod(output_dim)))
        model.add(Reshape(output_dim))  # scaling to the output dimension
        model.add(Activation("linear"))  # using a "soft" activation

        model.compile(optimizer=optimizer, loss=loss)
        print(model.summary())

        # fitting the model
        print("Fitting the model...")
        checkpoint = ModelCheckpoint(mod_file, monitor=monitor, verbose=verbose, save_best_only=True)
        callbacks_list = [checkpoint]

        model.fit(data["x_train"], data["y_train"],
                  batch_size=model_batch_size,
                  epochs=model_epochs,
                  validation_data=(data["x_test"], data["y_test"]),
                  callbacks=callbacks_list)