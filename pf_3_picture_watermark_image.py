import os
import glob
from PIL import Image

# watermark logo
logo_path = 'pics/logo.png'
logo = Image.open(logo_path)
logo = logo.convert("RGBA")
logo_x_dim, logo_y_dim = logo.size
logo = logo.resize((int(logo_x_dim/2), int(logo_y_dim/2)))

# inputs
img_path = 'pics/'
img_files = [img for img in glob.glob(img_path + '*.jpg')]

# outputs
output_path = 'pics/wlogo/'
output_name_tag = '_logo.png'
os.makedirs(output_path, exist_ok=True)

# gray box as logo background
bgox = Image.new('RGBA', (int(0.5*logo_x_dim)+4,
                          int(0.5*logo_y_dim)+4), color=(211, 211, 211, 85))

for img_file in img_files:
    img_file_name = os.path.basename(img_file)[:-4]
    photo = Image.open(img_file).convert("RGBA")

    x_dim, y_dim = photo.size
    res_x_dim = 1280
    res_y_dim = int(y_dim/x_dim * res_x_dim)
    photo = photo.resize((res_x_dim, res_y_dim))
    photo.paste(bgox, (res_x_dim-int(0.5*logo_x_dim)-7,
                       res_y_dim-int(0.5*logo_y_dim)-7), mask=bgox)

    photo.paste(logo, (res_x_dim-int(0.5*logo_x_dim)-5,
                       res_y_dim-int(0.5*logo_y_dim)-5), logo)
    photo.save(output_path+img_file_name+output_name_tag)
