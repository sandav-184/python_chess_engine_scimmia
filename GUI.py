from board import GameState
import pygame

# Gui variables
BORDER_WIDTH = 0
TILE_SIZE = 80
WINDOW_WIDTH, WINDOW_HEIGHT = 8 * TILE_SIZE + BORDER_WIDTH, 8 * TILE_SIZE + BORDER_WIDTH
ROWS, COLUMNS = 8, 8

# Color palette
BLACK_TILE_COLOR = (181, 136, 99)
WHITE_TILE_COLOR = (240, 217, 181)
WHITE_PIECE_COLOR = (255, 255, 255)
BLACK_PIECE_COLOR = (0, 0, 0)
HIGHLIGHT_COLOR = (246, 246, 105, 100)



# Pieces
PIECE_SYMBOLS = {1: "♟", 2: "♝", 3: "♞", 4: "♜", 5: "♛", 6: "♚"} #unicode


# Pygame initialization
pygame.init()
font = pygame.font.SysFont("applesymbols,segoeuisymbol,dejavusans,freeserif", 60)  # sceglie il primo tra i font che trova, linux inclus perchè kanga è un goy
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Python_Chess_V1")

#highlight square surface
HIGHLIGHT_SURFACE = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
HIGHLIGHT_SURFACE.fill(HIGHLIGHT_COLOR)


def make_piece_surface(symbol, fill, outline):   #  mette un outline e colora i pezzi
    """surf è un rettangolo transparente su cui puoi disegnare e che poi copierò su screen,
    partendo da in alto a sinistra disegno il pezzo nel colore dell'outline 9 volte con un po' di offset, e poi ci metto il pezzo
    nel colore del fill sopra, così ho fatto l'immagine del pezzo"""
    text = font.render(symbol, True, fill)         #fai 2 volte, una per l'outline e una per linterno, poi metto outline più grande del centro
    border = font.render(symbol, True, outline)     #True/False è l'anti alyasing
    w, h = text.get_size()
    surf = pygame.Surface((w+4, h+4), pygame.SRCALPHA)
    for dx in(0, 2, 4):
        for dy in(0, 2, 4):
            surf.blit(border, (dx, dy))
    surf.blit(text, (2, 2))
    return surf
    


def generate_pieces():
    piece_surfaces = {}
    for value, symbol in PIECE_SYMBOLS.items():
        piece_surfaces[value] = make_piece_surface(symbol, WHITE_PIECE_COLOR, BLACK_PIECE_COLOR)
        piece_surfaces[-value] = make_piece_surface(symbol, BLACK_PIECE_COLOR, WHITE_PIECE_COLOR)
    return piece_surfaces

def click_square(pos):
    mouse_x, mouse_y = pos
    clicked_square = (mouse_y//TILE_SIZE, mouse_x//TILE_SIZE)
    return clicked_square
    
def draw_highlight(selected_square, possible_moves):

    
    if selected_square is None:
        return
    row,col = selected_square
    screen.blit(HIGHLIGHT_SURFACE, (col*TILE_SIZE, row*TILE_SIZE))

    for square in possible_moves:
        m_row, m_col = square
        screen.blit(HIGHLIGHT_SURFACE, (m_col*TILE_SIZE, m_row*TILE_SIZE))
    
    
def draw_board():
    for row in range(ROWS):
        for col in range(COLUMNS):
            tile_color = WHITE_TILE_COLOR if (col + row) % 2 == 0 else BLACK_TILE_COLOR
            pygame.draw.rect(screen, tile_color, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def draw_pieces(piece_surfaces, board):
    for row in range(ROWS):
        for col in range(COLUMNS):
            piece = board[row][col]
            if piece != 0:
                surf = piece_surfaces[piece]
                rect = surf.get_rect(center=(col*TILE_SIZE+TILE_SIZE//2, row*TILE_SIZE+TILE_SIZE//2)) #dove posizionare il pezzo, uso il centro per facilità
                screen.blit(surf, rect)


def main():
    state = GameState()
    selected_square = None
    piece_surfaces = generate_pieces()
    
    
    running = True
    while running:
        for event in pygame.event.get():
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    
                    clicked = click_square(event.pos)
                    if selected_square is None:
                        if state.is_own_piece(clicked):
                            selected_square = clicked
                    else:
                        if clicked == selected_square:
                            selected_square = None
                        elif state.is_own_piece(clicked):
                            selected_square = clicked
                        else:
                            if state.move_piece(selected_square, clicked):
                                selected_square = None
                        
            if event.type == pygame.QUIT:
                running = False

        draw_board()
        draw_highlight(selected_square, state.get_moves(selected_square))
        draw_pieces(piece_surfaces, state.board)
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
    
    
