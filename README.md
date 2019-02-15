# Bilibili Remuxer

A remuxer for BiliBili Android Application
(tv.danmaku.bili, tv.danmaku.bilixl, com.bilibili.app.blue, com.bilibili.app.in).

## Dependencies

1.Python(>=3.4)

2.FFmpeg(Compiled)

## Usage
1. Filling FFmpeg's path in config.py.

2. Run it.
```
python remuxer.py [-h] [-b] [-m] [--version] input

positional arguments:
  input       The path where store /Android/ folder

optional arguments:
  -h, --help  show this help message and exit
  -b, --bind  Bind all video files and convert to mp4
  -m, --move  Move all files to tv.danmaku.bili
  -v, --version   show program's version number and exit
```

## License

MIT License

Copyright (c) 2017 Zhuo Yitao
