"""
Fichier original téléchargé ici : https://github.com/Camebush/real-time-yolov4-object-detection
"""

from cmd import PROMPT
import cv2
import numpy as np
import os
from datetime import datetime as dt

import utils.progress_bar as pb
from utils.frame_utils import rescale_frame

def _main(filepath, output = None,video_disp = False, frames_to_analyse=None, DEFAULT_CONFIANCE=0.5, SCALE=100, classes = None, no_output=False):
    # load our YOLO object detector trained on COCO dataset (80 classes)
    net = cv2.dnn.readNetFromDarknet('yolov4.cfg', 'yolov4.weights')
    ln = net.getLayerNames()
    ln = [ln[i- 1] for i in net.getUnconnectedOutLayers()]

    THRESHOLD = 0.4
    # load the COCO class labels our YOLO model was trained on
    with open('coco.names', 'r') as f:
        LABELS = f.read().splitlines()

    # initialize the video stream, pointer to output video file
    cap = cv2.VideoCapture(filepath)
    frames_num = int(cap. get(cv2. CAP_PROP_FRAME_COUNT))
    print(f"Nombre d'images de la vidéo traiter : {frames_num}")

    # modify max frame
    if frames_to_analyse:
        max_frame = frames_to_analyse
    else:
        max_frame = frames_num
    print(f"Nombre d'images à traiter : {max_frame}")

    # init frame counting and DataFrame
    frame = 0
    if output == None:
        results_file = ".".join(filepath.split(".")[0:-1]) + "_" + dt.now().strftime("%Y%m%d_%H%M%S")+".csv"
    else:
        results_file = output

    # initialize records
    with open(results_file, 'w') as result_file:
        result_file.write(";".join(["frame","box_x","box_y","box_w","box_h", "class", "confidence"]) + "\n")

    while True:
        _,image=cap.read()
        # Changement d'échelle de l'image si nécessaire
        if SCALE != 100:
            image = rescale_frame(image, percent=SCALE)
        height, width, _ = image.shape

        blob = cv2.dnn.blobFromImage(image, 1/255, (416, 416), (0,0,0), swapRB=True, crop=False)
        net.setInput(blob)
        layerOutputs = net.forward(ln)

        # initialize our lists of detected bounding boxes, confidences, and class IDs, respectively
        boxes = []
        confidences = []
        classIDs = []

        # loop over each of the layer outputs
        for output in layerOutputs:
            # loop over each of the detections
            for detection in output:
                # extract the class ID and confidence (i.e., probability)
                # of the current object detection
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]
                # filter out weak predictions by ensuring the detected
                # probability is greater than the minimum probability
                if confidence > DEFAULT_CONFIANCE:
                    # scale the bounding box coordinates back relative to
                    # the size of the image, keeping in mind that YOLO
                    # actually returns the center (x, y)-coordinates of
                    # the bounding box followed by the boxes' width and
                    # height
                    box = detection[0:4] * np.array([width, height, width, height])
                    (centerX, centerY, W, H) = box.astype("int")
                    # use the center (x, y)-coordinates to derive the top
                    # and and left corner of the bounding box
                    x = int(centerX - (W / 2))
                    y = int(centerY - (H / 2))
                    # update our list of bounding box coordinates,
                    # confidences, and class IDs
                    boxes.append([x, y, int(W), int(H)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)
            
        # apply non-maxima suppression to suppress weak, overlapping
        # bounding boxes
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, DEFAULT_CONFIANCE, THRESHOLD)

        # initialize a list of colors to represent each possible class label
        COLORS = np.random.uniform(0,255,size=(len(boxes), 3))

        # ensure at least one detection exists
        if len(indexes) > 0:
            # loop over the indexes we are keeping
            for i in indexes.flatten():
                if LABELS[classIDs[i]] in classes:
                    # extract the bounding box coordinates
                    (x, y, w, h) = boxes[i]
                    # draw a bounding box rectangle and label on the frame
                    color = COLORS[i]
                    text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
                    cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(image, text, (x, y + 20 ), cv2.FONT_HERSHEY_PLAIN, 1, color, 1)

                    # add the records to the file
                    with open(results_file, 'a') as result_file:
                        result_file.write(";".join([str(val) for val in [frame, x, y, w, h, LABELS[classIDs[i]], confidences[i]]]) + "\n")

        # Si on a choisit de regarder la vidéo pendant le traitement
        if video_disp:
            cv2.imshow('Image', image)

        if cv2.waitKey(1)==ord('q'):
            break

        frame+=1
        if (frame > max_frame):
            break
        pb.printProgressBar(frame, max_frame, prefix="Progression", decimals=2, length=100)
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-nv", "--no_video", help="Pour ne pas voir la sortie vidéo", action="store_true")
    parser.add_argument("-f", "--frames", help="Nombre d'images à traiter. Si l'argument n'est pas chosi, le code traite toute la vidéo", type=int)
    parser.add_argument("-i", "--input", help="(Requis) Chemin du fichier vers la vidéo à traiter", required=True)
    parser.add_argument("-o", "--output", help="Chemin vers le fichier de sortie. Si absent, enregistrement dans dossier vidéo entrée au format nom_video_date_heure.csv")
    parser.add_argument("--scale", help="Redimensionnement de la taille de la vidéo (en %%). ATTENTION : POUR L'ANALYSE IL FAUDRA PENSER A MODIFIER AUSSI L'ECHELLE. Defaut : 100%%", type=int, default=100)
    parser.add_argument("--confiance", help="Seuil de confiance entre 0 et 1 pour accepter une détection. Défaut : 0.5", type=float, default=0.5)
    parser.add_argument("--classes", "-c", help="Classes à détecter pour éviter. (Permet de ne pas détecter les feux de signalisation et les parapluies). Defaut: car, truck, motorbike, bus", nargs="+", default=["car", "bus", "truck", "motorbike"])
    parser.add_argument("--no_out", help="Pour ne pas enregistrer de résultats.", action="store_true")
    args = parser.parse_args()
    _main(args.input, output=args.output, video_disp = not(args.no_video), frames_to_analyse = args.frames, DEFAULT_CONFIANCE=args.confiance, SCALE = args.scale, classes = args.classes)

