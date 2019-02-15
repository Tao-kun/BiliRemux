# -*- coding: utf-8 -*-
import argparse
import glob
import json
import os
import re
import shutil
import sys

from config import *


def get_format(path):
    """
    Get the file's format by path.
    :param path: (str) The path of the file.
    :return: (str) The format of the file.
    """
    return path.split('.')[-1]


def convert_format(video_file_name, to_format):
    """
    Convert the name of a file to another format.
    Example: 0.mp4 -> 0.ts
    :param video_file_name: (str) Init file name.
    :param to_format: (str) New file format.
    :return: (str) Renamed file name.
    """
    return video_file_name.replace(get_format(video_file_name), to_format)


def get_video_dir_path(disk_drive):
    """
    Scan the external sdcard to get all downloaded videos' path.
    :param disk_drive: (str) Folder path where store /Android/ folder.
    :return: (list) All dictionaries which contain downloaded videos.
    """
    video_dir_paths = []
    for i in PACKAGE_NAMES:
        glob_param = os.path.join(
            disk_drive.replace('/', os.sep),
            DOWNLOAD_PATH.replace('/', os.sep)) \
            .format(i, '*', '*')
        glob_result = glob.glob(glob_param)
        video_dir_paths.extend(glob_result)
    return video_dir_paths


def find_flv_path(video_part_path):
    """
    Find flv/blv(BiliBili FLV)/mp4(segmented mp4) files from all videos.
    :param video_part_path: (str) A path of the dictionary of a downloaded video.
    :return: (str) The path of video which hadn't been remuxed.
    If the video had been remuxed or the download is not completed.
    :return: (NoneType) None
    """
    entry_json_path = '{}{}entry.json'.format(video_part_path, os.sep)
    with open(entry_json_path, 'rb') as f:
        entry_json = f.read().decode()
    video_information = json.loads(entry_json)
    if not video_information['is_completed']:
        return None
    video_file_name = video_information['type_tag']
    if not glob.glob('{}{}{}_remux.mp4'.format(video_part_path, os.sep, video_file_name)):
        # print(video_part_path, video_file_name)
        flv_video_path = glob.glob('{}{}{}'.format(video_part_path, os.sep, video_file_name))
        if len(flv_video_path) == 0:
            return None
        else:
            return flv_video_path[0]
    else:
        return None


def remux(flv_video_path):
    """
    Remux flv/blv(BiliBili FLV)/mp4(segmented mp4) into mp4.
    :param flv_video_path: (str) The path of video which have not been remuxed.
    :return: (NoneType) None
    """
    video_list = []
    filename_regex = re.compile(r'^\d\.(flv|blv|mp4)$')
    files_in_flv_path = glob.glob('{}{}*'.format(flv_video_path, os.sep))
    for file in files_in_flv_path:
        file_name = file.split(os.sep)[-1]
        if re.match(filename_regex, file_name):
            video_list.append(os.path.join(flv_video_path, file_name))
    if len(video_list) == 1:
        # MP4
        if video_list[0].split('.')[-1] == 'mp4':
            shutil.move(video_list[0], '{}_remux.mp4'.format(flv_video_path))
        # flv/blv
        else:
            command = FFMPEG_PATH + ' -i {}  -y -c copy {}_remux.mp4'
            os.system(command.format(video_list[0], flv_video_path))
    else:
        # Convert flv to ts, then concat them because flv could not concat successfully.
        # ffmpeg -i input1.flv -c copy -bsf:v h264_mp4toannexb -f mpegts input1.ts
        # ffmpeg -i input2.flv -c copy -bsf:v h264_mp4toannexb -f mpegts input2.ts
        # ffmpeg -i "concat:input1.ts|input2.ts" -c copy -bsf:a aac_adtstoasc -movflags +faststart output.mp4
        # REFER: http://blog.csdn.net/doublefi123/article/details/47276739
        for video in video_list:
            command = FFMPEG_PATH + ' -i {input} -c copy -f mpegts {output}'
            os.system(command.format(input=video, output=convert_format(video, 'ts')))
            os.remove(video)
        video_list = [convert_format(video, 'ts') for video in video_list]
        command = FFMPEG_PATH + ' -i "concat:{}" -c copy {}_remux.mp4'
        os.system(command.format('|'.join(video_list), flv_video_path))
    # delete flv/blv/mp4(segmented)
    for file in files_in_flv_path:
        try:
            os.remove(file)
        except:
            pass
    for file in video_list:
        try:
            os.remove(file)
        except:
            pass
    os.rmdir(flv_video_path)


def move_to_default_path(video_path):
    """
    Move videos to default path.
    Android/data/com.bilibili.app.blue/download -> Android/data/tv.danmaku.bili/download
    Android/data/tv.danmaku.bilixl/download -> Android/data/tv.danmaku.bili/download
    :param video_path:(tuple) A tuple of video path
    :return: (NoneType) None
    """
    for i in video_path:
        destination_path_entry_json = '{}{}entry.json'.format(i.replace(i.split(os.sep)[-4], 'tv.danmaku.bili'), os.sep)
        # i of video_path: Android/data/tv.danmaku.bilixl/download/aid/pid
        if i.split(os.sep)[-4] != 'tv.danmaku.bili' and not os.path.exists(destination_path_entry_json):
            destination_path = i.replace(i.split(os.sep)[-4], 'tv.danmaku.bili')
            shutil.move(i, destination_path)
            # Android/data/tv.danmaku.bilixl/download/aid/pid -> Android/data/tv.danmaku.bilixl/download/aid
            os.rmdir((os.sep).join(i.split(os.sep)[:-1]))
        else:
            continue


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Binding Bilibili Android Application downloaded video files')
    parser.add_argument('-b', '--bind', action='store_true', help='Bind all video files and convert to mp4')
    parser.add_argument('-m', '--move', action='store_true', help='Move all files to tv.danmaku.bili')
    parser.add_argument('-v', '--version', action='version', version='BiliRemux {}'.format(APP_VERSION))
    parser.add_argument('input', help='The path where store /Android/ folder')
    args = parser.parse_args()
    disk_drive = args.input
    if disk_drive[-1] != os.sep:
        disk_drive = '{}{}'.format(disk_drive, os.sep)
    video_path = get_video_dir_path(disk_drive)
    # print(video_path)
    if args.bind:
        # print('binding')
        if len(glob.glob(FFMPEG_PATH)) == 0:
            print('Cannot find ffmpeg! Exiting...')
            sys.exit(-1)
        for part in video_path:
            flv_path = find_flv_path(part)
            if flv_path is not None:
                remux(flv_path)
    if args.move:
        # print('moving')
        move_to_default_path(video_path)
