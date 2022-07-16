from moviepy.editor import *
import pygame


TIME_QUANTIUM = 0.1
TIME_X = 10

def important(time, diff):
    a = [video.audio.get_frame(time)[0]]

    for d in range(diff + 1):
        if time - d * TIME_QUANTIUM > 0:
            a.append(video.audio.get_frame(time - d * TIME_QUANTIUM)[0])
        if time + d < video.duration:
            a.append(video.audio.get_frame(time + d * TIME_QUANTIUM)[0])

    return sum([abs(i) for i in a]) / len(a) > MIN_VOLUME_LVL


video = VideoFileClip('test2.mp4')

result_clips = []

MIN_VOLUME_LVL = 0.005
print(video.duration)

clock = pygame.time.Clock()

for time in range((int(video.duration) + 1) * TIME_X - TIME_X + 1):
    if important(time / TIME_X, 3):
        result_clips.append(video.subclip(time / TIME_X, time / TIME_X + TIME_QUANTIUM))

print(result_clips)

result = concatenate_videoclips(result_clips[:-1:])
result.write_videofile('res.mp4')