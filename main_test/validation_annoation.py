import os, shutil, glob
import time
from multiprocessing import Pool
from os.path import basename as opbasename
from os.path import join as opjoin

SRC = 'old_labels'
NEW_LABLES = 'new_labels'
DEST = NEW_LABLES + '1'
DEST1 = NEW_LABLES + '2'
DEST2 = NEW_LABLES + '3'

for d in [DEST, DEST1, DEST2]:
    if not os.path.exists(d):
        os.mkdir(d)
    else:
        shutil.rmtree(d)
        os.mkdir(d)
# DEST_IMG = 'myimages'
# DEST_LABEL = 'mylabels'

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
    with open(opjoin(DEST1, filename), 'w') as f_write:
        f_write.writelines(newlines)


filepaths = glob.glob(os.path.join(SRC, '*.txt'))

start_time = time.perf_counter()
i = 0
for label_path in filepaths:
    i += 1
    with open(label_path, 'r') as fread:
        lines = fread.readlines()
        newlines = []
        for line in lines:
            lineparts = line.split(' ')
            oldcat = lineparts[0]
            newcat = new_label[oldcat]
            lineparts[0] = newcat

            newlines.append(' '.join(lineparts))

    with open(os.path.join(DEST, os.path.basename(label_path)), 'w') as fwrite:
        fwrite.writelines(newlines)
end_time = time.perf_counter()
        # print('-----------')
print(f'finished {i} in {end_time - start_time} seconds')

start_time = time.perf_counter()
for filepath in filepaths:
    read_file_and_write(filepath)
end_time = time.perf_counter()

print(f'Finished {i} in {end_time - start_time}')

start_time = time.perf_counter()
with Pool() as pool:
    pool.imap_unordered(read_file_and_write, filepaths)
end_time = time.perf_counter()

print(f'Finished {i} in {end_time - start_time}')
