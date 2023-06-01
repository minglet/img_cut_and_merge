import numpy as np
import math
import sys
from Piece import Piece
import cv2
import random

def random_effector(size_horizontal, size_vertical, temp, prob=0.5):
    # mirror effect
    if random.random() < prob:
        temp = np.flip(temp, axis=0)
        
    # flip effect
    if random.random() < prob:
        temp = np.flip(temp, axis=1)
    
    # rotate effect
    if random.random() < prob:
        rotation_angle = random.choice([90, -90])
        center = (size_horizontal // 2, size_vertical // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, rotation_angle, 1.0)
        temp = cv2.warpAffine(temp, rotation_matrix, (size_horizontal, size_vertical))
    temp = np.ascontiguousarray(temp)

    return temp


def get_pieces(img, img_row, img_col, img_chn, puzzle=True):
    # piece information
    cnt_column = int(sys.argv[2])   # cnt_column = int(input("Pieces in a column: "))
    cnt_row = int(sys.argv[3])      # cnt_row = int(input("Pieces in a row: "))
    cnt_total = cnt_row * cnt_column
    size_horizontal = math.ceil(img_col / cnt_row)
    size_vertical = math.ceil(img_row / cnt_column)
    p_list = []

    # creation of pieces
    for pIt in range(cnt_total):
        temp = np.zeros((size_vertical, size_horizontal, img_chn), dtype=np.uint8)
        start_row = size_vertical * math.floor(pIt / cnt_row)
        start_col = size_horizontal * (pIt % cnt_row)
        for i in range(start_row, start_row + size_vertical):
            if i >= img_row:
                break
            for j in range(start_col, start_col + size_horizontal):
                if j >= img_col:
                    continue
                temp[i - start_row][j - start_col] = img[i][j]
        if puzzle:
            temp = random_effector(size_horizontal, size_vertical, temp)
        p_list.append(Piece(pIt, size_vertical, size_horizontal, img_chn, (start_row, start_col), temp, cnt_total))
    return p_list, size_vertical, size_horizontal, cnt_row, cnt_column, cnt_total