# Nodeflow - Nodes
Templates for creating nodes in Nodeflow A.I.

Nodes are the base form of information in Nodeflow. You can create any type of data and the Attribute window will display the type of information.
There are two key classes for each node created, the node class which will create the node parameters and the action class.

The naming convention works as follows
filename = my_new_node.py
node = class MyNewNode(QWidget):
node action = class MyNewNodeAction(QWidget):

The best way to build a new node is to start with the default node and rename the file and classes to match untill we build a node build interface.
