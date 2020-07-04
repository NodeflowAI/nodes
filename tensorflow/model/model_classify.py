import os, cv2, re, random
from PyQt5.QtWidgets import QWidget, QAction

import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras import layers, models, optimizers
from tensorflow.keras import backend as K
from sklearn.model_selection import train_test_split

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
CSV = config['ACTION']['CSV']


class ModelClassify(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(ModelClassify, self).__init__()

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

        BATCH_SIZE = 16
        EPOCHS = 10
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

        nodeflow_main.createAttribute(node=n, name='Image_Dir', preset='String', socket=True, plug=True, dataType='str', dataAttr='dogs_cats')
        nodeflow_main.createAttribute(node=n, name='Dataset_Path', preset='Path', socket=True, plug=True, dataType='str', dataExpr=SPL + DATASET + SPL + ADD + name + ADD + NPZ)
        nodeflow_main.createAttribute(node=n, name='Model_Path', preset='Path', socket=True, plug=True, dataType='str', dataExpr=SPL + MODEL + SPL + ADD + name + ADD + MOD)
        nodeflow_main.createAttribute(node=n, name='Model_Weights_Path', preset='Path', socket=True, plug=True, dataType='str', dataExpr=SPL + MODEL + SPL + ADD + name + ADD + '"_weights"' + ADD + MOD)
        nodeflow_main.createAttribute(node=n, name='Settings_Path', preset='Path', socket=True, plug=True, dataType='str', dataExpr=SPL + SETTINGS + SPL + ADD + name + ADD + JSN)
        nodeflow_main.createAttribute(node=n, name='CSV_Path', preset='Path', socket=True, plug=True, dataType='str', dataExpr=SPL + SETTINGS + SPL + ADD + name + ADD + CSV)


class ModelClassifyAction(QAction):
    """Model Train"""
    def __init__(self, attrData, config):
        super(ModelClassifyAction, self).__init__()

        print("Model Classify")
        print(config)

        npz_path = attrData.get('Dataset_Path')
        # data = np.load(npz_path)
        mod_path = attrData.get('Model_Path')
        wgt_path = attrData.get('Model_Weights_Path')
        csv_path = attrData.get('CSV_Path')

        TRAIN_DIR = config.get('TRAIN')
        TEST_DIR = config.get('TEST')

        epochs = int(attrData.get('Epochs'))
        batch_size = int(attrData.get('Batch_Size'))

        optimizer = attrData.get('Optimizer')
        loss = attrData.get('Loss')
        monitor = attrData.get('Monitor')
        verbose = int(attrData.get('Verbose'))

        print('Data loaded')

        self.img_width = 150
        self.img_height = 150

        train_images_dogs_cats = [TRAIN_DIR + i for i in os.listdir(TRAIN_DIR)]  # use this for full dataset
        test_images_dogs_cats = [TEST_DIR + i for i in os.listdir(TEST_DIR)]

        print('Train directories')

        train_images_dogs_cats.sort(key=self.natural_keys)
        train_images_dogs_cats = train_images_dogs_cats[0:1300] + train_images_dogs_cats[12500:13800]

        test_images_dogs_cats.sort(key=self.natural_keys)

        print('Sort directories')
        print(train_images_dogs_cats)

        X, Y = self.prepare_data(train_images_dogs_cats)
        print(K.image_data_format())

        # First split the data in two sets, 80% for training, 20% for Val/Test)
        print('First split the data in two sets')

        X_train, X_val, Y_train, Y_val = train_test_split(X, Y, test_size=0.2, random_state=1)

        print('Set samples')

        nb_train_samples = len(X_train)
        nb_validation_samples = len(X_val)

        # Building the model
        print('Building the model')
        model = models.Sequential()

        model.add(layers.Conv2D(32, (3, 3), input_shape=(self.img_width, self.img_height, 3)))
        model.add(layers.Activation('relu'))
        model.add(layers.MaxPooling2D(pool_size=(2, 2)))

        model.add(layers.Conv2D(32, (3, 3)))
        model.add(layers.Activation('relu'))
        model.add(layers.MaxPooling2D(pool_size=(2, 2)))

        model.add(layers.Conv2D(64, (3, 3)))
        model.add(layers.Activation('relu'))
        model.add(layers.MaxPooling2D(pool_size=(2, 2)))

        model.add(layers.Flatten())
        model.add(layers.Dense(64))
        model.add(layers.Activation('relu'))
        model.add(layers.Dropout(0.5))
        model.add(layers.Dense(1))
        model.add(layers.Activation('sigmoid'))

        model.compile(loss='binary_crossentropy',
                      optimizer='rmsprop',
                      metrics=['accuracy'])

        model.summary()

        # This is the augmentation configuration we will use for training and validation
        train_datagen = ImageDataGenerator(
            rescale=1. / 255,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True)

        val_datagen = ImageDataGenerator(
            rescale=1. / 255,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True)

        # Prepare generators for training and validation sets
        train_generator = train_datagen.flow(np.array(X_train), Y_train, batch_size=batch_size)
        validation_generator = val_datagen.flow(np.array(X_val), Y_val, batch_size=batch_size)

        # Start training the model!
        history = model.fit_generator(
            train_generator,
            steps_per_epoch=nb_train_samples // batch_size,
            epochs=epochs,
            validation_data=validation_generator,
            validation_steps=nb_validation_samples // batch_size
        )

        print("Saved model to disk")
        print('######################### TRAINING COMPLETE #########################')

        # Save model to disk
        model.save_weights(wgt_path)
        model.save(mod_path)

        # Generate X_test and Y_test
        X_test, Y_test = self.prepare_data(test_images_dogs_cats)  # Y_test in this case will be []
        test_datagen = ImageDataGenerator(rescale=1. / 255)

        # Generate .csv
        test_generator = val_datagen.flow(np.array(X_test), batch_size=batch_size)
        prediction_probabilities = model.predict_generator(test_generator, verbose=verbose)

        counter = range(1, len(test_images_dogs_cats) + 1)
        solution = pd.DataFrame({"id": counter, "label": list(prediction_probabilities)})
        cols = ['label']

        for col in cols:
            solution[col] = solution[col].map(lambda x: str(x).lstrip('[').rstrip(']')).astype(float)

        solution.to_csv(csv_path, index=False)

        print("CSV model to disk")

    def atoi(self, text):
        return int(text) if text.isdigit() else text

    def natural_keys(self, text):
        return [self.atoi(c) for c in re.split('(\d+)', text)]

    def prepare_data(self, list_of_images):
        """
        Returns two arrays:
            x is an array of resized images
            y is an array of labels
        """
        x = []  # images as arrays
        y = []  # labels

        for image in list_of_images:
            x.append(cv2.resize(cv2.imread(image), (self.img_width, self.img_height), interpolation=cv2.INTER_CUBIC))

        for i in list_of_images:
            if 'dog' in i:
                y.append(1)
            elif 'cat' in i:
                y.append(0)
            # else:
            # print('neither cat nor dog name present in images')

        return x, y