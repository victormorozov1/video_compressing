from moviepy.editor import *

v = []
for i in range(10):
    v.append(VideoFileClip(f'res{i}.mp4'))
v.append(VideoFileClip('res10}.mp4'))
v = concatenate_videoclips(v)
v.write_videofile('y.mp4')