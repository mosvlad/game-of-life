import pygame

SCREEN_W = 800
SCREEN_H = 800
FIELD_SIZE = 100
CELL_SIZE_X = SCREEN_W / FIELD_SIZE
CELL_SIZE_Y = SCREEN_H / FIELD_SIZE

B = 3
S1 = 2
S2 = 3


def draw_grid(screen, n):
    for i in range(n):
        for j in range(n):
            pygame.draw.line(screen, (0, 0, 0), (i * SCREEN_H / n, j), (i * SCREEN_H / n, SCREEN_W))
            pygame.draw.line(screen, (0, 0, 0), (i, j * SCREEN_W / n), (SCREEN_H, j * SCREEN_W / n))


def draw_cells(screen, cells):
    for x in range(len(cells)):
        for y in range(len(cells[x])):
            if cells[x][y]:
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(y * SCREEN_W / FIELD_SIZE,
                                                                x * SCREEN_H / FIELD_SIZE,
                                                                CELL_SIZE_X,
                                                                CELL_SIZE_Y))


def get_cell_by_position(pos):
    x = int(pos[1] / CELL_SIZE_X)
    y = int(pos[0] / CELL_SIZE_Y)

    return x,y


def create_cells(n):
    field = []
    for i in range(n):
        tmp = []
        for j in range(n):
            tmp.append(False)
        field.append(tmp)
    return field


#в пустой (мёртвой) клетке, с которой соседствуют три живые клетки, зарождается жизнь;
#если у живой клетки есть две или три живые соседки, то эта клетка продолжает жить;
#в противном случае (если живых соседей меньше двух или больше трёх) клетка умирает
#(«от одиночества» или «от перенаселённости»).


def get_cell_neigbours_count(cells, x, y):
    neighbours_counter = 0
    if x + 1 < FIELD_SIZE and cells[x + 1][y]: neighbours_counter += 1
    if x - 1 >= 0 and cells[x - 1][y]: neighbours_counter += 1
    if y + 1 < FIELD_SIZE and cells[x][y + 1]: neighbours_counter += 1
    if y - 1 >= 0 and cells[x][y - 1]: neighbours_counter += 1

    if x + 1 < FIELD_SIZE and y + 1 < FIELD_SIZE and cells[x + 1][y + 1]: neighbours_counter += 1
    if x - 1 >= 0 and y - 1 >= 0 and cells[x - 1][y - 1]: neighbours_counter += 1
    if x - 1 >= 0 and y + 1 < FIELD_SIZE and cells[x - 1][y + 1]: neighbours_counter += 1
    if x + 1 < FIELD_SIZE and y - 1 >= 0 and cells[x + 1][y - 1]: neighbours_counter += 1

    return neighbours_counter


def update_cells(cells):
    new_cells = create_cells(FIELD_SIZE)
    for x in range(len(cells)):
        for y in range(len(cells[x])):
            neighbours = get_cell_neigbours_count(cells, x, y)
            if cells[x][y]:
                if neighbours < S1 or neighbours > S2:
                    new_cells[x][y] = False
                else:
                    new_cells[x][y] = True
            if not cells[x][y]:
                if neighbours == B:
                    new_cells[x][y] = True
    return new_cells


pygame.init()

screen = pygame.display.set_mode([SCREEN_W, SCREEN_H])
cells = create_cells(FIELD_SIZE)


run = True
pause = True
draw_flag = False
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            pause = not pause
        if event.type == pygame.MOUSEBUTTONDOWN:
            draw_flag = True
            pos = pygame.mouse.get_pos()
            x, y = get_cell_by_position(pos)
            cells[x][y] = True
        if event.type == pygame.MOUSEBUTTONUP:
            draw_flag = False
        if event.type == pygame.MOUSEMOTION:
            if draw_flag:
                pos = pygame.mouse.get_pos()

                x,y = get_cell_by_position(pos)
                cells[x][y] = True


    screen.fill((255, 255, 255))

    draw_grid(screen, FIELD_SIZE)
    if not pause:
        cells = update_cells(cells)
        pygame.time.wait(1)
    draw_cells(screen, cells)

    pygame.display.flip()

pygame.quit()
