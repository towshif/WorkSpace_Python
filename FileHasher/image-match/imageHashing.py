# 
# Created by towshif ali (tali) on 4/16/2018
#

# Code for the blogpost https://fullstackml.com/2016/07/02/wavelet-image-hash-in-python/

import PIL
from PIL import Image
import imagehash
from pprint import pprint

# hash1 = imagehash.whash(Image.open(r'H:\\temp\_2DieCornerLowMag.bmp.jpg'))
# hash1 = imagehash.whash(Image.open(r'H:\\temp\3DieCornerLowMag.jpg'))
# hash1 = imagehash.phash(Image.open(r'H:\\temp\1.jpg'))
hash1 = imagehash.whash(Image.open(r'H:\\temp\1.jpg'))
print(hash1)


# hash2 = imagehash.whash(Image.open(r'H:\\temp\_3DieCornerLowMag.jpg.jpg'))
# hash2 = imagehash.whash(Image.open(r'H:\\temp\2DieCornerLowMag.bmp'))
# hash2 = imagehash.phash(Image.open(r'H:\\temp\3.png'))
# hash2 = imagehash.phash(Image.open(r'H:\\temp\3.jpg'))
hash2 = imagehash.whash(Image.open(r'H:\\temp\3.png'))
print(hash2)

print (hash1 - hash2)
h = hash1 - hash2
print (100.0*h/(len(hash1.hash)**2.0))


