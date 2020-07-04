from PyQt5.QtWidgets import QWidget, QAction
import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Conv2DTranspose
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

class CompileModel(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(CompileModel, self).__init__()

        DATASET = config.get('DATASET')
        MODEL = config.get('MODEL')
        SETTINGS = config.get('SETTINGS')
        TEST = config.get('TEST')

        name = nn+'Model_Name'
        dat_dir = nn+'Dataset_Dir'
        dat_ext = nn+'Dataset_Ext'
        set_ext = nn+'Settings_Ext'
        set_dir = nn+'Settings_Dir'

        test_dir = nn+'Test_Dir'


        LOSS = 'binary_crossentropy'
        OPTIMIZER = 'adam'

        # Define hyperparameters
        INPUT_SIZE = 32
        SHAPE = 3
        BATCH_SIZE = 16
        STEPS_PER_EPOCH = 10
        EPOCHS = 10
        VERBOSE = 1
        STEPS = 1
        MONITOR = 'val_loss'
        CLASS_MODE = 'binary'
        NUM_FILTERS = 32
        FILTER_SIZE = 3
        ACTIVATION = 'relu'

        nodeflow_main.createAttribute(node=n, name='Model_Name', preset='String', socket=True, plug=True, dataType='str', dataAttr='')

        nodeflow_main.createAttribute(node=n, name='Epochs', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=EPOCHS)
        nodeflow_main.createAttribute(node=n, name='Input_Size', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=INPUT_SIZE)
        nodeflow_main.createAttribute(node=n, name='Shape', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=SHAPE)
        nodeflow_main.createAttribute(node=n, name='Batch_Size', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=BATCH_SIZE)
        nodeflow_main.createAttribute(node=n, name='Steps_Per_Epoch', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=STEPS_PER_EPOCH)
        nodeflow_main.createAttribute(node=n, name='Steps', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=STEPS)
        nodeflow_main.createAttribute(node=n, name='Class_Mode', preset='String', socket=True, plug=True, dataType='str', dataAttr=CLASS_MODE)
        nodeflow_main.createAttribute(node=n, name='Optimizer', preset='String', socket=True, plug=True, dataType='str', dataAttr=OPTIMIZER)
        nodeflow_main.createAttribute(node=n, name='Loss', preset='String', socket=True, plug=True, dataType='str', dataAttr=LOSS)
        nodeflow_main.createAttribute(node=n, name='Monitor', preset='String', socket=True, plug=False, dataType='str', dataAttr=MONITOR)
        nodeflow_main.createAttribute(node=n, name='Verbose', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=VERBOSE)

        nodeflow_main.createAttribute(node=n, name='Num_Filters', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=NUM_FILTERS)
        nodeflow_main.createAttribute(node=n, name='Filter_Size', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=FILTER_SIZE)
        nodeflow_main.createAttribute(node=n, name='Activation', preset='String', socket=True, plug=True, dataType='str', dataAttr=ACTIVATION)

        nodeflow_main.createAttribute(node=n, name='Loss', preset='String', socket=True, plug=True, dataType='str', dataAttr=LOSS)
        nodeflow_main.createAttribute(node=n, name='Optimizer', preset='String', socket=True, plug=True, dataType='str', dataAttr=OPTIMIZER)

        nodeflow_main.createAttribute(node=n, name='Test_Dir', preset='String', socket=True, plug=True, dataType='str', dataAttr='Girls')
        nodeflow_main.createAttribute(node=n, name='Test_Path', preset='String', socket=True, plug=True, dataType='str', dataAttr=TEST)

        nodeflow_main.createAttribute(node=n, name='Dataset_Ext', preset='String', socket=True, plug=True, dataType='str', dataAttr='.npz')
        nodeflow_main.createAttribute(node=n, name='Dataset_Dir', preset='String', socket=True, plug=True, dataType='str', dataExpr=name)
        nodeflow_main.createAttribute(node=n, name='Dataset_Path', preset='Path', socket=True, plug=True, dataType='str', dataExpr=SPL + DATASET + SPL + ADD + dat_dir + ADD + dat_ext)


        nodeflow_main.createAttribute(node=n, name='Settings_Ext', preset='String', socket=True, plug=False, dataType='str', dataAttr='.json')
        nodeflow_main.createAttribute(node=n, name='Settings_Dir', preset='String', socket=True, plug=False, dataType='str', dataExpr=test_dir)
        nodeflow_main.createAttribute(node=n, name='Settings_Path', preset='Path', socket=True, plug=True, dataType='str', dataExpr=SPL + SETTINGS + SPL + ADD + set_dir + ADD + set_ext)


class CompileModelAction(QAction):
    """Model Train"""

    def __init__(self, attrData, config):
        super(CompileModelAction, self).__init__()

        npz_path = attrData.get('Dataset_Path')
        data = np.load(npz_path)
        print("Data Loaded")

        mod_path = config.get('MODEL')
        #set_path = attrData.get('Settings_Path')

        #train_path = config.get('TRAIN')
        #test_path = config.get('TEST')
        print('Compile')


        #MODEL = attrData.get('Model_Name')

        # Define hyperparameters
        #INPUT_SIZE = int(attrData.get('Input_Size'))
        #SHAPE = int(attrData.get('Shape'))
        BATCH_SIZE = int(attrData.get('Batch_Size'))

        #STEPS_PER_EPOCH = int(attrData.get('Steps_Per_Epoch'))
        EPOCHS = int(attrData.get('Epochs'))
        MONITOR = attrData.get('Monitor')
        VERBOSE = int(attrData.get('Verbose'))

        #STEPS = int(attrData.get('Steps'))
        #CLASS_MODE = attrData.get('Class_Mode')
        OPTIMIZER = attrData.get('Optimizer')
        LOSS = attrData.get('Loss')

        print('Model Data Loaded')
        #NUM_FILTERS = int(attrData.get('Num_Filters'))
        #FILTER_SIZE = int(attrData.get('Filter_Size'))
        #ACTIVATION = attrData.get('Activation')

        dataX = "x_test"
        dataY = "y_test"

        input_dim = data[dataX].shape[1:]
        output_dim = data[dataY].shape[1:]



        model = Sequential()

        #exec('model.add(Conv2D(32, (3, 3), input_shape=(32, 32, 3), activation="relu"))')

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

        model.compile(optimizer=OPTIMIZER, loss=LOSS)
        print(model.summary())

        # fitting the model
        print("Fitting the model...")
        checkpoint = ModelCheckpoint(mod_path, monitor=MONITOR, verbose=VERBOSE, save_best_only=True)
        callbacks_list = [checkpoint]

        model.fit(data["x_train"], data["y_train"],
                  batch_size=BATCH_SIZE,
                  epochs=EPOCHS,
                  validation_data=(data[dataX], data[dataY]),
                  callbacks=callbacks_list)

        model.save_weights(mod_path)
        print("Saved model to disk")
        print('######################### TRAINING COMPLETE #########################')