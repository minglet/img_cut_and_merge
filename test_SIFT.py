import cv2

img_1 = cv2.imread('output_1.png', 0)
img_2 = cv2.imread('output_2.png', 0)

sift = cv2.SIFT_create()

keypoints_1, descriptors_1 = sift.detectAndCompute(img_1, None)
keypoints_2, descriptors_2 = sift.detectAndCompute(img_2, None)

matcher = cv2.FlannBasedMatcher()

# 특징점 매칭 수행
matches = matcher.match(descriptors_1, descriptors_2)

# 매칭 결과를 거리 기준으로 정렬
matches = sorted(matches, key=lambda x: x.distance)

# 상위 N개 매칭 결과 선택 (여기서는 10개 선택)
top_matches = matches[:10]

# 매칭 결과 시각화
match_image = cv2.drawMatches(img_1, keypoints_1, img_2, keypoints_2, top_matches, None)

# 결과 이미지 출력
cv2.imshow('Matches', match_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

