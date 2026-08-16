import sys, numpy as np
from PIL import Image, ImageDraw
src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert('RGB')
w, h = im.size
MARK = (255, 0, 255)
# seed the flood from the whole border so any edge-connected light background is caught
seeds = []
for x in range(0, w, 12): seeds += [(x, 0), (x, h-1)]
for y in range(0, h, 12): seeds += [(0, y), (w-1, y)]
for s in seeds:
    r, g, b = im.getpixel(s)
    if min(r, g, b) > 170:                    # only start on light (checker) pixels
        ImageDraw.floodfill(im, s, MARK, thresh=150)  # generous: fills all light bg, stops only at the dark outline
arr = np.array(im)
mask = np.all(arr == MARK, axis=-1)
alpha = np.where(mask, 0, 255).astype(np.uint8)
rgba = np.dstack([arr, alpha])
Image.fromarray(rgba, 'RGBA').save(out)
# report
z = int(mask.sum()); print(f'{w}x{h}: made {z} px ({100*z/(w*h):.1f}%) transparent')
# sanity: is a chest-area pixel (uniform) still opaque?
cx, cy = w//2, int(h*0.42)
print('uniform sample alpha at center-chest:', int(alpha[cy, cx]))
