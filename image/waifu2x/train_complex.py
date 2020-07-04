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
CSV = config['ACTION']['CSV']

N = '\n'
T = '\t'
TT = '\t\t'
TTT = '\t\t\t'

class TrainComplex(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(TrainComplex, self).__init__()

        nodeflow_main.createAttribute(node=n, name='Dataset_Dir', preset='String', socket=True, plug=True, dataType='str', dataAttr='')
        nodeflow_main.createAttribute(node=n, name='Validation_Rate', preset='Float', socket=True, plug=True, dataType='flt', dataAttr=0.05)
        nodeflow_main.createAttribute(node=n, name='NR_Rate', preset='Float', socket=True, plug=True, dataType='flt', dataAttr=0.65)
        nodeflow_main.createAttribute(node=n, name='Chroma_Subsampling_Rate', preset='Float', socket=True, plug=True, dataType='flt', dataAttr=0.5)
        nodeflow_main.createAttribute(node=n, name='Out_Size', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=64)
        nodeflow_main.createAttribute(node=n, name='Max_Size', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=256)
        nodeflow_main.createAttribute(node=n, name='Active_Cropping_Rate', preset='Float', socket=True, plug=True, dataType='flt', dataAttr=0.5)
        nodeflow_main.createAttribute(node=n, name='Active_Cropping_Tries', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=10)
        nodeflow_main.createAttribute(node=n, name='Random_Half_Rate', preset='Float', socket=True, plug=True, dataType='flt', dataAttr=0.0)
        nodeflow_main.createAttribute(node=n, name='Random_Color_Noise_Rate', preset='Float', socket=True, plug=True, dataType='flt', dataAttr=0.0)
        nodeflow_main.createAttribute(node=n, name='Random_Unsharp_Mask_Rate', preset='Float', socket=True, plug=True, dataType='flt', dataAttr=0.0)
        nodeflow_main.createAttribute(node=n, name='Learning_Rate', preset='Float', socket=True, plug=True, dataType='flt', dataAttr=0.00025)
        nodeflow_main.createAttribute(node=n, name='LR_Min', preset='Float', socket=True, plug=True, dataType='flt', dataAttr=0.00001)
        nodeflow_main.createAttribute(node=n, name='LR_Decay', preset='Float', socket=True, plug=True, dataType='flt', dataAttr=0.9)
        nodeflow_main.createAttribute(node=n, name='LR_Decay_Interval', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=5)
        nodeflow_main.createAttribute(node=n, name='Batch_Size', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=16)
        nodeflow_main.createAttribute(node=n, name='Patches', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=64)
        nodeflow_main.createAttribute(node=n, name='Validation_Crop_Rate', preset='Float', socket=True, plug=True, dataType='flt', dataAttr=0.5)
        nodeflow_main.createAttribute(node=n, name='Downsampling_Filters', preset='String', socket=True, plug=True, dataType='str', dataAttr='["box"]')
        nodeflow_main.createAttribute(node=n, name='Resize_Blur_Min', preset='Float', socket=True, plug=True, dataType='flt', dataAttr=0.95)
        nodeflow_main.createAttribute(node=n, name='Resize_Blur_Max', preset='Float', socket=True, plug=True, dataType='flt', dataAttr=1.05)
        nodeflow_main.createAttribute(node=n, name='Epoch', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=50)
        nodeflow_main.createAttribute(node=n, name='Inner_Epoch', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=4)
        nodeflow_main.createAttribute(node=n, name='Model_Name', preset='String', socket=True, plug=True, dataType='str', dataAttr='')
        nodeflow_main.createAttribute(node=n, name='Color', preset='String', socket=True, plug=True, dataType='str', dataAttr='rgb')
        nodeflow_main.createAttribute(node=n, name='Arch', preset='String', socket=True, plug=True, dataType='str', dataAttr='VGG7')
        nodeflow_main.createAttribute(node=n, name='Method', preset='String', socket=True, plug=True, dataType='str', dataAttr='scale')
        nodeflow_main.createAttribute(node=n, name='Noise_Level', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=1)
        nodeflow_main.createAttribute(node=n, name='Seed', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=11)
        nodeflow_main.createAttribute(node=n, name='GPU', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=-1)


class TrainComplexAction(QAction):
    """Model Create"""
    def __init__(self, attrData, config):
        super(TrainComplexAction, self).__init__()

        import os
        DD = ' -d ' + attrData.get('Dataset_Dir')
        VR = ' -v ' + str(attrData.get('Validation_Rate'))
        NR = ' -nr ' + str(attrData.get('NR_Rate'))
        CSR = ' -csr ' + str(attrData.get('Chroma_Subsampling_Rate'))
        OUT = ' -os ' + str(attrData.get('Out_Size'))
        MS = ' -ms ' + str(attrData.get('Max_Size'))
        ACR = ' -acr ' + str(attrData.get('Active_Cropping_Rate'))
        ACT = ' -act ' + str(attrData.get('Active_Cropping_Tries'))
        RHR = ' -rhr ' + str(attrData.get('Random_Half_Rate'))
        RCNR = ' -rcnr ' + str(attrData.get('Random_Color_Noise_Rate'))
        RUMR = ' -rumr ' + str(attrData.get('Random_Unsharp_Mask_Rate'))
        LR = ' -lr ' + str(attrData.get('Learning_Rate'))
        LRM = ' -lrm ' + str(attrData.get('LR_Min'))
        LRD = ' -lrd ' + str(attrData.get('LR_Decay'))
        LRDI = ' -lrdi ' + str(attrData.get('LR_Decay_Interval'))
        BS = ' -bs ' + str(attrData.get('Batch_Size'))
        P = ' -p ' + str(attrData.get('Patches'))
        VCR = ' -vcr ' + str(attrData.get('Validation_Crop_Rate'))
        DF = ' -df ' + attrData.get('Downsampling_Filters')
        MIN = ' -min ' + str(attrData.get('Resize_Blur_Min'))
        MAX = ' -max ' + str(attrData.get('Resize_Blur_Max'))
        EPO = ' -e ' + str(attrData.get('Epoch'))
        IE = ' -ie ' + str(attrData.get('Inner_Epoch'))
        MN = ' -mn ' + attrData.get('Model_Name')
        COL = ' -c ' + str(attrData.get('Color'))
        A = ' -a ' + str(attrData.get('Arch'))
        M = ' -m ' + str(attrData.get('Method'))
        NL = ' -nl ' + str(attrData.get('Noise_Level'))
        SEED = ' -s ' + str(attrData.get('Seed'))
        GPU = ' -g ' + str(attrData.get('GPU'))

        run = 'python C:/Code/nirvana/modules/waifu2x/pixpix_train.py'+DD+VR+NR+CSR+OUT+MS+ACR+ACT+RHR+RCNR+RUMR+LR+LRM+LRD+LRDI+BS+P+VCR+DF+MIN+MAX+EPO+IE+MN+COL+A+M+NL+SEED+GPU

        print(run)
        os.system(run)
