"""
Flappy Bird Clone

"""
import random

import arcade
import random
import pyglet
from pyglet.math import Vec2

"""
Redo using scene object


"""
# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 750
SCREEN_TITLE = "Flapping Birdy"

# Sprite Scaling
CHARACTER_SCALING = 1
PIPE_SCALING = 0.5
TILE_SCALING = 0.5

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 10
GRAVITY = 0.3
PLAYER_JUMP_SPEED = 10

# Player starting position
PLAYER_START_X = 200
PLAYER_START_Y = SCREEN_HEIGHT / 2

# How fast the camera pans to the player. 1.0 is instant
CAMERA_SPEED = 0.1

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN = 200

# misc
NUM_OBJECTS = 100

# LAYER_NAME_PIPES = "Pipes"
# LAYER_NAME_PLAYER = "Player"


class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        # Call the parent class's init function
        super().__init__(width, height, title)

        # our scene object
        self.scene = None

        # Store background
        self.background = None

        # Hold player sprite
        self.player_sprite = None

        # Our 'physics' engine
        self.physics_engine = None

        self.pipes_physics_engine = None

        # Create camera for scrolling screen
        self.camera = None

        # Load sounds
        self.jump_sound = arcade.load_sound("audio/audio_wing.wav")
        self.hit_pipe_sound = arcade.load_sound("audio/audio_hit.wav")

        # self.camera_sprites = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        # self.camera_gui = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        # A camera used to draw GUI elements
        self.gui_camera = None

        # Hold player score
        self.score = None


    def setup(self):
        # Initialize scene
        self.scene = arcade.Scene()

        # Create the Sprite Lists
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Pipes", use_spatial_hash=True)

        # Load background sprite/image
        # self.background = arcade.load_texture("images/background/background-day.png")
        self.background = arcade.set_background_color(arcade.csscolor.SKY_BLUE)

        # Set up the player, lay at coordinates
        self.player_sprite = arcade.Sprite("images/bird/yellowbird-upflap.png", CHARACTER_SCALING)
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.scene.add_sprite("Player", self.player_sprite)
        self.score = 0

        # This shows using a coordinate list to place sprites
        # coordinate_list = [[512, 0], [256, 0], [768, 0]]

        for x in range(0, 100000):
            ground = arcade.Sprite("images/base.png", TILE_SCALING)
            ground.center_x = x
            ground.center_y = 30
            self.scene.add_sprite("Ground", ground)

        for x in range(0, 1000000, 256):
            pipe = arcade.Sprite(
                "images/assets/pipe-green.png", PIPE_SCALING
            )
            pipe.center_x = x
            pipe.center_y = 50
            self.scene.add_sprite("Pipes", pipe)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["Ground"]
        )

        self.pipes_physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["Pipes"]
        )

        # Set up the Camera
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)

    def on_draw(self):
        # Clear the screen
        self.clear()

        # call before drawing window
        arcade.start_render()

        # Draw the background texture
        # arcade.draw_lrwh_rectangle_textured(0, 0,
        #                                     SCREEN_WIDTH, SCREEN_HEIGHT,
        #                                     self.background)
        # Draw player (bird) sprite
        self.scene.draw()

        # Activate GUI camera before drawing GUI elements
        self.gui_camera.use()

        # Render score/text
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 250, 700, arcade.color.WHITE, 20)

        # Activate our Camera
        self.camera.use()

        # # Select camera to draw sprites
        # self.camera_sprites.use()
        #
        # # Selected the unscrolled camera for our GUI
        # self.camera_gui.use()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W:
            arcade.play_sound(self.jump_sound)
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    # def scroll_to_player(self):
    #     """
    #     Scroll the window to the player.
    #     This method will attempt to keep the player at least VIEWPORT_MARGIN
    #     pixels away from the edge.
    #
    #     if CAMERA_SPEED is 1, the camera will immediately move to the desired position.
    #     Anything between 0 and 1 will have the camera move to the location with a smoother
    #     pan.
    #     """
    #
    #     position = Vec2(self.player_sprite.center_x - self.width / 2,
    #                     self.player_sprite.center_y - self.height / 2)
    #     self.camera_sprites.move_to(position, CAMERA_SPEED)

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )

        # Don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Move the player with the physics engine
        self.physics_engine.update()

        self.pipes_physics_engine.update()

        # Position the camera
        self.center_camera_to_player()

        # # Scroll screen to player
        # self.scroll_to_player()

        # Did the player fall off the map?
        if self.player_sprite.center_y < -100:
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y

        # # Check for collisions
        # pipe_hit_list = arcade.check_for_collision_with_lists(self.player_sprite, self.scene["Pipes"])
        #
        # # Loop through pipes and check collisions
        # for pipe in pipe_hit_list:
        #     arcade.play_sound(self.hit_pipe_sound)

    # def on_resize(self, width, height):
    #     """
    #     Resize window
    #     Handle the user grabbing the edge and resizing the window.
    #     """
    #     self.camera_sprites.resize(int(width), int(height))
    #     self.camera_gui.resize(int(width), int(height))

def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, "Flapping Bird")
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
