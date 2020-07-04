import os, cv2, re, random
from PyQt5.QtWidgets import QWidget, QAction

import configparser

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
CSV = config['ACTION']['CSV']


class ModelAnimals(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(ModelAnimals, self).__init__()

        DATASET = config.get('DATASET')
        MODEL = config.get('MODEL')
        SETTINGS = config.get('SETTINGS')
        WEIGHTS = config.get('WEIGHTS')

        VALIDATION = config.get('VALIDATION')

        name = nn+'Train_Name'

        BATCH_SIZE = 16
        EPOCHS = 10
        OPTIMIZER = 'rmsprop'
        LOSS = 'binary_crossentropy'
        MONITOR = 'val_loss'
        VERBOSE = 1

        nodeflow_main.createAttribute(node=n, name='Train_Name', preset='String', socket=True, plug=True, dataType='str', dataAttr='')

        nodeflow_main.createAttribute(node=n, name='Image_Size', preset='Integer', socket=True, plug=False, dataType='int', dataAttr=150)

        nodeflow_main.createAttribute(node=n, name='Epochs', preset='Integer', socket=True, plug=False, dataType='int', dataAttr=EPOCHS)
        nodeflow_main.createAttribute(node=n, name='Batch_Size', preset='Integer', socket=True, plug=False, dataType='int', dataAttr=BATCH_SIZE)
        nodeflow_main.createAttribute(node=n, name='Optimizer', preset='String', socket=True, plug=False, dataType='str', dataAttr=OPTIMIZER)
        nodeflow_main.createAttribute(node=n, name='Loss', preset='String', socket=True, plug=False, dataType='str', dataAttr=LOSS)
        nodeflow_main.createAttribute(node=n, name='Monitor', preset='String', socket=True, plug=False, dataType='str', dataAttr=MONITOR)
        nodeflow_main.createAttribute(node=n, name='Verbose', preset='Integer', socket=True, plug=False, dataType='int', dataAttr=VERBOSE)

        nodeflow_main.createAttribute(node=n, name='Image_Dir', preset='String', socket=True, plug=True, dataType='str', dataAttr='girl')
        nodeflow_main.createAttribute(node=n, name='Image_Path', preset='String', socket=True, plug=True, dataType='str', dataAttr='girl')

        nodeflow_main.createAttribute(node=n, name='Dataset_Path', preset='Path', socket=True, plug=True, dataType='str', dataExpr=SPL + DATASET + SPL + ADD + name + ADD + NPZ)
        nodeflow_main.createAttribute(node=n, name='Model_Path', preset='Path', socket=True, plug=True, dataType='str', dataExpr=SPL + MODEL + SPL + ADD + name + ADD + MOD)
        nodeflow_main.createAttribute(node=n, name='Weights_Path', preset='Path', socket=True, plug=True, dataType='str', dataExpr=SPL + WEIGHTS + SPL + ADD + name + ADD + '"_weights"' + ADD + MOD)
        nodeflow_main.createAttribute(node=n, name='Validation_Path', preset='Path', socket=True, plug=True, dataType='str', dataExpr=SPL + VALIDATION + SPL + ADD + name)
        nodeflow_main.createAttribute(node=n, name='Settings_Path', preset='Path', socket=True, plug=True, dataType='str', dataExpr=SPL + SETTINGS + SPL + ADD + name + ADD + JSN)
        nodeflow_main.createAttribute(node=n, name='CSV_Path', preset='Path', socket=True, plug=True, dataType='str', dataExpr=SPL + SETTINGS + SPL + ADD + name + ADD + CSV)


class ModelAnimalsAction(QAction):
    """Model Train"""
    def __init__(self, attrData, config):
        super(ModelAnimalsAction, self).__init__()

        from tensorflow.keras.preprocessing.image import ImageDataGenerator
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Conv2D, MaxPooling2D
        from tensorflow.keras.layers import Activation, Dropout, Flatten, Dense
        from tensorflow.keras import backend as K

        import numpy as np

        print("Model Classify")
        print(config)

        npz_path = attrData.get('Dataset_Path')
        # data = np.load(npz_path)
        mod_path = attrData.get('Model_Path')
        wgt_path = attrData.get('Weights_Path')
        csv_path = attrData.get('CSV_Path')

        img_dir = attrData.get('Image_Dir')
        train_path = config.get('TRAIN')

        train_data_dir = train_path + '/' + img_dir
        validation_data_dir = config.get('VALIDATION')

        img_size = int(attrData.get('Image_Size'))

        epochs = int(attrData.get('Epochs'))
        batch_size = int(attrData.get('Batch_Size'))

        optimizer = attrData.get('Optimizer')
        loss = attrData.get('Loss')
        monitor = attrData.get('Monitor')
        verbose = int(attrData.get('Verbose'))

        print('Data loaded')

        # dimensions of our images.
        img_width, img_height = img_size, img_size

        nb_train_samples = 2000
        nb_validation_samples = 800

        if K.image_data_format() == 'channels_first':
            input_shape = (3, img_width, img_height)
        else:
            input_shape = (img_width, img_height, 3)

        model = Sequential()
        model.add(Conv2D(32, (3, 3), input_shape=input_shape))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Conv2D(32, (3, 3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Conv2D(64, (3, 3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Flatten())
        model.add(Dense(64))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))
        model.add(Dense(1))
        model.add(Activation('sigmoid'))

        model.compile(loss=loss,
                      optimizer=optimizer,
                      metrics=['accuracy'])

        # this is the augmentation configuration we will use for training
        train_datagen = ImageDataGenerator(
            rescale=1. / 255,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True)

        # this is the augmentation configuration we will use for testing:
        # only rescaling
        test_datagen = ImageDataGenerator(rescale=1. / 255)

        train_generator = train_datagen.flow_from_directory(
            train_data_dir,
            target_size=(img_width, img_height),
            batch_size=batch_size,
            class_mode='binary')

        validation_generator = test_datagen.flow_from_directory(
            validation_data_dir,
            target_size=(img_width, img_height),
            batch_size=batch_size,
            class_mode='binary')

        model.fit_generator(
            train_generator,
            steps_per_epoch=nb_train_samples // batch_size,
            epochs=epochs,
            validation_data=validation_generator,
            validation_steps=nb_validation_samples // batch_size)

        model.save_weights(wgt_path)