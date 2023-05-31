from PIL import Image
import random

ori_img = Image.open('lenna.png')
img_1 = Image.open('output_1.png')
img_2 = Image.open('output_2.png')
img_3 = Image.open('output_3.png')
img_4 = Image.open('output_4.png')

image_list = [img_1, img_2, img_3, img_4]
nums = [0,1,2,3]
rand_num= random.sample(nums, k=4)

temp_list = []
for i in rand_num:
    temp_list.append(image_list[i])

w, h = ori_img.size
output = Image.new("RGB", (w, h))
width, height = img_1.size
coord = [(0,0), (0, height), (width, 0), (width, height)]
for im, xy in zip(temp_list, coord):
    output.paste(im, xy)

output.save('output_merge.png')