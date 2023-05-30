from PIL import Image
import random

# ori_img = Image.open('lenna.png') # 비율이 1:1
# ori_img = Image.open('sample_0.png') # 비율이 다른 경우
# n, m = map(int, input("n과 m을 입력하세요: ").split())

def cut_image(ori_img, n, m):
    width, height = ori_img.size
    quarter_width = width // n
    quarter_height = height // m

    # 1번째 영역
    cropped_img_1 = ori_img.crop((0, 0, quarter_width, quarter_height))
    cropped_img_1.save('random_1.png')

    # 2번째 영역
    cropped_img_2 = ori_img.crop((quarter_width, 0, width, quarter_height))
    cropped_img_2.save('random_2.png')

    # 3번째 영역
    cropped_img_3 = ori_img.crop((0, quarter_height, quarter_width, height))
    cropped_img_3.save('random_3.png')

    # 4번째 영역
    cropped_img_4 = ori_img.crop((quarter_width, quarter_height, width, height))
    cropped_img_4.save('random_4.png')

def mirroring(img_path):
    image = Image.open(img_path)
    img_mirror = image.transpose(Image.FLIP_LEFT_RIGHT)
    return img_mirror

def flip(image):
    # image = Image.open(img_path)
    img_flip = image.transpose(Image.FLIP_TOP_BOTTOM)

def rotation(image):
    # image = Image.open(img_path)
    angle = random.choice([90, -90])
    img_rotate = image.rotate(angle=angle)
    img_rotate.save('output_image')
    
def random_effect(image_path, output_path, prob=0.5):
    # mirroring
    image = Image.open(image_path)
    if random.random() < prob:
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
    
    if random.random() < prob:
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
    
    if random.random() < prob:
        angle = random.choice([90, -90])
        image = image.rotate(angle=angle)
    
    image.save(output_path)
    print("Done : Saved output image")
    
# cut_image(n, m)

image_path = "random_4.png"  # 입력 이미지 파일 경로
output_path = "output_4.png"
random_effect(image_path, output_path)    