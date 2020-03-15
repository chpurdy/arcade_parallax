import arcade
import random

class App(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "Parallaxing Demo")
        self.scroll_speed = 1

    def setup(self):
        '''
        create background layers
        '''
        self.bg_back = arcade.load_texture('graphics/Backgrounds/backgroundEmpty.png')
        self.bg_mid1 = arcade.load_texture('graphics/Backgrounds/Elements/cloudLayer1.png')
        self.bg_mid2 = arcade.load_texture('graphics/Backgrounds/Elements/cloudLayer2.png')
        
        self.clouds_back = arcade.SpriteList()
        self.clouds_front = arcade.SpriteList()
        
        # generate clouds 
        for i in range(100):
            cloud_num = random.randint(1,8)
            cloud = arcade.Sprite(f'graphics/PNG/Default/cloud{cloud_num}.png',scale=random.random(),center_x=random.randint(i*200,(i+1)*200),center_y=random.randint(self.height/3,self.height))
            self.clouds_back.append(cloud)
        
        for i in range(100):
            cloud_num = random.randint(1,8)
            cloud = arcade.Sprite(f'graphics/PNG/Default/cloud{cloud_num}.png',scale=random.random(),center_x=random.randint(i*200,(i+1)*200),center_y=random.randint(self.height/3,self.height))
            self.clouds_front.append(cloud)
        
        self.player = arcade.AnimatedTimeBasedSprite(center_x=50,center_y=self.width/2)
        self.player.change_x = self.scroll_speed
        for i in range(1,4):
            texture = arcade.load_texture(f'graphics/Planes/planeYellow{i}.png')
            frame = arcade.AnimationKeyframe(i,1,texture)
            self.player.frames.append(frame)
        
        
        
        
        # Viewport stuff
        
        self.left_view = 0
        self.bottom_view = 0
        self.bg_mid1_x = 0
        self.bg_mid2_x = self.width
        self.shake_screen = False
        self.shake_count = 0
        self.shake_intensity = 5
        




    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(self.left_view, self.bottom_view,self.width+self.shake_intensity, self.height+self.shake_intensity,self.bg_back)
        self.draw_mid_bg()
        self.clouds_back.draw()
        self.player.draw()
        self.clouds_front.draw()

    def on_update(self, dt):
        if not self.shake_screen:
            self.set_viewport(self.left_view, self.left_view + self.width, self.bottom_view, self.bottom_view + self.height)
        else:
            shake = [(self.shake_intensity,0),
                     (self.shake_intensity,self.shake_intensity),
                     (0,self.shake_intensity)]

            self.set_viewport(self.left_view + shake[self.shake_count][0], 
                              self.left_view + self.width + shake[self.shake_count][0], 
                              self.bottom_view + shake[self.shake_count][1], 
                              self.bottom_view + self.height+ + shake[self.shake_count][1])
            self.shake_count += 1
            if self.shake_count == 3:
                self.shake_screen = False
                self.shake_count = 0


        self.left_view += self.scroll_speed
        for cloud in self.clouds_back:
            cloud.center_x -= self.scroll_speed # move twice as fast as background

        for cloud in self.clouds_front:
            cloud.center_x -= self.scroll_speed*2 # move twice as fast as background
        self.player.update()
        self.player.update_animation()
        if self.player.center_x <= self.left_view + 50:
            self.player.center_x = self.left_view + 50
            self.player.change_x = self.scroll_speed

    def draw_mid_bg(self):
        
        # move left view to the far right
        if self.left_view >= self.bg_mid1_x + self.width:
            self.bg_mid1_x += self.width * 2
        
        if self.left_view >= self.bg_mid2_x + self.width:
            self.bg_mid2_x += self.width*2
        
        
        arcade.draw_lrwh_rectangle_textured(self.bg_mid1_x, 0, self.width, self.height/4, self.bg_mid1)
        arcade.draw_lrwh_rectangle_textured(self.bg_mid2_x, 0, self.width, self.height/4, self.bg_mid2)

    
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.UP:
            self.player.change_y = 3
            self.player.angle = 30

        elif symbol == arcade.key.DOWN:
            self.player.change_y = -3
            self.player.angle = -30

        if symbol == arcade.key.RIGHT:
            self.player.change_x += 3
        elif symbol == arcade.key.LEFT:
            if self.player.center_x > self.left_view + 50:
                self.player.change_x -= 3

        if symbol == arcade.key.SPACE:
            self.shake_screen = True
            self.shake_count = 0 

    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.UP:
            self.player.change_y = 0
            self.player.angle = 0

        elif symbol == arcade.key.DOWN:
            self.player.change_y = 0
            self.player.angle = 0
        if symbol == arcade.key.LEFT:
            self.player.change_x = 0

        elif symbol == arcade.key.RIGHT:
            self.player.change_x = 0

        


def main():
    app = App()
    app.setup()
    arcade.run()


if __name__ == "__main__":
    main()
        