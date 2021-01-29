from classes import *

clock = pygame.time.Clock()

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('caption')

    screen = pygame.display.set_mode(display_size)

    start_screen()  # заставка

    h = Hero('hero', 0, 0)
    player_group.add(h)

    level = get_level()
    while True:
        key = pygame.key.get_pressed()

        if key[pygame.K_w]:
            h.pos_y += speed

        if key[pygame.K_a]:
            h.pos_x += speed

        if key[pygame.K_s]:
            h.pos_y -= speed

        if key[pygame.K_d]:
            h.pos_x -= speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        level_render_prepare(h.pos_x, h.pos_y)

        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        other_group.draw(screen)
        player_group.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)
