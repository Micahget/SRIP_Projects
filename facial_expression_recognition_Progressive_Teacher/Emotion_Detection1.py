import sys
import argparse
import copy
import datetime

import numpy as np
import cv2 as cv

from facial_fer_model import FacialExpressionRecog


# sys.path.append('C:/Users/mikiy/OneDrive/Desktop/Image Processing Projects/opencv zoo/opencv_zoo/models/face_detection_yunet/yunet.py')
from yunet import YuNet

# Valid combinations of backends and targets
backend_target_pairs = [  
    [cv.dnn.DNN_BACKEND_OPENCV, cv.dnn.DNN_TARGET_CPU],
    [cv.dnn.DNN_BACKEND_CUDA,   cv.dnn.DNN_TARGET_CUDA],
    [cv.dnn.DNN_BACKEND_CUDA,   cv.dnn.DNN_TARGET_CUDA_FP16],
    [cv.dnn.DNN_BACKEND_TIMVX,  cv.dnn.DNN_TARGET_NPU],
    [cv.dnn.DNN_BACKEND_CANN,   cv.dnn.DNN_TARGET_NPU]
]

parser = argparse.ArgumentParser(description='Facial Expression Recognition')
parser.add_argument('--model', '-m', type=str, 
                    default='./facial_expression_recognition_mobilefacenet_2022july.onnx',
                    help='Path to the facial expression recognition model.')
parser.add_argument('--backend_target', '-bt', type=int, default=0,
                    help='''Choose one of the backend-target pair to run this demo:
                        {:d}: (default) OpenCV implementation + CPU
                    '''.format(*[x for x in range(len(backend_target_pairs))]))
args = parser.parse_args()


def visualize(image, det_res, fer_res, box_color=(0, 255, 0), text_color=(0, 0, 255)):

    print('%s %3d faces detected.' % (datetime.datetime.now(), len(det_res)))

    output = image.copy()
    landmark_color = [
        (255,  0,   0),  # right eye
        (0,    0, 255),  # left eye
        (0,  255,   0),  # nose tip
        (255,  0, 255),  # right mouth corner
        (0,  255, 255)   # left mouth corner
    ]

    for ind, (det, fer_type) in enumerate(zip(det_res, fer_res)):
        bbox = det[0:4].astype(np.int32)
        fer_type = FacialExpressionRecog.getDesc(fer_type)
        print("Face %2d: %d %d %d %d %s." %
              (ind, bbox[0], bbox[1], bbox[0]+bbox[2], bbox[1]+bbox[3], fer_type))
        cv.rectangle(output, (bbox[0], bbox[1]),
                     (bbox[0]+bbox[2], bbox[1]+bbox[3]), box_color, 2)
        cv.putText(output, fer_type,
                   (bbox[0], bbox[1]+12), cv.FONT_HERSHEY_DUPLEX, 0.5, text_color)
        landmarks = det[4:14].astype(np.int32).reshape((5, 2))
        for idx, landmark in enumerate(landmarks):
            cv.circle(output, landmark, 2, landmark_color[idx], 2)
    return output


# this function is used to run the model on the input image and get the results
def process(detect_model, fer_model, frame):
    h, w, _ = frame.shape
    detect_model.setInputSize([w, h])
    dets = detect_model.infer(frame)
    # print(dets)

    if dets is None:
        return False, None, None

    fer_res = np.zeros(0, dtype=np.int8)
    for face_points in dets:
        fer_res = np.concatenate(
            (fer_res, fer_model.infer(frame, face_points[:-1])), axis=0) 
        print( 'this is the output of the detected face emotion: ', fer_res)
        print ('this is the shape of the output of the detected face emotion: ', fer_res.shape)
        print ('this is the type of the output of the detected face emotion: ', type(fer_res))
    return True, dets, fer_res


if __name__ == '__main__':
    backend_id = backend_target_pairs[args.backend_target][0]
    target_id = backend_target_pairs[args.backend_target][1]

    detect_model = YuNet(
        modelPath='../face_detection_yunet/face_detection_yunet_2023mar.onnx')

    fer_model = FacialExpressionRecog(modelPath=args.model,
                                      backendId=backend_id,
                                      targetId=target_id)

    # if args.input is None:
    deviceId = 0
    cap = cv.VideoCapture(deviceId)

    while cv.waitKey(1) < 0:
        hasFrame, frame = cap.read()
        frame = cv.flip(frame, 1)
        if not hasFrame:
            print('No frames grabbed!')
            break
        # Get detection and fer results
        status, dets, fer_res = process(detect_model, fer_model, frame)
        if status:
            # Draw results on the input image
            frame = visualize(frame, dets, fer_res)
        # Visualize results in a new window
        cv.imshow('FER Demo', frame)
