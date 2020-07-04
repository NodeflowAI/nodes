from PyQt5.QtWidgets import QWidget, QAction
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Activation, Dense, Flatten, Reshape, Dropout, Conv2DTranspose
from tensorflow.keras.callbacks import ModelCheckpoint

import configparser
import numpy as np

# Action Settings
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

class ModelTrain(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(ModelTrain, self).__init__()

        DATASET = config.get('DATASET')
        MODEL = config.get('MODEL')
        SETTINGS = config.get('SETTINGS')

        name = nn+'Train_Name'
        dat_dir = nn+'Dataset_Dir'
        dat_ext = nn+'Dataset_Ext'
        mod_ext = nn+'Model_Ext'
        mod_dir = nn+'Model_Dir'
        set_ext = nn+'Settings_Ext'
        set_dir = nn+'Settings_Dir'

        BATCH_SIZE = 100
        EPOCHS = 60
        OPTIMIZER = 'adam'
        LOSS = 'mse'
        MONITOR = 'val_loss'
        VERBOSE = 1

        nodeflow_main.createAttribute(node=n, name='Train_Name', preset='String', socket=True, plug=True, dataType='str', dataAttr='')

        nodeflow_main.createAttribute(node=n, name='Epochs', preset='Integer', socket=True, plug=False, dataType='int', dataAttr=EPOCHS)
        nodeflow_main.createAttribute(node=n, name='Batch_Size', preset='Integer', socket=True, plug=False, dataType='int', dataAttr=BATCH_SIZE)
        nodeflow_main.createAttribute(node=n, name='Optimizer', preset='String', socket=True, plug=False, dataType='str', dataAttr=OPTIMIZER)
        nodeflow_main.createAttribute(node=n, name='Loss', preset='String', socket=True, plug=False, dataType='str', dataAttr=LOSS)
        nodeflow_main.createAttribute(node=n, name='Monitor', preset='String', socket=True, plug=False, dataType='str', dataAttr=MONITOR)
        nodeflow_main.createAttribute(node=n, name='Verbose', preset='Integer', socket=True, plug=False, dataType='int', dataAttr=VERBOSE)

        nodeflow_main.createAttribute(node=n, name='Dataset_Path', preset='Path', socket=True, plug=True, dataType='str', dataExpr=SPL + DATASET + SPL + ADD + name + ADD + NPZ)
        nodeflow_main.createAttribute(node=n, name='Model_Path', preset='Path', socket=True, plug=True, dataType='str', dataExpr=SPL + MODEL + SPL + ADD + name + ADD + MOD)
        nodeflow_main.createAttribute(node=n, name='Settings_Path', preset='Path', socket=True, plug=True, dataType='str', dataExpr=SPL + SETTINGS + SPL + ADD + name + ADD + JSN)

class ModelTrainAction(QAction):
    """Model Train"""
    def __init__(self, attrData, config):
        super(ModelTrainAction, self).__init__()

        print("Loading previously created data...")

        npz_path = attrData.get('Dataset_Path')
        data = np.load(npz_path)
        mod_path = attrData.get('Model_Path')

        dataX = "x_test"
        dataY = "y_test"

        epochs = int(attrData.get('Epochs'))
        batch_size = int(attrData.get('Batch_Size'))

        optimizer = attrData.get('Optimizer')
        loss = attrData.get('Loss')
        monitor = attrData.get('Monitor')
        verbose = int(attrData.get('Verbose'))

        input_dim = data[dataX].shape[1:]
        output_dim = data[dataY].shape[1:]

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
                  batch_size=batch_size,
                  epochs=epochs,
                  validation_data=(data[dataX], data[dataY]),
                  callbacks=callbacks_list)

        model.save_weights(mod_path)
        print("Saved model to disk")
        print('######################### TRAINING COMPLETE #########################')