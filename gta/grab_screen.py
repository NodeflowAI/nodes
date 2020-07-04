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

class GrabScreen(QWidget):
    def __init__(self, nodeflow_main, n, nn, config):
        super(GrabScreen, self).__init__()

        TOP = 0
        BOTTOM = 100
        LEFT = 0
        RIGHT = 300

        nodeflow_main.createAttribute(node=n, name='Top_Position', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=TOP)
        nodeflow_main.createAttribute(node=n, name='Bottom_Position', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=BOTTOM)
        nodeflow_main.createAttribute(node=n, name='Left_Position', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=LEFT)
        nodeflow_main.createAttribute(node=n, name='Right_Position', preset='Integer', socket=True, plug=True, dataType='int', dataAttr=RIGHT)

class GrabScreenAction(QAction):
    """Model Create"""
    def __init__(self, attrData, config):
        super(GrabScreenAction, self).__init__()

        import cv2
        import numpy as np
        import win32gui, win32ui, win32con, win32api

        top = int(attrData.get('Top_Position'))
        left = int(attrData.get('Left_Position'))

        y2 = int(attrData.get('Bottom_Position'))
        x2 = int(attrData.get('Right_Position'))


        # Done by Frannecklp
        def grab_screen(winName: str = "Grand Theft Auto V"):
            desktop = win32gui.GetDesktopWindow()

            # get area by a window name
            gtawin = win32gui.FindWindow(None, winName)
            # get the bounding box of the window
            left, top, x2, y2 = win32gui.GetWindowRect(gtawin)
            # cut window boarders

            width = x2 - left + 1
            height = y2 - top + 1

            # the device context(DC) for the entire window (title bar, menus, scroll bars, etc.)
            hwindc = win32gui.GetWindowDC(desktop)
            # Create a DC object from an integer handle
            srcdc = win32ui.CreateDCFromHandle(hwindc)
            # Create a memory device context that is compatible with the source DC
            memdc = srcdc.CreateCompatibleDC()
            # Create a bitmap object
            bmp = win32ui.CreateBitmap()
            # Create a bitmap compatible with the specified device context
            bmp.CreateCompatibleBitmap(srcdc, width, height)
            # Select an object into the device context.
            memdc.SelectObject(bmp)
            # Copy a bitmap from the source device context to this device context
            # parameters: destPos, size, dc, srcPos, rop(the raster operation))
            memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)

            # the bitmap bits
            signedIntsArray = bmp.GetBitmapBits(True)
            # form a 1-D array initialized from text data in a string.
            img = np.fromstring(signedIntsArray, dtype='uint8')
            img.shape = (height, width, 4)

            # Delete all resources associated with the device context
            srcdc.DeleteDC()
            memdc.DeleteDC()
            # Releases the device context
            win32gui.ReleaseDC(desktop, hwindc)
            # Delete the bitmap and freeing all system resources associated with the object.
            # After the object is deleted, the specified handle is no longer valid.
            win32gui.DeleteObject(bmp.GetHandle())

            return cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)