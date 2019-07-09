import fgarcade as ge
from fgarcade.enums import Command
from arcade import SpriteList
import fgarcade.game.platforms
from arcade import check_for_collision
import arcade
from fgarcade import Player


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
    def init_world(self):
        self.world_color = 'yellow'
        self.player_initial_position = (5, 1.5)
        self.create_tower(12, 2, coords=(0, 1))
        self.create_ground(10, coords=(0, 0), smooth_ends=False)
        self.create_platform(3, coords=(12,3))
        self.create_platform(2, coords=(17,6))
        self.create_platform(3, coords=(20,2))
        self.create_platform(2, coords=(25,5))
        self.create_platform(3, coords=(28,2))
        self.create_platform(2, coords=(32,4))
        self.create_ground(33, coords=(38, 0), smooth_ends=False)
        self.create_ground(2, coords=(42, 1))
        #inimigo
        self.create_ground(2, coords=(52, 1))
        self.create_ramp('up', 6, coords=(65, 1))
        self.create_platform(2, coords=(69,9))
        self.create_platform(1, coords=(72,5))
        self.create_platform(10, coords=(75,2))
        self.create_ground(10, coords=(90, 0))
        #inimigo
        self.create_tower(12, coords=(100, 0))

    def init_enemies(self):

        self.enemies = SpriteList(is_static=True)
        def create_enemy(x,y):
            enemy = self.create_object('enemy/enemyWalking_1',(x,y), role=self.enemies)
            self.enemies.append(enemy)
        create_enemy(5,1)

    def draw_elements(self):
        super().draw_elements()
        self.enemies.draw()

    def update_enemy(self,dt):
        if not self.game_over:
            self.enemies.update()
            self.physics_engine.update()
        if len(arcade.check_for_collision_with_list(self.player, self.enemies)) > 0:
            print("morreu")

    def update(self, dt):
        super().update(dt)
        self.update_enemy(dt)
        self.update_clock(dt)

    def death(self):

        self.dead = update_actions()

    def init_items(self):
        pass
    def init(self):
        self.init_world()
        self.init_items()
        self.init_enemies()
        #self.update_enemy()

if __name__ == "__main__":
    Game().run()
