import cv2
import numpy as np
import os
import sys
from pathlib import Path
from checkInput import check_input
import readImage as readImg
from makePieces import get_pieces
import drawPieces as drawP
import Piece


if __name__ == "__main__":
    # initialization and read image
    check_input("unpuzzler.py")
    filename = sys.argv[1]
    fileTest = Path(filename)
    if not fileTest.is_file():
        print("Image file NOT found.")
        sys.exit(1)
    img, imgRow, imgCol, imgChn = readImg.read_image(filename, cv2.IMREAD_COLOR)

    # get pieces from image
    pList, pSize_vertical, pSize_horizontal, pCnt_row, pCnt_column, pCnt_total = get_pieces(img, imgRow, imgCol, imgChn, puzzle=False)

    for i in range(pCnt_total):
        for j in range(i + 1, pCnt_total):
            if i == j:
                continue
            Piece.piece_difference(pList[i], pList[j])
        # print("pList[i].difference")
        # print(pList[i].difference)
        Piece.update_piece(pList, pList[i])
    # print("=========1=============")

    next_list = [0]
    left_list = []
    while True:
        if len(next_list) == 0:
            break
        else:
            i = next_list[0]
            if i in left_list:
                next_list.pop(0)
            else:
                next_list.extend(Piece.find_neighbors(pList[i]))
                next_list.pop(0)
                left_list.append(i)
    
    unique_list = []
    for item in left_list:
        if item not in unique_list:
            unique_list.append(item)
    for i in range(pCnt_total):
        for j in range(i + 1, pCnt_total):
            if i == j:
                continue
            Piece.piece_difference(pList[unique_list[i]], pList[unique_list[j]])
        Piece.update_piece(pList, pList[unique_list[i]])
    
    # determine starting pixel to fill in image
    startPiece = []
    none_cnt = 0
    for piece in pList:
        Piece.find_neighbors(piece)
        print(piece.neighbors)
        if piece.neighbors[0] is None and piece.neighbors[3] is None:
            if none_cnt < piece.neighbors.count(None):
                startPiece.append(piece)
                none_cnt = piece.neighbors.count(None)
            else:
                startPiece.insert(0, piece)
    if len(startPiece) == 0:
        print("Could not find starting piece... but here is an attempt.")
        startPiece.append(pList[0])
    # print(startPiece)
    # fill in image using neighbor information
    black = np.zeros((pSize_vertical, pSize_horizontal, imgChn), dtype=np.uint8)
    blackPiece = Piece.Piece(-1, pSize_vertical, pSize_horizontal, imgChn, (0, 0), black, pCnt_total)
    temp = [blackPiece for x in range(pCnt_total)]
    temp[0] = startPiece[0]
    
    next_i = [0]
    trash = []
    while True:
        i = next_i[0]
        # print("next_i")
        # print(next_i)
        # print("trash")
        # print(trash)
        if i in trash:
            next_i.pop(0)
            if len(next_i) == 0:
                break
            else:
                continue
        else:
            if temp[i].neighbors[0] is not None:
                temp[i - pCnt_row] = pList[temp[i].neighbors[0]]
                next_i.append(i - pCnt_row)
            if temp[i].neighbors[1] is not None:
                temp[i + 1] = pList[temp[i].neighbors[1]]
                next_i.append(i + 1)
            if temp[i].neighbors[2] is not None:
                temp[i + pCnt_row] = pList[temp[i].neighbors[2]]
                next_i.append(i + pCnt_row)
            if temp[i].neighbors[3] is not None:
                temp[i - 1] = pList[temp[i].neighbors[3]]
                next_i.append(i - 1)
            next_i.pop(0)
            trash.append(i)
    # for i in range(pCnt_total):
    #         if i % pCnt_row < pCnt_row - 1 and temp[i].neighbors[1] is not None:
    #             temp[i + 1] = pList[temp[i].neighbors[1]]
    #         if i / pCnt_row < pCnt_column - 1 and temp[i].neighbors[2] is not None:
    #             temp[i + pCnt_row] = pList[temp[i].neighbors[2]]
    # show and save result image
    filename = os.path.splitext(filename)[0] + "_solve.png"
    temp = drawP.combine_pieces(pSize_vertical, pSize_horizontal, pCnt_row, pCnt_column, pCnt_total, imgChn, temp)
    drawP.draw_image(temp, filename + " - Solved Image")
    cv2.imwrite(filename, temp)