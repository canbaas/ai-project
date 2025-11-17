import tkinter as tk
from tkinter import messagebox
import random
import time

# Chess piece Unicode symbols
PIECE_SYMBOLS = {
    'king': '♚', 'queen': '♛', 'rook': '♜',
    'bishop': '♝', 'knight': '♞', 'pawn': '♟'
}

# Piece values for AI evaluation
PIECE_VALUES = {
    'pawn': 10,
    'knight': 30,
    'bishop': 30,
    'rook': 50,
    'queen': 90,
    'king': 900
}

class ChessGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess Game - You vs AI")
        self.root.configure(bg='#1e293b')
        
        # Game state
        self.board = self.initialize_board()
        self.selected_square = None
        self.valid_moves = []
        self.current_player = 'white'
        self.game_over = False
        self.winner = None
        self.captured_pieces = {'white': [], 'black': []}
        self.ai_enabled = True  # AI plays as black
        self.ai_thinking = False
        
        # Colors
        self.light_square = '#f0d9b5'
        self.dark_square = '#b58863'
        self.highlight_color = '#3b82f6'
        self.valid_move_color = '#86efac'
        self.capture_color = '#ef4444'
        
        # Create UI
        self.create_widgets()
        self.render_board()
        self.update_sidebar()
    
    def initialize_board(self):
        board = [[None for _ in range(8)] for _ in range(8)]
        
        # Pawns
        for i in range(8):
            board[1][i] = {'type': 'pawn', 'color': 'black'}
            board[6][i] = {'type': 'pawn', 'color': 'white'}
        
        # Rooks
        board[0][0] = board[0][7] = {'type': 'rook', 'color': 'black'}
        board[7][0] = board[7][7] = {'type': 'rook', 'color': 'white'}
        
        # Knights
        board[0][1] = board[0][6] = {'type': 'knight', 'color': 'black'}
        board[7][1] = board[7][6] = {'type': 'knight', 'color': 'white'}
        
        # Bishops
        board[0][2] = board[0][5] = {'type': 'bishop', 'color': 'black'}
        board[7][2] = board[7][5] = {'type': 'bishop', 'color': 'white'}
        
        # Queens
        board[0][3] = {'type': 'queen', 'color': 'black'}
        board[7][3] = {'type': 'queen', 'color': 'white'}
        
        # Kings
        board[0][4] = {'type': 'king', 'color': 'black'}
        board[7][4] = {'type': 'king', 'color': 'white'}
        
        return board
    
    def create_widgets(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='#1e293b')
        main_frame.pack(padx=20, pady=20)
        
        # Sidebar
        sidebar = tk.Frame(main_frame, bg='#334155', width=280)
        sidebar.pack(side=tk.LEFT, padx=(0, 20), fill=tk.Y)
        
        # Title
        title_label = tk.Label(sidebar, text="♔ Chess", font=('Arial', 24, 'bold'),
                              bg='#334155', fg='white')
        title_label.pack(pady=20)
        
        # Mode indicator
        mode_label = tk.Label(sidebar, text="You (White) vs AI (Black)", 
                             font=('Arial', 10, 'bold'),
                             bg='#334155', fg='#fbbf24')
        mode_label.pack()
        
        # Current turn
        turn_frame = tk.Frame(sidebar, bg='#334155')
        turn_frame.pack(pady=10)
        
        tk.Label(turn_frame, text="Current Turn", font=('Arial', 10),
                bg='#334155', fg='#94a3b8').pack()
        
        self.turn_label = tk.Label(turn_frame, text="White (You)", font=('Arial', 16, 'bold'),
                                   bg='white', fg='#1e293b', width=14, pady=10)
        self.turn_label.pack(pady=5)
        
        # AI thinking indicator
        self.ai_label = tk.Label(sidebar, text="", font=('Arial', 10, 'italic'),
                                bg='#334155', fg='#fbbf24')
        self.ai_label.pack()
        
        # Game over message
        self.game_over_frame = tk.Frame(sidebar, bg='#10b981')
        self.game_over_label = tk.Label(self.game_over_frame, text="Game Over!",
                                       font=('Arial', 14, 'bold'), bg='#10b981', fg='white')
        self.game_over_label.pack(pady=5)
        self.winner_label = tk.Label(self.game_over_frame, text="",
                                     font=('Arial', 12), bg='#10b981', fg='white')
        self.winner_label.pack(pady=5)
        
        # Captured pieces
        tk.Label(sidebar, text="You Captured", font=('Arial', 10),
                bg='#334155', fg='#94a3b8').pack(pady=(20, 5))
        self.captured_white_label = tk.Label(sidebar, text="", font=('Arial', 20),
                                            bg='#1e293b', fg='black', height=2, width=12)
        self.captured_white_label.pack()
        
        tk.Label(sidebar, text="AI Captured", font=('Arial', 10),
                bg='#334155', fg='#94a3b8').pack(pady=(20, 5))
        self.captured_black_label = tk.Label(sidebar, text="", font=('Arial', 20),
                                            bg='#1e293b', fg='white', height=2, width=12)
        self.captured_black_label.pack()
        
        # New game button
        new_game_btn = tk.Button(sidebar, text="🔄 New Game", font=('Arial', 14, 'bold'),
                                bg='#3b82f6', fg='white', command=self.reset_game,
                                cursor='hand2', relief=tk.FLAT, pady=10)
        new_game_btn.pack(pady=20, padx=20, fill=tk.X)
        
        # Chess board frame
        board_frame = tk.Frame(main_frame, bg='#334155', padx=20, pady=20)
        board_frame.pack(side=tk.LEFT)
        
        # Create board squares
        self.squares = []
        for row in range(8):
            row_squares = []
            for col in range(8):
                color = self.light_square if (row + col) % 2 == 0 else self.dark_square
                square = tk.Label(board_frame, text="", font=('Arial', 48),
                                 bg=color, width=2, height=1,
                                 relief=tk.RAISED, borderwidth=2)
                square.grid(row=row, column=col, padx=1, pady=1)
                square.bind('<Button-1>', lambda e, r=row, c=col: self.handle_click(r, c))
                row_squares.append(square)
            self.squares.append(row_squares)
    
    def get_valid_moves(self, row, col):
        piece = self.board[row][col]
        if not piece:
            return []
        
        moves = []
        piece_type = piece['type']
        color = piece['color']
        
        def is_valid(r, c):
            return 0 <= r < 8 and 0 <= c < 8
        
        def is_empty_or_enemy(r, c):
            return not self.board[r][c] or self.board[r][c]['color'] != color
        
        if piece_type == 'pawn':
            direction = -1 if color == 'white' else 1
            start_row = 6 if color == 'white' else 1
            
            if is_valid(row + direction, col) and not self.board[row + direction][col]:
                moves.append((row + direction, col))
                if row == start_row and not self.board[row + 2 * direction][col]:
                    moves.append((row + 2 * direction, col))
            
            for dc in [-1, 1]:
                nr, nc = row + direction, col + dc
                if is_valid(nr, nc) and self.board[nr][nc]:
                    if self.board[nr][nc]['color'] != color:
                        moves.append((nr, nc))
        
        elif piece_type == 'rook':
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                r, c = row + dr, col + dc
                while is_valid(r, c):
                    if not self.board[r][c]:
                        moves.append((r, c))
                    else:
                        if self.board[r][c]['color'] != color:
                            moves.append((r, c))
                        break
                    r += dr
                    c += dc
        
        elif piece_type == 'knight':
            for dr, dc in [(2, 1), (2, -1), (-2, 1), (-2, -1),
                          (1, 2), (1, -2), (-1, 2), (-1, -2)]:
                r, c = row + dr, col + dc
                if is_valid(r, c) and is_empty_or_enemy(r, c):
                    moves.append((r, c))
        
        elif piece_type == 'bishop':
            for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                r, c = row + dr, col + dc
                while is_valid(r, c):
                    if not self.board[r][c]:
                        moves.append((r, c))
                    else:
                        if self.board[r][c]['color'] != color:
                            moves.append((r, c))
                        break
                    r += dr
                    c += dc
        
        elif piece_type == 'queen':
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0),
                          (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                r, c = row + dr, col + dc
                while is_valid(r, c):
                    if not self.board[r][c]:
                        moves.append((r, c))
                    else:
                        if self.board[r][c]['color'] != color:
                            moves.append((r, c))
                        break
                    r += dr
                    c += dc
        
        elif piece_type == 'king':
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0),
                          (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                r, c = row + dr, col + dc
                if is_valid(r, c) and is_empty_or_enemy(r, c):
                    moves.append((r, c))
        
        return moves
    
    def evaluate_board(self):
        """Evaluate board position for AI"""
        score = 0
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece:
                    value = PIECE_VALUES[piece['type']]
                    if piece['color'] == 'black':
                        score += value
                    else:
                        score -= value
        return score
    
    def get_all_moves(self, color):
        """Get all possible moves for a color"""
        all_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece['color'] == color:
                    moves = self.get_valid_moves(row, col)
                    for move in moves:
                        all_moves.append(((row, col), move))
        return all_moves
    
    def make_ai_move(self):
        """AI makes a move (simple evaluation-based)"""
        if self.game_over or self.ai_thinking:
            return
        
        self.ai_thinking = True
        self.ai_label.config(text="🤔 AI is thinking...")
        self.root.update()
        
        # Simulate thinking delay
        time.sleep(0.5)
        
        all_moves = self.get_all_moves('black')
        
        if not all_moves:
            self.ai_thinking = False
            self.ai_label.config(text="")
            return
        
        best_move = None
        best_score = float('-inf')
        
        # Evaluate each possible move
        for (from_pos, to_pos) in all_moves:
            fr, fc = from_pos
            tr, tc = to_pos
            
            # Simulate move
            moving_piece = self.board[fr][fc]
            captured_piece = self.board[tr][tc]
            self.board[tr][tc] = moving_piece
            self.board[fr][fc] = None
            
            # Evaluate position
            score = self.evaluate_board()
            
            # Bonus for capturing pieces
            if captured_piece:
                score += PIECE_VALUES[captured_piece['type']] * 2
            
            # Bonus for advancing pawns
            if moving_piece['type'] == 'pawn':
                score += (7 - tr) * 2
            
            # Bonus for center control
            if 2 <= tr <= 5 and 2 <= tc <= 5:
                score += 5
            
            # Add some randomness for variety
            score += random.uniform(-5, 5)
            
            # Undo move
            self.board[fr][fc] = moving_piece
            self.board[tr][tc] = captured_piece
            
            if score > best_score:
                best_score = score
                best_move = (from_pos, to_pos)
        
        # Make the best move
        if best_move:
            (fr, fc), (tr, tc) = best_move
            moving_piece = self.board[fr][fc]
            captured_piece = self.board[tr][tc]
            
            if captured_piece:
                self.captured_pieces['black'].append(captured_piece)
                if captured_piece['type'] == 'king':
                    self.game_over = True
                    self.winner = 'black'
            
            self.board[tr][tc] = moving_piece
            self.board[fr][fc] = None
            
            # Pawn promotion
            if moving_piece['type'] == 'pawn' and tr == 7:
                self.board[tr][tc] = {'type': 'queen', 'color': 'black'}
            
            self.current_player = 'white'
            
            if self.game_over:
                messagebox.showinfo("Game Over", "AI wins! Better luck next time!")
        
        self.ai_thinking = False
        self.ai_label.config(text="")
        self.render_board()
        self.update_sidebar()
    
    def handle_click(self, row, col):
        if self.game_over or self.ai_thinking:
            return
        
        # Only allow white (player) to move
        if self.current_player != 'white':
            return
        
        if self.selected_square:
            sr, sc = self.selected_square
            
            if (row, col) in self.valid_moves:
                # Make move
                moving_piece = self.board[sr][sc]
                captured_piece = self.board[row][col]
                
                if captured_piece:
                    self.captured_pieces['white'].append(captured_piece)
                    if captured_piece['type'] == 'king':
                        self.game_over = True
                        self.winner = 'white'
                
                self.board[row][col] = moving_piece
                self.board[sr][sc] = None
                
                # Pawn promotion
                if moving_piece['type'] == 'pawn' and row == 0:
                    self.board[row][col] = {'type': 'queen', 'color': 'white'}
                
                self.current_player = 'black'
                self.selected_square = None
                self.valid_moves = []
                
                self.render_board()
                self.update_sidebar()
                
                if self.game_over:
                    messagebox.showinfo("Game Over", "You win! Congratulations!")
                else:
                    # AI's turn
                    self.root.after(500, self.make_ai_move)
            else:
                self.selected_square = None
                self.valid_moves = []
        
        elif self.board[row][col] and self.board[row][col]['color'] == 'white':
            self.selected_square = (row, col)
            self.valid_moves = self.get_valid_moves(row, col)
        
        self.render_board()
        self.update_sidebar()
    
    def render_board(self):
        for row in range(8):
            for col in range(8):
                square = self.squares[row][col]
                base_color = self.light_square if (row + col) % 2 == 0 else self.dark_square
                
                # Reset square
                square.config(bg=base_color, relief=tk.RAISED, borderwidth=2)
                
                # Highlight selected
                if self.selected_square == (row, col):
                    square.config(relief=tk.SUNKEN, borderwidth=4, 
                                 highlightbackground=self.highlight_color,
                                 highlightthickness=3)
                
                # Show valid moves
                if (row, col) in self.valid_moves:
                    if self.board[row][col]:
                        square.config(highlightbackground=self.capture_color,
                                    highlightthickness=4)
                    else:
                        square.config(bg=self.valid_move_color)
                
                # Display piece
                piece = self.board[row][col]
                if piece:
                    symbol = PIECE_SYMBOLS[piece['type']]
                    color = 'white' if piece['color'] == 'white' else 'black'
                    square.config(text=symbol, fg=color)
                else:
                    square.config(text="")
    
    def update_sidebar(self):
        # Update turn display
        if self.current_player == 'white':
            self.turn_label.config(text="White (You)", bg='white', fg='#1e293b')
        else:
            self.turn_label.config(text="Black (AI)", bg='#1e293b', fg='white')
        
        # Update game over
        if self.game_over:
            self.game_over_frame.pack(pady=10)
            if self.winner == 'white':
                self.winner_label.config(text="You win! 🎉")
            else:
                self.winner_label.config(text="AI wins! Try again!")
        else:
            self.game_over_frame.pack_forget()
        
        # Update captured pieces
        white_captured = ' '.join([PIECE_SYMBOLS[p['type']] 
                                   for p in self.captured_pieces['white']])
        self.captured_white_label.config(text=white_captured)
        
        black_captured = ' '.join([PIECE_SYMBOLS[p['type']] 
                                   for p in self.captured_pieces['black']])
        self.captured_black_label.config(text=black_captured)
    
    def reset_game(self):
        self.board = self.initialize_board()
        self.selected_square = None
        self.valid_moves = []
        self.current_player = 'white'
        self.game_over = False
        self.winner = None
        self.captured_pieces = {'white': [], 'black': []}
        self.ai_thinking = False
        self.render_board()
        self.update_sidebar()

if __name__ == '__main__':
    root = tk.Tk()
    game = ChessGame(root)
    root.mainloop()