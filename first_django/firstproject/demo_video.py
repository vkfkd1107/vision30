# Required libraries
#-*-encoding:utf-8-*-
import Core.utils as utils
import keras_ocr
import easyocr
import cv2
import numpy as np
import time
import tensorflow as tf
import pytesseract
import os

from Core.config import cfg
from Core.yolov4 import YOLOv4, decode
from absl import app, flags
from absl.flags import FLAGS
from PIL import ImageFont, ImageDraw, Image
from Ninv import predict

kor_set = [
    '가', '나', '다', '라', '마', '하',
    '거', '너', '더', '러', '머', '버', '서', '어', '저', '허',
    '고', '노', '도', '로', '모', '보', '소', '오', '조', '호',
    '구', '누', '두', '루', '무', '부', '수', '우', '주',
    ]

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

gpus = tf.config.experimental.list_physical_devices('GPU')
tf.config.experimental.set_virtual_device_configuration(gpus[0],
    [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=2048)]) # limits gpu memory usage


reader = easyocr.Reader(['ko'])
pipeline = keras_ocr.pipeline.Pipeline() # downloads pretrained weights for text detector and recognizer

tf.keras.backend.clear_session()

STRIDES = np.array(cfg.YOLO.STRIDES)
ANCHORS = utils.get_anchors(cfg.YOLO.ANCHORS, False)
NUM_CLASS = len(utils.read_class_names(cfg.YOLO.CLASSES))
XYSCALE = cfg.YOLO.XYSCALE

flags.DEFINE_string('input', 'inputs/demo1.mp4', 'path to input video')
flags.DEFINE_string('output', 'results/output.avi', 'path to save results')
flags.DEFINE_integer('size', 608, 'resize images to')

input_path = ''
output_path = ''

def easyocrprediction(img):
    prediction_groups = reader.readtext(img, detail=0, blocklist = '!"#$%&\'()*+,-./:;<=>?@[\\]^_{|}~')
    print('Easyocr prediction: ', prediction_groups)
    return prediction_groups

def tesseractprediction(img):
    text = pytesseract.image_to_string(img, lang="kor")
    print('pytesseract prediction: ', text)
    return text

def Ninvprediction():
    ninvpred = predict.predict(r"temp\img.jpg", 'Ninv/saved_models/weights_best.pb')
    print("Ninv prediction: ", ninvpred)
    return ninvpred

def platePattern(string):
    '''Returns true if passed string follows
    the pattern of indian license plates,
    returns false otherwise.
    '''
    if len(string) == 7:
        if string[:2].isnumeric() == True and string[2].isalpha() == True and string[2] in kor_set and string[3:].isnumeric() == True:
            return True
        else:
            return False
    elif len(string) == 8:
        if string[:3].isnumeric() == True and string[3].isalpha() == True and string[3] in kor_set and string[4:].isnumeric() == True:
            if 100 <= int(string[4:]) <= 699:
                return True
            else:
                return False
    else:
        return False

def drawText(img, plates):
    '''Draws recognized plate numbers on the
    top-left side of frame
    '''
    string  = 'plates detected :- '
    for i in range(len(plates)):
        string = string + ',' + plates[i]
    
    print('string: ', string)
    fontpath = "fonts/gulim.ttc"
    font = ImageFont.truetype(fontpath, 10)

    (text_width, text_height) = font.getsize(string)
    box_coords = ((1, 30), (10 + text_width, 20 - text_height))
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    draw.rectangle((box_coords[0], box_coords[1]), fill='black')
    draw.text((5,17), string, font=font, fill='white')

    return np.array(img_pil)
    
def plateDetect(frame, input_size, model):
    '''Preprocesses image and pass it to
    trained model for license plate detection.
    Returns bounding box coordinates.
    '''
    frame_size = frame.shape[:2]
    image_data = utils.image_preprocess(np.copy(frame), [input_size, input_size])
    image_data = image_data[np.newaxis, ...].astype(np.float32)

    pred_bbox = model.predict(image_data)
    pred_bbox = utils.postprocess_bbbox(pred_bbox, ANCHORS, STRIDES, XYSCALE)

    bboxes = utils.postprocess_boxes(pred_bbox, frame_size, input_size, 0.25)
    bboxes = utils.nms(bboxes, 0.213, method='nms')
    
    return bboxes

def main(_argv):
    input_layer = tf.keras.layers.Input([FLAGS.size, FLAGS.size, 3])
    feature_maps = YOLOv4(input_layer, NUM_CLASS)
    bbox_tensors = []
    for i, fm in enumerate(feature_maps):
        bbox_tensor = decode(fm, NUM_CLASS, i)
        bbox_tensors.append(bbox_tensor)
    
    model = tf.keras.Model(input_layer, bbox_tensors)
    utils.load_weights(model, 'data/yolov4-obj_last.weights')
    
    vid = cv2.VideoCapture(FLAGS.input) # Reading input
    return_value, frame = vid.read()
    
    fourcc = cv2.VideoWriter_fourcc('F', 'M', 'P', '4')
    out = cv2.VideoWriter(FLAGS.output, fourcc, 10.0, (frame.shape[1],frame.shape[0]), True)

    plates = []

    n = 0
    Sum = 0
    while True:
        start = time.time()
        n += 1
        return_value, frame = vid.read()        
        if return_value is False:
            break
        if frame is None:
            continue
            
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        bboxes = plateDetect(frame, FLAGS.size, model) # License plate detection
        for i in range(len(bboxes)):
            img = frame[int(bboxes[i][1]):int(bboxes[i][3]), int(bboxes[i][0]):int(bboxes[i][2])]
            # cv2.imwrite(r"temp\img.jpg", img)
            print("============================================================")

            prediction_groups = easyocrprediction(img)

            string = ''
            if len(prediction_groups) != 0:
                for j in range(len(prediction_groups)):
                    string = string+ prediction_groups[j]
            
            string = string.replace(' ','').lstrip()
            print('string: ', string)

            if platePattern(string) == True and string not in plates:
                plates.append(string)
        
            print('plates:' , plates)
        if len(plates) > 0:
            frame = drawText(frame, plates)
        
        frame = utils.draw_bbox(frame, bboxes) # Draws bounding box around license plate
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        Sum += time.time()-start
        print('Avg fps:- ', Sum/n, '\n\n')

        out.write(frame)
        cv2.imshow("result", frame)
        if cv2.waitKey(1) == 27: break

    out.release()
    cv2.destroyAllWindows()

    print('*'*30)
    print("video detection complete")
    print('*'*30)

if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass