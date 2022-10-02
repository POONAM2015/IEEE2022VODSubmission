# IEEE2022-VOD-Submission
The repository contains the source code for reproducing the results of my submission to vehicle orientation detection challenge of IEEE Big Data Cup 2022.

# Steps
## Download this repo
Download this repository either using `git clone` or downloading the source code as zip.
After cloning, enter the directory using `cd IEEE2022-VOD-Submission`.

## Copying the data
### Training data
Copy training images (both train-1 and train-2 data) and their yolo labels to `main_train/images` and `main_train/labels` respectively.

### Validation data
- [Vehicle Orientation Dataset](https://github.com/sekilab/VehicleOrientationDataset) has been used for validation.
- Copy validation images and their yolo labels to `main_test/images` and `main_test/labels` respectively.

### Test data
Copy images of test-1 and test-2 (provided by Challenge) to `test_1/images` and `test_2/images` respectively.


## Training the model & Inference

### Creating and running Docker Image
Make a docker image containing [YOLOv7 source code](https://github.com/WongKinYiu/yolov7) using the command
```bash
docker build -t yolov7:pytorch21.08-py3 .
```
Start the docker container using
```bash
nvidia-docker run --rm --name yolov7_vehicle_docker -p 6006:6006 --ipc=host -it -v "`pwd`":/usr/src/mydataset -v "`pwd`/yolov7_vehicle/runs":/usr/src/app/yolov7/runs --shm-size=8g yolov7:pytorch21.08-py3
```

### Running the model for training and inference
Run `yolov7_vehicle/runs/work.ipynb`

## Performance 



# References
1. https://github.com/WongKinYiu/yolov7
2. https://github.com/sekilab/VehicleOrientationDataset
