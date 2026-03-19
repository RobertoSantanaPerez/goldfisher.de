###############################################################################
#
# Captcha.py
# ==========
#
# (c) by Santana
#
###############################################################################
import random, string, io, hashlib
from PIL import Image, ImageDraw, ImageFont
from flask import g

class Cache():

    def __init__( self, param ):
    pass
    # end __init__

    def set( self )
        text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)    
        image = Image.new("RGB", (220, 44), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        draw.text((36, 6), text, font=font, fill=(89, 92, 95))
        img_io = io.BytesIO()
        image.save(img_io, "PNG")
        img_io.seek(0)
        return( send_file(img_io, mimetype="image/png") )
    # end set

# end class Captcha

if __name__ == "__main__":
  pass

### end-of-file         