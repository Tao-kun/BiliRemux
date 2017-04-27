# -*- coding: utf-8 -*-
import glob
import json
import os
import shutil
import sys

from config import *


def remux(flv_video_path):
    '''
    Remux flv/blv(BiliBili FLV)/mp4(segmented mp4) into mp4.
    :param flv_video_path: (str) The path of video which hadn't been remuxed.
    :return: (NoneType) None
    '''
    video_list = []
    files_in_flv_path = glob.glob('{}{}*'.format(flv_video_path, os.sep))
    for file in files_in_flv_path:
        file_name = file.split(os.sep)[-1]
        if 5 <= len(file_name) < 10:
            video_list.append(os.path.join(flv_video_path, file_name))
    if len(video_list) == 1:
        # MP4
        if video_list[0].split('.')[-1] == 'mp4':
            shutil.move(video_list[0], '{}_remux.mp4'.format(flv_video_path))
        # blv/flv
        else:
            command = FFMPEG_PATH + ' -i {}  -y -vcodec copy -acodec copy {}_remux.mp4'
            os.system(command.format(video_list[0], flv_video_path))
    else:
        command = FFMPEG_PATH + ' -i "concat:{}" -c copy -bsf:a aac_adtstoasc {}_remux.mp4'
        os.system(command.format('|'.join(video_list), flv_video_path))
    for file in files_in_flv_path:
        try:
            os.remove(file)
        except:
            pass
    os.rmdir(flv_video_path)


def get_video_dir_path():
    '''
    Scan the external sdcard to get all downloaded videos' path.
    :return: (list) All dictionaries which contain downloaded videos.
    '''
    video_dir_paths = []
    disk_drive = sys.argv[1]
    for i in PACKAGE_NAMES:
        glob_param = os.path.join(disk_drive, DOWNLOAD_PATH.replace('/', os.sep)).format(i, '*', '*')
        glob_result = glob.glob(glob_param)
        video_dir_paths.extend(glob_result)
        return video_dir_paths


def find_flv_path(video_part_path):
    '''
    Find flv/blv(BiliBili FLV)/mp4(segmented mp4) files from all videos.
    :param video_part_path: (str) A path of the dictionary of a downloaded video.
    :return: (str) The path of video which hadn't been remuxed.
    If the video had been remuxed.
    :return: (NoneType) None
    '''
    entry_json_path = '{}{}entry.json'.format(video_part_path, os.sep)
    with open(entry_json_path, "rb") as f:
        entry_json = f.read().decode()
    video_information = json.loads(entry_json)
    if not video_information['is_completed']:
        return None
    video_file_name = video_information['type_tag']
    if not glob.glob('{}{}{}_remux.mp4'.format(video_part_path, os.sep, video_file_name)):
        print(video_part_path, video_file_name)
        flv_video_path = glob.glob('{}{}{}'.format(video_part_path, os.sep, video_file_name))[0]
        return flv_video_path
    else:
        return None


if __name__ == '__main__':
    video_path = get_video_dir_path()
    for part in video_path:
        flv_path = find_flv_path(part)
        if flv_path is not None:
            remux(flv_path)
