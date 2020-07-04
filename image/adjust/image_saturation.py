from PyQt5.QtWidgets import QWidget, QAction
from PyQt5 import QtCore

import os
from PIL import Image, ImageEnhance

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

BRIGHTNESS_FACTOR_MIN = 0.5
BRIGHTNESS_FACTOR_MAX = 1.5

class ImageSaturation(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(ImageSaturation, self).__init__()

        name = nn + 'Image_Name'

        nodeflow_main.createAttribute(node=n, name='Image_Sat', preset='Image', socket=True, plug=True, dataType='img', dataExpr=name)
        nodeflow_main.createAttribute(node=n, name='Image_Name', preset='Image', socket=True, plug=True, dataType='img', dataAttr='')
        nodeflow_main.createAttribute(node=n, name='Saturation', preset='Float', socket=True, plug=True, dataType='flt', dataAttr='')

class ImageSaturationAction(QAction):
    """Model Create"""
    signal_Saturation = QtCore.pyqtSignal(object)

    def __init__(self, attrData, config):
        super(ImageSaturationAction, self).__init__()

        IMAGE = attrData.get('Image_Name')
        SATURATION = int(attrData.get('Saturation'))
        IMAGES = config.get('IMAGES')

        global save_path
        save_path = IMAGES + 'Saturation_' + os.path.basename(IMAGE)

        print(save_path)

        im = Image.open(IMAGE)
        enhancer = ImageEnhance.Color(im)
        enhanced_im = enhancer.enhance(SATURATION)
        self.signal_Saturation.emit(enhanced_im)
        enhanced_im.show()
