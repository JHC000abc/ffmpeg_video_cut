# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@contact: JHC000abc@gmail.com
@file: process_control.py
@time: 2023/1/30 21:46 $
@desc:

"""
import os
from threading import Thread
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from util import util_ffmpeg
from gui.ui import process
from PyQt5 import QtWidgets, QtCore
from setting import setting
import time



class Process(QtWidgets.QWidget):
    single = QtCore.pyqtSignal(int)
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.ui = process.Ui_Form()
        self.ui.setupUi(self)
        # 隐藏标题栏
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(self.width(),self.height())
        self.slot()
        self.view()
        self._thread()
        self.top_status = False

    def _thread(self):
        """

        :return:
        """
        self.t1 = None
        self.t2 = None
        self.t3 = None

    def view(self):
        """

        :return:
        """
        self.ui.progressBar.hide()
        self.ui.lineEdit_out_name.setPlaceholderText(
            "请输入保存名，如需输出在单独文件夹下请参考'/savepath/video'")
        self.ui.lineEdit_start.hide()
        self.ui.lineEdit_end.hide()
        self.ui.lineEdit_num.hide()

        myValidator = QRegExpValidator(QRegExp("^[0-9]+$"))
        self.ui.lineEdit_start.setValidator(myValidator)
        self.ui.lineEdit_end.setValidator(myValidator)
        self.ui.lineEdit_num.setValidator(myValidator)

        self.ui.lineEdit_in.setReadOnly(True)
        self.ui.lineEdit_out.setReadOnly(True)


    def slot(self):
        """

        :return:
        """
        self.ui.pushButton_in.clicked.connect(self.slot_btn_in)
        self.ui.pushButton_out.clicked.connect(self.slot_btn_out)
        self.ui.lineEdit_out_name.textEdited.connect(self.slot_btn_out_name)
        self.ui.radioButton_second.clicked.connect(self.slot_rdbtn_second)
        self.ui.radioButton_round.clicked.connect(self.slot_rdbtn_round)
        self.ui.radioButton_all.clicked.connect(self.slot_rdbtn_all)
        self.ui.pushButton_start_cut.clicked.connect(self.slot_start)
        self.ui.pushButton_fork.clicked.connect(self.slot_btn_fork)
        self.ui.pushButton_top.clicked.connect(self.slot_btn_top)
        self.single.connect(self.add_bar)

    def slot_btn_top(self):
        if self.top_status == False:
            self.setWindowFlags(Qt.WindowStaysOnTopHint | self.windowFlags())
            self.top_status = True
        else:
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.top_status = False
        self.show()


    def slot_btn_fork(self):
        """

        :return:
        """
        self.window().hide()
        self.closeEvent()


    def closeEvent(self):
        """
        关闭窗口触发以下事件
        :return:
        """
        msg = QMessageBox()
        a = msg.warning(self, None, '你确定要退出吗?', QMessageBox.Yes | QMessageBox.No,
                                 QMessageBox.No)  # "退出"代表的是弹出框的标题,"你确认退出.."表示弹出框的内容
        if a == QMessageBox.Yes:
            if self.t1:
                self.t1.join()
            if self.t2:
                self.t2.join()
            if self.t3:
                self.t3.join()
            else:
                pass
            os._exit(0)
        else:
            self.window().show()


    def slot_start(self):
        """

        :return:
        """
        self.check_input()



    def check_input(self):
        """

        :return:
        """
        if self.ui.lineEdit_in.text() == "":
            self.show_warning("请选择视频文件")
            self.get_file()

        elif self.ui.lineEdit_out.text() == "":
            self.show_warning("请选择输出路径")
            self.get_path()
        elif self.ui.lineEdit_out_name.text() == "":
            self.show_warning("请输入保存名")
        elif not self.ui.lineEdit_out_name.text().startswith("/"):
            self.ui.lineEdit_out_name.clear()
            self.show_warning("保存名[必须以 / 开头]")
        else:
            if self.ui.radioButton_second.isChecked() == False and self.ui.radioButton_round.isChecked() == False and self.ui.radioButton_all.isChecked() == False:
                self.show_warning("请选择处理条件")
            else:
                if self.ui.radioButton_second.isChecked():
                    if self.ui.lineEdit_start.text() == "":
                        self.show_warning("请输入要截取的时间点")
                    else:
                        file, second, out_file = self.ui.lineEdit_in.text(), self.ui.lineEdit_start.text(
                        ), self.ui.lineEdit_out.text().replace(":/", "://") + self.ui.lineEdit_out_name.text()
                        self.t1 = Thread(target=util_ffmpeg.split_specify_time,
                                         args=(file, second, out_file))
                        self.t1.start()
                        self.change_start_status_run_bar()
                elif self.ui.radioButton_round.isChecked():
                    if self.ui.lineEdit_start.text() == "":
                        self.show_warning("请输入开始截取时间")
                    elif self.ui.lineEdit_end.text() == "":
                        self.show_warning("请输入结束截取时间")
                    elif self.ui.lineEdit_num.text() == "":
                        self.show_warning("请输入每秒截取数")
                    else:
                        file, num, start, end, out_name = self.ui.lineEdit_in.text(), self.ui.lineEdit_num.text(), self.ui.lineEdit_start.text(
                        ), self.ui.lineEdit_end.text(), self.ui.lineEdit_out.text().replace(":/",
                                                                                            "://") + self.ui.lineEdit_out_name.text()
                        self.t2 = Thread(target=util_ffmpeg.split_video_between_start_and_end,
                                         args=(file, num, start, end, out_name))
                        self.t2.start()
                        self.change_start_status_run_bar()
                elif self.ui.radioButton_all.isChecked():
                    if self.ui.lineEdit_num.text() == "":
                        self.show_warning("请输入每秒截取数")
                    else:
                        file, num, out_name = self.ui.lineEdit_in.text(), self.ui.lineEdit_num.text(
                        ), self.ui.lineEdit_out.text().replace(":/", "://") + self.ui.lineEdit_out_name.text()
                        self.t3 = Thread(
                            target=util_ffmpeg.split_video, args=(
                                file, num, out_name))
                        self.t3.start()
                        self.change_start_status_run_bar()
                else:
                    print("异常")

    def change_start_status_run_bar(self):
        self.ui.pushButton_start_cut.setDisabled(True)
        setting.LOAD_STATUS = 0
        Thread(target=self.show_bar).start()

    def hide_fotter(self):
        """

        :return:
        """
        self.ui.lineEdit_start.hide()
        self.ui.lineEdit_end.hide()
        self.ui.lineEdit_num.hide()

    def slot_rdbtn_round(self):
        """

        :return:
        """
        if self.ui.radioButton_round.isChecked():
            self.hide_fotter()

            self.ui.lineEdit_start.setPlaceholderText("请输入开始截取时间")
            self.ui.lineEdit_end.setPlaceholderText("请输入结束截取时间")
            self.ui.lineEdit_num.setPlaceholderText("请输入每秒截取数")

            self.ui.lineEdit_start.show()
            self.ui.lineEdit_end.show()
            self.ui.lineEdit_num.show()

    def slot_rdbtn_second(self):
        """

        :return:
        """
        if self.ui.radioButton_second.isChecked():
            self.hide_fotter()
            self.ui.lineEdit_start.show()
            self.ui.lineEdit_start.setPlaceholderText("请输入要截取时间点")

    def slot_rdbtn_all(self):
        """

        :return:
        """
        if self.ui.radioButton_all.isChecked():
            self.hide_fotter()
            self.ui.lineEdit_num.show()
            self.ui.lineEdit_num.setPlaceholderText("请输入每秒截取数")

    def slot_btn_in(self):
        """

        :return:
        """
        file = self.get_file()
        print(file)

    def slot_btn_out(self):
        """

        :return:
        """
        self.get_path()

    def slot_btn_out_name(self):
        """

        :return:
        """
        print(self.ui.lineEdit_out_name.text())

    def get_path(self):
        """

        :return:
        """
        select_path = ""
        while select_path == "":
            self.ui.lineEdit_out.clear()
            _path = QFileDialog()
            select_path = _path.getExistingDirectory(self, "请选择文件夹路径", None)
            if os.path.isdir(select_path) and select_path:
                self.ui.lineEdit_out.setText(select_path)
                break
            else:
                self.show_warning("未选择路径")

    def get_file(self):
        """

        :return:
        """
        file = ""
        while file == "":
            self.ui.lineEdit_in.clear()
            dir = QFileDialog()  # 创建文件对话框
            # dir.setDirectory("D:\\")   # 设置初始路径为D盘
            # dir.setDirectory(".\\")  # 设置初始路径为D盘
            # 设置只显示视频文件
            dir.setNameFilter("视频文件(*.mp4)")
            if dir.exec_():  # 判断是否选择了文件
                self.ui.lineEdit_in.setText(
                    dir.selectedFiles()[0])  # 将选择的文件显示在文本框中
                file = dir.selectedFiles()[0]
                break
            else:
                self.show_warning("未选择视频文件")
                # self.get_file()
        return file

    def show_warning(self, text):
        """

        :param text:
        :return:
        """
        msg_box = QMessageBox(QMessageBox.Warning, 'Warning', text)
        if self.top_status == True:
            self.top_status = True
            self.slot_btn_top()
            msg_box.setWindowFlags(Qt.FramelessWindowHint)
            msg_box.show()
            msg_box.exec_()
            self.top_status = False
            self.slot_btn_top()

        else:
            msg_box.setWindowFlags(Qt.FramelessWindowHint)
            msg_box.show()
            msg_box.exec_()

    def add_bar(self,num):
        """

        :param num:
        :return:
        """
        if num == -1:
            self.ui.progressBar.setValue(0)
            self.ui.progressBar.show()
        elif num > 0 and num<100:
            self.ui.progressBar.setValue(num)
        elif num == 100:
            self.ui.progressBar.hide()
            self.ui.pushButton_start_cut.setDisabled(False)
            setting.LOAD_STATUS = -1
        else:
            print("异常")

    def show_bar(self):
        """

        :return:
        """
        print(setting.LOAD_STATUS)
        while setting.LOAD_STATUS >= 0:
            if setting.LOAD_STATUS == 0:
                self.single.emit(-1)
            else:
                print(setting.LOAD_STATUS)
                self.single.emit(setting.LOAD_STATUS)
                time.sleep(0.1)
                if setting.LOAD_STATUS+1 > 100:
                    setting.LOAD_STATUS = -1
                    break
        self.single.emit(100)


