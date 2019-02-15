# -*- coding: utf-8 -*-

# App Version
APP_VERSION = '0.1.1'

# Please change it into the dictionary which contains your FFmpeg(.exe).
FFMPEG_PATH = r'D:\ffmpeg-4.0-win64-shared\bin\ffmpeg.exe'

# There are at least 3 version of BilBili Offical Application.
# tv.danmaku.bili              哔哩哔哩(正式版)
# tv.danmaku.bilixl            哔哩哔哩白(怀旧版)
# com.bilibili.app.blue        哔哩哔哩概念版(测试版)
# com.bilibili.app.in          哔哩哔哩(Google Play 版)
PACKAGE_NAMES = ('tv.danmaku.bili', 'tv.danmaku.bilixl', 'com.bilibili.app.blue', 'com.bilibili.app.in')

# Description for 3 {}.
# 1. 3 applications' package names
# 2. avid
# 3. part id
DOWNLOAD_PATH = 'Android/data/{}/download/{}/{}'
