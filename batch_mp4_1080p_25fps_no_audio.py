#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import ffmpeg

# 1. 待扫描的根目录
SRC_DIR = r'/home/ubuntu/Projects/ruzhen/MVS/gps_unet_test/gps_new/VGGT_test/demo_capture_test/github_page/Photons-AAAI2026-Demo/assets'          # 改成你的路径
# 2. 输出目录（会自动创建）
DST_DIR = os.path.join(SRC_DIR, '1080p_no_audio')

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def list_mp4_files(root):
    """递归找出所有 mp4"""
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            if f.lower().endswith('.mp4'):
                yield os.path.join(dirpath, f)

def build_out_path(src_path, src_root, dst_root):
    """保持目录层级映射到输出文件夹"""
    rel = os.path.relpath(src_path, src_root)
    return os.path.join(dst_root, rel)

def transcode(in_file, out_file):
    """
    转码：1920x1080, 25fps, 无音频, 等比缩放+黑边
    """
    ensure_dir(os.path.dirname(out_file))
    print(f'Processing: {in_file}  ->  {out_file}')

    try:
        (
            ffmpeg
            .input(in_file)
            .output(out_file,
                    vf='scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2',
                    r=25,          # 帧率
                    an=None,       # 去除音频
                    vcodec='libx264',
                    crf=23,        # 画质，越小越清晰，体积越大
                    preset='fast') # 编码速度与压缩率权衡
            .overwrite_output()
            .run(quiet=False)
        )
    except ffmpeg.Error as e:
        print('[ERROR] ffmpeg 出错：', e.stderr.decode('utf8', errors='ignore'))

def main():
    if not os.path.isdir(SRC_DIR):
        sys.exit('源目录不存在: ' + SRC_DIR)

    mp4_list = list(list_mp4_files(SRC_DIR))
    if not mp4_list:
        print('未找到任何 MP4 文件')
        return

    print(f'共发现 {len(mp4_list)} 个 MP4，开始处理...\n')
    for src in mp4_list:
        dst = build_out_path(src, SRC_DIR, DST_DIR)
        transcode(src, dst)

    print('\n全部完成！')

if __name__ == '__main__':
    main()