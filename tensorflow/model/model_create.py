from PyQt5.QtWidgets import QWidget, QAction
import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Activation, Dense, Flatten, Reshape, Dropout, Conv2DTranspose
from tensorflow.keras.callbacks import ModelCheckpoint

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

class ModelCreate(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(ModelCreate, self).__init__()

        DATASET = config.get('DATASET')
        MODEL = config.get('MODEL')
        SETTINGS = config.get('SETTINGS')

        name = nn+'Model_Name'

        BATCH_SIZE = 100
        EPOCHS = 60
        INPUT_SIZE = 32
        OUTPUT_SIZE = 128
        SHAPE_SIZE = 1

        OPTIMIZER = 'adam'
        LOSS = 'mse'
        MONITOR = 'val_loss'
        VERBOSE = 1

        nodeflow_main.createAttribute(node=n, name='Model_Name', preset='String', socket=True, plug=True, dataType='str', dataAttr='')

        nodeflow_main.createAttribute(node=n, name='Optimizer', preset='String', socket=True, plug=True, dataType='str', dataAttr=OPTIMIZER)
        nodeflow_main.createAttribute(node=n, name='Loss_Function', preset='String', socket=True, plug=True, dataType='str', dataAttr=LOSS)
        nodeflow_main.createAttribute(node=n, name='Monitor', preset='String', socket=True, plug=True, dataType='str', dataAttr=MONITOR)
        nodeflow_main.createAttribute(node=n, name='Input_Size', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=INPUT_SIZE)
        nodeflow_main.createAttribute(node=n, name='Output_Size', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=OUTPUT_SIZE)
        nodeflow_main.createAttribute(node=n, name='Shape_Size', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=SHAPE_SIZE)

        nodeflow_main.createAttribute(node=n, name='Verbose', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=VERBOSE)
        nodeflow_main.createAttribute(node=n, name='Model_Epochs', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=EPOCHS)
        nodeflow_main.createAttribute(node=n, name='Training_Epochs', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=EPOCHS)
        nodeflow_main.createAttribute(node=n, name='Model_Batch_Size', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=BATCH_SIZE)
        nodeflow_main.createAttribute(node=n, name='Training_Batch_Size', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=BATCH_SIZE)

        nodeflow_main.createAttribute(node=n, name='Dataset_Path', preset='Path', socket=True, plug=True, dataType='str', dataExpr=SPL + DATASET + SPL + ADD + name + ADD + NPZ)
        nodeflow_main.createAttribute(node=n, name='Model_Path', preset='Path', socket=True, plug=True, dataType='str', dataExpr=SPL + MODEL + SPL + ADD + name + ADD + MOD)
        nodeflow_main.createAttribute(node=n, name='Settings_Path', preset='Path', socket=True, plug=True, dataType='str', dataExpr=SPL + SETTINGS + SPL + ADD + name + ADD + JSN)

class ModelCreateAction(QAction):
    """Model Create"""
    def __init__(self, attrData, config):
        super(ModelCreateAction, self).__init__()

        print(config)

        # loading previously created data
        print("Loading previously created data...")

        npz_path = attrData.get('Dataset_Path')
        mod_path = attrData.get('Model_Path')

        data = np.load(npz_path)

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
        checkpoint = ModelCheckpoint(mod_path, monitor=monitor, verbose=verbose, save_best_only=True)
        callbacks_list = [checkpoint]

        model.fit(data["x_train"], data["y_train"],
                  batch_size=model_batch_size,
                  epochs=model_epochs,
                  validation_data=(data["x_test"], data["y_test"]),
                  callbacks=callbacks_list)

        model.save_weights(mod_path)
        print("Saved model to disk")
        print('######################### TRAINING COMPLETE #########################')