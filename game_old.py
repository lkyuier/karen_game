import random
import pygame
import sys

from Character import Character
from commons import generate_shards, create_checkerboard, update_text_surfaces, \
    remove_shared, check_collision, generate_monster, draw_text, check_collision_with_monsters
from movement import control_movement

# 常量定义
SCREEN_WIDTH, SCREEN_HEIGHT, MAX_TEXT_WIDTH = 800, 600, 100
person_speed = 3
jump_speed = -15
gravity = 0.5
num_shards = 30
TILE_SIZE = 50
NUM_MONSTERS = 1

WHITE = (255, 255, 255)
MIRROR_SIZE = (200, 200)
MIRROR_MOVE_INTERVAL = 3000  # 3秒（以毫秒为单位）

# 对话内容列表
DIALOGS_ALL_CONTENT = [
    "bailiu: 在必要的时候你伸手帮我一下，我们互利互惠，互相合作怎么样？",
    "mushicheng:OK,那就合作吧。",
    "mushicheng:我们信息共享，互相帮助，我不白用，1积分的诚意给你。",
    "mushicheng:我的诚意就是--",
    "mushicheng:白柳你哭的诚恳一点，我也不是不能勉为其难地伸出援手。",
    "god: 恭喜玩家白柳首先触发主线任务--",
    "god: 收集末班车上的碎镜片",
    "mushicheng: 白柳，你怎么触发的主线任务？你都没动过。",
    "bailiu: 我怎么没动。我脑子在动啊，牧四诚。",
    "bailiu: "
]
DIALOGS_AFTER_SHARDS = [
    "bailiu:你觉得这些怪物为什么阻拦我们收集碎镜片呢？",
    "mushicheng: 为什么？",
    "bailiu:只有一个原因，",
    "bailiu:他们在害怕这面镜子。",
    "bailiu:他们之所以变成现在的样子--",
    "bailiu:都是这面镜子导致的。"
]
DIALOGS_AFTER_MIRROR = [
    "god: 恭喜玩家白柳解锁所有主线任务以及怪物书通关《爆裂末班车》",
    "god: 玩家达成true ending--",
    "god: 《永远停止的末班列车》",
    "god: 从那场爆炸开始--",
    "god: 死去的乘客们日复一日地被那面可怕的镜子困在这里",
    "god: 重复着他们死前一个小时的痛苦。",
    "god: 他们惨叫着，哀嚎着",
    "god: 偷偷藏起那面镜子的碎片四处躲藏--",
    "god: 可惜都无济于事。",
    "god: 那面毫无人类情感的镜子依旧循环燃烧着他们--",
    "god: 烧成灰烬焦炭都不曾停息。",
    "god: 终于有一天--",
    "god: 有人停止了这班被大火熊熊燃烧过的镜中末班车",
    "god: 乘客们微笑着走出了列车。",
    "god: 就算是死亡，",
    "god: --他们也终于可以到站了。"
]


# 初始化 pygame
def initialize_pygame():
    pygame.init()


# 主游戏循环
def start_game():
    global DIALOGS_ALL_CONTENT, dialogue_finished, current_dialog_index, mirror_position, mirror_health, score

    initialize_pygame()
    font = pygame.font.Font("C:/Windows/Fonts/simhei.ttf", 18)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    background = create_checkerboard(pygame, SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE)

    shards, shard_image = generate_shards(pygame, num_shards, SCREEN_WIDTH, SCREEN_HEIGHT)

    person_mushicheng = Character("mushicheng", 'assets/images/mushichen.png', SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 50,
                                  SCREEN_WIDTH, SCREEN_HEIGHT)
    person_bailiu = Character("bailiu", 'assets/images/bailiu.png', SCREEN_WIDTH // 4 + 50, SCREEN_HEIGHT // 2 + 10,
                              SCREEN_WIDTH, SCREEN_HEIGHT)

    # 加载镜子的图片
    mirror_image = pygame.image.load('assets/images/mirror.png')  # 替换为你镜子图片的路径
    mirror_image = pygame.transform.scale(mirror_image, MIRROR_SIZE)  # 调整图片大小

    characters = [person_mushicheng, person_bailiu]

    # 初始化镜子位置和定时器
    mirror_position = generate_random_mirror_position(characters, MIRROR_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT)
    last_mirror_move_time = pygame.time.get_ticks()

    # 初始化镜子血量
    mirror_health = 15

    current_dialog_index = 0
    collected_shards = 0
    total_shards = len(shards)

    # 初始化计分板
    score = 0

    monsters, monster_image = generate_monster(pygame, NUM_MONSTERS, SCREEN_WIDTH, SCREEN_HEIGHT,
                                               shards, characters)
    dialogue_finished = False

    while True:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            current_dialog_index = handle_dialogue(event, current_dialog_index, DIALOGS_ALL_CONTENT)

        if current_dialog_index >= len(DIALOGS_ALL_CONTENT):
            dialogue_finished = True

        keys = pygame.key.get_pressed()

        person_mushicheng.control_movement(keys, person_speed, jump_speed, gravity)
        person_bailiu.control_movement(keys, person_speed, jump_speed, gravity)

        previous_collected_shards = collected_shards
        collected_shards = remove_shared(collected_shards, shards, shard_image, person_mushicheng, person_bailiu)

        # 如果碎镜片被收集，增加分数
        if collected_shards > previous_collected_shards:
            score += 1

        if collected_shards == total_shards:
            current_dialog_index = 0  # 重置对话索引
            collected_shards = 0
            DIALOGS_ALL_CONTENT = DIALOGS_AFTER_SHARDS  # 重新赋值为新对话
            dialogue_finished = False

        if check_collision_with_monsters(person_mushicheng.x, person_mushicheng.y, person_bailiu.x, person_bailiu.y,
                                         monsters):
            start_game()
            return

        # 检查角色是否与镜子碰撞
        mirror_rect = pygame.Rect(mirror_position[0], mirror_position[1], MIRROR_SIZE[0], MIRROR_SIZE[1])
        for character in characters:
            character_rect = pygame.Rect(character.x, character.y, character.image.get_width(),
                                         character.image.get_height())
            if mirror_rect.colliderect(character_rect):
                mirror_health -= 1
                # 更新镜子位置以防止连续碰撞
                mirror_position = generate_random_mirror_position(characters, MIRROR_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT)
                break

        # 检查镜子血量是否归零
        if mirror_health <= 0 and DIALOGS_ALL_CONTENT != DIALOGS_AFTER_MIRROR:
            DIALOGS_ALL_CONTENT = DIALOGS_AFTER_MIRROR  # 切换对话内容
            current_dialog_index = 0  # 重置对话索引
            dialogue_finished = False

        # 每3秒钟移动一次镜子
        if current_time - last_mirror_move_time > MIRROR_MOVE_INTERVAL:
            mirror_position = generate_random_mirror_position(characters, MIRROR_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT)
            last_mirror_move_time = current_time

        render_game(screen, background, person_mushicheng, person_bailiu, shards, shard_image, monsters, monster_image,
                    font, dialogue_finished, current_dialog_index, mirror_image, mirror_position, mirror_health, score)

        clock.tick(30)


def render_game(screen, background, person_mushicheng, person_bailiu, shards, shard_image, monsters, monster_image,
                font, dialogue_finished, current_dialog_index, mirror_image, mirror_position, mirror_health, score):
    screen.blit(background, (0, 0))
    screen.blit(person_mushicheng.image, (person_mushicheng.x, person_mushicheng.y))
    screen.blit(person_bailiu.image, (person_bailiu.x, person_bailiu.y))

    for shard in shards:
        screen.blit(shard_image, shard.topleft)

    for monster in monsters:
        screen.blit(monster_image, monster.topleft)

    if not dialogue_finished:
        # 去除对话中的角色名字
        dialogue_text = DIALOGS_ALL_CONTENT[current_dialog_index]
        dialogue_text = dialogue_text.split(":")[-1].strip()  # 去除冒号前的内容
        draw_text(screen, dialogue_text, (50, 50), font, BLACK)  # 黑色文本
    else:
        # 绘制镜子的图片
        screen.blit(mirror_image, mirror_position)  # 在新位置绘制镜子

    # 绘制镜子的血量
    draw_text(screen, f"Mirror Health: {mirror_health}", (10, 10), font, BLACK)

    # 绘制计分板
    draw_text(screen, f"Score: {score}", (SCREEN_WIDTH - 120, 10), font, BLACK)

    pygame.display.flip()


if __name__ == "__main__":
    start_game()
