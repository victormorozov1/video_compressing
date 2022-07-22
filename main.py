import multiprocessing

from moviepy.editor import *
from multiprocessing import Process

TIME_X = 100
TIME_QUANTIUM = 1 / TIME_X
MIN_VOLUME_LVL = 0.0003
PROCESS_NUM = 3

video = VideoFileClip('2n.mp4').subclip(0, 20)


def important(time, diff):
    a = [video.audio.get_frame(time)[0]]

    for d in range(diff + 1):
        if time - d * TIME_QUANTIUM > 0:
            a.append(video.audio.get_frame(time - d * TIME_QUANTIUM)[0])
        if time + d < video.duration:
            a.append(video.audio.get_frame(time + d * TIME_QUANTIUM)[0])

    return sum([abs(i) for i in a]) / len(a) > MIN_VOLUME_LVL


def video_processing(start_time, end_time, ind, return_dict):
    print(start_time, end_time)

    result_clips_times = []

    for time in range(start_time * TIME_X, end_time * TIME_X):
        print(f'PROCESS-{ind}: {int((time / TIME_X - start_time) / (end_time - start_time) * 100)}%')
        if important(time / TIME_X, 3):
            result_clips_times.append((time / TIME_X, time / TIME_X + TIME_QUANTIUM))

    return_dict[ind] = result_clips_times


if __name__ == '__main__':
    manager = multiprocessing.Manager()
    return_dict = manager.dict()

    one_process_video_time = video.duration // PROCESS_NUM

    processes = []

    for i in range(1, PROCESS_NUM):
        processes.append(
            Process(
                target=video_processing,
                args=((i - 1) * one_process_video_time, i * one_process_video_time, i, return_dict)
            )
        )
    processes.append(
        Process(
            target=video_processing,
            args=((PROCESS_NUM - 1) * one_process_video_time, video.duration, PROCESS_NUM, return_dict)
        )
    )

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    print('All videos are processed.')

    processed_videos = []
    for i in range(1, PROCESS_NUM + 1):
        processed_videos.extend([video.subclip(*j) for j in return_dict[i]])
    concatenate_videoclips(processed_videos).write_videofile('res.mp4')