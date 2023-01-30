# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@contact: JHC000abc@gmail.com
@file: util_ffmpeg.py
@time: 2023/1/30 20:44 $
@desc:

"""
import os
import re
import subprocess
from setting import setting


def compute_progress_and_send_progress(process):
    """

    :param process:
    :return:
    """
    duration = None
    while process.poll() is None:
        line = process.stderr.readline().strip()
        if line:
            duration_res = re.search(r'Duration: (?P<duration>\S+)', line)
            if duration_res is not None:
                duration = duration_res.groupdict()['duration']
                duration = re.sub(r',', '', duration)

            result = re.search(r'time=(?P<time>\S+)', line)
            if result is not None and duration is not None:
                elapsed_time = result.groupdict()['time']

                currentTime = get_seconds(elapsed_time)
                allTime = get_seconds(duration)

                progress = currentTime * 100 / allTime
                setting.LOAD_STATUS = int(progress)
                # print(setting.LOAD_STATUS)
        else:
            setting.LOAD_STATUS = -1


def get_seconds(time):
    """

    :param time:
    :return:
    """
    h = int(time[0:2])
    m = int(time[3:5])
    s = int(time[6:8])
    ms = int(time[9:12])
    ts = (h * 60 * 60) + (m * 60) + s + (ms / 1000)
    return ts


def make_path(path):
    """

    :param path:
    :return:
    """
    _path = os.path.split(path)[0]
    # print("_path",_path)
    os.makedirs(_path, exist_ok=True)


def split_video_range(file, out_file, start, end):
    """
    范围截取
    :param file:
    :param out_file:
    :param start:
    :param end:
    :return:
    """
    # 从start，截取到end
    make_path(out_file)
    cmd = "ffmpeg -ss {} -i {} -to {} -c:v copy -c:a copy  {}".format(
        start, file, end - start, out_file)
    print(cmd)
    run(cmd)


def split_specify_time(file, second, out_file):
    """
    指定时间截取
    :param file:
    :param second:
    :param out_file:
    :return:
    """
    # 截取第1分50秒的图片
    make_path(out_file)
    cmd = "ffmpeg -y -i {} -vframes 1 -q:v 2 -f image2 -ss {} {}_{}.jpg".format(
        file, second, out_file, second)
    print(cmd)
    run(cmd)


def split_video_between_start_and_end(file, num, start, end, out_name):
    """
    范围截取，指定开始，指定结束，指定抽取率
    :param file:
    :param num:
    :param start:
    :param end:
    :param out_name:
    :return:
    """
    make_path(out_name)
    # 从第15秒开始以每秒截取7张图片的速度,截取5秒时长的图片[5*7=35张]
    cmd = "ffmpeg -y -i {} -r {} -ss {} -t {} {}_%4d.jpg".format(
        file, num, start, int(end) - int(start), out_name)
    print(cmd)
    run(cmd)


def split_video(file, num, out_name):
    """
    所有截取
    :param file:
    :param num:
    :param out_name:
    :return:
    """
    make_path(out_name)
    print(out_name)
    # 每秒抽num帧
    cmd = "ffmpeg -y -i {} -r {} {}_%4d.jpg".format(file, num, out_name)
    print(cmd)
    run(cmd)


def run(cmd, retry=3):
    """

    :param cmd:
    :param retry:
    :return:
    """
    flag = False
    while not flag and retry > 0:
        try:
            process = subprocess.Popen(cmd,
                                       stderr=subprocess.PIPE,
                                       bufsize=0,
                                       universal_newlines=True,
                                       shell=True
                                       )
            flag = True
            compute_progress_and_send_progress(process)
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            retry -= 1

# if __name__ == '__main__':
#     file = R"E:\Desktop\ffmpeg\\test\stand.mp4"
#     out_file = R"E:\Desktop\ffmpeg\1.jpg"
#     start = 3
#     end = 5
#     second = 4
#     # split_video_range(file, out_file, start, end)
#     # split_specify_time(file, second, out_file)
#     num = 2
#     out_name = R"E:\Desktop\ffmpeg\video\result"
#     make_path(file)
#     # split_video_between_start_and_end(file, num, start, end, out_name)
#     # split_video(file, num, out_name)
