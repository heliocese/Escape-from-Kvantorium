class Hero:

    def __init__(self, pos):
        self.x, self.y = pos

    def get_position(self):
        return self.x, self.y

    def set_position(self, pos):  # изменение координат
        self.x, self.y = pos

    # def render(self, screen):  # отрисовка персонажа

