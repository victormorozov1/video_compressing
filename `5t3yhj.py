from moviepy.editor import *
import pygame


def important(time, diff):
    a = [video.audio.get_frame(time)[0]]

    for d in range(diff + 1):
        if time - d > 0:
            a.append(video.audio.get_frame(time - d)[0])
        if time + d < video.duration:
            a.append(video.audio.get_frame(time + d)[0])

    return sum([abs(i) for i in a]) / len(a) > MIN_VOLUME_LVL


video = VideoFileClip('test2.mp4')

result_clips = []

MIN_VOLUME_LVL = 0.0006
print(video.duration)

clock = pygame.time.Clock()

for time in range(int(video.duration) + 1):
    if important(time, 0):
        result_clips.append(video.subclip(time, time + 1))

result = concatenate_videoclips(result_clips[:-1:])
result.write_videofile('res.mp4')