# code_opencv.py

Ce programme réalise le traitement d'image à partir de la Camera Module 3

Il permet de
- acquérir les images de la caméra avec Picamera2
- définir une zone d'intérêt correspondant au convoyeur
- convertir l'image dans l'espace colorimétrique HSV
- détecter les cubes selon leur couleur
- détecter les contours
- calculer la position X et Y du cube
- déterminer son orientation

# code_opencv_serveur_modbus.py

Ce programme combine le traitement d'image OpenCV(code précédant) avec un serveur Modbus TCP

Les informations calculées par OpenCV sont écrites dans les coils et les holding registers du serveur modbus afin d'être accessibles depuis un client distant.

Les informations transmises sont:
- présence du cube
- position X et Y
- orientation
- code de la couleur

# interface_client_modbus.py

Ce programme constitue le client modbus TCP du système

Il se connecte au serveur Modbus exécuté sur le Raspberry Pi et récupère les données

Une interface graphique développée avec Tkinter permet d'afficher:
- l'état de la connexion
- la présence du cube
- sa couleur
- sa position X et Y
- son orientation
