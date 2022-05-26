import pygame      #line 10 - line 94 Dim
                   #line 97 - line 197 Mal
import time        #line 272 - line 350 Por
import easygui
import sys

board = [['  ' for i in range(8)] for i in range(8)]


class Piece:
    def __init__(self, team, type, image, killable=False):
        self.team = team
        self.type = type
        self.killable = killable
        self.image = image


def create_board(board):
    for i in range(8):
        for j in range(8):
            board[i][j] = "  "

    board[0] = [Piece('b', 'r', 'b_rook.png'), Piece('b', 'kn', 'b_knight.png'), Piece('b', 'b', 'b_bishop.png'), \
               Piece('b', 'q', 'b_queen.png'), Piece('b', 'k', 'b_king.png'), Piece('b', 'b', 'b_bishop.png'), \
               Piece('b', 'kn', 'b_knight.png'), Piece('b', 'r', 'b_rook.png')]

    board[7] = [Piece('w', 'r', 'w_rook.png'), Piece('w', 'kn', 'w_knight.png'), Piece('w', 'b', 'w_bishop.png'), \
               Piece('w', 'q', 'w_queen.png'), Piece('w', 'k', 'w_king.png'), Piece('w', 'b', 'w_bishop.png'), \
               Piece('w', 'kn', 'w_knight.png'), Piece('w', 'r', 'w_rook.png')]

    for i in range(8):
        board[1][i] = Piece('b', 'p', 'b_pawn.png')
        board[6][i] = Piece('w', 'p', 'w_pawn.png')
    return board



def on_board(position):
    if position[0] > -1 and position[1] > -1 and position[0] < 8 and position[1] < 8:
        return True



def convert_to_readable(board):
    output = ''

    for i in board:
        for j in i:
            try:
                output += j.team + j.type + ', '
            except:
                output += j + ', '
        output += '\n'
    return output

########################################################################################################################


def deselect():
    for row in range(len(board)):
        for column in range(len(board[0])):
            if board[row][column] == 'x ':
                board[row][column] = '  '
            else:
                try:
                    board[row][column].killable = False
                except:
                    pass
    return convert_to_readable(board)



def highlight(board):
    highlighted = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 'x ':
                highlighted.append((i, j))
            else:
                try:
                    if board[i][j].killable:
                        highlighted.append((i, j))
                except:
                    pass
    return highlighted

def check_team(moves, index):
    row, col = index
    if moves%2 == 0:
        if board[row][col].team == 'w':
            return True
    else:
        if board[row][col].team == 'b':
            return True

def threat_map(color):
    threat_map = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            piece = board[i][j]
            if piece != "x " and piece != "  "  and piece.team != color:
                if piece.type == 'p':
                    if piece.team == 'b':
                        threat_map.extend(highlight(pawn_moves_b((i,j))))
                        deselect()
                        remove_highlight(grid)
                    else:
                        threat_map.extend(highlight(pawn_moves_w((i,j))))
                        deselect()
                        remove_highlight(grid)

                if piece.type == 'k':
                    threat_map.extend(highlight(king_moves((i,j))))
                    deselect()
                    remove_highlight(grid)

                if piece.type == 'r':
                    threat_map.extend(highlight(rook_moves((i,j))))
                    deselect()
                    remove_highlight(grid)

                if piece.type == 'b':
                    threat_map.extend(highlight(bishop_moves((i,j))))
                    deselect()
                    remove_highlight(grid)

                if piece.type == 'q':
                    threat_map.extend(highlight(queen_moves((i,j))))
                    deselect()
                    remove_highlight(grid)

                if piece.type == 'kn':
                    threat_map.extend(highlight(knight_moves((i,j))))
                    deselect()
                    remove_highlight(grid)

    return threat_map

def message(msg):
    font = pygame.font.SysFont(None, 50)
    text = font.render(msg,True,RED,BLACK)
    textrect = text.get_rect()
    textrect.center = (400,400)
    x = True
    while x :
        global WIN
        WIN.blit(text,textrect)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x = False
            pygame.display.update()

def button(screen,position,text):
    font = pygame.font.SysFont(None, 30)
    buttontext = font.render(text,True,WHITE)
    x,y = position
    pygame.draw.rect(screen,RED,[x,y,400,50])
    textrect = buttontext.get_rect()
    textrect.center = ((x+400/2),(y+25))
    screen.blit(buttontext,textrect)



def buttonreset(screen,position):
    x,y = position
    pygame.draw.rect(screen,BLACK,[x,y,400,50])


def check_sax(color):
    for i in range(len(board)):
        for j in range(len(board[0])):
            piece = board[i][j]
            if piece != "x " and piece != "  "  and piece.team == color and piece.type == "k":
                threatmap = threat_map(color)
                print(threatmap)
                if ((i,j)) in threatmap:
                    print("King Sax")
                    pygame.mixer.Sound.play(king_treat)
                    message("THE KING IS UNDER THREAT")


def select_moves(piece, index, moves):
    if check_team(moves, index):

        check_sax(piece.team)

        if piece.type == 'p':
            if piece.team == 'b':
                return highlight(pawn_moves_b(index))
            else:
                return highlight(pawn_moves_w(index))

        if piece.type == 'k':
            return highlight(king_moves(index))

        if piece.type == 'r':
            return highlight(rook_moves(index))

        if piece.type == 'b':
            return highlight(bishop_moves(index))

        if piece.type == 'q':
            return highlight(queen_moves(index))

        if piece.type == 'kn':
            return highlight(knight_moves(index))

########################################################################################################################

def pawn_moves_b(index):
    if index[0] == 1:
        if board[index[0] + 2][index[1]] == '  ' and board[index[0] + 1][index[1]] == '  ':
            board[index[0] + 2][index[1]] = 'x '
    bottom3 = [[index[0] + 1, index[1] + i] for i in range(-1, 2)]

    for positions in bottom3:
        if on_board(positions):
            if bottom3.index(positions) % 2 == 0:
                try:
                    if board[positions[0]][positions[1]].team != 'b':
                        board[positions[0]][positions[1]].killable = True
                except:
                    pass
            else:
                if board[positions[0]][positions[1]] == '  ':
                    board[positions[0]][positions[1]] = 'x '    #
    return board

def pawn_moves_w(index):
    if index[0] == 6:
        if board[index[0] - 2][index[1]] == '  ' and board[index[0] - 1][index[1]] == '  ':
            board[index[0] - 2][index[1]] = 'x '
    top3 = [[index[0] - 1, index[1] + i] for i in range(-1, 2)]

    for positions in top3:
        if on_board(positions):
            if top3.index(positions) % 2 == 0:
                try:
                    if board[positions[0]][positions[1]].team != 'w':
                        board[positions[0]][positions[1]].killable = True
                except:
                    pass
            else:
                if board[positions[0]][positions[1]] == '  ':
                    board[positions[0]][positions[1]] = 'x '
    return board



def king_moves(index):
    for y in range(3):
        for x in range(3):
            if on_board((index[0] - 1 + y, index[1] - 1 + x)):
                if board[index[0] - 1 + y][index[1] - 1 + x] == '  ':
                    board[index[0] - 1 + y][index[1] - 1 + x] = 'x '
                else:
                    if board[index[0] - 1 + y][index[1] - 1 + x].team != board[index[0]][index[1]].team:
                        board[index[0] - 1 + y][index[1] - 1 + x].killable = True
    return board



def rook_moves(index):
    cross = [[[index[0] + i, index[1]] for i in range(1, 8 - index[0])],
             [[index[0] - i, index[1]] for i in range(1, index[0] + 1)],
             [[index[0], index[1] + i] for i in range(1, 8 - index[1])],
             [[index[0], index[1] - i] for i in range(1, index[1] + 1)]]

    for direction in cross:
        for positions in direction:
            if on_board(positions):
                if board[positions[0]][positions[1]] == '  ':
                    board[positions[0]][positions[1]] = 'x '
                else:
                    if board[positions[0]][positions[1]].team != board[index[0]][index[1]].team:
                        board[positions[0]][positions[1]].killable = True
                    break
    return board



def bishop_moves(index):
    diagonals = [[[index[0] + i, index[1] + i] for i in range(1, 8)],
                 [[index[0] + i, index[1] - i] for i in range(1, 8)],
                 [[index[0] - i, index[1] + i] for i in range(1, 8)],
                 [[index[0] - i, index[1] - i] for i in range(1, 8)]]

    for direction in diagonals:
        for positions in direction:
            if on_board(positions):
                if board[positions[0]][positions[1]] == '  ':
                    board[positions[0]][positions[1]] = 'x '
                else:
                    if board[positions[0]][positions[1]].team != board[index[0]][index[1]].team:
                        board[positions[0]][positions[1]].killable = True
                    break
    return board



def queen_moves(index):
    board = rook_moves(index)
    board = bishop_moves(index)
    return board



def knight_moves(index):
    for i in range(-2, 3):
        for j in range(-2, 3):
            if i ** 2 + j ** 2 == 5:
                if on_board((index[0] + i, index[1] + j)):
                    if board[index[0] + i][index[1] + j] == '  ':
                        board[index[0] + i][index[1] + j] = 'x '
                    else:
                        if board[index[0] + i][index[1] + j].team != board[index[0]][index[1]].team:
                            board[index[0] + i][index[1] + j].killable = True
    return board

########################################################################################################################
pygame.init()
WIDTH = 800
HEIGHT = 850
WIN = pygame.display.set_mode((WIDTH, HEIGHT))



pygame.display.set_caption("Chess")
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
YELLOW = (204, 204, 0)
BLUE = (50, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
################

Move_sound = pygame.mixer.Sound("chess_move.wav")
kill_sound = pygame.mixer.Sound("killpoints.wav")
king_treat = pygame.mixer.Sound("KING_threat.wav")
end_sound = pygame.mixer.Sound("applause.wav")
music = pygame.mixer.music.load("jazzy-vibes81.mp3")
pygame.mixer.music.play(-1)


################

class Node:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = int(col * width)
        self.y = int(row * width)
        self.colour = WHITE


    def draw(self, WIN):
        pygame.draw.rect(WIN, self.colour, (self.x, self.y, WIDTH / 8, WIDTH / 8))

    def setup(self, WIN):

        if isinstance(board[self.row][self.col], Piece):
            WIN.blit(pygame.image.load(board[self.row][self.col].image), (self.x + 20, self.y + 20))


def make_grid(rows, width):
    grid = []
    gap = WIDTH // rows

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap)
            grid[i].append(node)
            if (i+j)%2 ==1:
                grid[i][j].colour = GREY

    return grid


def update_bg(win, grid, rows, width):
    for row in grid:
        for spot in row:
            spot.draw(win)


    pygame.display.update()


def update_display(win, grid, rows, width):
    for row in grid:
        for spot in row:
            spot.draw(win)
            spot.setup(win)

    pygame.display.update()


def Find_Node(pos, WIDTH):
    interval = WIDTH / 8
    y, x = pos
    rows = y // interval
    columns = x // interval
    return int(rows), int(columns)


def display_potential_moves(positions, grid):
    for i in positions:
        x, y = i
        grid[x][y].colour = BLUE


def remove_highlight(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i+j)%2 == 0:
                grid[i][j].colour = WHITE
            else:
                grid[i][j].colour = GREY
    return grid

record_moves = []
def printAllMoves():
    fn = easygui.filesavebox("Save moves list", "Chess", "*.txt");
    if not fn:
        return
    f = open(fn, "w")
    for m in record_moves:
        tm = {
            "w": "White",
            "b": "Black"
        }
        tp = {
            "r": "Rook",
            "kn": "Knight",
            "b": "Bishop",
            "q": "Queen",
            "k": "King",
            "p": "Pawn"
        }
        hor = ['A','B','C','D','E','F','G','H'];
        print("{} {}, {}{} -> {}{}".format(tm[m[4]], tp[m[5]], hor[m[1]], 8 - m[0], hor[m[3]], 8 - m[2]))
        f.write("{} {}, {}{} -> {}{}\n".format(tm[m[4]], tp[m[5]], hor[m[1]], 8 - m[0], hor[m[3]], 8 - m[2]))
    f.write("\n\n")
    f.close()
    record_moves.clear()

def main(WIN, WIDTH):
    create_board(board)
    global savegame
    global rungame
    global record_moves
    savegame = False
    button(WIN, [0, 801], "RESTART")    ####### KOUMPI RESTART
    moves = 0
    selected = False
    piece_to_move = []
    global grid
    grid = make_grid(8, WIDTH)
    update_display(WIN, grid, 8, WIDTH)
    game = True
    while game:

        pygame.time.delay(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                pos = pygame.mouse.get_pos()
                bx, by = pos
                if (bx <= 400 and by > 800):
                    game = False
                    break
                y, x = Find_Node(pos, WIDTH)

                if selected == False:
                    try:
                        possible = select_moves((board[x][y]), (x, y), moves)
                        for positions in possible:
                            row, col = positions
                            grid[row][col].colour = BLUE
                        piece_to_move = x, y
                        selected = True
                    except:
                        piece_to_move = []
                        print('Can\'t select')


                else:
                    try:
                        if board[x][y].killable == True:
                            pygame.mixer.Sound.play(kill_sound)
                            row, col = piece_to_move
                            if board[x][y].type == "k":
                                print("CHECK MATE")

                                board[x][y] = board[row][col]
                                board[row][col] = '  '
                                deselect()
                                remove_highlight(grid)
                                moves += 1
                                print(convert_to_readable(board))
                                pygame.time.delay(50)
                                game = False
                                rungame = False
                                savegame = True
                                pygame.mixer.Sound.play(end_sound)
                                message("GAME OVER.THANK YOU FOR PLAYING")

                            board[x][y] = board[row][col]
                            board[row][col] = '  '
                            record_moves.append(
                                [row, col, x, y, board[x][y].team, board[x][y].type])
                            deselect()
                            remove_highlight(grid)

                            moves += 1
                            record_moves.append(
                                [row, col, x, y, board[x][y].team, board[x][y].type])
                            print(convert_to_readable(board))
                        else:
                            deselect()
                            remove_highlight(grid)
                            selected = False
                            print("Deselected")
                    except:
                        if board[x][y] == 'x ':
                            pygame.mixer.Sound.play(Move_sound)
                            row, col = piece_to_move
                            board[x][y] = board[row][col]
                            board[row][col] = '  '
                            deselect()
                            remove_highlight(grid)

                            moves += 1
                            print(convert_to_readable(board))
                        else:
                            deselect()
                            remove_highlight(grid)
                            selected = False
                            print("Invalid move")
                    selected = False

            update_display(WIN, grid, 8, WIDTH)





newgame = True
savegame = False
rungame = False
while newgame:
    global grid
    grid = make_grid(8, WIDTH)
    button(WIN, [0, 801], "START")
    if savegame == True:
        button(WIN, [401, 801], "SAVE PREVIOUS GAME")
    update_bg(WIN,grid,8,WIDTH)
    pygame.time.delay(50)
    bx = 0
    by = 0
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            bx,by = pygame.mouse.get_pos()
        if (bx <= 400 and by > 800):                 
            rungame = True
        if (bx >= 401 and bx <= 800 and by > 800):
            savegame = False
            buttonreset(WIN, [401, 801])
            printAllMoves()
        if  event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()




    while rungame == True:
        main(WIN, WIDTH)










