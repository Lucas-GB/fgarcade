import fgarcade as ge
from fgarcade.enums import Command
from arcade import SpriteList
import fgarcade.game.platforms
import arcade
from fgarcade import Player
from arcade import check_for_collision_with_list
from arcade import AnimatedTimeSprite
from fgarcade.game.player import AnimatedWalkingSprite

class Player(ge.Player):
    is_kicking = False
    _not_kicking_texture = None


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.kicking_texture = self._load('switch1')

    def update_actions(self, commands, physics):
        self.is_kicking = bool(commands & Command.SPACE)
        super().update_actions(commands, physics)

    def update_animation(self):
        super().update_animation()

        if self.is_kicking:
            if self._texture != self.kicking_texture:
                self._not_kicking_texture = self._texture
            self._texture = self.kicking_texture

        elif self._not_kicking_texture is not None:
            self._texture = self._not_kicking_texture
            self._not_kicking_texture = None


class Game(ge.Platformer):
    """
    Simple platformer example
    """
    title = 'Simple platformer'
    player_initial_tile = 4, 1
    player_class = Player
    game_over = False
    score = 0
    timer = 0.0
    life = 0
    def init_world(self):
        self.world_color = 'yellow'
        self.player_initial_position = (5, 1.5)
        self.create_tower(12, 2, coords=(0, 1))
        self.create_ground(10, coords=(0, 0), smooth_ends=False)
        self.create_platform(3, coords=(12,3))
        self.create_platform(2, coords=(17,6))
        self.create_platform(5, coords=(20,2))
        self.create_platform(2, coords=(25,5))
        self.create_platform(3, coords=(28,2))
        self.create_platform(2, coords=(32,4))
        self.create_ground(33, coords=(38, 0), smooth_ends=False)
        self.create_ground(2, coords=(42, 1))
        #inimigo
        self.create_ground(2, coords=(52, 1))
        self.create_ramp('up', 6, coords=(65, 1))
        #self.create_platform(2, coords=(69,9))
        self.create_platform(1, coords=(72,5))
        self.create_platform(10, coords=(75,2))
        self.create_ground(10, coords=(90, 0))
        #inimigo
        self.create_tower(12, coords=(100, 0))

    def init_enemies(self):
        
        self.enemies_list = SpriteList(is_static=True)
        def create_enemy(x,y):
            enemy = self.create_object('other/spikes/spikes-high',(x,y))
            self.enemies_list.append(enemy)
        create_enemy(7,1)
        create_enemy(45,1)
        create_enemy(48,1)
        create_enemy(22,3)
        create_enemy(54,1)
        create_enemy(57,1)
        create_enemy(60,1)
        create_enemy(63,1)
        create_enemy(77,2.9)
        create_enemy(80,2.9)
        create_enemy(83,2.9)
        
        
    def init_flag(self):
        self.flags_list = SpriteList(is_static=True)
        def create_flag(x,y):
            flag = self.create_object('other/flag/flagRed_up',(x,y))
            self.flags_list.append(flag)
        create_flag(98,1)
    
    def init_coins(self):
        self.coins_list = SpriteList()
        def create_coin(x,y):
            coin = self.create_object('other/items/yellowJewel',(x,y))
            self.coins_list.append(coin)
        create_coin(7,4)
        create_coin(20,8)
        create_coin(12,7)
        create_coin(23,8)
        create_coin(35,7)            
        create_coin(46,4)
        create_coin(49,5)
        create_coin(42,5)
        create_coin(50,5)
        create_coin(55,2)
        create_coin(57,4)
        create_coin(60,3)
        create_coin(63,5)   
        create_coin(75,5)
        create_coin(77,4)
        create_coin(80,7)
        create_coin(81,3)       

    
    def draw_elements(self):
        super().draw_elements()
        self.enemies_list.draw()
        output = f"Pontos: {self.score}"
        arcade.draw_text(output,640,550,arcade.color.BLACK,20)
        minutes = int(self.timer) // 60
        seconds = int(self.timer) % 60
        output_timer = f"Tempo: {minutes:02d}:{seconds:02d}"
        arcade.draw_text(output_timer,620,570,arcade.color.BLACK,20)
        output_life = f"Vidas: {self.life}"
        arcade.draw_text(output_life,640,530,arcade.color.BLACK,20)

    def update_collision(self,dt):
        if not self.game_over:
            self.enemies_list.update()
            if len(check_for_collision_with_list(self.player, self.enemies_list)) > 0:
                self.score = 0
                print('morreu')
                self.life -= 1
                #voltar para o a posição de inicio
            if len(check_for_collision_with_list(self.player, self.flags_list)) > 0:
                pass
                #passar de fase aparecer na tela stats
            hit_coin = check_for_collision_with_list(self.player, self.coins_list)
            for coin in hit_coin:
                coin.remove_from_sprite_lists()
                self.score += 1
                if self.score % 10 == 0:
                    self.life += 1

    def update(self, dt):
        super().update(dt)
        self.update_collision(dt)   
        self.timer += dt

    def init(self):
        self.init_world()
        self.init_flag()
        self.init_enemies()
        self.init_coins()

if __name__ == "__main__":
    Game().run()
