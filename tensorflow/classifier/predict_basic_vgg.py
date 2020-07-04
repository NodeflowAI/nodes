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

class PredictBasicVgg(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(PredictBasicVgg, self).__init__()

        DATASET = config.get('DATASET')
        MODEL = config.get('MODEL')

        name = nn+'Model_Name'

        steps = nn+'Steps'
        batch_size = nn+'Batch_Size'

        FILTER_SIZE = 3
        NUM_FILTERS = 32
        INPUT_SIZE = 32
        MAXPOOL_SIZE = 2
        BATCH_SIZE = 16
        STEPS = 20000
        EPOCHS = 10

        nodeflow_main.createAttribute(node=n, name='Model_Name', preset='String', socket=True, plug=True, dataType='str', dataAttr='model_vgg')

        nodeflow_main.createAttribute(node=n, name='Filter_Size', preset='String', socket=True, plug=False, dataType='int', dataAttr=FILTER_SIZE)
        nodeflow_main.createAttribute(node=n, name='Num_Filters', preset='String', socket=True, plug=False, dataType='int', dataAttr=NUM_FILTERS)
        nodeflow_main.createAttribute(node=n, name='Input_Size', preset='String', socket=True, plug=False, dataType='int', dataAttr=INPUT_SIZE)
        nodeflow_main.createAttribute(node=n, name='Maxpool_Size', preset='Integer', socket=True, plug=False, dataType='int', dataAttr=MAXPOOL_SIZE)
        nodeflow_main.createAttribute(node=n, name='Batch_Size', preset='Integer', socket=True, plug=False, dataType='int', dataAttr=BATCH_SIZE)
        nodeflow_main.createAttribute(node=n, name='Steps', preset='Integer', socket=True, plug=False, dataType='int', dataAttr=STEPS)
        nodeflow_main.createAttribute(node=n, name='Epoch_Steps', preset='Integer', socket=True, plug=False, dataType='int', dataExpr=steps + DIV + batch_size)
        nodeflow_main.createAttribute(node=n, name='Epochs', preset='Integer', socket=True, plug=False, dataType='int', dataAttr=EPOCHS)
        nodeflow_main.createAttribute(node=n, name='Image_Paths', preset='Image', socket=True, plug=False, dataType='img', dataAttr='')

        nodeflow_main.createAttribute(node=n, name='Dataset_Path', preset='Path', socket=True, plug=True, dataType='str', dataExpr=SPL + DATASET + SPL + ADD + name + ADD + NPZ)
        nodeflow_main.createAttribute(node=n, name='Model_Path', preset='Path', socket=True, plug=True, dataType='str', dataExpr=SPL + MODEL + SPL + ADD + name + ADD + MOD)

class PredictBasicVggAction(QAction):
    """Model Train"""
    def __init__(self, attrData, config):
        super(PredictBasicVggAction, self).__init__()

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
        '''
        test_set = testing_data_generator.flow_from_directory (dat_path,
                                                     target_size=(INPUT_SIZE, INPUT_SIZE),
                                                     batch_size=BATCH_SIZE,
                                                     class_mode=CLASS_MODE)
        '''

        for img_path in img_paths:
            test_set = image.load_img(img_path, target_size=(INPUT_SIZE, INPUT_SIZE))

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