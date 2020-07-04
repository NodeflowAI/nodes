from PyQt5.QtWidgets import QWidget, QAction
import os
import piexif

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.layers import Dropout, Flatten, Dense
from tensorflow.keras.preprocessing.image import ImageDataGenerator

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

class BasicCnn(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(BasicCnn, self).__init__()

        DATASET = config.get('DATASET')
        MODEL = config.get('MODEL')
        SETTINGS = config.get('SETTINGS')
        TRAIN = config.get('TRAIN')
        TEST = config.get('TEST')

        name = nn+'Model_Name'

        # Define hyperparameters
        INPUT_SIZE = 32
        SHAPE = 3
        BATCH_SIZE = 16
        STEPS_PER_EPOCH = 10
        EPOCHS = 10
        VERBOSE = 1
        STEPS = 1

        CLASS_MODE = 'binary'
        OPTIMIZER = 'adam'
        LOSS = 'binary_crossentropy'

        nodeflow_main.createAttribute(node=n, name='Model_Name', preset='String', socket=True, plug=True, dataType='str', dataAttr='Basic_cnn')

        nodeflow_main.createAttribute(node=n, name='Train_Image', preset='String', socket=True, plug=True, dataType='str', dataAttr=TRAIN)
        nodeflow_main.createAttribute(node=n, name='Test_Image', preset='String', socket=True, plug=True, dataType='str', dataAttr=TEST)

        nodeflow_main.createAttribute(node=n, name='Epochs', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=EPOCHS)
        nodeflow_main.createAttribute(node=n, name='Input_Size', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=INPUT_SIZE)
        nodeflow_main.createAttribute(node=n, name='Shape', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=SHAPE)
        nodeflow_main.createAttribute(node=n, name='Batch_Size', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=BATCH_SIZE)
        nodeflow_main.createAttribute(node=n, name='Steps_Per_Epoch', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=STEPS_PER_EPOCH)
        nodeflow_main.createAttribute(node=n, name='Steps', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=STEPS)
        nodeflow_main.createAttribute(node=n, name='Class_Mode', preset='String', socket=True, plug=True, dataType='str', dataAttr=CLASS_MODE)
        nodeflow_main.createAttribute(node=n, name='Optimizer', preset='String', socket=True, plug=True, dataType='str', dataAttr=OPTIMIZER)
        nodeflow_main.createAttribute(node=n, name='Loss', preset='String', socket=True, plug=True, dataType='str', dataAttr=LOSS)
        nodeflow_main.createAttribute(node=n, name='Verbose', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=VERBOSE)

        # LAYER 1
        L1_NUM_FILTERS = 32
        L1_FILTER_SIZE = 3
        L1_ACTIVATION = 'relu'
        nodeflow_main.createAttribute(node=n, name='L1_Num_Filters', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=L1_NUM_FILTERS)
        nodeflow_main.createAttribute(node=n, name='L1_Filter_Size', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=L1_FILTER_SIZE)
        nodeflow_main.createAttribute(node=n, name='L1_Activation', preset='String', socket=True, plug=True, dataType='str', dataAttr=L1_ACTIVATION)

        # LAYER 2
        L2_MAXPOOL_SIZE = 2
        nodeflow_main.createAttribute(node=n, name='L2_Steps', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=L2_MAXPOOL_SIZE)

        # LAYER 3
        L3_NUM_FILTERS = 32
        L3_FILTER_SIZE = 3
        L3_ACTIVATION = 'relu'
        nodeflow_main.createAttribute(node=n, name='L3_Num_Filters', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=L3_NUM_FILTERS)
        nodeflow_main.createAttribute(node=n, name='L3_Filter_Size', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=L3_FILTER_SIZE)
        nodeflow_main.createAttribute(node=n, name='L3_Activation', preset='String', socket=True, plug=True, dataType='str', dataAttr=L3_ACTIVATION)

        # LAYER 4
        L4_MAXPOOL_SIZE = 2
        nodeflow_main.createAttribute(node=n, name='L4_Steps', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=L4_MAXPOOL_SIZE)

        # LAYER 6
        L6_UNITS = 128
        L6_ACTIVATION = 'sigmoid'
        nodeflow_main.createAttribute(node=n, name='L6_Steps', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=L6_UNITS)
        nodeflow_main.createAttribute(node=n, name='L6_Activation', preset='String', socket=True, plug=True, dataType='str', dataAttr=L6_ACTIVATION)

        # LAYER 7
        L7_DROPOUT = 0.5
        nodeflow_main.createAttribute(node=n, name='L7_Dropout', preset='Float', socket=True, plug=True, dataType='flt', dataAttr=L7_DROPOUT)

        # LAYER 8
        L8_UNITS = 1
        L8_ACTIVATION = 'sigmoid'
        nodeflow_main.createAttribute(node=n, name='L8_Units', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=L8_UNITS)
        nodeflow_main.createAttribute(node=n, name='L8_Activation', preset='String', socket=True, plug=True, dataType='str', dataAttr=L8_ACTIVATION)

        nodeflow_main.createAttribute(node=n, name='Image_Paths', preset='Image', socket=True, plug=False, dataType='img', dataAttr='')
        nodeflow_main.createAttribute(node=n, name='Dataset_Path', preset='Path', socket=True, plug=True, dataType='str', dataExpr=SPL + DATASET + SPL + ADD + name + ADD + NPZ)
        nodeflow_main.createAttribute(node=n, name='Model_Path', preset='Path', socket=True, plug=True, dataType='str', dataExpr=SPL + MODEL + SPL + ADD + name + ADD + MOD)
        nodeflow_main.createAttribute(node=n, name='Settings_Path', preset='Path', socket=True, plug=True, dataType='str', dataExpr=SPL + SETTINGS + SPL + ADD + name + ADD + JSN)

class BasicCnnAction(QAction):
    """Basic Cnn Action"""
    def __init__(self, attrData, config):
        super(BasicCnnAction, self).__init__()

        mod_path = attrData.get('Model_Path')
        set_path = attrData.get('Settings_Path')

        train_path = attrData.get('Train_Image')
        test_path = attrData.get('Test_Image')

        img_paths = attrData.get('Image_Paths')
        dir = 'Girls'

        self.remove_exif_data(train_path, test_path, dir)

        # Define hyperparameters
        INPUT_SIZE = int(attrData.get('Input_Size'))
        SHAPE = int(attrData.get('Shape'))
        BATCH_SIZE = int(attrData.get('Batch_Size'))
        STEPS_PER_EPOCH = int(attrData.get('Steps_Per_Epoch'))
        EPOCHS = int(attrData.get('Epochs'))
        VERBOSE = int(attrData.get('Verbose'))
        STEPS = int(attrData.get('Steps'))
        CLASS_MODE = attrData.get('Class_Mode')
        OPTIMIZER = attrData.get('Optimizer')
        LOSS = attrData.get('Loss')

        model = Sequential()

        # LAYER 1
        L1_NUM_FILTERS = int(attrData.get('L1_Num_Filters'))
        L1_FILTER_SIZE = int(attrData.get('L1_Filter_Size'))
        L1_ACTIVATION = attrData.get('L1_Activation')
        model.add(Conv2D(L1_NUM_FILTERS, (L1_FILTER_SIZE, L1_FILTER_SIZE), input_shape=(INPUT_SIZE, INPUT_SIZE, SHAPE), activation=L1_ACTIVATION))

        # LAYER 2
        L2_MAXPOOL_SIZE = int(attrData.get('L2_Steps'))
        model.add(MaxPooling2D(pool_size=(L2_MAXPOOL_SIZE, L2_MAXPOOL_SIZE)))

        # LAYER 3
        L3_NUM_FILTERS = int(attrData.get('L3_Num_Filters'))
        L3_FILTER_SIZE = int(attrData.get('L3_Filter_Size'))
        L3_ACTIVATION = attrData.get('L3_Activation')
        model.add(Conv2D(L3_NUM_FILTERS, (L3_FILTER_SIZE, L3_FILTER_SIZE), activation=L3_ACTIVATION))

        # LAYER 4
        L4_MAXPOOL_SIZE = int(attrData.get('L4_Steps'))
        model.add(MaxPooling2D(pool_size=(L4_MAXPOOL_SIZE, L4_MAXPOOL_SIZE)))

        # LAYER 5
        model.add(Flatten())

        # LAYER 6
        L6_UNITS = int(attrData.get('L6_Steps'))
        L6_ACTIVATION = attrData.get('L6_Activation')
        model.add(Dense(units=L6_UNITS, activation=L6_ACTIVATION))

        # LAYER 7
        L7_DROPOUT = float(attrData.get('L7_Dropout'))
        model.add(Dropout(L7_DROPOUT))

        # LAYER 8
        L8_UNITS = int(attrData.get('L8_Units'))
        L8_ACTIVATION = attrData.get('L8_Activation')
        model.add(Dense(units=L8_UNITS, activation=L8_ACTIVATION))

        model.compile(optimizer=OPTIMIZER, loss=LOSS, metrics=['accuracy'])

        training_data_generator = ImageDataGenerator(rescale=1. / 255)
        testing_data_generator = ImageDataGenerator(rescale=1. / 255)

        training_set = training_data_generator.flow_from_directory(train_path,
                                                                   target_size=(INPUT_SIZE, INPUT_SIZE),
                                                                   batch_size=BATCH_SIZE,
                                                                   class_mode=CLASS_MODE)

        test_set = testing_data_generator.flow_from_directory(test_path,
                                                              target_size=(INPUT_SIZE, INPUT_SIZE),
                                                              batch_size=BATCH_SIZE,
                                                              class_mode=CLASS_MODE)

        model.fit_generator(training_set, steps_per_epoch=STEPS_PER_EPOCH, epochs=EPOCHS, verbose=VERBOSE)

        score = model.evaluate_generator(test_set, steps=STEPS)

        for idx, metric in enumerate(model.metrics_names):
            print("{}: {}".format(metric, score[idx]))

        model_json = model.to_json()

        with open(set_path, "w") as json_file:
            json_file.write(model_json)

        model.save_weights(mod_path)
        print("Saved model to disk")

    def remove_exif_data(self, train_path, test_path, dir):
        _, _, train_images = next(os.walk(train_path))
        for img in train_images:
            try:
                piexif.remove(train_path + dir + img)
            except:
                pass

        _, _, test_images = next(os.walk(test_path))
        for img in test_images:
            try:
                piexif.remove(test_path + dir + img)
            except:
                pass