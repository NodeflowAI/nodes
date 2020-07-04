from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel, QGridLayout, QScrollArea
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
import configparser
import numpy as np
from PIL import Image
import cv2

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure, SubplotParams
from tensorflow.keras.models import load_model

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

class ModelView(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(ModelView, self).__init__()

        DATASET = config.get('DATASET')
        MODEL = config.get('MODEL')

        name = nn+'Model_Name'

        IMAGES = 30
        ROW = 10
        COL = 10

        nodeflow_main.createAttribute(node=n, name='Model_Name', preset='String', socket=True, plug=True, dataType='str', dataAttr='ImageGirlDataset')
        nodeflow_main.createAttribute(node=n, name='Cmap', preset='String', socket=True, plug=True, dataType='str', dataAttr='Greys_r')
        nodeflow_main.createAttribute(node=n, name='Images', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=IMAGES)
        nodeflow_main.createAttribute(node=n, name='Images_Column', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=COL)
        nodeflow_main.createAttribute(node=n, name='Images_Row', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=ROW)
        nodeflow_main.createAttribute(node=n, name='Dataset_Path', preset='Path', socket=True, plug=True, dataType='str', dataExpr=SPL + DATASET + SPL + ADD + name + ADD + NPZ)
        nodeflow_main.createAttribute(node=n, name='Model_Path', preset='Path', socket=True, plug=True, dataType='str', dataExpr=SPL + MODEL + SPL + ADD + name + ADD + MOD)

class ModelViewAction(QMainWindow):
    """Model Create"""
    def __init__(self, attrData, config):
        super(ModelViewAction, self).__init__()

        print(attrData)
        self.attrData = attrData

        self.npz_file = attrData.get('Dataset_Path')
        self.mod_file = attrData.get('Model_Path')

        self.img_num = int(attrData.get('Images'))
        self.img_row = int(attrData.get('Images_Row'))
        self.img_col = int(attrData.get('Images_Column'))

        # loading data
        print("Loading previously created data...")
        self.data = np.load(self.npz_file)

        # loading the previous model
        print("Loading Model")
        self.model = load_model(self.mod_file)

        # making a prediction on test dataset
        self.y_pred = self.model.predict(self.data["x_test"])

        self.gridLayout = QGridLayout()
        self.window = QWidget()
        self.window.setContentsMargins(0, 0, 0, 0)
        self.window.setLayout(self.gridLayout)

        self.images = []
        self.buildLayout(self.img_num, self.img_row, self.img_col)
        self.window.update()

    def buildLayout(self, img_num, img_row, img_col):
        for i in range(img_row):
            l = []
            for j in range(img_col):
                img_num += 1

                self.widget = QWidget()
                self.widget.setContentsMargins(0, 0, 0, 0)
                self.label = QLabel(self.widget)
                self.image = self.ColourMap(img_num)
                self.label.setPixmap(self.image)
                self.label.setContentsMargins(0, 0, 0, 0)
                self.label.setFixedSize(100, 100)
                l.append(self.label)
                self.gridLayout.addWidget(self.label, i, j)
                self.gridLayout.setColumnMinimumWidth(j, 0)
                self.gridLayout.setContentsMargins(0, 0, 0, 0)
                self.gridLayout.setSpacing(0)

            self.images.append(l)
            self.gridLayout.setRowMinimumHeight(i, 0)

        self.scroll = QScrollArea()
        self.scroll.setMinimumHeight(1000)
        self.scroll.setContentsMargins(0, 0, 0, 0)
        self.scroll.setWidget(self.window)
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.update()

        self.setCentralWidget(self.scroll)

    def ColourMap(self, img):

        sp = SubplotParams(left=0., bottom=0., right=1., top=1.)
        fig = Figure((1, 1), subplotpars=sp)
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        #test = self.numpy2pil(self.y_pred)
        ax.imshow(self.y_pred[img, img:, img:, 0])
        ax.set_axis_off()
        canvas.draw()
        size = canvas.size()
        width, height = size.width(), size.height()

        #RGB_img = cv2.cvtColor(canvas.buffer_rgba(), cv2.COLOR_BGR2RGB)

        img = QImage(canvas.buffer_rgba(), width, height, QImage.Format_ARGB32)
        return QPixmap(img)


    def numpy2pil(np_array: np.ndarray):
        """
        Convert an HxWx3 numpy array into an RGB Image
        """

        assert_msg = 'Input shall be a HxWx3 ndarray'
        assert isinstance(np_array, np.ndarray), assert_msg
        assert len(np_array.shape) == 3, assert_msg
        assert np_array.shape[2] == 3, assert_msg

        img = Image.fromarray(np_array, 'RGB')
        return img
