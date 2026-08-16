import sys, numpy as np
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert('RGBA')
arr = np.array(im).astype(int)
h, w = arr.shape[:2]
for n,(x,y) in {'TL':(2,2),'TR':(w-3,2),'BL':(2,h-3),'BR':(w-3,h-3)}.items():
    print(n, tuple(arr[y, x]))
R, G, B = arr[..., 0], arr[..., 1], arr[..., 2]
mask = (G > R + 25) & (G > B + 25)              # green-dominant = background
arr[..., 3] = np.where(mask, 0, 255)
# de-spill: on kept pixels, clamp green down to max(R,B) to kill the green halo
keep = ~mask
gspill = keep & (G > np.maximum(R, B))
arr[..., 1] = np.where(gspill, np.maximum(R, B), G)
Image.fromarray(arr.astype('uint8'), 'RGBA').save(out)
print(f'keyed {int(mask.sum())} px ({100*mask.sum()/(w*h):.1f}%) transparent; despilled {int(gspill.sum())} px')
print('chest alpha (should be 255):', int(arr[int(h*0.42), w//2, 3]))
