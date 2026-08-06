from picamera2 import Picamera2
import numpy as np
import cv2

camera = Picamera2()    

config = camera.create_preview_configuration(main={"size": (640, 480), "format": "RGB888"})

camera.configure(config)
camera.start() 

while True:
    frame = camera.capture_array()
    belt = frame[22:431, 231:516]
    
    
    #couleur
    image_hsv = cv2.cvtColor(belt, cv2.COLOR_BGR2HSV)
    
 #  cv2.imshow("hsv", image_hsv)

# ===========================
# Définition des plages HSV
# ===========================

# Rouge (2 plages car le rouge est aux extrémités du cercle HSV)
    lower_rouge1 = np.array([0, 80, 70])
    upper_rouge1 = np.array([10, 255, 255])

    lower_rouge2 = np.array([170, 80, 70])
    upper_rouge2 = np.array([179, 255, 255])



# Vert
    lower_vert = np.array([35,80,80])
    upper_vert = np.array([85,255,255])

# Bleu
    lower_bleu = np.array([105, 100, 70])
    upper_bleu = np.array([130, 255, 255])

# Jaune
    lower_jaune = np.array([20,100,100])
    upper_jaune = np.array([35,255,255])



    mask1 = cv2.inRange(image_hsv, lower_rouge1, upper_rouge1)
    mask2 = cv2.inRange(image_hsv, lower_rouge2, upper_rouge2)

    mask_rouge = mask1  + mask2

    mask_vert = cv2.inRange(image_hsv, lower_vert, upper_vert)
    mask_bleu = cv2.inRange(image_hsv, lower_bleu, upper_bleu)
    mask_jaune = cv2.inRange(image_hsv, lower_jaune, upper_jaune)

    #cv2.imshow("masque rouge", mask_rouge)
    
    couleurs = [("Rouge", mask_rouge, (0, 0, 255)),("Vert", mask_vert, (0, 255, 0)),
    ("Jaune", mask_jaune, (0, 255, 255)),("Bleu", mask_bleu, (255, 0, 0))]

    for nom_couleur, masque, couleur_dessin in couleurs:

      contours_couleur, _ = cv2.findContours(masque,cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)

      for cnt in contours_couleur:

        area = cv2.contourArea(cnt)

        if area > 500:

            rect = cv2.minAreaRect(cnt)

            (cx, cy) = rect[0]
            angle = rect[2]

            box = cv2.boxPoints(rect)
            box = box.astype(int)

            cv2.drawContours(belt,[box],0, couleur_dessin,2)

            cv2.circle(belt,(int(cx), int(cy)),4,(255, 255, 255),-1)

            text = (f"{nom_couleur} "
                f"X:{int(cx)} "
                f"Y:{int(cy)} "
                f"Angle:{angle:.1f}")

            cv2.putText(belt, text, (int(cx) - 60, int(cy) - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                        couleur_dessin, 2)



    
    
    
    
    cv2.imshow("Detection des cubes", belt)


    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
camera.stop()




