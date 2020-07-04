from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
from skimage.transform import resize
import numpy as np

from PyQt5.QtWidgets import QWidget, QAction

# Action Settings
import configparser
config = configparser.ConfigParser()
config.read('config/action_settings.ini')
DOT = config['ACTION']['DOT']
SEP = config['ACTION']['SEP']
ADD = config['ACTION']['ADD']
SUB = config['ACTION']['SUB']
DIV = config['ACTION']['DIV']
MUL = config['ACTION']['MUL']
SPL = config['ACTION']['SPL']
NPZ = config['ACTION']['NPZ']
MOD = config['ACTION']['MOD']
JSN = config['ACTION']['JSN']
N = '\n'
T = '\t'
TT = '\t\t'
TTT = '\t\t\t'

class ModelDisplay(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(ModelDisplay, self).__init__()

        name = nn+'Dataset_Name'

        DATASET = config.get('DATASET')
        MODEL = config.get('MODEL')

        nodeflow_main.createAttribute(node=n, name='Dataset_Name', preset='String', socket=True, plug=True, dataType='str', dataAttr='')
        nodeflow_main.createAttribute(node=n, name='Dataset_Path', preset='Path', socket=False, plug=True, dataType='str', dataExpr=SPL + DATASET + SPL + ADD + name + ADD + NPZ)
        nodeflow_main.createAttribute(node=n, name='Model_Path', preset='Path', socket=False, plug=True, dataType='str', dataExpr=SPL + MODEL + SPL + ADD + name + ADD + MOD)
        nodeflow_main.createAttribute(node=n, name='Size', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=1)
        nodeflow_main.createAttribute(node=n, name='Row', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=1)
        nodeflow_main.createAttribute(node=n, name='Column', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=1)


class ModelDisplayAction(QAction):
    """Model Create"""
    def __init__(self, attrData, config):
        super(ModelDisplayAction, self).__init__()

        NPZ_FILE = attrData.get('Dataset_Path')
        MOD_FILE = attrData.get('Model_Path')
        SIZE = int(attrData.get('Size'))
        ROW = int(attrData.get('Row'))
        COLUMN = int(attrData.get('Column'))

        # loading data
        print("Loading previously created data...")
        data = np.load(NPZ_FILE)

        # loading the previous model
        print("Loading Model")
        model = load_model(MOD_FILE)

        # making a prediction on test dataset
        y_pred = model.predict(data["x_test"])


        # plotting some random images of the dataset
        for i in np.random.random_integers(COLUMN, ROW, size=SIZE):

            # input image
            plt.subplot(221)
            plt.imshow(data["x_test"][i,:,:,0], cmap="Greys_r")
            plt.title("Low res. input image")
            plt.axis("off")

            # target image
            plt.subplot(222)
            plt.imshow(data["y_test"][i,:,:,0], cmap="Greys_r")
            plt.title("High res. target image")
            plt.axis("off")

            # rescaled image
            plt.subplot(223)
            resized = resize(data["x_test"][i,:,:,0], (128, 128), mode="constant")
            plt.imshow(resized, cmap="Greys_r")
            plt.title("Rescaled high res. image")
            plt.axis("off")

            # model2 predicted image
            plt.subplot(224)
            plt.imshow(y_pred[i,:,:,0], cmap="Greys_r")
            plt.title("Model high res. reconstruction")
            plt.axis("off")

            plt.show()