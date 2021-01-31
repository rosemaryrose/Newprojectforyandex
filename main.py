from classes import *

clock = pygame.time.Clock()

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('caption')

    screen = pygame.display.set_mode(display_size)

    start_screen()  # заставка

    level = Level('level1')
    level_map = level.get_level()

    hero = Hero(level.spawn_point[0] * tile_width, level.spawn_point[1] * tile_height)
    player_group.add(hero)

    while True:
        key = pygame.key.get_pressed()

        if key[pygame.K_w]:
            level.move(0, speed)
            hero.pos_y -= speed

        if key[pygame.K_a]:
            level.move(speed, 0)
            hero.pos_x -= speed

        if key[pygame.K_s]:
            level.move(0, -speed)
            hero.pos_x += speed

        if key[pygame.K_d]:
            level.move(-speed, 0)
            hero.pos_y += speed

        for event in pygame.event.get():
            if key[pygame.K_t]:
                print(str(hero.pos_x) + '  ' + str(hero.pos_y))

            if event.type == pygame.QUIT:
                terminate()

        level.level_render_prepare()

        screen.fill((0, 0, 0))
        level.sprite_group.draw(screen)
        other_group.draw(screen)
        player_group.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)
