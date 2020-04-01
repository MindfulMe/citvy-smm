import random
import textwrap
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

def make_artwork(in_file, out_file, text):

    if not in_file.lower().endswith(".jpg") and not in_file.lower().endswith(".jpeg"):
        im = Image.open(in_file)
        rgb_im = im.convert('RGB')
        new_name = in_file.split(".")[0]
        in_file = f"{new_name}.jpg"
        rgb_im.save(in_file)

    img = Image.open(in_file)
    draw = ImageDraw.Draw(img)

    cr = 0 # count of russian chars
    ce = 0 # count of english chars

    for char in text:
        n = ord(char)
        if n > 1040 and n < 1103:
            cr += 1
        elif n > 65 and n < 122:
            ce += 1

    if cr > ce:
        lang = "Russian"
    else:
        lang = "English"

    W, H = img.size
    colors = [{"bg_color": "#ffffff", "txt_color": "#000000"}, {"bg_color": "#000000", "txt_color": "#ffffff"}]
    color = random.choice(colors)
    ff = random.randint(1, 10) # random font-family [1-10]
    fz = H//12 # font-size
    font = ImageFont.truetype(f"font-lang/{lang}/{ff}.ttf", fz)
    w, h = font.getsize(text)

    words = text.split()
    max_len = max(list(map(len, words)))

    if w >= W/1.5:
        lines = textwrap.wrap(text, width=max_len)
        heigth = len(lines)
        y = (H-h*heigth)/2
        for line in lines:
            font = ImageFont.truetype(f"font-lang/{lang}/{ff}.ttf", fz)
            w, h = font.getsize(line)
            x = (W-w)/2
            draw.rectangle((x, y, x+w, y+h), fill=color["bg_color"])
            draw.text((x, y), text=line, fill=color["txt_color"], font=font)
            y += h
    else:
        draw.rectangle(((W-w)/2, (H-h)/2, (W-w)/2+w, (H-h)/2+h), fill=color["bg_color"])
        draw.text(xy=((W-w)/2, (H-h)/2-(fz/8)), text=text, fill=color["txt_color"], font=font)

    font = ImageFont.truetype(f"font-lang/English/citvy.ttf", fz//2)
    w, h = font.getsize("CITVY")
    draw.text(xy=(W-w-(w/4), H-h-(h/4)), text="CITVY", fill=(0, 0, 0), font=font)
    draw.text(xy=(W-w-(w/4), H-h-(h/4)), text="CITVY", fill=(255, 255, 255), font=font)
    
    img.save(out_file)