from PyQt5.QtWidgets import QWidget, QAction
import numpy as np

from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image

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

class PredictBasicCnn(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(PredictBasicCnn, self).__init__()

        MODEL = config.get('MODEL')
        SETTINGS = config.get('SETTINGS')
        TEST = config.get('TEST')

        name = nn+'Model_Name'

        INPUT_SIZE = 32
        BATCH_SIZE = 16
        CLASS_MODE = 'binary'
        LOSS = 'binary_crossentropy'
        OPTIMIZER = 'adam'
        STEPS = 100
        PREDICT_BATCH_SIZE = 3

        nodeflow_main.createAttribute(node=n, name='Model_Name', preset='String', socket=True, plug=True, dataType='str', dataAttr='model_cnn')

        nodeflow_main.createAttribute(node=n, name='Class_Mode', preset='String', socket=True, plug=True, dataType='str', dataAttr=CLASS_MODE)
        nodeflow_main.createAttribute(node=n, name='Loss', preset='String', socket=True, plug=True, dataType='str', dataAttr=LOSS)
        nodeflow_main.createAttribute(node=n, name='Optimizer', preset='String', socket=True, plug=True, dataType='str', dataAttr=OPTIMIZER)
        nodeflow_main.createAttribute(node=n, name='Input_Size', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=INPUT_SIZE)
        nodeflow_main.createAttribute(node=n, name='Batch_Size', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=BATCH_SIZE)
        nodeflow_main.createAttribute(node=n, name='Steps', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=STEPS)
        nodeflow_main.createAttribute(node=n, name='Predict_Batch_Size', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=PREDICT_BATCH_SIZE)

        nodeflow_main.createAttribute(node=n, name='Image_Paths', preset='Image', socket=True, plug=True, dataType='img', dataAttr='')
        nodeflow_main.createAttribute(node=n, name='Image_Dir', preset='String', socket=True, plug=True, dataType='str', dataAttr=TEST)

        nodeflow_main.createAttribute(node=n, name='Model_Path', preset='Path', socket=True, plug=True, dataType='str', dataExpr=SPL + MODEL + SPL + ADD + name + ADD + MOD)
        nodeflow_main.createAttribute(node=n, name='Settings_Path', preset='Path', socket=True, plug=True, dataType='str', dataExpr=SPL + SETTINGS + SPL + ADD + name + ADD + JSN)

class PredictBasicCnnAction(QAction):
    """Model Train"""
    def __init__(self, attrData, config):
        super(PredictBasicCnnAction, self).__init__()

        img_paths = attrData.get('Image_Paths')
        mod_path = attrData.get('Model_Path')
        set_path = attrData.get('Settings_Path')
        dat_path = attrData.get('Image_Dir')

        # Define Hyperparameters
        INPUT_SIZE = int(attrData.get('Input_Size'))
        BATCH_SIZE = int(attrData.get('Batch_Size'))
        CLASS_MODE = attrData.get('Class_Mode')
        LOSS = attrData.get('Loss')
        OPTIMIZER = attrData.get('Optimizer')
        STEPS = int(attrData.get('Steps'))
        PREDICT_BATCH_SIZE = int(attrData.get('Predict_Batch_Size'))

        testing_data_generator = ImageDataGenerator(rescale=1./255)
        test_set = testing_data_generator.flow_from_directory(dat_path,
                                                     target_size=(INPUT_SIZE, INPUT_SIZE),
                                                     batch_size=BATCH_SIZE,
                                                     class_mode=CLASS_MODE)


        json_file = open(set_path, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)

        # load weights into new model
        loaded_model.load_weights(mod_path)
        print("Loaded model from disk")

        # evaluate loaded model on test data
        loaded_model.compile(loss=LOSS, optimizer=OPTIMIZER, metrics=['accuracy'])

        score = loaded_model.evaluate_generator(test_set, steps=STEPS)

        for idx, metric in enumerate(loaded_model.metrics_names):
            print("{}: {}".format(metric, score[idx]))

        # dimensions of our images
        img_width, img_height = 32, 32

        xList = []

        # predicting images
        for img_path in img_paths:
            img = image.load_img(img_path, target_size=(img_width, img_height))

            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            xList.append(x)

        images = np.vstack(xList)
        classes = loaded_model.predict(images, batch_size=PREDICT_BATCH_SIZE)

        print(classes)