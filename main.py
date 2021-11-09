import sys 
import math
import cv2
from PIL import Image #ImageEnhance
import numpy as np
import datetime
import os
import shutil  # Библиотека для работы с файлами
import moviepy.editor as mpy  # Библиотека для записи видео
import glob  # расширение для использования Unix обозначений при задании пути к файлу

# Стутусы отображения
isColor = True
isLogo = False
isCaption = False
isClock = False
isRecord = False

# Получаем кадр с видеокамеры
frame = cv2.VideoCapture(0)
height = int(frame.get(4))
width = int(frame.get(4))

def addcolor(img):
    img = cv2.cvtColor(img, cv2.COLOR)

isFlip = False
isAddColor = False

out = None


# Загружаем картинки
record_icon_img = cv2.imread('record-icon.png', cv2.IMREAD_UNCHANGED)

# Переводим массивы в объекты Pillow
record_icon = Image.fromarray(record_icon_img)

# Тут будет храниться номер кадра
file_counter = 0
# Директория для записи кадров
videoDir = 'video'



# Накладываем значок индикатора записи
def add_record(img):
	# Переводим массив изображения в объект Pillow и преобразуем в тип RGBA с маской прозрачности
	img_out = Image.fromarray(img)

	img_out.paste(record_icon, (10, 420), record_icon)

	return np.asarray(img_out, dtype='uint8')



# Начинаем запись
def start_recording():
	global file_counter

	if os.path.isdir(videoDir):
		shutil.rmtree(videoDir+'/')  # удаляем каталог вместе с содержимым

	os.mkdir(videoDir)
	file_counter = 0


# Заканчиваем запись
def stop_recording():
	if os.path.isdir(videoDir):
		gif_name = 'second_video.gif'
		video_name = 'second_video.mp4'
		fps = 10

		files = glob.glob(videoDir + '/*.png')
		files.sort()

		file_list = []
		for i in files:
			for j in range(3):
				file_list.append(i)

		clip = mpy.ImageSequenceClip(file_list, fps=fps)
		#clip.write_gif('{}'.format(gif_name), fps=fps)
		clip.write_videofile(video_name)


def save_frame(img):
	global file_counter

	file_name = "%05d" % file_counter
	cv2.imwrite(videoDir+'/'+file_name+".png", img)

	file_counter += 1



while True:
    status, image = frame.read()
    image = image.copy()
    if isFlip:
        image = cv2.flip(image, -1)  # 0 – по вертикали, 1 – по горизонтали, (-1) – по вертикали и по горизонтали

    hsv_min = np.array((40, 40, 70), np.uint8)
    hsv_max = np.array((50, 50, 100), np.uint8)

    # Меняем цветовую модель с BGR на HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    if not isAddColor:
        image = cv2.cvtColor(image, cv2.COLOR_HSV2RGB)
        image[(...,1)] = image[(...,0)] * 1.10
        np.clip(image, 0, 255)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)



    image_done = image.copy()
    if isRecord:
        save_frame(image)
        image = add_record(image)
    # if isRecord:
	# 	save_frame(image)
	# 	image = add_record(image)


    cv2.imshow("TV", image_done)
    k = cv2.waitKey(30)

    if k == 100:
        isAddColor = not isAddColor
    
    
    # Обрабатываем нажатие клавиши S для поворота 180
    if k == 83:
    
        isFlip = not isFlip
        
    # нажмите на кнопку r чтобы начать запись,чтобы закончить запись нажмите r
    if k == 114:
        if not isRecord:
            start_recording() # начинаем запись
            isRecord = True
        else:
            stop_recording()
            isRecord = False

    # Обрабатываем нажатие клавиши Esc для выхода
    if k == 27:
        break

frame.release()
cv2.destroyAllWindows()
