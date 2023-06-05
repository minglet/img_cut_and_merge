import numpy as np
import cv2

# Piece class, holds data of each piece
class Piece:
    def __init__(self, num, s_vert, s_horz, chn, start, data, total):
        self.pieceNum = num
        self.size_vertical = s_vert
        self.size_horizontal = s_horz
        self.pieceChn = chn
        self.pieceStart = start
        self.pieceData = np.ndarray((s_vert, s_horz, chn), buffer=data, dtype=np.uint8)
        self.pieceTotal = total

        # the 4 borders of the piece
        self.sideUp = []
        self.sideRight = []
        self.sideDown = []
        self.sideLeft = []

        for i in range(self.size_horizontal):
            if (self.pieceData[0][i] == 0).all():
                self.sideUp.append(self.pieceData[1][i])    
            else:
                self.sideUp.append(self.pieceData[0][i])
            if (self.pieceData[-1][i] == 0).all():
                self.sideDown.append(self.pieceData[-2][i])
            else:
                self.sideDown.append(self.pieceData[-1][i])

        for i in range(self.size_vertical):
            if (self.pieceData[i][-1] == 0).all():
                self.sideRight.append(self.pieceData[i][-2])    
            else:
                self.sideRight.append(self.pieceData[i][-1])
            if (self.pieceData[i][0] == 0).all():
                self.sideLeft.append(self.pieceData[i][1])
            else:
                self.sideLeft.append(self.pieceData[i][0])

        self.sides = [self.sideUp, self.sideRight, self.sideDown, self.sideLeft]

        self.difference = [None for x in range(total)]

        self.neighbors = [None for x in range(4)]


# determine difference of pixel's each channel value
def pixel_difference(px1, px2):
    PIXEL_DIFFERENCE_THRESHOLD = 30
    diff = 0
    for i in range(len(px1)):
        diff += abs(int(px1[i] - int(px2[i])))
    return False if diff < PIXEL_DIFFERENCE_THRESHOLD else True


# calculate different pixels between two sides
def side_difference(side1, side2, reverse=False):
    difference = 0
    if reverse:
        side2_reverse = side2[::-1]  
        for i in range(len(side1)):
            difference += 1 if pixel_difference(side1[i], side2_reverse[i]) else 0
    else:
        for i in range(len(side1)):
            difference += 1 if pixel_difference(side1[i], side2[i]) else 0
    return difference

def piece_difference_test(piece1: Piece, piece2: Piece):
    # 8가지 경우의 수 나누기
    top_basic = side_difference(piece1.sideUp, piece2.sideDown)
    top_rot90 = side_difference(piece1.sideUp, piece2.sideLeft)
    top_rot270 = side_difference(piece1.sideUp, piece2.sideRight, reverse=True)
    top_flip = side_difference(piece1.sideUp, piece2.sideUp)
    top_mirror = side_difference(piece1.sideUp, piece2.sideDown, reverse=True)
    top_mir_flp = side_difference(piece1.sideUp, piece2.sideUp, reverse=True)
    top_mir_r90 = side_difference(piece1.sideUp, piece2.sideRight)
    top_mir_r270 = side_difference(piece1.sideUp, piece2.sideLeft, reverse=True)
    
    right_basic = side_difference(piece1.sideRight, piece2.sideLeft)
    right_rot90 = side_difference(piece1.sideRight, piece2.sideUp, reverse=True)
    right_rot270 = side_difference(piece1.sideRight, piece2.sideDown)
    right_flip = side_difference(piece1.sideRight, piece2.sideLeft, reverse=True)
    right_mirror = side_difference(piece1.sideRight, piece2.sideRight)
    right_mir_flp = side_difference(piece1.sideRight, piece2.sideRight, reverse=True)
    right_mir_r90 = side_difference(piece1.sideRight, piece2.sideUp)
    right_mir_r270 = side_difference(piece1.sideRight, piece2.sideDown, reverse=True)
    
    bottom_basic = side_difference(piece1.sideDown, piece2.sideUp)
    bottom_rot90 = side_difference(piece1.sideDown, piece2.sideRight)
    bottom_rot270 = side_difference(piece1.sideDown, piece2.sideLeft, reverse=True)
    bottom_flip = side_difference(piece1.sideDown, piece2.sideDown)
    bottom_mirror = side_difference(piece1.sideDown, piece2.sideUp, reverse=True)
    bottom_mir_flp = side_difference(piece1.sideDown, piece2.sideDown, reverse=True)
    bottom_mir_r90 = side_difference(piece1.sideDown, piece2.sideLeft)
    bottom_mir_r270 = side_difference(piece1.sideDown, piece2.sideRight, reverse=True)
    
    left_basic = side_difference(piece1.sideLeft, piece2.sideRight)
    left_rot90 = side_difference(piece1.sideLeft, piece2.sideDown, reverse=True)
    left_rot270 = side_difference(piece1.sideLeft, piece2.sideUp)
    left_flip = side_difference(piece1.sideLeft, piece2.sideRight, reverse=True)
    left_mirror = side_difference(piece1.sideLeft, piece2.sideLeft)
    left_mir_flp = side_difference(piece1.sideLeft, piece2.sideLeft, reverse=True)
    left_mir_r90 = side_difference(piece1.sideLeft, piece2.sideDown)
    left_mir_r270 = side_difference(piece1.sideLeft, piece2.sideUp, reverse=True)
    
    # clockwise direction
    temp1 = [[top_basic, top_rot90, top_rot270, top_flip, top_mirror, top_mir_flp, top_mir_r90, top_mir_r270], \
        [right_basic, right_rot90, right_rot270, right_flip, right_mirror, right_mir_flp, right_mir_r90, right_mir_r270], \
        [bottom_basic, bottom_rot90, bottom_rot270, bottom_flip, bottom_mirror, bottom_mir_flp, bottom_mir_r90, bottom_mir_r270],\
        [left_basic, left_rot90, left_rot270, left_flip, left_mirror, left_mir_flp, left_mir_r90, left_mir_r270]]
    
    temp2 = [[bottom_basic, bottom_rot90, bottom_rot270, bottom_flip, bottom_mirror, bottom_mir_flp, bottom_mir_r90, bottom_mir_r270], \
        [left_basic, left_rot90, left_rot270, left_flip, left_mirror, left_mir_flp, left_mir_r90, left_mir_r270], \
        [top_basic, top_rot90, top_rot270, top_flip, top_mirror, top_mir_flp, top_mir_r90, top_mir_r270], \
        [right_basic, right_rot90, right_rot270, right_flip, right_mirror, right_mir_flp, right_mir_r90, right_mir_r270]]
    
    for i in range(len(temp1)):
        temp1[i] = (min(temp1[i]), i, temp1[i].index(min(temp1[i]))) # (3, 0, 4)
        temp2[i] = (min(temp2[i]), i, -1)
    
    # non-decreasing sort of difference
    piece1.difference[piece2.pieceNum] = sorted(temp1)
    piece2.difference[piece1.pieceNum] = sorted(temp2)
    print(piece1.difference)
       
# calculate difference between two pieces in all directions
def piece_difference(piece1: Piece, piece2: Piece):
    # 8가지 경우의 수 나누기
    top_basic = side_difference(piece1.sideUp, piece2.sideDown)
    top_rot90 = side_difference(piece1.sideUp, piece2.sideLeft)
    top_rot270 = side_difference(piece1.sideUp, piece2.sideRight, reverse=True)
    top_flip = side_difference(piece1.sideUp, piece2.sideUp)
    top_mirror = side_difference(piece1.sideUp, piece2.sideDown, reverse=True)
    top_mir_flp = side_difference(piece1.sideUp, piece2.sideUp, reverse=True)
    top_mir_r90 = side_difference(piece1.sideUp, piece2.sideRight)
    top_mir_r270 = side_difference(piece1.sideUp, piece2.sideLeft, reverse=True)
    
    right_basic = side_difference(piece1.sideRight, piece2.sideLeft)
    right_rot90 = side_difference(piece1.sideRight, piece2.sideUp, reverse=True)
    right_rot270 = side_difference(piece1.sideRight, piece2.sideDown)
    right_flip = side_difference(piece1.sideRight, piece2.sideLeft, reverse=True)
    right_mirror = side_difference(piece1.sideRight, piece2.sideRight)
    right_mir_flp = side_difference(piece1.sideRight, piece2.sideRight, reverse=True)
    right_mir_r90 = side_difference(piece1.sideRight, piece2.sideUp)
    right_mir_r270 = side_difference(piece1.sideRight, piece2.sideDown, reverse=True)
    
    bottom_basic = side_difference(piece1.sideDown, piece2.sideUp)
    bottom_rot90 = side_difference(piece1.sideDown, piece2.sideRight)
    bottom_rot270 = side_difference(piece1.sideDown, piece2.sideLeft, reverse=True)
    bottom_flip = side_difference(piece1.sideDown, piece2.sideDown)
    bottom_mirror = side_difference(piece1.sideDown, piece2.sideUp, reverse=True)
    bottom_mir_flp = side_difference(piece1.sideDown, piece2.sideDown, reverse=True)
    bottom_mir_r90 = side_difference(piece1.sideDown, piece2.sideLeft)
    bottom_mir_r270 = side_difference(piece1.sideDown, piece2.sideRight, reverse=True)
    
    left_basic = side_difference(piece1.sideLeft, piece2.sideRight)
    left_rot90 = side_difference(piece1.sideLeft, piece2.sideDown, reverse=True)
    left_rot270 = side_difference(piece1.sideLeft, piece2.sideUp)
    left_flip = side_difference(piece1.sideLeft, piece2.sideRight, reverse=True)
    left_mirror = side_difference(piece1.sideLeft, piece2.sideLeft)
    left_mir_flp = side_difference(piece1.sideLeft, piece2.sideLeft, reverse=True)
    left_mir_r90 = side_difference(piece1.sideLeft, piece2.sideDown)
    left_mir_r270 = side_difference(piece1.sideLeft, piece2.sideUp, reverse=True)
    
    # clockwise direction
    temp1 = [[top_basic, top_rot90, top_rot270, top_flip, top_mirror, top_mir_flp, top_mir_r90, top_mir_r270], \
        [right_basic, right_rot90, right_rot270, right_flip, right_mirror, right_mir_flp, right_mir_r90, right_mir_r270], \
        [bottom_basic, bottom_rot90, bottom_rot270, bottom_flip, bottom_mirror, bottom_mir_flp, bottom_mir_r90, bottom_mir_r270],\
        [left_basic, left_rot90, left_rot270, left_flip, left_mirror, left_mir_flp, left_mir_r90, left_mir_r270]]
    
    temp2 = [[bottom_basic, bottom_rot90, bottom_rot270, bottom_flip, bottom_mirror, bottom_mir_flp, bottom_mir_r90, bottom_mir_r270], \
        [left_basic, left_rot90, left_rot270, left_flip, left_mirror, left_mir_flp, left_mir_r90, left_mir_r270], \
        [top_basic, top_rot90, top_rot270, top_flip, top_mirror, top_mir_flp, top_mir_r90, top_mir_r270], \
        [right_basic, right_rot90, right_rot270, right_flip, right_mirror, right_mir_flp, right_mir_r90, right_mir_r270]]
    
    for i in range(len(temp1)):
        temp1[i] = (min(temp1[i]), i, temp1[i].index(min(temp1[i]))) # (3, 0, 4)
        temp2[i] = (min(temp2[i]), i, -1)
    
    # non-decreasing sort of difference
    piece1.difference[piece2.pieceNum] = sorted(temp1)
    piece2.difference[piece1.pieceNum] = sorted(temp2)
    
    
def rotate(temp, angle, hor, ver):
    center = (hor // 2, ver // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    temp = cv2.warpAffine(temp, rotation_matrix, (hor, ver))
    return temp

def flip(temp):
    temp = np.flip(temp, axis=0)
    return temp

def mirror(temp):
    temp = np.flip(temp, axis=1)
    return temp

def effector(piece: Piece, num):
    temp = piece.pieceData
    if num == 0:
        temp = piece.pieceData
    elif num == 1:
        temp = rotate(temp, 90, piece.size_horizontal, piece.size_vertical)
    elif num == 2: 
        temp = rotate(temp, -90, piece.size_horizontal, piece.size_vertical)
    elif num == 3:
        temp = flip(temp)
    elif num == 4:
        temp = mirror(temp)
    elif num == 5:
        temp = mirror(temp)
        temp = flip(temp)
    elif num == 6:
        temp = mirror(temp)
        temp = rotate(temp, 90, piece.size_horizontal, piece.size_vertical)
    elif num == 7:
        temp = mirror(temp)
        temp = rotate(temp, -90, piece.size_horizontal, piece.size_vertical)
    temp_ = np.ascontiguousarray(temp)
    piece.pieceData = temp_


# search for neighbors
def update_piece(pList, piece: Piece):
    DIFFERENCE_RATE_THRESHOLD = 0.4
    candidates = [None for x in range(4)]
    # find the best candidate for each direction
    for i in range(len(piece.difference)):
        if piece.difference[i] is None:
            continue
        temp = piece.difference[i][0] # (60,0,2)
        if candidates[temp[1]] is None or candidates[temp[1]][1][0] > temp[0]:
            candidates[temp[1]] = (i, temp)

    for entry in candidates:
        if entry is not None and entry[1][0] <= DIFFERENCE_RATE_THRESHOLD *\
                (piece.size_vertical if (entry[1][1] == 1 or entry[1][1] == 3) else piece.size_horizontal):
                    if entry[1][2] != -1:
                        target_piece = pList[entry[0]]
                        effector(target_piece, entry[1][2])
                        # side update
                        target_piece.sideUp[i] = target_piece.pieceData[0][i]
                        for i in range(target_piece.size_horizontal):
                            if (target_piece.pieceData[0][i] == 0).all():
                                target_piece.sideUp[i] = target_piece.pieceData[1][i]    
                            else:
                                target_piece.sideUp[i] = target_piece.pieceData[0][i]
                            if (target_piece.pieceData[-1][i] == 0).all():
                                target_piece.sideDown[i] = target_piece.pieceData[-2][i]
                            else:
                                target_piece.sideDown[i] = target_piece.pieceData[-1][i]

                        for i in range(target_piece.size_vertical):
                            if (target_piece.pieceData[i][-1] == 0).all():
                                target_piece.sideRight[i] = target_piece.pieceData[i][-2]
                            else:
                                target_piece.sideRight[i] = target_piece.pieceData[i][-1]
                            if (target_piece.pieceData[i][0] == 0).all():
                                target_piece.sideLeft[i] = target_piece.pieceData[i][1]
                            else:
                                target_piece.sideLeft[i] = target_piece.pieceData[i][0]
                                
def find_neighbors(piece: Piece):
    piece.neighbors = [None for x in range(4)]
    DIFFERENCE_RATE_THRESHOLD = 0.4
    candidates = [None for x in range(4)]
    # find the best candidate for each direction
    for i in range(len(piece.difference)):
        if piece.difference[i] is None:
            continue
        temp = piece.difference[i][0] # (60,0,2)
        if candidates[temp[1]] is None or candidates[temp[1]][1][0] > temp[0]:
            candidates[temp[1]] = (i, temp)
    # test if candidate is eligible as neighbor
    for entry in candidates:
        if entry is not None and entry[1][0] <= DIFFERENCE_RATE_THRESHOLD *\
                (piece.size_vertical if (entry[1][1] == 1 or entry[1][1] == 3) else piece.size_horizontal):
            piece.neighbors[entry[1][1]] = entry[0]
    neighbor = piece.neighbors
    neighbor = [value for value in neighbor if value is not None]
    return neighbor
