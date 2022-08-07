# video_compressing

Данный код делает видео короче за счет удаления отрывков видео с низким уровнем звука. Это может быть полезно напрмер для сокращения лекций.

Например данная прорграмма сокращает длительность видео  ```input.mp4``` в 2 раза без потери важной информации. Результат записывается в ```output.mp4```.

Чтобы обработать выше видео:

1) ```git clone https://github.com/victormorozov1/video_compressing.git```
2) ```pip install moviepy```
3) Установите ```ffmpeg```

4) Поместите видео в папку с программой.

5) В командной строке запустите ```.\main.py {video_name}.mp4```. Результат запишется в ```output.mp4```.

Для каждого видео нужно использовать свой уровень громкости. По умолчанию он стоит ```0.01```. Если вырезаются важные куски видео то нужно понижать этот уровень. 
Если хочется сократить видео сильнее то нужно повысить этот уровень.

Чтобы указать свой уровень громкости:

```.\main.py {video_name}.mp4 {ваш уровень громкости}```. Напрмер: ```.\main.py lesson1.mp4 0.003```
