# img_cut_and_merge
## Description
**puzzler.py** : 이미지를 M x N으로 조각내어 mirror, flip, rotation(90도 또는 270도) 효과를 0.5의 확률로 변환한 뒤 셔플한다.   
**unpuzzler.py** : 섞인 이미지를 상하좌우면의 픽셀값을 비교하여 원본 이미지를 재현한다.

</br>

## Instruction 
### puzzling image
M, N 크기로 원본 이미지를 조각내서 mirror `&rarr` flip `&rarr` rotation 순서로 0.5의 확률로 변환 효과를 주고, 조각의 순서를 섞는다.
이미지는 {image_file_name}_puzzle.png의 이름으로 저장된다.

</br>


```
[usage]: python puzzler.py image_file_name M N
[example]: $ python puzzler.py lenna.png 3 3
```
</br>

![puzzled_image](/puzzle_python/lenna_puzzle.png)

</br>


### unpuzzling image
1. 조각의 변환은 8가지의 경우의 수가 나오는데, 각 조각에 8가지 경우의 상하좌우 픽셀값을 비교하고 threshold를 주어 가장 이웃한 조각을 선별한다.
2. 0번째 조각을 기준 조각으로 시작해서 앞서 구한 이웃한 조각 순서로 차례로 위의 과정을 한번 더 진행한다.   
 (예) 0번 조각의 이웃한 조각이 3과 5번이라면, 다음 비교 기준은 3번 조각, 5번 조각 순서로 비교를 진행
3. 기준 조각과 비교 조각 간의 변환 관계를 구한 다음 기준 조각을 중심으로 비교 조각을 변환시킨다.
4. 모든 조각의 이웃한 조각을 구하면 왼쪽 상단의 조각부터 정한 다음 그 조각을 기준으로 이웃한 조각을 따라가며 퍼즐 조각을 맞춘다.

</br>

```
[usage]: python unpuzzler.py file_name M N
[example]: $ python unpuzzler.py lenna_puzzle.png 3 3
```
</br>

![puzzled_image](/puzzle_python/lenna_puzzle_solve.png)

</br>

## Result & Discussions
현재 2 x 2, 3 x 3에 대해서만 테스트를 완료 한 상태이고, 이미지가 1:1 비율이 아닌 다른 이미지 비율에 대해서는 정확하게 동작하지 않는 상태이다.   
1:1 비율이 아닌 다른 비율의 이미지에 적용하기 위해서는 모든 조각의 가로 세로 픽셀을 동일하게 해야한다. 그렇게 하기 위해서는 rotation 효과가 적용된 조각들을 한방향으로 (예: 90도) 회전시켜 가로 세로 픽셀을 동일하게 맞춘 뒤 위의 과정을 진행하는 방법을 생각해 볼 수 있다.

