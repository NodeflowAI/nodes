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

class ImageSharpness(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(ImageSharpness, self).__init__()

        nodeflow_main.createAttribute(node=n, name='Image_Name', preset='Image', socket=True, plug=True, dataType='img', dataAttr='')
        nodeflow_main.createAttribute(node=n, name='Sharpness', preset='Float', socket=True, plug=True, dataType='flt', dataAttr='')

class ImageSharpnessAction(QAction):
    """Model Create"""
    signal_Sharpness = QtCore.pyqtSignal(object)

    def __init__(self, attrData, config):
        super(ImageSharpnessAction, self).__init__()

        IMAGE = attrData.get('Image_Name')
        SHARPNESS = int(attrData.get('Sharpness'))
        IMAGES = config.get('IMAGES')

        global save_path
        save_path = IMAGES + 'Sharpness_' + os.path.basename(IMAGE)

        print(save_path)

        im = Image.open(IMAGE)
        enhancer = ImageEnhance.Sharpness(im)
        enhanced_im = enhancer.enhance(SHARPNESS)
        self.signal_Sharpness.emit(enhanced_im)
        enhanced_im.show()