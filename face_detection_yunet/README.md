# Face Detection with OpenCV and yunet Model

YuNet is a light-weight, fast and accurate face detection model, which achieves 0.834(AP_easy), 0.824(AP_medium), 0.708(AP_hard) on the WIDER Face validation set. This project is used to detect faces in images and videos using YuNet model with OpenCV.

Notes:

- Model source: [here](https://github.com/Micahget/IITGN_SRIP_Projects/blob/main/face_detection_yunet/face_detection_yunet_2023mar_int8.onnx).
- This model can detect **faces of pixels between around 10x10 to 300x300** due to the training scheme.

## Demo

### Python

Run the following command to try the demo:

```shell
# detect on camera input
python detectFaces.py

```

## Reference

- https://github.com/opencv/opencv_zoo/tree/main/models/face_detection_yunet
- https://github.com/ShiqiYu/libfacedetection.train
