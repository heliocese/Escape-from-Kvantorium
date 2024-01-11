class Timer:
    def __init__(self, x, y, font):
        self.time = 0
        self.seconds = '0' + str(self.time % 60) if self.time % 60 < 10 else str(self.time % 60)
        self.minutes = '0' + str(self.time // 60) if self.time // 60 < 10 else str(self.time // 60)
        self.pause = False
        self.font = font
        self.count = 0
        self.x, self.y = x, y
        self.text = self.font.render(f'Время {self.minutes}:{self.seconds}', True, (9, 9, 9))
        self.rect = self.text.get_rect(center=(x, y))

    def pauses(self):
        self.pause = True

    def draw(self, screen):
        screen.blit(self.text, self.rect)

    def update(self):
        if not self.pause:
            self.time += 1
            self.seconds = '0' + str(self.time % 60) if self.time % 60 < 10 else str(self.time % 60)
            self.minutes = '0' + str(self.time // 60) if self.time // 60 < 10 else str(self.time // 60)
            self.text = self.font.render(f'Время {self.minutes}:{self.seconds}', True, (9, 9, 9))

    def get_time(self):  # возвращает время в секундах
        return self.time
