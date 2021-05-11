import pygame
from nq1 import NQ

n = 0

def draw_board(the_board):
    pygame.init()
    colors = [(112,128,144), (47,79,79)]

    surface_sz = 480
    sq_sz = surface_sz // n
    surface_sz = n * sq_sz

    surface = pygame.display.set_mode((surface_sz, surface_sz))

    ball = pygame.image.load("queen.png")

    ball_offset = (sq_sz - ball.get_width()) // 2
    mainloop = True
    while mainloop:

        ev = pygame.event.poll()
        if ev.type == pygame.QUIT:
            break;

        for row in range(n):
            c_indx = row % 2
            for col in range(n):
                the_square = (col * sq_sz, row * sq_sz, sq_sz, sq_sz)
                surface.fill(colors[c_indx], the_square)

                c_indx = (c_indx + 1) % 2

        for (col, row) in enumerate(the_board):
            surface.blit(ball,
                         (col * sq_sz + ball_offset, row * sq_sz + ball_offset))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    mainloop = False

        pygame.display.flip()

    pygame.quit()


def show_columns(x):
    print("columns: {} ".format(x))
    if len(x) != 0:
        draw_board(x)


def process(n):
    nqueens = NQ(n, show_columns)
    nqueens.place(0)
    return nqueens.columns


if __name__ == "__main__":
    n = int(input("Enter the size of chess board\n"))
    process(n)