# 
# Created by towshif ali (tali) on 4/16/2018
#

from image_match.goldberg import ImageSignature
gis = ImageSignature()
# a = gis.generate_signature('https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Mona_Lisa,_by_Leonardo_da_Vinci,_from_C2RMF_retouched.jpg/687px-Mona_Lisa,_by_Leonardo_da_Vinci,_from_C2RMF_retouched.jpg')
# b = gis.generate_signature('https://pixabay.com/static/uploads/photo/2012/11/28/08/56/mona-lisa-67506_960_720.jpg')
# print gis.normalized_distance(a, b)
#
# c = gis.generate_signature('https://upload.wikimedia.org/wikipedia/commons/e/e0/Caravaggio_-_Cena_in_Emmaus.jpg')
# print gis.normalized_distance(a, c)
#
# d = gis.generate_signature('https://c2.staticflickr.com/8/7158/6814444991_08d82de57e_z.jpg')
# print gis.normalized_distance(a, d)


from PIL import Image, ExifTags
import os
import traceback

def processImageThumb(path, fileName):
    try :
        image=Image.open(os.path.join(path, fileName))
        # for orientation in ExifTags.TAGS.keys() :
        #     if ExifTags.TAGS[orientation]=='Orientation' : break
        # exif=dict(image._getexif().items())
        #
        # if   exif[orientation] == 3 :
        #     image=image.rotate(180, expand=True)
        # elif exif[orientation] == 6 :
        #     image=image.rotate(270, expand=True)
        # elif exif[orientation] == 8 :
        #     image=image.rotate(90, expand=True)

        THUMB_WIDTH = 300
        THUMB_HIGHT = 300

        img = image.thumbnail((THUMB_WIDTH , THUMB_HIGHT), Image.ANTIALIAS)
        img = image.convert('RGB')
        img.save(os.path.join(path,"_"+fileName+".jpg"), "JPEG")

    except:
        traceback.print_exc()


from PIL import Image

processImageThumb(r'H:\\temp', '2DieCornerLowMag.bmp')
processImageThumb(r'H:\\temp', '3DieCornerLowMag.jpg')

a = gis.generate_signature(r'H:\\temp\3.jpg')
b = gis.generate_signature(r'H:\\temp\3.png')

# a = gis.generate_signature(r'H:\\temp\1.jpg')
# b = gis.generate_signature(r'H:\\temp\2.jpg')
# a = gis.generate_signature(r'H:\\temp\_2DieCornerLowMag.bmp.jpg')
# b = gis.generate_signature(r'H:\\temp\_3DieCornerLowMag.jpg.jpg')

# a = gis.generate_signature(img1)
# b = gis.generate_signature(img2)

print gis.normalized_distance(a, b)






