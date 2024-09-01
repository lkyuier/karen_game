import pygame


class Character:
    def __init__(self, name, image_path, start_x, start_y, screen_width, screen_height):
        self.name = name
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (150, 150))  # Adjust size as needed
        self.x = start_x
        self.y = start_y
        self.is_jumping = False
        self.jump_velocity = 0
        self.is_turn = False
        self.screen_width = screen_width
        self.screen_height = screen_height

    def control_movement(self, keys, person_speed, jump_speed, gravity):
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

        if self.name not in key_maps:
            raise ValueError(f"Unknown character name: {self.name}")

        keys_map = key_maps[self.name]

        # Handle horizontal movement
        if keys[keys_map["move_left"]]:
            self.x -= person_speed
        if keys[keys_map["move_right"]]:
            self.x += person_speed

        # Handle jumping and gravity
        if keys[keys_map["jump"]] and not self.is_jumping:
            self.is_jumping = True
            self.jump_velocity = jump_speed

        if self.is_jumping:
            self.y += self.jump_velocity
            self.jump_velocity += gravity
            if self.y >= self.screen_height // 2 - self.image.get_height() // 2:
                self.y = self.screen_height // 2 - self.image.get_height() // 2
                self.is_jumping = False

        # Handle fast fall
        if keys[keys_map["fast_fall"]]:
            self.y += 35  # Fast fall speed

        # Prevent the character from falling below the screen
        if self.y > self.screen_height - self.image.get_height():
            self.y = self.screen_height - self.image.get_height()