# -*- coding: utf-8 -*-

# Please change it into the dictionary which contains your FFmpeg(.exe).
FFMPEG_PATH = r'D:\MarukoToolbox\tools\ffmpeg.exe'

# There are at least 3 version of BilBili Application.
# tv.danmaku.bili              哔哩哔哩动画(正式版)
# tv.danmaku.bilixl            哔哩哔哩白（怀旧版)
# com.bilibili.app.blue        哔哩哔哩概念版（测试版）
PACKAGE_NAMES = ('tv.danmaku.bili', 'tv.danmaku.bilixl', 'com.bilibili.app.blue')

# Description for 3 {}.
# 1. 3 applications' package names
# 1. avid
# 3. part id
DOWNLOAD_PATH = 'Android/data/{}/download/{}/{}'
