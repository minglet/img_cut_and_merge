import cv2
import numpy as np

img = cv2.imread('output_merge.png', 0)
# img = cv2.imread('lenna.png', 0)

w, h = img.shape
half_w, half_h = w//2, h//2

blurred = cv2.GaussianBlur(img, (5, 5), 0)

# Canny 에지 검출을 통한 경계선 검출
edges = cv2.Canny(blurred, 50, 150, apertureSize=3)

# Hough 변환을 이용한 직선 검출
lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=90)

# 검출된 직선들을 원본 이미지에 그리기
if lines is not None:
    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        if (half_h - 5 < y1 < half_h + 5) | (half_w - 5 < y2 < half_w + 5) | (half_h - 5 < y2 < half_h + 5) | (half_w - 5 < y1 < half_w + 5):
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 255), 2) # 어차피 흑백이라 색 안바뀜
        # cv2.line(img, (x1, y1), (x2, y2), (0, 255, 255), 2) # 어차피 흑백이라 색 안바뀜s
        print(x1, y1, x2, y2)


# 결과 이미지 출력
cv2.imshow('Hough Lines', img)
cv2.waitKey(0)
cv2.destroyAllWindows()