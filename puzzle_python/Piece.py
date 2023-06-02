import numpy as np
import pdb

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
            self.sideUp.append(self.pieceData[0][i])
            self.sideDown.append(self.pieceData[-1][i])

        for i in range(self.size_vertical):
            self.sideRight.append(self.pieceData[i][-1])
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
def side_difference(side1, side2, mirror=False):
    difference = 0
    side2_mirror = side2[::-1]
    if mirror:
        for i in range(len(side1)):
            difference += 1 if pixel_difference(side1[i], side2_mirror[i]) else 0
    else:
        for i in range(len(side1)):
            difference += 1 if pixel_difference(side1[i], side2[i]) else 0
    return difference


# calculate difference between two pieces in all directions
def piece_difference(piece1: Piece, piece2: Piece):
    top_basic = side_difference(piece1.sideUp, piece2.sideDown)
    top_rot90 = side_difference(piece1.sideUp, piece2.sideRight)
    top_rot270 = side_difference(piece1.sideUp, piece2.sideLeft)
    top_flip = side_difference(piece1.sideUp, piece2.sideUp)
    top_mirror = side_difference(piece1.sideUp, piece2.sideDown, mirror=True)
    right_basic = side_difference(piece1.sideRight, piece2.sideLeft)
    right_rot90 = side_difference(piece1.sideRight, piece2.sideDown)
    right_rot270 = side_difference(piece1.sideRight, piece2.sideUp)
    right_flip = side_difference(piece1.sideRight, piece2.sideRight)
    right_mirror = side_difference(piece1.sideRight, piece2.sideLeft, mirror=True)
    bottom_basic = side_difference(piece1.sideDown, piece2.sideUp)
    bottom_rot90 = side_difference(piece1.sideDown, piece2.sideLeft)
    bottom_rot270 = side_difference(piece1.sideDown, piece2.sideRight)
    bottom_flip = side_difference(piece1.sideDown, piece2.sideDown)
    bottom_mirror = side_difference(piece1.sideDown, piece2.sideUp, mirror=True)
    left_basic = side_difference(piece1.sideLeft, piece2.sideRight)
    left_rot90 = side_difference(piece1.sideLeft, piece2.sideUp)
    left_rot270 = side_difference(piece1.sideLeft, piece2.sideDown)
    left_flip = side_difference(piece1.sideLeft, piece2.sideLeft)
    left_mirror = side_difference(piece1.sideLeft, piece2.sideRight, mirror=True)
    
    # clockwise direction
    temp1 = [[top_basic, top_rot90, top_rot270, top_flip, top_mirror], [right_basic, right_rot90, right_rot270, right_flip, right_mirror], \
        [bottom_basic, bottom_rot90, bottom_rot270, bottom_flip, bottom_mirror], [left_basic, left_rot90, left_rot270, left_flip, left_mirror]]
    temp2 = [[bottom_basic, bottom_rot90, bottom_rot270, bottom_flip, bottom_mirror], [left_basic, left_rot90, left_rot270, left_flip, left_mirror], \
        [top_basic, top_rot90, top_rot270, top_flip, top_mirror], [right_basic, right_rot90, right_rot270, right_flip, right_mirror]]
    
    for i in range(len(temp1)):
        temp1[i] = (min(temp1[i]), i, temp1[i].index(min(temp1[i])))
        temp2[i] = (min(temp2[i]), i, temp2[i].index(min(temp2[i])))
        
    # non-decreasing sort of difference
    piece1.difference[piece2.pieceNum] = sorted(temp1)
    piece2.difference[piece1.pieceNum] = sorted(temp2)

# search for neighbors
def find_neighbors(piece: Piece):
    DIFFERENCE_RATE_THRESHOLD = 0.6
    candidates = [None for x in range(4)]
    # find the best candidate for each direction
    for i in range(len(piece.difference)):
        if piece.difference[i] is None:
            continue
        temp = piece.difference[i][0]
        if candidates[temp[1]] is None or candidates[temp[1]][1][0] > temp[0]:
            candidates[temp[1]] = (i, temp)

    # test if candidate is eligible as neighbor
    for entry in candidates:
        if entry is not None and entry[1][0] <= DIFFERENCE_RATE_THRESHOLD *\
                (piece.size_vertical if (entry[1][1] == 1 or entry[1][1] == 3) else piece.size_horizontal):
            piece.neighbors[entry[1][1]] = entry[0]