# settings.py
from PIL import Image

# Основні налаштування екрану
WIDTH, HEIGHT = 900, 600
CELL_SIZE = 45
FPS = 25

# Швидкість
PACMAN_SPEED = 1 / 5
GHOST_SPEED = 1 / 15

# Шляхи до зображень
PACMAN_ICON = 'assets/pacman.png'
GHOST1_ICON = 'assets/ghost1.png'
GHOST2_ICON = 'assets/ghost2.png'
GHOST3_ICON = 'assets/ghost3.png'
GHOST4_ICON = 'assets/ghost4.png'
FOOD_ICON = 'assets/food.png'


def resize_image(input_path, output_path, new_width):
    img = Image.open(input_path)
    width_percent = new_width / float(img.size[0])
    new_height = int((float(img.size[1]) * width_percent))
    resized_img = img.resize((new_width, new_height))
    resized_img.save(output_path)


resize_image(PACMAN_ICON, PACMAN_ICON, CELL_SIZE)
resize_image(GHOST1_ICON, GHOST1_ICON, CELL_SIZE)
resize_image(GHOST2_ICON, GHOST2_ICON, CELL_SIZE)
resize_image(GHOST3_ICON, GHOST3_ICON, CELL_SIZE)
resize_image(GHOST4_ICON, GHOST4_ICON, CELL_SIZE)
resize_image(FOOD_ICON, FOOD_ICON, CELL_SIZE)
