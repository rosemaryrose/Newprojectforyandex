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

    while True:
        key = pygame.key.get_pressed()
        hero.flip_picture('hero1')

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
                print(level.doors)
                print(get_cell((hero.pos_x, hero.pos_y)))

            if event.type == pygame.QUIT:
                terminate()

        hero_cell = get_cell((hero.pos_x + (tile_width - hero.width) // 2 + hero.width // 2,
                              hero.pos_y + tile_height - hero.height // 2))

        if hero.in_cell(level_map) == '0':
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

        level.level_render_prepare()

        screen.fill((0, 0, 0))
        level.sprite_group.draw(screen)
        other_group.draw(screen)
        hero.sprite_group.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)
