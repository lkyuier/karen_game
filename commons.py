import os
import random
import pygame

def split_text(text, font, max_width):
    """
    将长文本拆分成多行文本，每行宽度不超过max_width。
    """
    lines = []
    words = text.split(' ')
    current_line = ''
    for word in words:
        test_line = f"{current_line} {word}".strip()
        test_surface = font.render(test_line, True, (0, 0, 0))

        if test_surface.get_width() <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines

def render_text(text, font, max_width):
    """
    渲染多行文本为Surface列表，每行宽度不超过max_width。
    """
    lines = split_text(text, font, max_width)
    line_surfaces = [font.render(line, True, (0, 0, 0)) for line in lines]
    return line_surfaces

def create_checkerboard(pygame, width, height, tile_size):
    """
    创建白灰相间的棋盘格背景。
    """
    checkerboard = pygame.Surface((width, height))
    colors = [(255, 255, 255), (192, 192, 192)]

    for y in range(0, height, tile_size):
        for x in range(0, width, tile_size):
            rect = pygame.Rect(x, y, tile_size, tile_size)
            pygame.draw.rect(checkerboard, colors[((x // tile_size) + (y // tile_size)) % 2], rect)
    return checkerboard

def update_text_surfaces(dialogue_index, dialogs_all, font, max_text_width):
    """
    更新文本渲染并返回相关的对话信息。
    """
    text = dialogs_all[dialogue_index]
    if text.startswith("mushicheng:"):
        is_mushicheng_turn = True
        is_bailiu_turn = False
        text = text[len("mushicheng:"):]
        dialogue_color = (255, 0, 0)  # 红色代表Mushicheng

    elif text.startswith("bailiu:"):
        text = text[len("bailiu:"):]
        is_mushicheng_turn = False
        is_bailiu_turn = True
        dialogue_color = (78, 78, 255)  # 蓝色代表Bailiu

    elif text.startswith("god:"):
        text = text[len("god:"):]
        dialogue_color = (255, 255, 255)  # 白色代表God
        is_mushicheng_turn = False
        is_bailiu_turn = False

    text_surfaces = render_text(text, font, max_text_width)
    return is_mushicheng_turn, is_bailiu_turn, dialogue_color, text_surfaces

def collect_shared(pygame, shards, pos_x, pos_y, width, height, collected_shards, num_shards, dialogs_all, font):
    """
    碰撞检测和收集碎镜片
    """
    for shard in shards[:]:
        if pygame.Rect(pos_x, pos_y, width, height).colliderect(shard):
            shards.remove(shard)
            collected_shards += 1
            if collected_shards >= num_shards:
                dialogs_all.extend([
                    "bailiu:你认为这些怪物为什么会收集镜片不让我们拿到？",
                    "mushicheng:为什么？",
                    "bailiu:因为他们在害怕这面镜子。",
                    "bailiu:我猜测他们现在这副模样就是完整的镜子导致的。"
                ])
                current_dialogue_index = len(dialogs_all) - 1
                is_mushicheng_turn, is_bailiu_turn, dialogue_color, text_surfaces = update_text_surfaces(
                    current_dialogue_index, dialogs_all, font, 200)
    return is_mushicheng_turn, is_bailiu_turn, dialogue_color, text_surfaces

import random
import pygame

def load_shard_images(directory):
    """
    从指定目录加载所有碎片图像并返回它们的列表。
    """
    shard_images = []
    for filename in os.listdir(directory):
        if filename.endswith('.png'):  # 只加载png文件
            shard_image = pygame.image.load(os.path.join(directory, filename))
            shard_image = pygame.transform.scale(shard_image, (50, 50))
            shard_images.append(shard_image)
    return shard_images

def generate_shards_new(pygame, num_shards, screen_width, screen_height):
    """
    生成不重叠的带有闪光效果的碎镜片并返回它们的位置列表及其图像。
    """
    shard_images = load_shard_images('images/shards4.png')  # 加载所有碎片图像

    shards = []
    shard_surfaces = []
    attempts = 0  # 用于限制尝试次数，防止无限循环

    while len(shards) < num_shards and attempts < num_shards * 10:
        attempts += 1
        x = random.randint(0, screen_width - 50)
        y = random.randint(0, screen_height - 50)

        new_shard = pygame.Rect(x, y, 50, 50)

        if all(not new_shard.colliderect(existing_shard) for existing_shard in shards):
            shards.append(new_shard)

            # 随机选择一个碎片图像
            shard_image = random.choice(shard_images).copy()

            # 创建一个用于叠加闪光效果的表面
            glitter_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
            for i in range(50):  # 控制闪光点的数量
                # 生成闪光点
                glitter_x = random.randint(0, 49)
                glitter_y = random.randint(0, 49)
                color = (255, 255, 255, random.randint(150, 255))  # 闪光颜色（白色，带透明度）
                glitter_surface.set_at((glitter_x, glitter_y), color)

            # 将闪光效果叠加到碎片图像上
            shard_image.blit(glitter_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

            shard_surfaces.append(shard_image)

    return shards, shard_surfaces

def generate_shards(pygame, num_shards, screen_width, screen_height):
    """
    生成不重叠的带有闪光效果的碎镜片并返回它们的位置列表及其图像。
    """
    shard_image = pygame.image.load('assets/images/shards5-removebg-preview.png')
    shard_image = pygame.transform.scale(shard_image, (50, 50))
    shard_width, shard_height = shard_image.get_width(), shard_image.get_height()

    shards = []
    attempts = 0  # 用于限制尝试次数，防止无限循环

    # 创建一个用于叠加闪光效果的表面
    glitter_surface = pygame.Surface((shard_width, shard_height), pygame.SRCALPHA)
    for i in range(50):  # 控制闪光点的数量
        # 生成闪光点
        x = random.randint(0, shard_width - 1)
        y = random.randint(0, shard_height - 1)
        color = (255, 255, 255, random.randint(150, 255))  # 闪光颜色（白色，带透明度）
        glitter_surface.set_at((x, y), color)

    # 将闪光效果叠加到每个碎片上
    shard_image.blit(glitter_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

    while len(shards) < num_shards and attempts < num_shards * 10:
        attempts += 1
        x = random.randint(0, screen_width - shard_width)
        y = random.randint(0, screen_height - shard_height)

        new_shard = pygame.Rect(x, y, shard_width, shard_height)

        if all(not new_shard.colliderect(existing_shard) for existing_shard in shards):
            shards.append(new_shard)

    return shards, shard_image

def generate_shards_discard(pygame, num_shards, screen_width, screen_height):
    """
    生成不重叠的碎镜片并返回它们的位置列表及其图像。
    """
    shard_image = pygame.image.load('images/shard.png')
    shard_image = pygame.transform.scale(shard_image, (30, 30))
    shard_width, shard_height = shard_image.get_width(), shard_image.get_height()

    shards = []
    attempts = 0  # 用于限制尝试次数，防止无限循环

    while len(shards) < num_shards and attempts < num_shards * 10:
        attempts += 1
        x = random.randint(0, screen_width - shard_width)
        y = random.randint(0, screen_height - shard_height)

        new_shard = pygame.Rect(x, y, shard_width, shard_height)

        if all(not new_shard.colliderect(existing_shard) for existing_shard in shards):
            shards.append(new_shard)

    return shards, shard_image

def generate_monster(pygame, num_monsters, screen_width, screen_height, shards, characters):
    """
    生成不与碎镜片和人物重叠的怪物，并返回它们的位置列表及其图像。
    """
    monster_image = pygame.image.load('assets/images/monster.png')
    monster_image = pygame.transform.scale(monster_image, (75, 75))
    monster_width, monster_height = monster_image.get_width(), monster_image.get_height()

    monsters = []
    attempts = 0  # 用于限制尝试次数，防止无限循环

    while len(monsters) < num_monsters and attempts < num_monsters * 10:
        attempts += 1
        x = random.randint(0, screen_width - monster_width)
        y = random.randint(0, screen_height - monster_height)

        new_monster = pygame.Rect(x, y, monster_width, monster_height)

        # 检查是否与已有的怪物、碎镜片或人物重叠
        if all(not new_monster.colliderect(existing_monster) for existing_monster in monsters) and \
           all(not new_monster.colliderect(shard) for shard in shards) and \
           all(not new_monster.colliderect(pygame.Rect(character.x, character.y, character.image.get_width(), character.image.get_height())) for character in characters):
            monsters.append(new_monster)

    return monsters, monster_image


def generate_monster_old2(pygame, num_monsters, screen_width, screen_height, shards, characters):
    """
    生成不与碎镜片和人物重叠的怪物，并返回它们的位置列表及其图像。
    """
    monster_image = pygame.image.load('images/monster.png')
    monster_image = pygame.transform.scale(monster_image, (100, 100))
    monster_width, monster_height = monster_image.get_width(), monster_image.get_height()

    monsters = []
    attempts = 0  # 用于限制尝试次数，防止无限循环

    while len(monsters) < num_monsters and attempts < num_monsters * 10:
        attempts += 1
        x = random.randint(0, screen_width - monster_width)
        y = random.randint(0, screen_height - monster_height)

        new_monster = pygame.Rect(x, y, monster_width, monster_height)

        # 检查是否与已有的怪物、碎镜片或人物重叠
        if all(not new_monster.colliderect(existing_monster) for existing_monster in monsters) and \
           all(not new_monster.colliderect(shard) for shard in shards) and \
           all(not new_monster.colliderect(character) for character in characters):
            monsters.append(new_monster)

    return monsters, monster_image


def generate_monster_old(pygame, num_monsters, screen_width, screen_height):
    """
    生成不重叠的怪物并返回它们的位置列表及其图像。
    """
    monster_image = pygame.image.load('images/monster.png')
    monster_image = pygame.transform.scale(monster_image, (100, 100))
    monster_width, monster_height = monster_image.get_width(), monster_image.get_height()

    monsters = []
    attempts = 0  # 用于限制尝试次数，防止无限循环

    while len(monsters) < num_monsters and attempts < num_monsters * 10:
        attempts += 1
        x = random.randint(0, screen_width - monster_width)
        y = random.randint(0, screen_height - monster_height)

        new_monster = pygame.Rect(x, y, monster_width, monster_height)

        if all(not new_monster.colliderect(existing_monster) for existing_monster in monsters):
            monsters.append(new_monster)

    return monsters, monster_image

def control_movement_old(keys, x, y, is_jumping, person_height, jump_velocity, person_name, person_speed, jump_speed, gravity, screen_height):
    """
    控制角色的移动、跳跃和快速下落
    """
    key_maps = {
        "mushicheng": {
            "move_left": pygame.K_a,
            "move_right": pygame.K_s,
            "jump": pygame.K_w,
            "fast_fall": pygame.K_z
        },
        "bailiu": {
            "move_left": pygame.K_k,
            "move_right": pygame.K_l,
            "jump": pygame.K_o,
            "fast_fall": pygame.K_m
        }
    }

    if person_name not in key_maps:
        raise ValueError("Unknown person_name: " + person_name)

    keys_map = key_maps[person_name]

    # Movement left and right
    if keys[keys_map["move_left"]]:
        x -= person_speed
    if keys[keys_map["move_right"]]:
        x += person_speed

    # Jump (ascending)
    if keys[keys_map["jump"]] and not is_jumping:
        is_jumping = True
        jump_velocity = jump_speed

    # Fast fall
    if keys[keys_map["fast_fall"]]:
        y += 35  # Fast fall, adjust the multiplier as needed

    # Handle jumping and gravity
    if is_jumping:
        y += jump_velocity
        jump_velocity += gravity
        if y >= screen_height // 2 - person_height // 2:
            y = screen_height // 2 - person_height // 2
            is_jumping = False

    # Prevent the character from falling below the screen
    if y > screen_height - person_height:
        y = screen_height - person_height

    return x, y, is_jumping, jump_velocity

def draw_text(screen, text_surfaces, is_mushicheng_turn, mushicheng_x, mushicheng_y, is_bailiu_turn, bailiu_x, bailiu_y, person_width, person_height, max_text_width):
    """
    在屏幕上绘制文本。
    """
    if text_surfaces:
        if is_mushicheng_turn:
            text_x = mushicheng_x + (person_width - max_text_width) // 2
            text_y = mushicheng_y - sum(surf.get_height() for surf in text_surfaces) + person_height + 3
        elif is_bailiu_turn:
            text_x = bailiu_x + (person_width - max_text_width) // 2
            text_y = bailiu_y - sum(surf.get_height() for surf in text_surfaces) - 20
        else:
            text_x = max_text_width // 2
            text_y = sum(surf.get_height() for surf in text_surfaces) - 20

        for i, text_surface in enumerate(text_surfaces):
            screen.blit(text_surface, (text_x, text_y + i * text_surface.get_height()))

def check_collision(rect1, rect2):
    """
    检查两个矩形是否发生碰撞。
    """
    return rect1.colliderect(rect2)
def remove_shared(collected_shards, shards, shard_image, mushicheng, bailiu):
    """
    检测角色与碎镜片的碰撞，移除已收集的碎镜片。
    """
    for shard in shards[:]:
        shard_rect = pygame.Rect(shard.topleft, (shard.width, shard.height))
        mushicheng_rect = pygame.Rect(mushicheng.x, mushicheng.y, mushicheng.image.get_width(), mushicheng.image.get_height())
        bailiu_rect = pygame.Rect(bailiu.x, bailiu.y, bailiu.image.get_width(), bailiu.image.get_height())

        if check_collision(shard_rect, mushicheng_rect) or check_collision(shard_rect, bailiu_rect):
            shards.remove(shard)
            collected_shards += 1
    return collected_shards

def remove_shared_old(collected_shards, shards, shard_image, mushicheng_x, mushicheng_y, bailiu_x, bailiu_y, person_mushicheng,person_bailiu):
    """
    检测角色与碎镜片的碰撞，移除已收集的碎镜片。
    """
    for shard in shards[:]:
        shard_rect = pygame.Rect(shard.topleft, (shard.width, shard.height))
        mushicheng_rect = pygame.Rect(mushicheng_x, mushicheng_y, person_mushicheng.get_width(), person_mushicheng.get_height())
        bailiu_rect = pygame.Rect(bailiu_x, bailiu_y, person_bailiu.get_width(), person_bailiu.get_height())

        if check_collision(shard_rect, mushicheng_rect) or check_collision(shard_rect, bailiu_rect):
            shards.remove(shard)
            collected_shards += 1
    return collected_shards


def check_collision_with_monsters(mushicheng_x, mushicheng_y, bailiu_x, bailiu_y, monsters):
    """
    检测人物是否与怪物发生碰撞。
    """
    mushicheng_rect = pygame.Rect(mushicheng_x, mushicheng_y, 100, 100)
    bailiu_rect = pygame.Rect(bailiu_x, bailiu_y, 100, 100)

    for monster in monsters:
        if mushicheng_rect.colliderect(monster) or bailiu_rect.colliderect(monster):
            return True

    return False


# 随机生成镜子的位置，确保它不与角色重叠
def generate_random_mirror_position(characters, mirror_size, screen_width, screen_height):
    while True:
        x = random.randint(0, screen_width - mirror_size[0])
        y = random.randint(0, screen_height - mirror_size[1])
        mirror_rect = pygame.Rect(x, y, mirror_size[0], mirror_size[1])

        # 检查是否与任何角色重叠
        overlap = False
        for character in characters:
            if mirror_rect.colliderect(
                    pygame.Rect(character.x, character.y, character.image.get_width(), character.image.get_height())):
                overlap = True
                break

        if not overlap:
            return x, y

BLACK = (0, 0, 0)
# 在屏幕上绘制文本的函数
def draw_text(surface, text, position, font, color=BLACK):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)


# 处理对话的函数
def handle_dialogue(event, current_dialogue_index, dialogues):
    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        current_dialogue_index += 1
    return current_dialogue_index