# Analyse d'image par IA : Utilisation de Yolov4

VERSION STREAMING YOUTUBE (vidéo entrante : https://www.youtube.com/watch?v=5_XSYlAfJZM)
Il s'agit d'un fork de https://gitlab.cerema.fr/Aurelien.clairais/yolov4-detection permettant l'analyse "en temps réel" d'un flux live youtube.
Pour tenir quelque chose de proche du temps réel, sur ma machine, j'ai décidé de sauter 24 images (à modifier dans `main.py`). Je pense qu'on peut obtenir des performances nettement meilleures sur des machines plus puissantes et CUDA (sur des CG NVIDIA)

## Installation avec Anaconda

1. Créer un environnement virtuel vide

```
conda create -n myenv python pip --no-default-packages
```

2. Installer les dépendances
```
pip install -r requirements.txt
```

3. Télécharger les fichiers de Yolov4

- **cfg** : https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.cfg
- **weights** : https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights
- **Coco names** : https://github.com/pjreddie/darknet/blob/master/data/coco.names

3. Lancer le code
```
python main.py
```

## Utilisation sur une autre vidéo

Modifier le fichier `main.py` à la ligne 20 avec le nom du fichier contenant la vidéo à analyser.

```python
# initialize the video stream, pointer to output video file
cap = cv2.VideoCapture("https://www.youtube.com/watch?v=RQA5RcIZlAM")
```

### Quelques vidéos live sur lesquelles jouer :
- [Village of Tilton - Traffic Camera](https://www.youtube.com/watch?v=5_XSYlAfJZM)
- [LIVE】Tokyo Shinjuku Live Cam新宿大ガード交差点【2022】](https://www.youtube.com/watch?v=RQA5RcIZlAM)
- [ LIVE 】東京都 新宿 歌舞伎町 24時間 ライブ / Tokyo Shinjuku Kabukicho Live
](https://www.youtube.com/watch?v=DjdUEyjx8GM) (piétons)

Suggestion de recherche : https://www.youtube.com/results?search_query=traffic+camera+real+time


## Crédits 

Github original de `main.py` : https://github.com/Camebush/real-time-yolov4-object-detection

Site officiel YOLO: https://pjreddie.com/darknet/yolo/

## Bugs

- `main.py`: Lancement impossible pour `FRAME_SKIP`<2