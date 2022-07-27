import multiprocessing
from moviepy.editor import *
from multiprocessing import Process
from time import time
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

TIME_X = 100
TIME_QUANTIUM = 1 / TIME_X
MIN_VOLUME_LVL = 0.003
PROCESS_NUM = 4
VIDEO_NAME = '4n.mp4'
SPACE_TIME = 1

video = VideoFileClip(VIDEO_NAME)
print(video.duration)


def important(time, diff):
    a = [video.audio.get_frame(time)[0]]

    for d in range(diff + 1):
        if time - d * TIME_QUANTIUM > 0:
            a.append(video.audio.get_frame(time - d * TIME_QUANTIUM)[0])
        if time + d < video.duration:
            a.append(video.audio.get_frame(time + d * TIME_QUANTIUM)[0])

    return sum([abs(i) for i in a]) / len(a) > MIN_VOLUME_LVL


def video_processing(start_time, end_time, ind, return_dict):
    files = []
    print(start_time, end_time)

    result_clips_times = []

    for time in range(start_time * TIME_X, end_time * TIME_X):
        if important(time / TIME_X, 3):
            result_clips_times.append([time / TIME_X, time / TIME_X + TIME_QUANTIUM])

    if not result_clips_times:
        return

    result_clips_times2 = [result_clips_times[0]]

    for time_interval in result_clips_times[1::]:

        if time_interval[0] - result_clips_times2[-1][1] < SPACE_TIME:
            result_clips_times2[-1][1] = time_interval[1]
        else:
            result_clips_times2.append(time_interval)

    for i in range(len(result_clips_times2)):
        filename = f"videos/res{ind}-{i}.mp4"
        ffmpeg_extract_subclip(VIDEO_NAME, *result_clips_times2[i], targetname=filename)
        files.append(filename)
    return_dict[ind] = files


if __name__ == '__main__':
    start_time = time()

    manager = multiprocessing.Manager()
    return_dict = manager.dict()

    print('duration:', video.duration)
    one_process_video_time = int(video.duration) // PROCESS_NUM
    print(int(video.duration))
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

    print('All videos are processed.')

    all_video_names = open("list.txt", "w")
    for i in sorted(return_dict.keys()):
        for filename in return_dict[i]:
            all_video_names.write(f"file '{filename}'\n")

    all_video_names.close()

    os.system('concatenate_videos.bat')

    print(time() - start_time)
