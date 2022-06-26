import string
from tkinter.ttk import Separator
import pandas as pd
import os
import numpy as np

import cv2

import utils.progress_bar as pb

def main(input_video, input_data, sep="point-virgule", arg_frames=None, fps=60):
    #...
    if arg_frames == None:
        frames_disp = np.infty
    else:
        frames_disp = arg_frames
    #...
    # Gestion du separateur
    sep_dict = {
        "point-virgule" : ";",
        "virgule" : ",",
        "tabulation" : "\t"
    }
    records = pd.read_csv(input_data, sep=sep_dict[sep])

    # Read the original video analysis
    # initialisation
    frame = 0
    cap = cv2.VideoCapture(input_video)

    #...
    total_frames = min([max(records["frame"]), frames_disp, int(cap. get(cv2. CAP_PROP_FRAME_COUNT))])

    while True: 
        _,image=cap.read()
        height, width, _ = image.shape
        # ...
        # Récupération des records de cette frame
        recs = records[records["frame"]==frame].reset_index()

        COLORS = np.random.uniform(0,255,size=(recs.shape[0], 3))
        for index, row in recs.iterrows():
            # Même code ici que dans "read_data.py"
            #...
            # draw a bounding box rectangle and label on the frame
            color = COLORS[index]
            text = "{}: {:.4f}".format(row["class"], row["confidence"])
            cv2.rectangle(image, (row["box_x"], row["box_y"]), (row["box_x"] + row["box_w"], row["box_y"] + row["box_h"]), [0,0,0], 2)
            cv2.putText(image, text, (row["box_x"], row["box_y"] + 20 ), cv2.FONT_HERSHEY_PLAIN, 2, [0,0,0], 2)

        # Afficher l'image
        cv2.imshow('Image', image)
        pb.printProgressBar(frame, total_frames, prefix="Progression", decimals=2, length=100)
        frame+=1

        # 60 fps donc 15 millisecondes dans waitKey
        if cv2.waitKey(int(1000/fps))==ord('q'):
            break

        if frame > total_frames:
            break
    # Libérer les ressources à la fin
    cap.release()
    cv2.destroyAllWindows()
    

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-iv", "--in_video", help="Chemin vers la vidéo à lire", required=True)
    parser.add_argument("-id", "--in_data", help="Chemin vers le fichier csv des informations traitées", required=True)
    parser.add_argument("--sep", help="Séparateur de colonne dans le csv : point-virgule, virgule, tabulation. Défaut : point-virgule", default="point-virgule", choices=['virgule', 'point-virgule', 'tabulation'])
    parser.add_argument("-f", "--frames", help="Nombre d'image à afficher (est capé au nombre d'entrées dans les données automatiquement). Défaut: Nombre d'images dans les données", type=int)
    parser.add_argument("--fps", help="Nombre maximum d'image par seconde (N'allant pas au dela des capacité de la machine). Defaut: 60.", type=int, default=60)
    args = parser.parse_args()
    print(args)
    main(args.in_video, args.in_data, sep=args.sep, arg_frames=args.frames, fps=args.fps)