import multiprocessing
import sys
from moviepy.editor import *
from multiprocessing import Process
from time import time
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os
import shutil

TIME_X = 100
TIME_QUANTIUM = 1 / TIME_X
MIN_VOLUME_LVL = float(sys.argv[2]) if len(sys.argv) >= 3 else 0.01
PROCESS_NUM = 4
VIDEO_NAME = sys.argv[1] if len(sys.argv) >= 2 else 'input.mp4'
SPACE_TIME = 1

video = VideoFileClip(VIDEO_NAME)


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
        if important(time / TIME_X, 3):
            result_clips_times.append([time / TIME_X, time / TIME_X + TIME_QUANTIUM])

    return_dict[ind] = result_clips_times


def check_video_folder():
    if not os.path.exists('videos'):
        os.mkdir('videos')


def delete_video_folder():
    shutil.rmtree('videos')


def main():
    check_video_folder()

    manager = multiprocessing.Manager()
    return_dict = manager.dict()

    print('duration:', video.duration)
    print('video name:', VIDEO_NAME)
    print('min volume level:', MIN_VOLUME_LVL)

    one_process_video_time = int(video.duration) // PROCESS_NUM

    print(one_process_video_time)

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
            args=((PROCESS_NUM - 1) * one_process_video_time, int(video.duration), PROCESS_NUM, return_dict)
        )
    )

    print(processes)

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    time_intervals = []
    for a in return_dict.values():
        time_intervals.extend(a)
    time_intervals.sort()

    time_intervals2 = [time_intervals[0]]
    for time_interval in time_intervals[1::]:
        if time_interval[0] - time_intervals2[-1][1] < SPACE_TIME:
            time_intervals2[-1][1] = time_interval[1]
        else:
            time_intervals2.append(time_interval)

    print(time_intervals2)
    files = []
    for i in range(len(time_intervals2)):
        filename = f"videos/res{i}.mp4"
        ffmpeg_extract_subclip(VIDEO_NAME, *time_intervals2[i], targetname=filename)
        files.append(filename)

    all_video_names = open("list.txt", "w")
    for filename in files:
        all_video_names.write(f"file '{filename}'\n")

    all_video_names.close()

    os.system('concatenate_videos.bat')

    delete_video_folder()


if __name__ == '__main__':
    start_time = time()

    try:
        main()
    except BaseException as e:
        print(e)

    print('working time:', time() - start_time)


