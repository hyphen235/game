import arcade

WIDTH = 1000
HEIGHT = 600
MOVEMENT_SPEED = 3
PLAYER = "player(female).png" 
#Player(male.png)



class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        
        super().__init__(width, height, title)
        self.set_mouse_visible(True)        
        arcade.set_background_color(arcade.csscolor.BLUE)
        self.player = arcade.Sprite(PLAYER, 1.5)
        
    def on_draw(self):
        arcade.start_render()
        self.player.draw()

   
    def setup(self):
        self.coin.center_x = 50
        self.coin.center_y = 50
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
   
    def update(self, delta_time):
        self.player.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.A:
            self.player.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.D: 
            self.player.change_x = MOVEMENT_SPEED
        elif key == arcade.key.W:
            self.player.change_y = MOVEMENT_SPEED
        elif key == arcade.key.S:   
            self.player.change_y = -MOVEMENT_SPEED
    



    def on_key_release(self, key, modifiers):
        if key == arcade.key.A or key == arcade.key.D:
            self.player.change_x = 0
        if key == arcade.key.W or key == arcade.key.S:   
            self.player.change_y = 0

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            print(x, y)
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            print(x, y)

def main():
    window = MyGame(WIDTH, HEIGHT, "Deez")
    arcade.run()
main()

