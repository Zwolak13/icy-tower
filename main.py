import pygame

from game import fonts as fonts_module
from game.game import Game
from game.constants import FPS, TITLE, PLAY, DEAD


def main():
    pygame.init()
    screen   = pygame.display.set_mode((400, 600))
    pygame.display.set_caption('Icy Tower')
    clock    = pygame.time.Clock()
    fonts    = fonts_module.create()
    game     = Game(fonts)
    jump_now = False

    while True:
        jump_now = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if game.state == DEAD:
                    if event.key == pygame.K_RETURN:
                        if game.name_in.strip():
                            game.submit_score()
                    elif event.key == pygame.K_BACKSPACE:
                        game.name_in = game.name_in[:-1]
                    elif event.unicode and event.unicode.isprintable() and len(game.name_in) < 14:
                        game.name_in += event.unicode.upper()

                elif game.state == TITLE:
                    if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                        game.start()

                elif game.state == PLAY:
                    if event.key in (pygame.K_UP, pygame.K_SPACE, pygame.K_w):
                        jump_now = True

        pressed = pygame.key.get_pressed()
        game.update(pressed, jump_now)
        game.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
