from PyQt5.QtWidgets import QWidget, QAction
import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.models import save_model
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

class CompileModel(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(CompileModel, self).__init__()

        DATASET = config.get('DATASET')
        MODEL = config.get('MODEL')
        SETTINGS = config.get('SETTINGS')
        TEST = config.get('TEST')

        name = nn+'Model_Name'

        LOSS = 'binary_crossentropy'
        OPTIMIZER = 'adam'

        # Define hyperparameters
        DATAX = "x_test"
        DATAY = "y_test"
        TRAINX = "x_train"
        TRAINY = "y_train"
        SHAPE = 3
        STEPS = 1
        BATCH_SIZE = 16
        STEPS_PER_EPOCH = 10
        EPOCHS = 10
        VERBOSE = 1
        MONITOR = 'val_loss'
        NUM_FILTERS = 32
        FILTER_SIZE = 3
        ACTIVATION = 'relu'

        nodeflow_main.createAttribute(node=n, name='Model_Name', preset='String', socket=True, plug=True, dataType='str', dataAttr='')

        nodeflow_main.createAttribute(node=n, name='Epochs', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=EPOCHS)
        nodeflow_main.createAttribute(node=n, name='DataX', preset='String', socket=True, plug=True, dataType='str', dataAttr=DATAX)
        nodeflow_main.createAttribute(node=n, name='DataY', preset='String', socket=True, plug=True, dataType='str', dataAttr=DATAY)
        nodeflow_main.createAttribute(node=n, name='TrainX', preset='String', socket=True, plug=True, dataType='str', dataAttr=TRAINX)
        nodeflow_main.createAttribute(node=n, name='TrainY', preset='String', socket=True, plug=True, dataType='str', dataAttr=TRAINY)

        nodeflow_main.createAttribute(node=n, name='Shape', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=SHAPE)
        nodeflow_main.createAttribute(node=n, name='Batch_Size', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=BATCH_SIZE)
        nodeflow_main.createAttribute(node=n, name='Steps_Per_Epoch', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=STEPS_PER_EPOCH)
        nodeflow_main.createAttribute(node=n, name='Steps', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=STEPS)

        nodeflow_main.createAttribute(node=n, name='Optimizer', preset='String', socket=True, plug=True, dataType='str', dataAttr=OPTIMIZER)
        nodeflow_main.createAttribute(node=n, name='Loss', preset='String', socket=True, plug=True, dataType='str', dataAttr=LOSS)
        nodeflow_main.createAttribute(node=n, name='Monitor', preset='String', socket=True, plug=False, dataType='str', dataAttr=MONITOR)
        nodeflow_main.createAttribute(node=n, name='Verbose', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=VERBOSE)

        nodeflow_main.createAttribute(node=n, name='Num_Filters', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=NUM_FILTERS)
        nodeflow_main.createAttribute(node=n, name='Filter_Size', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=FILTER_SIZE)
        nodeflow_main.createAttribute(node=n, name='Activation', preset='String', socket=True, plug=True, dataType='str', dataAttr=ACTIVATION)

        nodeflow_main.createAttribute(node=n, name='Loss', preset='String', socket=True, plug=True, dataType='str', dataAttr=LOSS)
        nodeflow_main.createAttribute(node=n, name='Optimizer', preset='String', socket=True, plug=True, dataType='str', dataAttr=OPTIMIZER)

        nodeflow_main.createAttribute(node=n, name='Dataset_Path', preset='Path', socket=True, plug=True, dataType='str', dataExpr=SPL + DATASET + SPL + ADD + name + ADD + NPZ)
        nodeflow_main.createAttribute(node=n, name='Model_Path', preset='Path', socket=True, plug=True, dataType='str', dataExpr=SPL + MODEL + SPL + ADD + name + ADD + MOD)
        nodeflow_main.createAttribute(node=n, name='Settings_Path', preset='Path', socket=True, plug=True, dataType='str', dataExpr=SPL + SETTINGS + SPL + ADD + name + ADD + JSN)

class CompileModelAction(QAction):
    """Model Train"""

    def __init__(self, attrData, config):
        super(CompileModelAction, self).__init__()

        npz_path = attrData.get('Dataset_Path')
        mod_path = attrData.get('Model_Path')
        set_path = attrData.get('Settings_Path')
        data = np.load(npz_path)
        print("Data Loaded")

        #train_path = config.get('TRAIN')
        #test_path = config.get('TEST')

        #MODEL = attrData.get('Model_Name')

        # Define hyperparameters
        EPOCHS = int(attrData.get('Epochs'))
        BATCH_SIZE = int(attrData.get('Batch_Size'))
        MONITOR = attrData.get('Monitor')
        VERBOSE = int(attrData.get('Verbose'))
        OPTIMIZER = attrData.get('Optimizer')
        LOSS = attrData.get('Loss')
        STEPS = attrData.get('Steps')
        dataX = attrData.get('DataX')
        dataY = attrData.get('DataY')
        trainX = attrData.get('TrainX')
        trainY = attrData.get('TrainY')

        input_dim = data[dataX].shape[1:]
        output_dim = data[dataY].shape[1:]
        print('Model Data Loaded')

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

        model.fit(data[trainX], data[trainY],
                  batch_size=BATCH_SIZE,
                  epochs=EPOCHS,
                  validation_data=(data[dataX], data[dataY]),
                  callbacks=callbacks_list)

        model.save_weights(mod_path)

        #score = model.evaluate_generator(data, steps=STEPS)

        #for idx, metric in enumerate(model.metrics_names):
            #print("{}: {}".format(metric, score[idx]))

        model_json = model.to_json()

        with open(set_path, "w") as json_file:
            json_file.write(model_json)

        model.save_weights(mod_path)
        print("Saved model to disk")

        print('######################### TRAINING COMPLETE #########################')