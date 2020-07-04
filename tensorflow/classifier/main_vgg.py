from PyQt5.QtWidgets import QWidget, QAction

from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Flatten
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

class MainVgg(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(MainVgg, self).__init__()

        MODEL = config.get('MODEL')
        SETTINGS = config.get('SETTINGS')
        TRAIN = config.get('TRAIN')
        TEST = config.get('TEST')

        name = nn+'Model_Name'

        # Define hyperparameters
        INPUT_SIZE = 256
        BATCH_SIZE = 16
        STEPS_PER_EPOCH = 200
        EPOCHS = 10
        VERBOSE = 1
        STEPS = 100

        CLASS_MODE = 'binary'
        OPTIMIZER = 'adam'
        LOSS = 'binary_crossentropy'

        nodeflow_main.createAttribute(node=n, name='Model_Name', preset='String', socket=True, plug=True, dataType='str', dataAttr='mainVgg')

        nodeflow_main.createAttribute(node=n, name='Train_Image', preset='String', socket=True, plug=True, dataType='str', dataAttr=TRAIN)
        nodeflow_main.createAttribute(node=n, name='Test_Image', preset='String', socket=True, plug=True, dataType='str', dataAttr=TEST)

        nodeflow_main.createAttribute(node=n, name='Epochs', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=EPOCHS)
        nodeflow_main.createAttribute(node=n, name='Input_Size', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=INPUT_SIZE)
        nodeflow_main.createAttribute(node=n, name='Batch_Size', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=BATCH_SIZE)
        nodeflow_main.createAttribute(node=n, name='Steps_Per_Epoch', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=STEPS_PER_EPOCH)
        nodeflow_main.createAttribute(node=n, name='Steps', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=STEPS)
        nodeflow_main.createAttribute(node=n, name='Class_Mode', preset='String', socket=True, plug=True, dataType='str', dataAttr=CLASS_MODE)
        nodeflow_main.createAttribute(node=n, name='Optimizer', preset='String', socket=True, plug=True, dataType='str', dataAttr=OPTIMIZER)
        nodeflow_main.createAttribute(node=n, name='Loss', preset='String', socket=True, plug=True, dataType='str', dataAttr=LOSS)
        nodeflow_main.createAttribute(node=n, name='Verbose', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=VERBOSE)

        nodeflow_main.createAttribute(node=n, name='Model_Path', preset='Path', socket=True, plug=True, dataType='str', dataExpr=SPL + MODEL + SPL + ADD + name + ADD + MOD)
        nodeflow_main.createAttribute(node=n, name='Settings_Path', preset='Path', socket=True, plug=True, dataType='str', dataExpr=SPL + SETTINGS + SPL + ADD + name + ADD + JSN)

class MainVggAction(QAction):
    """Model Train"""
    def __init__(self, attrData, config):
        super(MainVggAction, self).__init__()

        src = config.get('IMAGE')
        # Define hyperparameters
        INPUT_SIZE = 256 #Change this to 48 if the code is taking too long to run
        BATCH_SIZE = 16
        STEPS_PER_EPOCH = 200
        EPOCHS = 3

        vgg16 = VGG16(include_top=False, weights='imagenet', input_shape=(INPUT_SIZE, INPUT_SIZE, 3))

        # Freeze the pre-trained layers
        for layer in vgg16.layers:
            layer.trainable = False

        # Add a fully connected layer with 1 node at the end
        input_ = vgg16.input
        output_ = vgg16(input_)
        last_layer = Flatten(name='flatten')(output_)
        last_layer = Dense(1, activation='sigmoid')(last_layer)
        model = Model(input=input_, output=last_layer)

        model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

        training_data_generator = ImageDataGenerator(rescale = 1./255)
        testing_data_generator = ImageDataGenerator(rescale = 1./255)

        training_set = training_data_generator.flow_from_directory(src+'Train/',
                                                        target_size = (INPUT_SIZE, INPUT_SIZE),
                                                        batch_size = BATCH_SIZE,
                                                        class_mode = 'binary')

        test_set = testing_data_generator.flow_from_directory(src+'Test/',
                                                     target_size = (INPUT_SIZE, INPUT_SIZE),
                                                     batch_size = BATCH_SIZE,
                                                     class_mode = 'binary')

        print("""
              Caution: VGG16 model training can take up to an hour if you are not running Keras on a GPU.
              If the code takes too long to run on your computer, you may reduce the INPUT_SIZE paramater in the code to speed up model training.
              """)

        model.fit_generator(training_set, steps_per_epoch = STEPS_PER_EPOCH, epochs = EPOCHS, verbose=1)

        score = model.evaluate_generator(test_set, steps=100)

        for idx, metric in enumerate(model.metrics_names):
            print("{}: {}".format(metric, score[idx]))

        model_json = model.to_json()
        with open("model_food_vgg.json", "w") as json_file:
            json_file.write(model_json)

        model.save_weights("model_food_vgg.h5")
        print("Saved model to disk")