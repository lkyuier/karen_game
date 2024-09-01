import random
import pygame
import sys
from Character import Character
from commons import generate_shards, create_checkerboard, remove_shared, check_collision_with_monsters
from movement import control_movement

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
MIRROR_SIZE = (200, 200)
MIRROR_MOVE_INTERVAL = 3000  # 3 seconds in milliseconds
BLACK = (0, 0, 0)
TILE_SIZE = 50

def draw_text(surface, text, position, font, color=BLACK):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)

def handle_dialogue(event, current_dialogue_index, dialogues):
    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        current_dialogue_index += 1
    return current_dialogue_index

def generate_random_mirror_position(characters, mirror_size, screen_width, screen_height):
    while True:
        x = random.randint(0, screen_width - mirror_size[0])
        y = random.randint(0, screen_height - mirror_size[1])
        mirror_rect = pygame.Rect(x, y, mirror_size[0], mirror_size[1])

        overlap = False
        for character in characters:
            if mirror_rect.colliderect(
                    pygame.Rect(character.x, character.y, character.image.get_width(), character.image.get_height())):
                overlap = True
                break

        if not overlap:
            return x, y

def main():
    pygame.init()
    font = pygame.font.Font(None, 18)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    background = create_checkerboard(pygame, SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE=50)

    shards, shard_image = generate_shards(pygame, 30, SCREEN_WIDTH, SCREEN_HEIGHT)

    person_mushicheng = Character("mushicheng", 'assets/images/mushichen.png', SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 50,
                                  SCREEN_WIDTH, SCREEN_HEIGHT)
    person_bailiu = Character("bailiu", 'assets/images/bailiu.png', SCREEN_WIDTH // 4 + 50, SCREEN_HEIGHT // 2 + 10,
                              SCREEN_WIDTH, SCREEN_HEIGHT)

    mirror_image = pygame.image.load('assets/images/mirror.png')
    mirror_image = pygame.transform.scale(mirror_image, MIRROR_SIZE)

    characters = [person_mushicheng, person_bailiu]
    mirror_position = generate_random_mirror_position(characters, MIRROR_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT)
    last_mirror_move_time = pygame.time.get_ticks()
    mirror_health = 15
    current_dialog_index = 0
    collected_shards = 0
    total_shards = len(shards)
    score = 0
    dialogue_finished = False

    monsters, monster_image = generate_monster(pygame, 1, SCREEN_WIDTH, SCREEN_HEIGHT, shards, characters)

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

        person_mushicheng.control_movement(keys, 3, -15, 0.5)
        person_bailiu.control_movement(keys, 3, -15, 0.5)

        previous_collected_shards = collected_shards
        collected_shards = remove_shared(collected_shards, shards, shard_image, person_mushicheng, person_bailiu)

        if collected_shards > previous_collected_shards:
            score += 1

        if collected_shards == total_shards:
            current_dialog_index = 0
            collected_shards = 0
            DIALOGS_ALL_CONTENT = DIALOGS_AFTER_SHARDS
            dialogue_finished = False

        if check_collision_with_monsters(person_mushicheng.x, person_mushicheng.y, person_bailiu.x, person_bailiu.y,
                                         monsters):
            main()
            return

        mirror_rect = pygame.Rect(mirror_position[0], mirror_position[1], MIRROR_SIZE[0], MIRROR_SIZE[1])
        for character in characters:
            character_rect = pygame.Rect(character.x, character.y, character.image.get_width(),
                                         character.image.get_height())
            if mirror_rect.colliderect(character_rect):
                mirror_health -= 1
                mirror_position = generate_random_mirror_position(characters, MIRROR_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT)
                break

        if mirror_health <= 0 and DIALOGS_ALL_CONTENT != DIALOGS_AFTER_MIRROR:
            DIALOGS_ALL_CONTENT = DIALOGS_AFTER_MIRROR
            current_dialog_index = 0
            dialogue_finished = False

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
        dialogue_text = DIALOGS_ALL_CONTENT[current_dialog_index]
        dialogue_text = dialogue_text.split(":")[-1].strip()
        draw_text(screen, dialogue_text, (50, 50), font, BLACK)
    else:
        screen.blit(mirror_image, mirror_position)

    draw_text(screen, f"Mirror Health: {mirror_health}", (10, 10), font, BLACK)
    draw_text(screen, f"Score: {score}", (SCREEN_WIDTH - 120, 10), font, BLACK)

    pygame.display.flip()

if __name__ == "__main__":
    main()
