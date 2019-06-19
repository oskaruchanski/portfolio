from imutils import paths
import numpy as np
import cv2
import os

logo_path = 'pics/logo.png'
logo = cv2.imread(logo_path, cv2.IMREAD_UNCHANGED)
logo_x_dim, logo_y_dim = logo.shape[:2]
logo.show
