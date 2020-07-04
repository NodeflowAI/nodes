from threading import Thread
from PyQt5.QtWidgets import QWidget, QAction

from PIL import Image
import os
import numpy as np
import shutil
import posixpath
import imageio

from skimage.color import rgb2gray
from skimage.transform import resize
from skimage.io import imread, concatenate_images

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

class ModelPrep(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(ModelPrep, self).__init__()

        DATASET = config.get('DATASET')

        name = nn+'Dataset_Name'

        INPUT_SIZE = 32
        OUTPUT_SIZE = 128
        SHAPE_SIZE = 1

        nodeflow_main.createAttribute(node=n, name='Dataset_Name', preset='String', socket=True, plug=True, dataType='str', dataAttr='')
        nodeflow_main.createAttribute(node=n, name='Image_Paths', preset='Image', socket=True, plug=False, dataType='img', dataAttr='')
        nodeflow_main.createAttribute(node=n, name='Input_Size', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=INPUT_SIZE)
        nodeflow_main.createAttribute(node=n, name='Output_Size', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=OUTPUT_SIZE)
        nodeflow_main.createAttribute(node=n, name='Shape_Size', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=SHAPE_SIZE)
        nodeflow_main.createAttribute(node=n, name='Dataset_Path', preset='Path', socket=False, plug=True, dataType='str', dataExpr=SPL + DATASET + SPL + ADD + name + ADD + NPZ)

class ModelPrepAction(QAction):
    """Main widget"""
    def __init__(self, attrData, config):
        super(ModelPrepAction, self).__init__()

        self.mod_tmp_dir = 'temp'
        self.datasetPath = attrData.get('Dataset_Path')
        self.imagePaths = attrData.get('Image_Paths')

        # defining input and output size
        self.image_size_max = 1000
        input = int(attrData.get('Input_Size'))
        output = int(attrData.get('Output_Size'))
        print(input, output)

        self.input_size = (input, input)
        self.output_size = (output, output)
        print(self.input_size, self.output_size)

        self.img_dataset = self.datasetPath

        self.mod_tmp_path = config.get('TEMP')
        print(self.mod_tmp_path)

        try:
            self.delModelFiles()
        except:
            print('No Temp Model Dir Exists')

        os.mkdir(self.mod_tmp_path)
        self.copyModelFiles(self.imagePaths)

    def delModelFiles(self):
        """ param <path> could either be relative or absolute. """
        if os.path.isdir(self.mod_tmp_path):
            shutil.rmtree(self.mod_tmp_path)  # remove dir and all contains
        else:
            raise ValueError("file {} is not a file or dir.".format(self.mod_tmp_path))

    def resize_aspect_fit(self, src, dst):
        file = os.path.basename(src)
        save_dst = posixpath.join(dst, file)
        print(src, save_dst[:-4])
        img = Image.open(src)
        size = img.size
        ratio = float(self.image_size_max) / max(size)
        new_image_size = tuple([int(x * ratio) for x in size])
        im = img.resize(new_image_size, Image.ANTIALIAS)
        new_im = Image.new("RGB", (self.image_size_max, self.image_size_max))
        new_im.paste(im, ((self.image_size_max - new_image_size[0]) // 2, (self.image_size_max - new_image_size[1]) // 2))
        new_im.crop()
        new_im.save(save_dst, quality=95)

    def resize_image(self, src, dst):
        file = os.path.basename(src)
        save_dst = posixpath.join(dst, file)
        print(src, save_dst[:-4])
        img = Image.open(src)
        size = img.size
        ratio = float(self.image_size_max) / max(size)
        new_image_size = tuple([int(x * ratio) for x in size])
        im = img.resize(new_image_size, Image.ANTIALIAS)
        im.save(save_dst, quality=90)

    def copyModelFiles(self, paths):
        for path in paths:
            self.mod_tmp_file = os.path.basename(path)
            self.mod_tmp = posixpath.join(self.mod_tmp_path, self.mod_tmp_file)
            self.path = os.path.realpath(path)
            image = Image.open(self.path)
            img_width, img_height = image.size
            if img_width > self.image_size_max or img_height > self.image_size_max:
                self.resize_image(self.path, self.mod_tmp_path)

            else:
                Thread(target=shutil.copy, args=[self.path, self.mod_tmp]).start()

        self.loadDataset()

    def loadDataset(self):
        # loading and reshaping train set
        x_train, y_train = self._loadImages(self.mod_tmp_path, self.input_size, self.output_size)
        x_train = x_train.reshape(x_train.shape[0], x_train.shape[1], x_train.shape[2], 3)
        y_train = y_train.reshape(y_train.shape[0], y_train.shape[1], y_train.shape[2], 3)
        print(x_train.shape, y_train.shape)

        # loading and reshaping validation set
        x_test, y_test = self._loadImages(self.mod_tmp_path, self.input_size, self.output_size)
        x_test = x_test.reshape(x_test.shape[0], x_test.shape[1], x_test.shape[2], 3)
        y_test = y_test.reshape(y_test.shape[0], y_test.shape[1], y_test.shape[2], 3)
        print(x_test.shape, y_test.shape)

        # saving the data in arrays
        print("Creating a compressed dataset...")

        np.savez_compressed(self.img_dataset,
                            x_train=x_train,
                            y_train=y_train,
                            x_test=x_test,
                            y_test=y_test)

        print('Completed saving dataset')
        self.delModelFiles()

    # function for importing images from a folder
    def _loadImages(self, path, input_size, output_size):
        x_ = []
        y_ = []
        counter, totalnumber = 1, len(os.listdir(path))
        for imgpath in os.listdir(path):
            if counter % 100 == 0:
                print("Importing image %s of %s (%s%%)" %(counter, totalnumber, round(counter/totalnumber*100)))
            y = imread(path + "/" + imgpath)
            y = resize(y, output_size, mode="constant")
            x = resize(y, input_size, mode="constant")
            x_.append(x)
            y_.append(y)
            counter += 1
        return concatenate_images(x_), concatenate_images(y_)

    # function for importing a video, frame by frame
    def _loadVideo(self, filepath, input_size, output_size):
        vid = imageio.get_reader(filepath,  "ffmpeg")
        video_len = vid.get_length()
        counter, totalnumber = 1, video_len
        y_ = []
        x_ = []
        for i in range(0, video_len - 1):
            if counter % 100 == 0:
                print("Importing frame %s of %s (%s%%)" % (counter, totalnumber, round(counter / totalnumber * 100)))
            y_frame = resize(vid.get_data(i), output_size, mode="constant")
            y_frame = rgb2gray(y_frame)
            x_frame = resize(y_frame, input_size, mode="constant")
            y_.append(y_frame)
            x_.append(x_frame)
            counter += 1
        return concatenate_images(x_), concatenate_images(y_)
