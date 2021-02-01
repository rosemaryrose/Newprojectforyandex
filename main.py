from classes import *

clock = pygame.time.Clock()

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Treasure in Hue')

    screen = pygame.display.set_mode(display_size)

    start_screen(screen, clock)  # заставка

    level = Level('level1')
    level_map = level.get_level_map()

    hero = Hero(level.spawn_point[0] * tile_width, level.spawn_point[1] * tile_height)

    mini_game_flag_event = True
    end_flag_event = True
    end = True
    while True:
        key = pygame.key.get_pressed()
        hero.flip_picture('hero1')

        other_group.empty()

        if key[pygame.K_w]:
            if hero.can_go_way(level_map, 'w'):
                hero.flip_picture('hero4')
                level.move(0, speed)
                hero.pos_y -= speed

        if key[pygame.K_a]:
            if hero.can_go_way(level_map, 'a'):
                hero.flip_picture('hero2')
                level.move(speed, 0)
                hero.pos_x -= speed

        if key[pygame.K_s]:
            if hero.can_go_way(level_map, 's'):
                hero.flip_picture('hero1')
                level.move(0, -speed)
                hero.pos_y += speed

        if key[pygame.K_d]:
            if hero.can_go_way(level_map, 'd'):
                hero.flip_picture('hero3')
                level.move(-speed, 0)
                hero.pos_x += speed

        for event in pygame.event.get():
            if key[pygame.K_t]:
                print(mini_game_flag_event)

            if event.type == pygame.QUIT:
                terminate()

        hero_cell = get_cell((hero.pos_x + (tile_width - hero.width) // 2 + hero.width // 2,
                              hero.pos_y + tile_height - hero.height // 2))

        if hero.in_cell(level_map) == '!':
            end_screen(screen, clock)
        elif hero.in_cell(level_map) == '*' and end_game_flag_event and end:
            if cryst_collected == 36:
                res = os.system('final_game.py')

                if res == 1:
                    x = level.doors[str(hero_cell)][0][0]
                    y = level.doors[str(hero_cell)][0][1]

                    level = Level(level.doors[str(hero_cell)][1], spawn_point=[x, y])
                    level_map = level.get_level_map()

                    hero = Hero(x * tile_width, y * tile_height)
                    hero.sprite_group.empty()
                    hero.sprite_group.add(hero)

                    level.level_render_prepare()
                    screen.fill((0, 0, 0))
                    level.sprite_group.draw(screen)
                    hero.sprite_group.draw(screen)
                    other_group.draw(screen)
                    pygame.display.flip()

                    end = False
                if res == 0:
                    end_game_flag_event = False
        elif hero.in_cell(level_map) == '0':
            res = level.doors[str(hero_cell)][1]

            if res == 'exit':
                terminate()

            x = level.doors[str(hero_cell)][0][0]
            y = level.doors[str(hero_cell)][0][1]

            level = Level(level.doors[str(hero_cell)][1], spawn_point=[x, y])
            level_map = level.get_level_map()

            hero = Hero(x * tile_width, y * tile_height)
            hero.sprite_group.empty()
            hero.sprite_group.add(hero)
        elif hero.in_cell(level_map) == 'x' and mini_game_flag_event:
            res = 0
            game = ''

            if [hero_cell, level.level_name] not in played_game:
                game = random.choice(game_list)
                res = os.system(game)

            if res == 1:
                cryst_collected += 12
                del game_list[game_list.index(game)]
                played_game.append([hero_cell, level.level_name])
            elif res == 0:
                mini_game_flag_event = False
        else:
            if hero.in_cell(level_map) != 'x':
                mini_game_flag_event = True
            if hero.in_cell(level_map) != '*':
                end_game_flag_event = True

        level.level_render_prepare()

        screen.fill((0, 0, 0))
        level.sprite_group.draw(screen)
        hero.sprite_group.draw(screen)
        other_group.draw(screen)

        font = pygame.font.Font('data/na-vyrost.ttf', 15)
        font1 = pygame.font.Font('data/na-vyrost.ttf', 15)
        string_rendered = font.render('Collected crystals: ' + str(cryst_collected), 1, pygame.Color('White'))
        string_rendered2 = font1.render('Collected crystals: ' + str(cryst_collected), 1, pygame.Color('Black'))
        string_rendered1 = font.render('HP: ' + str(hp), 1, pygame.Color('White'))
        string_rendered12 = font.render('HP: ' + str(hp), 1, pygame.Color('Black'))
        intro_rect = string_rendered.get_rect()
        intro_rect1 = string_rendered.get_rect()
        intro_rect2 = string_rendered.get_rect()
        intro_rect21 = string_rendered.get_rect()

        intro_rect.top = 40
        intro_rect.x = 10
        intro_rect2.top = 42
        intro_rect2.x = 12

        intro_rect1.top = 10
        intro_rect1.x = 10
        intro_rect21.top = 12
        intro_rect21.x = 12

        screen.blit(string_rendered2, intro_rect2)
        screen.blit(string_rendered, intro_rect)
        screen.blit(string_rendered12, intro_rect21)
        screen.blit(string_rendered1, intro_rect1)

        pygame.display.flip()
        clock.tick(FPS)
