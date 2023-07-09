
# Progressive Teacher

Progressive Teacher: [Boosting Facial Expression Recognition by A Semi-Supervised Progressive Teacher](https://scholar.google.com/citations?view_op=view_citation&hl=zh-CN&user=OCwcfAwAAAAJ&citation_for_view=OCwcfAwAAAAJ:u5HHmVD_uO8C)

Note:

- [MobileFaceNet](https://link.springer.com/chapter/10.1007/978-3-319-97909-0_46) is used as the backbone and the model is able to classify seven basic facial expressions (angry, disgust, fearful, happy, neutral, sad, surprised).
- [facial_expression_recognition_mobilefacenet_2022july.onnx](https://github.com/opencv/opencv_zoo/raw/master/models/facial_expression_recognition/facial_expression_recognition_mobilefacenet_2022july.onnx) is implemented here.

## Project setup

- install the latest `opencv-python`:

  ```shell
  python3 -m pip install opencv-python
  # Or upgrade to the latest version
  python3 -m pip install --upgrade opencv-python
  ```

## Demo

***NOTE***: This demo uses [../face_detection_yunet](../face_detection_yunet) as face detector.

Run the following command to try the demo:

```shell
# recognize the facial expression from camera input
python Emotion_Detection1.py
```



## Reference

- <https://github.com/opencv/opencv_zoo/tree/main/models/facial_expression_recognition>
