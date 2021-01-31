from classes import *

clock = pygame.time.Clock()

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('caption')

    screen = pygame.display.set_mode(display_size)

    start_screen()  # заставка

    level = Level('level1')
    level_map = level.get_level_map()

    hero = Hero(level.spawn_point[0] * tile_width, level.spawn_point[1] * tile_height)
    player_group.add(hero)

    while True:
        key = pygame.key.get_pressed()

        if key[pygame.K_w]:
            if hero.can_go_way(level_map, 'w'):
                level.move(0, speed)
                hero.pos_y -= speed

        if key[pygame.K_a]:
            if hero.can_go_way(level_map, 'a'):
                level.move(speed, 0)
                hero.pos_x -= speed

        if key[pygame.K_s]:
            if hero.can_go_way(level_map, 's'):
                level.move(0, -speed)
                hero.pos_y += speed

        if key[pygame.K_d]:
            if hero.can_go_way(level_map, 'd'):
                level.move(-speed, 0)
                hero.pos_x += speed

        for event in pygame.event.get():
            if key[pygame.K_t]:
                print(level.doors)

            if event.type == pygame.QUIT:
                terminate()

        hero_cell = get_cell((hero.pos_x + (tile_width - hero.width) // 2 + hero.width // 2,
                              hero.pos_y + tile_height - hero.height // 2))

        if hero.in_cell(level_map) == '0':
            x = level.doors[str(hero_cell)][0][0]
            y = level.doors[str(hero_cell)][0][1]

            level = Level(level.doors[str(hero_cell)][1], spawn_point=[x, y])
            level_map = level.get_level_map()

            hero = Hero(x * tile_width, y * tile_height)
            player_group.empty()
            player_group.add(hero)

        level.level_render_prepare()

        screen.fill((0, 0, 0))
        level.sprite_group.draw(screen)
        other_group.draw(screen)
        player_group.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)
