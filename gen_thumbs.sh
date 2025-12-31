#!/usr/bin/env bash

mkdir -p assets/thumbs

for f in assets/*.mp4; do
  ffmpeg -y -ss 2 -i "$f" \
    -vf "scale=1920:-1" \
    -frames:v 1 \
    "assets/thumbs/$(basename "${f%.mp4}").jpg"
done

