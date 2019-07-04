from imutils import paths
import numpy as np
import glob
import cv2
import os

# logo infos
logo_path = 'pics/logo.png'
logo = cv2.imread(logo_path, cv2.IMREAD_UNCHANGED)
logo_x_dim, logo_y_dim = logo.shape[:2]

(B, G, R, A) = cv2.split(logo)
B = cv2.bitwise_and(B, B, mask=A)
G = cv2.bitwise_and(G, G, mask=A)
R = cv2.bitwise_and(R, R, mask=A)
logo = cv2.merge([B, G, R, A])

# inputs
img_path = 'pics/'
images = [img for img in glob.glob(img_path + '*.jpg')]
images[0]

# outputs
output_path = 'pics/watermarked/'
output_name_tag = '_logo.png'
os.makedirs(output_path, exist_ok=True)

for img in images:
    image = cv2.imread(img)
    (h, w) = image.shape[:2]
    image = np.dstack([image, np.ones((h, w), dtype="uint8") * 255])

    overlay = np.zeros((h, w, 4), dtype="uint8")
    overlay[h - logo_x_dim - 10:h - 10, w - logo_y_dim - 10:w - 10] = logo

    # blend the two images together using transparent overlays
    output = image.copy()
    cv2.addWeighted(overlay, 1.0, output, 1.0, 0, output)

    # write the output image to disk
    filename = img[img.rfind(os.path.sep) + 1:]
    p = os.path.sep.join((output_path, filename))
    cv2.imwrite(p, output)
