# 
# Created by towshif ali (tali) on 4/19/2018
#

import os
from PIL import Image

imagetest = Image.open(r"H:\temp\images\28226\Copy_ch0_die0.mim")

list(imagetest.getdata())

print(list)