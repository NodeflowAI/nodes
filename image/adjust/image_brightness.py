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

class ImageBrightness(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(ImageBrightness, self).__init__()

        name = nn + 'Image_Name'
        BRT = 1.0

        nodeflow_main.createAttribute(node=n, name='Image_Name', preset='Image', socket=True, plug=True, dataType='img', dataAttr='')
        nodeflow_main.createAttribute(node=n, name='Brightness', preset='Float', socket=True, plug=True, dataType='flt', dataAttr=BRT)

class ImageBrightnessUpdate(QAction):
    """Model Create"""
    signal_Brightness = QtCore.pyqtSignal(object)

    def __init__(self, attrData, config):
        super(ImageBrightnessUpdate, self).__init__()

        IMAGE = attrData.get('Image_Name')
        BRIGHTNESS = int(attrData.get('Brightness'))
        IMAGES = config.get('IMAGES')

        save_path = IMAGES + 'Bright_' + os.path.basename(IMAGE)
        print(save_path)

        im = Image.open(IMAGE)
        enhancer = ImageEnhance.Brightness(im)
        enhanced_im = enhancer.enhance(BRIGHTNESS)
        self.signal_Brightness.emit(enhanced_im)
        enhanced_im.show()
        #enhanced_im.save(save_path)