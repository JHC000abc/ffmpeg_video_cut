# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@contact: JHC000abc@gmail.com
@file: start.py
@time: 2023/1/30 21:45 $
@desc:

"""
import qdarkstyle
import sys
from PyQt5 import QtWidgets, QtCore
from gui.control.process_control import Process



if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    Form = Process()
    Form.show()
    Form.setFixedSize(Form.width(), Form.height())
    sys.exit(app.exec_())