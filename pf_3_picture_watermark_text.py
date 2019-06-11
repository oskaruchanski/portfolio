# bulk adding watermark to pictures in given location
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import glob
import os

# inputs
img_path = 'pics/'
img_files = [img for img in glob.glob(img_path + '*.jpg')]

# outputs
output_path = 'pics/marked/'
output_name_tag = '_watermarked.jpg'
os.makedirs(output_path, exist_ok=True)

# font setting
wm_text = 'downloaded from pixabay.com'
wm_font = ImageFont.truetype('/Library/Fonts/AmericanTypewriter.ttc', size=20)
wm_x_dim, wm_y_dim = wm_font.getsize(wm_text)
wm_color = (255, 255, 255)

for img_file in img_files:
    img_file_name = os.path.basename(img_file)[:-4]
    photo = Image.open(img_file)

    x_dim, y_dim = photo.size
    res_x_dim = 1280
    res_y_dim = int(y_dim/x_dim * res_x_dim)
    photo = photo.resize((res_x_dim, res_y_dim))

    drawing = ImageDraw.Draw(photo)

    wm_position = (res_x_dim-wm_x_dim-5, res_y_dim-wm_y_dim-5)
    drawing.text(wm_position, wm_text, fill=wm_color, font=wm_font)
    photo.save(output_path+img_file_name+output_name_tag)
