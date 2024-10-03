import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter, QColor, QFont


class SnakeGame(QWidget):
    grid_size = None
    speed = None
    snake = None
    direction = None
    food = None
    score = None
    game_over = None
    timer = None

    def __init__(self):
        super().__init__()
        self.init_game()

    def init_game(self):
        self.grid_size = 20
        self.speed = 100
        self.snake = [(5, 5), (5, 4), (5, 3)]  # Starting snake positions
        self.direction = Qt.Key_Right  # Start direction to the right
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False

        # Set up the timer for moving the snake
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.move_snake)
        self.timer.start(self.speed)

        # Window size and settings
        self.setFixedSize(400, 400)
        self.setWindowTitle('Snake Game')

        # Set focus to capture key events
        self.setFocusPolicy(Qt.StrongFocus)

        self.show()

    def generate_food(self):
        # Generate random food position that is not on the snake
        while True:
            food = (random.randint(0, 19), random.randint(0, 19))
            if food not in self.snake:
                return food

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw_game(qp)
        qp.end()

    def draw_game(self, qp):
        # Set color and draw the snake
        qp.setBrush(QColor(0, 255, 0))
        for segment in self.snake:
            qp.drawRect(segment[0] * self.grid_size, segment[1] * self.grid_size, self.grid_size, self.grid_size)

        # Draw the food
        qp.setBrush(QColor(255, 0, 0))
        qp.drawEllipse(self.food[0] * self.grid_size, self.food[1] * self.grid_size, self.grid_size, self.grid_size)

        # Draw score
        qp.setPen(QColor(255, 255, 255))
        qp.setFont(QFont('Arial', 14))
        qp.drawText(10, 30, f'Score: {self.score}')

        # Game over text
        if self.game_over:
            qp.setPen(QColor(255, 0, 0))
            qp.setFont(QFont('Arial', 24))
            qp.drawText(self.rect(), Qt.AlignCenter, 'Game Over')

    def keyPressEvent(self, event):
        if not self.game_over:
            key = event.key()

            # Control snake movement and prevent it from moving in the opposite direction
            if key == Qt.Key_Up and self.direction != Qt.Key_Down:
                self.direction = Qt.Key_Up
            elif key == Qt.Key_Down and self.direction != Qt.Key_Up:
                self.direction = Qt.Key_Down
            elif key == Qt.Key_Left and self.direction != Qt.Key_Right:
                self.direction = Qt.Key_Left
            elif key == Qt.Key_Right and self.direction != Qt.Key_Left:
                self.direction = Qt.Key_Right

    def move_snake(self):
        if self.game_over:
            return

        head_x, head_y = self.snake[0]

        if self.direction == Qt.Key_Up:
            head_y -= 1
        elif self.direction == Qt.Key_Down:
            head_y += 1
        elif self.direction == Qt.Key_Left:
            head_x -= 1
        elif self.direction == Qt.Key_Right:
            head_x += 1

        # Check if the snake runs into walls or itself
        if head_x < 0 or head_x >= 20 or head_y < 0 or head_y >= 20 or (head_x, head_y) in self.snake:
            self.game_over = True
            self.timer.stop()
            self.update()
            return

        # Insert the new head
        new_head = (head_x, head_y)
        self.snake = [new_head] + self.snake

        # Check if the snake eats the food
        if new_head == self.food:
            self.score += 1
            self.food = self.generate_food()
        else:
            self.snake.pop()  # Remove the tail

        self.update()


class SnakeGameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.game = SnakeGame()
        self.setCentralWidget(self.game)
        self.setWindowTitle("Futuristic Snake Game")
        self.setGeometry(300, 300, 400, 400)
        self.show()


def main():
    app = QApplication(sys.argv)
    window = SnakeGameWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()