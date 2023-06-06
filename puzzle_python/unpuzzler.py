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
        Piece.update_piece(pList, pList[i])

    next_list = [0]
    unique_list = []
    while True:
        if len(next_list) == 0:
            break
        else:
            i = next_list[0]
            if i in unique_list:
                next_list.pop(0)
            else:
                next_list.extend(Piece.find_neighbors(pList[i]))
                next_list.pop(0)
                unique_list.append(i)
    
    if len(unique_list) != pCnt_total:
        temp_list = [x for x in range(pCnt_total)]
        for tmp in temp_list:
            found = False
            for num in unique_list:
                if num == tmp:
                    found = True
                    break
            if not found:
                unique_list.append(tmp)
    
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
    # fill in image using neighbor information
    black = np.zeros((pSize_vertical, pSize_horizontal, imgChn), dtype=np.uint8)
    blackPiece = Piece.Piece(-1, pSize_vertical, pSize_horizontal, imgChn, (0, 0), black, pCnt_total)
    temp = [blackPiece for x in range(pCnt_total)]
    temp = Piece.puzzle_of_number(temp, startPiece, pCnt_row, pList)
            
    # show and save result image
    filename = os.path.splitext(filename)[0] + "_solve.png"
    temp = drawP.combine_pieces(pSize_vertical, pSize_horizontal, pCnt_row, pCnt_column, pCnt_total, imgChn, temp)
    drawP.draw_image(temp, filename + " - Solved Image")
    cv2.imwrite(filename, temp)