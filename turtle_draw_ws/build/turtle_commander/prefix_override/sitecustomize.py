import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/frequis/ros/Visao-computacional-Ros/turtle_draw_ws/install/turtle_commander'
