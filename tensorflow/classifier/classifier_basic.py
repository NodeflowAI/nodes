from PyQt5.QtWidgets import QWidget, QAction
from threading import Thread
import os, re

from tensorflow.keras.models import model_from_json
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

class ClassifierBasic(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(ClassifierBasic, self).__init__()

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

        nodeflow_main.createAttribute(node=n, name='Model_Name', preset='String', socket=True, plug=True, dataType='str', dataAttr='model_cnn')

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

class ClassifierBasicAction(QAction):
    """Model Train"""
    def __init__(self, attrData, config):
        super(ClassifierBasicAction, self).__init__()

        src_path = config.get('IMAGES')
        predict_path = config.get('PREDICT')

        src_images = attrData.get('Image_Path')
        #for image in src_images:
        #    self.copyImage(image, src_path)

        npz_path = attrData.get('Dataset_Path')
        mod_path = attrData.get('Model_Path')

        INPUT_SIZE = int(attrData.get('Input_Size'))
        FILTER_SIZE = int(attrData.get('Filter_Size'))
        NUM_FILTERS = int(attrData.get('Num_Filters'))

        MAXPOOL_SIZE = int(attrData.get('Num_Filters'))
        BATCH_SIZE = int(attrData.get('Batch_Size'))

        EPOCHS = int(attrData.get('Epochs'))

        testing_data_generator = ImageDataGenerator(rescale = 1./255)
        test_set = testing_data_generator.flow_from_directory(src_path+'test/',
                                                     target_size = (INPUT_SIZE, INPUT_SIZE),
                                                     batch_size = BATCH_SIZE,
                                                     class_mode = 'binary')


        json_file = open('C:/Nodeflow/training/settings/model_cnn.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)

        # load weights into new model
        loaded_model.load_weights(mod_path)
        print("Loaded model from disk")

        # evaluate loaded model on test data
        loaded_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        score = loaded_model.evaluate_generator(test_set, steps=100)

        #for idx, metric in enumerate(loaded_model.metrics_names):
        #    print("{}: {}".format(metric, score[idx]))


        # dimensions of our images
        #img_width, img_height = 32, 32

        # load the model we saved
        # model = load_model('model.h5')
        # model.compile(loss='binary_crossentropy',
        #               optimizer='rmsprop',
        #               metrics=['accuracy'])

        # predicting images
        #img = image.load_img(predict_path+'dog.jpg', target_size=(img_width, img_height))
        #img2 = image.load_img(predict_path+'cat.jpg', target_size=(img_width, img_height))
        #x = image.img_to_array(img)
        #x = np.expand_dims(x, axis=0)

        #b = image.img_to_array(img2)
        #b = np.expand_dims(b, axis=0)

        #images = np.vstack([x, b])
        #classes = loaded_model.predict(images, batch_size=3)
        #print(classes)

    def copyImage(self, src, dst):
        img_name = os.path.basename(src)
        img_prefix = re.sub('[!@#$]', '', img_name).replace(" ", "_").replace("__", "_").replace("-", "_")
        img_path = os.path.join(dst, img_prefix)
        self.shutil.copy(src, img_path)
        self.thread(self.shutil.copy, [src, img_path])

    def thread(self, target, args):
        thread = Thread(target=target, args=args)
        thread.daemon = True
        thread.start()