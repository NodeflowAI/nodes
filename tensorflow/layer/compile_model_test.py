from PyQt5.QtWidgets import QWidget, QAction

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

class CompileModel(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(CompileModel, self).__init__()

        LOSS = 'binary_crossentropy'
        OPTIMIZER = 'adam'

        nodeflow_main.createAttribute(node=n, name='Model_Name', preset='String', socket=True, plug=True, dataType='str', dataAttr='')

        # Define hyperparameters
        INPUT_SIZE = 32
        SHAPE = 3
        BATCH_SIZE = 16
        STEPS_PER_EPOCH = 10
        EPOCHS = 10
        VERBOSE = 1
        STEPS = 1
        CLASS_MODE = 'binary'
        NUM_FILTERS = 32
        FILTER_SIZE = 3
        ACTIVATION = 'relu'

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

        nodeflow_main.createAttribute(node=n, name='Num_Filters', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=NUM_FILTERS)
        nodeflow_main.createAttribute(node=n, name='Filter_Size', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=FILTER_SIZE)
        nodeflow_main.createAttribute(node=n, name='Activation', preset='String', socket=True, plug=True, dataType='str', dataAttr=ACTIVATION)

        nodeflow_main.createAttribute(node=n, name='Loss', preset='String', socket=True, plug=True, dataType='str', dataAttr=LOSS)
        nodeflow_main.createAttribute(node=n, name='Optimizer', preset='String', socket=True, plug=True, dataType='str', dataAttr=OPTIMIZER)

class CompileModelAction(QAction):
    """Model Train"""

    def __init__(self, attrData, config):
        super(CompileModelAction, self).__init__()

        mod_path = config.get('MODEL')

        train_path = config.get('TRAIN')
        test_path = config.get('TEST')
        print('Compile')

        MODEL = attrData.get('Model_Name')

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

        #(globals()[MODEL]) = Sequential()
        #model = globals()[MODEL]
        #print(model)
        NUM_FILTERS = int(attrData.get('Num_Filters'))
        FILTER_SIZE = int(attrData.get('Filter_Size'))
        ACTIVATION = attrData.get('Activation')

        model = Sequential()

        model.add(Conv2D(NUM_FILTERS, (FILTER_SIZE, FILTER_SIZE), input_shape=(INPUT_SIZE, INPUT_SIZE, SHAPE), activation=ACTIVATION))


        model.add(MaxPooling2D(pool_size=(2, 2)))
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

        #with open(set_path, "w") as json_file:
            #json_file.write(model_json)

        model.save_weights(mod_path)
        print("Saved model to disk")