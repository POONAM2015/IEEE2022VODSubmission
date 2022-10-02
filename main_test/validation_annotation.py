import os, shutil, glob
import time
from multiprocessing import Pool
from os.path import basename as opbasename
from os.path import join as opjoin

SRC = 'old_labels' # contains VOD labels
DEST = 'new_labels' # contains SOD labels

if os.path.exists(DEST):
    shutil.rmtree(DEST)
os.mkdir(DEST)

new_label = {'0': '0',
'1':'1',
'2':'2',
'3':'12',
'4':'13',
'5': '14',
'6':'3',
'7':'4',
'8':'5',
'9':'6',
'10':'7',
'11':'8',
'12':'9',
'13':'10',
'14':'11'}

def read_file_and_write(filepath):
    filename = opbasename(filepath)
    with open(filepath, 'r') as f_read:
        lines = f_read.readlines()
        newlines = []
        for line in lines:
            lineparts = line.split(' ')
            oldcat = lineparts[0]
            newcat = new_label[oldcat]
            lineparts[0] = newcat

            newlines.append(' '.join(lineparts))
    with open(opjoin(DEST, filename), 'w') as f_write:
        f_write.writelines(newlines)


filepaths = glob.glob(os.path.join(SRC, '*.txt'))

start_time = time.perf_counter()
with Pool() as pool:
    res = pool.imap_unordered(read_file_and_write, filepaths)
    for r in res:
        print(r)
end_time = time.perf_counter()

print(f'Finished {i} in {end_time - start_time}')
