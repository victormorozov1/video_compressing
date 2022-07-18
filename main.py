from moviepy.editor import *
from multiprocessing import Process


TIME_QUANTIUM = 0.1
TIME_X = 10
MIN_VOLUME_LVL = 0.005
PROCESS_NUM = 3

def important(time, diff, video):
    a = [video.audio.get_frame(time)[0]]

    for d in range(diff + 1):
        if time - d * TIME_QUANTIUM > 0:
            a.append(video.audio.get_frame(time - d * TIME_QUANTIUM)[0])
        if time + d < video.duration:
            a.append(video.audio.get_frame(time + d * TIME_QUANTIUM)[0])

    return sum([abs(i) for i in a]) / len(a) > MIN_VOLUME_LVL


def video_processing(start_time, end_time, ind):
    print(start_time, end_time)
    video = VideoFileClip('2n.mp4')
    result_clips = []

    for time in range(start_time * TIME_X, end_time * TIME_X):
        print(f'PROCESS-{ind}: {int((time / TIME_X - start_time) / (end_time - start_time) * 100)}%')
        if important(time / TIME_X, 3, video):
            result_clips.append(video.subclip(time / TIME_X, time / TIME_X + TIME_QUANTIUM))

    if result_clips:
        concatenate_videoclips(result_clips).write_videofile(f'res{ind}.mp4')


if __name__ == '__main__':
    result_clips = []
    video = VideoFileClip('2n.mp4').subclip(0, 100)

    one_process_video_time = video.duration // PROCESS_NUM

    processes = []

    for i in range(1, PROCESS_NUM):
        processes.append(Process(target=video_processing, args=((i - 1) * one_process_video_time, i * one_process_video_time, i,)))
    processes.append(Process(target=video_processing, args=((PROCESS_NUM - 1) * one_process_video_time, video.duration, PROCESS_NUM,)))

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    print('All videos are processed.')

    processed_videos = []
    for i in range(1, PROCESS_NUM + 1):
        processed_videos.append(VideoFileClip(f'res{i}.mp4'))
    concatenate_videoclips(processed_videos).write_videofile('res.mp4')