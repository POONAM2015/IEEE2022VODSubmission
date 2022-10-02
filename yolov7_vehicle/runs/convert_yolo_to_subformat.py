import os, glob
import cv2
from typing import List
from multiprocessing import Pool
import time, argparse

def convert_bb(dh, dw, bbox) -> List[float]:
    """
    draws bounding boxes on the image and returns the image with bounding box on it
    :param image: numpy array of the image
    :param bboxes: List[List[float]] -- list of bounding boxes
    :return: numpy array of image with bounding boxes drawn on it
    """
    
    x, y, w, h = bbox
    l = (x - w / 2) * dw
    r = (x + w / 2) * dw
    t = (y - h / 2) * dh
    b = (y + h / 2) * dh
    
    if l < 0:
        l = 0
    if r > dw - 1:
        r = dw - 1
    if t < 0:
        t = 0
    if b > dh - 1:
        b = dh - 1
    
    return [l, t, r, b]


def bb(image_path: str, label_path: str) -> List[float]:
    """
    extracts details of all bounding boxes from the label path and returns its list
    :param image_path: str, is the path of image
    :param label_path: str, is the path of label (annotation)
    :return: List[List[float]] which is the list of all bounding boxes,
    where, each bounding box is a list of [x, y, w, h] in the normalised form as is in the yolo format
    """
    img = cv2.imread(image_path)
    dh, dw, _ = img.shape

    # reads the label.txt
    fl = open(label_path, 'r')
    data = fl.readlines()
    fl.close()

    lines = ''
    linesep = ' '

    for dt in data:
        line = []
        ctype, x, y, w, h, c = map(float, dt.split(' '))
        line.append(classes_dict[int(ctype)])
        xmin, ymin, xmax, ymax = list(map(str, convert_bb(dh, dw, [x,y,w,h])))
        c = str(round(c, 2))
        for _ in [c, xmin, ymin, xmax, ymax]:
            line.append(_)        
        lines +=  linesep + ' '.join(line)
    lines += '\n'
    return lines


def mywritefunc(imagepath, labelpath, filename):
    # read every label, find every image, write on the ans.txt
    labelbasename = os.path.basename(labelpath)   
    with open(filename, 'a') as f:
        lines = bb(imagepath, labelpath)
        f.write(labelbasename + lines)    
    f.close()


def func(I, L, filename):
    image_ext = '.jpg'
    for label_path in glob.glob(os.path.join(L, '*.txt')):
        basename = os.path.basename(label_path)
        image_name = basename[:-4] + image_ext
        image_path = os.path.join(I, image_name)
        # if counter == 5:
        #     return
        try:
            mywritefunc(image_path, label_path, filename)
            # counter += 1
        except Exception:
            print(label_path)


classes_dict = ['car_back', 'car_side', 'car_front', 
'truck_back', 'truck_side', 'truck_front', 
'motorcycle_back', 'motorcycle_side', 'motorcycle_front', 
'cycle_back', 'cycle_side','cycle_front',
'bus_back', 'bus_side', 'bus_front']


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--imagepath', type=str, default='/usr/src/mydataset/test_1/images', help='enter folderpath containing images')
    parser.add_argument('--labelpath', type=str, help='enter folderpath containing labels of above images')
    # parser.add_argument('--filename', type=str, help='enter filename to store .txt file')
    opt = parser.parse_args()

    if opt.imagepath == 'test_1':
        IMAGEPATH = '/usr/src/mydataset/test_1/images'
    elif opt.imagepath == 'test_2':
        IMAGEPATH = '/usr/src/mydataset/test_2/images'
    else:
        IMAGEPATH = opt.imagepath
    
    f = opt.labelpath.split('/')[-2]

    print(f'image source: {IMAGEPATH}')
    FILENAME = f'runs/submissions/{f}.txt'
    print(f'Writing file {FILENAME}')

    start_time = time.perf_counter()
    func(IMAGEPATH, opt.labelpath, FILENAME)
    end_time = time.perf_counter()
    print(f'Time taken: ({end_time-start_time})s')
    print(f'Finished. Output saved in {FILENAME} .')