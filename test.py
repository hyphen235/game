import arcade

import os

SPRITE_SCALING_BOX = 0.5
SPRITE_SCALING_PLAYER = 0.3

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

MOVEMENT_SPEED = 2.5

VIEWPORT_MARGIN = 200
RIGHT_FACING = 0
LEFT_FACING = 1
SPRITE_SCALING_ISLAND = 0.5
PLAYER_FRAMES = 8
PLAYER_FRAMES_PER_TEXTURE = 8


class InstructionView(arcade.View):
    
    def setup():

        return

    def on_show(self):
    
        arcade.set_background_color(arcade.csscolor.LIGHT_BLUE)
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Main Menu lol", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 
                        arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("click to begin", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2-75, 
                        arcade.color.BLACK, font_size=20, anchor_x="center")

        return

def load_texture_pair(file_name):

    return [
        arcade.load_texture(file_name),
        arcade.load_texture(file_name, flipped_horizontally=True)]






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
        
        




class GameView(arcade.View):
    
    

    def __init__(self):
       
        super().__init__()

        
        
    



        self.background = None

        self.player_list = None
        self.wall_list = None

        self.floor_list = None
        self.player_sprite = None

        
        self.physics_engine = None

    def setup(self):

        
        arcade.set_background_color(arcade.color.LIGHT_BLUE)

        self.view_left = 0
        self.view_bottom = 0

        
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.floor_list = arcade.SpriteList()
     
        self.score = 0

       
        self.player_sprite = Player()
        self.player_sprite.center_x = SCREEN_WIDTH/2
        self.player_sprite.center_y = SCREEN_HEIGHT/2
        self.player_list.append(self.player_sprite)

        floor = arcade.Sprite("islandWIP.png", SPRITE_SCALING_ISLAND)
        floor.center_x = 300
        floor.center_y = 300
        self.floor_list.append(floor)

        #wall = arcade.Sprite("sand.png", SPRITE_SCALING_BOX)
        #wall.center_x = 300
       # wall.center_y = 200
        #self.wall_list.append(wall)

       # wall = arcade.Sprite("sand.png", SPRITE_SCALING_BOX)
        #wall.center_x = 300
        #wall.center_y = 280
       # self.wall_list.append(wall)
        
        #wall = arcade.Sprite("sand.png", SPRITE_SCALING_BOX)
       # wall.center_x = 380
       # wall.center_y = 200
       # self.wall_list.append(wall)

       # wall = arcade.Sprite("sand.png", SPRITE_SCALING_BOX)
       # wall.center_x = 380
       # wall.center_y = 280
        #self.wall_list.append(wall)

        #self.background = arcade.load_texture("Water-1.png")

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)


    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)
        
        
        
        
        return



    def on_draw(self):
       
        #self.floor_list.draw()
        self.player_list.draw()
        
        self.wall_list.draw()

        changed = False

     
        left_boundary = self.view_left + VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

       
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

        #arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)


    def update(self, delta_time):
        self.physics_engine.update()
        self.player_sprite.update_animation()

    def on_key_press(self, key, modifiers):
       

        if key == arcade.key.W:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.S:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.A:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        

        if key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.change_x = 0


    def on_mouse_press(self, x, y, button, modifiers):
            if button == arcade.MOUSE_BUTTON_LEFT:
                print(x, y)
            elif button == arcade.MOUSE_BUTTON_RIGHT:
                print(x, y)

def main():
    """ Main method """
    
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "bruh")
    start_view = InstructionView()
    window.show_view(start_view)
    start_view.setup()
    arcade.run()


if __name__ == "__main__":
    main()