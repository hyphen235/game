from PIL.Image import alpha_composite
import arcade
import random
import os

SPRITE_SCALING_BOX = 0.5
SPRITE_SCALING_PLAYER = 0.3

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

MOVEMENT_SPEED = 2

VIEWPORT_MARGIN = 200
RIGHT_FACING = 0
LEFT_FACING = 1
SPRITE_SCALING_ISLAND = 0.5
PLAYER_FRAMES = 8
PLAYER_FRAMES_PER_TEXTURE = 8
SPRITE_SCALING_COIN = 1
COIN_COUNT = 25


def load_texture_pair(file_name):

    return [
        arcade.load_texture(file_name),
        arcade.load_texture(file_name, flipped_horizontally=True)]

class MenuView(arcade.View):
    """ Class that manages the 'menu' view. """

    def on_show(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.DARK_BLUE)

    def on_draw(self):
        """ Draw the menu """
        arcade.start_render()
        arcade.draw_text("DELUGE", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                         arcade.color.WHITE, font_size=72, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ Use a mouse press to advance to the 'game' view. """
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)


class GameView(arcade.View):
    """ Manage the 'game' view for our program. """

    def __init__(self):
        super().__init__()
        self.background = None

        self.player_list = None
        self.wall_list = None
        self.win_list = None
        self.floor_list = None
        self.player_sprite = None
        
        self.coin = None
        self.score = 0
        
        self.physics_engine = None

        self.touch_cave = False

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.total_time = 0.0
        self.output = "00:00:00"


    def setup(self):
      
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)
        arcade.set_background_color(arcade.color.LIGHT_BLUE)

        self.map = arcade.load_texture("map.png")
       
        self.view_left = 0
        self.view_bottom = 0

        arcade.set_background_color(arcade.csscolor.LIGHT_BLUE)
        self.win_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.floor_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.total_time = 0.0
        self.score = 0
        self.win_sprite = Win(500, 1000)
        self.win_list.append(self.win_sprite)
        self.player_sprite = Player()
        self.player_sprite.center_x = SCREEN_WIDTH/2
        self.player_sprite.center_y = SCREEN_HEIGHT/2
        self.player_list.append(self.player_sprite)

       
        for i in range(COIN_COUNT):
            coin = arcade.Sprite("placeholder.png", SPRITE_SCALING_COIN)
        
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)
       
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)

        


    
    
    def on_draw(self):
        """ Draw everything for the game. """
        arcade.start_render()
    
        
        self.wall_list.draw()
        


        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

        changed = True
        
        arcade.draw_lrwh_rectangle_textured(-500, -1200, 2500, 2500, self.map)
        
        self.win_list.draw()
        self.floor_list.draw()
        
        self.player_list.draw()
        left_boundary = self.view_left + VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True
        self.coin_list.draw()
       
        right_boundary = self.view_left + SCREEN_WIDTH - VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

      
        top_boundary = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

    
        bottom_boundary = self.view_bottom + VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

     
        self.view_left = int(self.view_left)
        self.view_bottom = int(self.view_bottom)

        
        if changed:
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left - 1,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom - 1)
    
        arcade.draw_text(self.output,
                         self.player_sprite.center_x, self.player_sprite.center_y + 50,
                         arcade.color.WHITE, 25,
                         anchor_x="center")


    def on_key_press(self, key, modifiers):
        """ Handle keypresses. In this case, we'll just count a 'space' as
        game over and advance to the game over view. """
        self.player_sprite.on_key_press(key, modifiers)
        if key == arcade.key.SPACE:
            game_over_view = GameOverView()
            self.window.show_view(game_over_view)

        if key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.D:
            self.right_pressed = True


    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.D:
            self.right_pressed = False

    def on_mouse_press(self, x, y, button, modifiers):
        if button == MOUSE_BUTTON_LEFT:
            print(self.get_view()[0]+x, self.get_view()[2]+y)

    def update(self, delta_time):
       

        self.total_time += delta_time
        
        minutes = int(self.total_time) // 60
        seconds = int(self.total_time) % 60
        seconds_100s = int((self.total_time - seconds) * 100)
        self.output = f"{minutes:02d}:{seconds:02d}:{seconds_100s:02d}"

        self.coin_list.update()

        # Generate a list of all sprites that collided with the player.
        coins_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                              self.coin_list)


        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = MOVEMENT_SPEED + 1
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -MOVEMENT_SPEED - 1
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = MOVEMENT_SPEED

        self.player_sprite.update()
        self.player_sprite.update_animation()
        self.physics_engine.update()
        

class Win(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__("placeholder.png", 1)
        self.center_x = x
        self.center_y = y


class GameOverView(arcade.View):
    """ Class to manage the game over view """
    def on_show(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """ Draw the game over view """
        arcade.start_render()
        arcade.draw_text("Game Over - press ESCAPE to advance", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                         arcade.color.WHITE, 30, anchor_x="center")

    def on_key_press(self, key, _modifiers):
        """ If user hits escape, go back to the main menu view """
        if key == arcade.key.ESCAPE:
            menu_view = MenuView()
            self.window.show_view(menu_view)



class Player(arcade.Sprite):

    def __init__(self):
        super().__init__("Geoffery.png", SPRITE_SCALING_PLAYER)
        self.character_face_direction = RIGHT_FACING
        
        self.cur_texture = 0
        
        self.virtual_texture = 0

        self.idle_texture_pair = load_texture_pair("Geoffery.png")
        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair(f"./walk/walk{i}.png")
            self.walk_textures.append(texture)

        self.texture = self.idle_texture_pair[0]
    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.change_y = MOVEMENT_SPEED
        elif key == arcade.key.S:
            self.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.A:
            self.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.change_x = MOVEMENT_SPEED
        
    def on_key_release(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.S:
            self.change_y = 0
            print("y=0")
        elif key == arcade.key.A or key == arcade.key.D:
            self.change_x = 0

    def update(self):
        
        self.center_x += self.change_x

    def update_animation(self, delta_time: float = 1 / 60):
        
        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        if self.change_x == 0:
            
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        

        self.virtual_texture += 1
        if self.virtual_texture > PLAYER_FRAMES * PLAYER_FRAMES_PER_TEXTURE:
            self.cur_texture = 0
            self.virtual_texture = 0
        if (self.virtual_texture +1) % PLAYER_FRAMES_PER_TEXTURE == 0:
            self.cur_texture = self.virtual_texture // PLAYER_FRAMES_PER_TEXTURE
            self.texture = self.walk_textures[self.cur_texture][
               self.character_face_direction
            ]
        return
        

class boat():
    
    def __init__(self):




        return






def main():
    """ Main method """
    
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "bruh")
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()