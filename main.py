# Create a more exaggerated "puppet mouth" animation from the provided GIF image.
# We'll take the first frame, separate an approximate jaw region, and animate it
# opening with a dark mouth interior to create a creepy puppet-like effect.

from PIL import Image, ImageDraw
import numpy as np

src_path = "./epstein.png"
try:
    base = Image.open(src_path).convert("RGBA")
except:
    # fallback if only the gif exists
    gif_path = "/mnt/data/epstein_puppet_laugh.gif"
    base = Image.open(gif_path).convert("RGBA")

w, h = base.size

# approximate mouth center
cx = int(w * 0.53)
cy = int(h * 0.60)

# jaw mask area
jaw_top = int(h * 0.58)
jaw_img = base.crop((0, jaw_top, w, h))

frames = []
open_amounts = [0,6,12,18,24,18,12,6,0]

for amt in open_amounts:
    frame = base.copy()
    canvas = Image.new("RGBA", (w, h), (0,0,0,0))
    canvas.paste(frame, (0,0))
    
    # draw mouth interior (black ellipse)
    mouth = ImageDraw.Draw(canvas)
    mouth_w = int(w*0.18)
    mouth_h = int(amt*1.6)
    if mouth_h > 0:
        mouth.ellipse(
            (cx-mouth_w//2, cy, cx+mouth_w//2, cy+mouth_h),
            fill=(10,10,10,255)
        )
    
    # move jaw downward
    canvas.paste(jaw_img, (0, jaw_top + amt), jaw_img)
    
    frames.append(canvas)

out_path = "./epstein.gif"
frames[0].save(
    out_path,
    save_all=True,
    append_images=frames[1:],
    duration=80,
    loop=0,
    disposal=2
)

out_path