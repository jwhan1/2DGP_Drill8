# 왼/오른쪽 방향키,대쉬,타이머
#잠,대기,달리기,빨리 달리기
# Game object class here

from pico2d import load_image


class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(400, 30)

    def update(self):
        pass


