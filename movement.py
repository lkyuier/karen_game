import pygame


def control_movement(keys, x, y, is_jumping, person_height, jump_velocity, person_name, person_speed, jump_speed, gravity, screen_height, fast_fall_speed=35):
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
        raise ValueError(f"Unknown person_name: {person_name}")

    keys_map = key_maps[person_name]

    # Handle horizontal movement
    x = handle_horizontal_movement(keys, keys_map, x, person_speed)

    # Handle jumping and gravity
    y, is_jumping, jump_velocity = handle_jumping_and_gravity(
        keys, keys_map, y, is_jumping, jump_velocity, person_height, jump_speed, gravity, screen_height
    )

    # Handle fast fall
    y = handle_fast_fall(keys, keys_map, y, fast_fall_speed, screen_height, person_height)

    return x, y, is_jumping, jump_velocity

def handle_horizontal_movement(keys, keys_map, x, person_speed):
    """处理水平移动"""
    if keys[keys_map["move_left"]]:
        x -= person_speed
    if keys[keys_map["move_right"]]:
        x += person_speed
    return x

def handle_jumping_and_gravity(keys, keys_map, y, is_jumping, jump_velocity, person_height, jump_speed, gravity, screen_height):
    """处理跳跃和重力"""
    if keys[keys_map["jump"]] and not is_jumping:
        is_jumping = True
        jump_velocity = jump_speed

    if is_jumping:
        y += jump_velocity
        jump_velocity += gravity
        if y >= screen_height // 2 - person_height // 2:
            y = screen_height // 2 - person_height // 2
            is_jumping = False

    return y, is_jumping, jump_velocity

def handle_fast_fall(keys, keys_map, y, fast_fall_speed, screen_height, person_height):
    """处理快速下落"""
    if keys[keys_map["fast_fall"]]:
        y += fast_fall_speed
    y = min(y, screen_height - person_height)  # 防止人物掉出屏幕
    return y
