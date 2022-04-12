import os
from ocr import ocr
import time
import shutil
import numpy as np
from PIL import Image
from glob import glob
import cv2
import argparse
from speed_schema import SpeedSchema


def single_pic_proc(image_file):
    image = np.array(Image.open(image_file).convert('RGB'))
    result, image_framed = ocr(image)
    return result,image_framed



def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
def get_color(image):
    return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image,5)
 
#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]



def run(args):
    video_path = args.input
    vid = cv2.VideoCapture('tempdir/' + video_path)
    if not vid.isOpened():
        # print('/home/test/git_temp/Project_V/ServerTele/app/pyscripts/yolo/yolo.py/../../tempdir/aa25193476823fe1791f0fe9c76eaef1')
        raise IOError("Couldn't open webcam or video")

    counter = 0
    setFPS = 25
    vs = SpeedSchema('Speed', args.input)

    avg_speed = 0
    while True:
        return_value, frame = vid.read()
        if frame is None:
            break
        image = Image.fromarray(frame)
        result = np.asarray(image)
        # print(result.shape)
        result = result[300:, 298:380,:]
        # print(result.shape)
        
        
        # result = sharp(result)

        result = get_grayscale(result)
        result = cv2.bitwise_not(result)
        result = thresholding(result)
        result = get_color(result)
        # result = apply_brightness_contrast(result, 0, 80)
        # result = sharp(result)
        # print(result)
        # result[:, ] = 255
        # cv2.imwrite( '_out/Frame'+str(counter)+'.jpg', result)

        
        txt, image_framed = ocr(result)
        for key in txt:
            new_string = txt[key][1]
            emp_str = ""
            for m in new_string:
                if m.isdigit():
                    emp_str = emp_str + m
            if emp_str != '':
                emp_str = int(emp_str)
                avg_speed += emp_str
        if (counter+1) % setFPS == 0:
            vs.create_one({
                'vidID': args.input,
                'time': int(counter / setFPS) + 1,
                'speed': avg_speed/setFPS
            })
            print(f'{counter}: {round(avg_speed/setFPS, 1)}')
            avg_speed = 0
            
        counter += 1
        cv2.namedWindow("result", cv2.WINDOW_NORMAL)
        cv2.imshow("result", result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    # class YOLO defines the default value, so suppress any default here
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    '''
    Command line options
    '''
    parser.add_argument(
        '--input', type=str,
        help='input name of file'
    )
    FLAGS = parser.parse_args()
    run(FLAGS)