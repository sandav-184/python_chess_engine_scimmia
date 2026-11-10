#Chess_Engine_V1 Santoro Davide.                 8\11\2026
import copy

WHITE_TO_MOVE = 1
BLACK_TO_MOVE = -1

ROOK_DIRECTIONS = ((1,0), (-1,0), (0,-1), (0,1))
BISHOP_DIRECTIONS = ((1,1),(-1,1), (-1, -1), (1, -1))
QUEEN_DIRECTION = ((1,1),(-1,1), (-1, -1), (1, -1), (1,0), (-1,0), (0,-1), (0,1))




#MOVES
KNIGHT_OFFSETS = ((-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1))
KING_OFFSETS = ((1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1))


STARTING_BOARD =   [[-4,-3,-2,-5,-6,-2,-3,-4],
                    [-1,-1,-1,-1,-1,-1,-1,-1],
                    [ 0, 0, 0, 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0, 0, 0, 0],
                    [ 1, 1, 1, 1, 1, 1, 1, 1],
                    [ 4, 3, 2, 5, 6, 2, 3, 4]]



def in_bounds(row, col):
    return 0 <= row <8 and 0 <= col <8
        


class GameState:
    
    def __init__(self):
        self.board = copy.deepcopy(STARTING_BOARD)
        self.turn = WHITE_TO_MOVE
    
    def flip_turn(self):
        self.turn*=-1
    
    def piece_at(self, square):
        row, col = square
        return self.board[row][col]
    
    def is_own_piece(self, square):
        return self.piece_at(square)*self.turn > 0 
    
    def move_piece(self, from_square, to_square):

        if not self.is_own_piece(from_square):
            return False
        if self.is_own_piece(to_square):
            return False

        if to_square not in self.get_moves(from_square):
            return False

        
        from_square_row, from_square_col = from_square
        to_square_row, to_square_col = to_square
        
        self.board[to_square_row][to_square_col] = self.board[from_square_row][from_square_col]
        self.board[from_square_row][from_square_col] = 0
        self.flip_turn()
        
        return True
    
    
    def step_moves(self, square, offsets):
        moves = []
        row, col = square
        piece = self.piece_at(square)
        
        for d_row, d_col in offsets:
             
            new_row = row + d_row
            new_col = col + d_col
            
            if in_bounds(new_row, new_col) :
                target = self.piece_at((new_row, new_col))
                if piece*target<=0:
                    moves.append((new_row, new_col))
        return moves     

    def slide_moves(self, square, direction):
        moves = []
        row, col = square
        piece = self.piece_at(square)
        
        for d_row, d_col in direction:
            new_row = row + d_row
            new_col = col + d_col
            
            while in_bounds(new_row, new_col):
                target = self.piece_at((new_row, new_col))
                
                if target == 0:
                    moves.append((new_row, new_col))
                    new_row += d_row
                    new_col += d_col
                elif target*piece < 0:
                    moves.append((new_row, new_col))
                    break
                elif piece*target > 0:
                    break
        
        return moves

    
    def knight_moves(self,square):
        return self.step_moves(square, KNIGHT_OFFSETS)    
    
    def king_moves(self,square):
        return self.step_moves(square, KING_OFFSETS)    

    def queen_moves(self, square):
        return self.slide_moves(square, QUEEN_DIRECTION)
    
    def bishop_moves(self, square):
        return self.slide_moves(square, BISHOP_DIRECTIONS)
    
    def rook_moves(self, square):
        return self.slide_moves(square, ROOK_DIRECTIONS)
    
    def pawn_moves(self, square):
        row, col = square
        moves = []
        direction = self.piece_at(square)*-1
        piece = self.piece_at(square)
        starting_row = 6 if piece == 1 else 1


        if self.piece_at((row+direction, col)) == 0:
            moves.append((row+direction, col))
            if row == starting_row and self.piece_at((row + 2*direction, col)) == 0:
                moves.append((row + 2*direction, col))

        for d_col in (-1, 1):
            if self.piece_at((row+direction, col + d_col))*piece < 0:
                moves.append((row+direction, col + d_col))

        return moves


    def get_moves(self, square):
        piece = self.piece_at(square)
        moves = []
        
        match abs(piece):
            case 1:
                moves.extend(self.pawn_moves(square))
            case 2:
                moves.extend(self.bishop_moves(square))
            case 3:
                moves.extend(self.knight_moves(square))
            case 4:
                moves.extend(self.rook_moves(square))
            case 5:
                moves.extend(self.queen_moves(square))
            case 6:
                moves.extend(self.king_moves(square))
            case _ :
                return []

        return moves
    



   
    
        
