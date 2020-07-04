from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel, QGridLayout, QScrollArea
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import os
import random

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure, SubplotParams

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

class VisualizeDataset(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(VisualizeDataset, self).__init__()

        DATASET = config.get('DATASET')
        MODEL = config.get('MODEL')
        SETTINGS = config.get('SETTINGS')
        IMAGE = config.get('IMAGE')

        name = nn+'Model_Name'
        img_dir = nn+'Image_Dir'

        ROWS = 5
        COLUMNS = 5
        FIG_X = 10
        FIG_Y = 10

        nodeflow_main.createAttribute(node=n, name='Model_Name', preset='String', socket=True, plug=True, dataType='str', dataAttr='model_cnn')

        nodeflow_main.createAttribute(node=n, name='Image_Dir', preset='String', socket=True, plug=True, dataType='str', dataAttr='Vagina')
        nodeflow_main.createAttribute(node=n, name='Image_Path', preset='String', socket=True, plug=True, dataType='str', dataAttr=IMAGE)

        nodeflow_main.createAttribute(node=n, name='Num_Rows', preset='String', socket=True, plug=False, dataType='int', dataAttr=ROWS)
        nodeflow_main.createAttribute(node=n, name='Num_Columns', preset='String', socket=True, plug=False, dataType='int', dataAttr=COLUMNS)

        nodeflow_main.createAttribute(node=n, name='Fig_X', preset='String', socket=True, plug=False, dataType='int', dataAttr=FIG_X)
        nodeflow_main.createAttribute(node=n, name='Fig_Y', preset='String', socket=True, plug=False, dataType='int', dataAttr=FIG_Y)

        nodeflow_main.createAttribute(node=n, name='Image_Paths', preset='Path', socket=True, plug=False, dataType='str', dataExpr=SPL + IMAGE + SPL + ADD + img_dir + SEP)
        nodeflow_main.createAttribute(node=n, name='Dataset_Path', preset='Path', socket=True, plug=True, dataType='str', dataExpr=SPL + DATASET + SPL + ADD + name + ADD + NPZ)
        nodeflow_main.createAttribute(node=n, name='Model_Path', preset='Path', socket=True, plug=True, dataType='str', dataExpr=SPL + MODEL + SPL + ADD + name + ADD + MOD)
        nodeflow_main.createAttribute(node=n, name='Settings_Path', preset='Path', socket=True, plug=True, dataType='str', dataExpr=SPL + SETTINGS + SPL + ADD + name + ADD + JSN)


class VisualizeDatasetAction(QMainWindow):
    """Model Train"""
    def __init__(self, attrData, config):
        super(VisualizeDatasetAction, self).__init__()

        img_path = attrData.get('Image_Paths')
        img_row = int(attrData.get('Num_Rows'))
        img_col = int(attrData.get('Num_Columns'))
        img_num = img_col * img_row

        fig_x = int(attrData.get('Fig_X'))
        fig_y = int(attrData.get('Fig_Y'))

        # Get list of file names
        _, _, images = next(os.walk(img_path))

        print(images)
        for idx, img in enumerate(random.sample(images, img_num)):
            self.img_read = plt.imread(img_path+img)
            print(self.img_read)

        self.gridLayout = QGridLayout()
        self.window = QWidget()
        self.window.setContentsMargins(0, 0, 0, 0)
        self.window.setLayout(self.gridLayout)

        self.images = []
        self.buildLayout(img_num, img_row, img_col)
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

        ax.imshow(self.img_read)

        ax.set_axis_off()
        canvas.draw()
        size = canvas.size()
        width, height = size.width(), size.height()
        im = QImage(canvas.buffer_rgba(), width, height, QImage.Format_ARGB32)

        return QPixmap(im)
