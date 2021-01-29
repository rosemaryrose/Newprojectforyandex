from classes import *

clock = pygame.time.Clock()

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('caption')

    screen = pygame.display.set_mode(display_size)

    start_screen()  # заставка
    level_render('level1')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        tiles_group.draw(screen)
        other_group.draw(screen)
        player_group.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)
