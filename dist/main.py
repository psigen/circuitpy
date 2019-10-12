import adafruit_imageload
import analogio
import board
import digitalio
import displayio
import time
from gamepadshift import GamePadShift

display = board.DISPLAY

# Load the sprite sheet (bitmap)
sprite_sheet, palette = adafruit_imageload.load("/tiny_dungeon_world.bmp",
                                                bitmap=displayio.Bitmap,
                                                palette=displayio.Palette)

# Create the sprite TileGrid
sprite = displayio.TileGrid(sprite_sheet,
                            pixel_shader=palette,
                            width=1,
                            height=1,
                            tile_width=16,
                            tile_height=16,
                            default_tile=0)

# Create the castle TileGrid
castle = displayio.TileGrid(sprite_sheet,
                            pixel_shader=palette,
                            width=16,
                            height=19,
                            tile_width=16,
                            tile_height=16)

# Create a Group to hold the sprite and add it
sprite_group = displayio.Group()
sprite_group.append(sprite)

# Create a Group to hold the castle and add it
castle_group = displayio.Group(scale=3)
castle_group.append(castle)

# Create a Group to hold the sprite and castle
group = displayio.Group()

# Add the sprite and castle to the group
group.append(castle_group)
group.append(sprite_group)

# Castle tile assignments
# corners
castle[0, 0] = 3  # upper left
castle[5, 0] = 5  # upper right
castle[0, 4] = 9  # lower left
castle[5, 4] = 11  # lower right
# top / bottom walls
for x in range(1, 5):
    castle[x, 0] = 4  # top
    castle[x, 4] = 10  # bottom
# left/ right walls
for y in range(1, 4):
    castle[0, y] = 6  # left
    castle[5, y] = 8  # right
# floor
for x in range(1, 5):
    for y in range(1, 4):
        castle[x, y] = 7  # floor

# put the sprite somewhere in the castle
sprite.x = 110
sprite.y = 70

# Initialize controller input
joystick_x = analogio.AnalogIn(board.JOYSTICK_X)
joystick_y = analogio.AnalogIn(board.JOYSTICK_Y)

pad = GamePadShift(digitalio.DigitalInOut(board.BUTTON_CLOCK),
                   digitalio.DigitalInOut(board.BUTTON_OUT),
                   digitalio.DigitalInOut(board.BUTTON_LATCH))

# Add the Group to the Display
while not pad.get_pressed():
    sprite.x += int((joystick_x.value - 32767) / 5000)
    sprite.y += int((joystick_y.value - 32767) / 5000)
    display.show(group)
    time.sleep(0.1)
