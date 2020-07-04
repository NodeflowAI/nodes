from threading import Thread
from PyQt5.QtWidgets import QWidget, QAction

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
N = '\n'
T = '\t'
TT = '\t\t'
TTT = '\t\t\t'

class WindowFunction(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(WindowFunction, self).__init__()

        name = nn+'Window_Name'

        nodeflow_main.createAttribute(node=n, name='Window_Name', preset='String', socket=True, plug=True, dataType='str', dataAttr='')

class WindowFunctionAction(QAction):
    """Main widget"""
    def __init__(self, attrData, config):
        super(WindowFunctionAction, self).__init__()

        WINDOW_NAME = attrData.get('Window_Name')

        L1 = 'def '+WINDOW_NAME+'():'
        L2 =   T+'title = "PyQt5 Image"'
        L3 =   T+'left = 500'
        L4 =   T+'top = 200'
        L5 =   T+'width = 400'
        L6 =   T+'height = 300'
        L7 =   T+'iconName = "nodz.png"'
        L8 =   T+'print(title)'

        lineData = []
        for i in range(1, 9):
            line = eval('L'+str(i))
            lineData.append(line)

        lineJoin = '\n'.join(lineData)
        func_exec = WINDOW_NAME + '()'
        main_exec = lineJoin + N + func_exec

        print(main_exec)
        exec(main_exec)


        '''
        L3 =   T+'left = 500'
        L4 =   T+'top = 200'
        L5 =   T+'width = 400'
        L6 =   T+'height = 300'
        L7 =   T+'iconName = "nodz.png"'
        L8 =   T+'setWindowTitle(title)'
        L9 =   T+'setWindowIcon(QtGui.QIcon(iconName))'
        L10 =   T+'setGeometry(left, top, width, height)'
        L11 =   T+'vbox = QVBoxLayout()'
        L12 =   T+'labelImage = QLabel()'
        L13 =   T+'pixmap = QPixmap("nodz.png")'
        L14 =   T+'labelImage.setPixmap(pixmap)'
        L15 =   T+'vbox.addWidget(labelImage)'
        L16 =   T+'setLayout(vbox)'
        L17 =   T+'labelImage.show()'
        
        '''