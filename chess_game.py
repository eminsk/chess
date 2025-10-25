"""
Professional Chess Game with Modern GUI

A high-performance, memory-efficient chess implementation using functional programming paradigms
"""

import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass
from typing import Optional, Tuple, List, Set, Dict, Callable
from enum import Enum, auto
from functools import lru_cache, partial
from itertools import product
import copy
import random

class SimpleAI:
    def __init__(self, engine):
        self.engine = engine

    def evaluate_move(self, move):
        captured = self.engine.board.get(move)
        if not captured:
            return 0
        values = {
            "PAWN": 1, "KNIGHT": 3, "BISHOP": 3,
            "ROOK": 5, "QUEEN": 9, "KING": 0
        }
        return values[captured.piece_type.name]

    def choose_move(self):
        moves = [
            (pos, move)
            for pos, piece in list(self.engine.board.items())
            if piece.color == self.engine.current_turn
            for move in self.engine.get_legal_moves(pos)
        ]
        if not moves:
            return None
        weighted = [(f, t, self.evaluate_move(t)) for f, t in moves]
        best_value = max(v for _, _, v in weighted)
        best_options = [(f, t) for f, t, v in weighted if v == best_value]
        return random.choice(best_options)

class PieceType(Enum):
    """Chess piece types enumeration"""
    KING = auto()
    QUEEN = auto()
    ROOK = auto()
    BISHOP = auto()
    KNIGHT = auto()
    PAWN = auto()


class Color(Enum):
    """Chess piece colors"""
    WHITE = auto()
    BLACK = auto()


@dataclass(frozen=True)
class Position:
    """Immutable position representation"""
    row: int
    col: int

    def __add__(self, other: Tuple[int, int]) -> Optional['Position']:
        """Add offset to position"""
        new_row, new_col = self.row + other[0], self.col + other[1]
        return Position(new_row, new_col) if 0 <= new_row < 8 and 0 <= new_col < 8 else None

    def to_algebraic(self) -> str:
        """Convert to algebraic notation"""
        return f"{chr(97 + self.col)}{8 - self.row}"


@dataclass(frozen=True)
class ChessPiece:
    """Immutable chess piece representation"""
    piece_type: PieceType
    color: Color

    @property
    def symbol(self) -> str:
        """Unicode chess symbols"""
        symbols = {
            (PieceType.KING, Color.WHITE): '♔',
            (PieceType.QUEEN, Color.WHITE): '♕',
            (PieceType.ROOK, Color.WHITE): '♖',
            (PieceType.BISHOP, Color.WHITE): '♗',
            (PieceType.KNIGHT, Color.WHITE): '♘',
            (PieceType.PAWN, Color.WHITE): '♙',
            (PieceType.KING, Color.BLACK): '♚',
            (PieceType.QUEEN, Color.BLACK): '♛',
            (PieceType.ROOK, Color.BLACK): '♜',
            (PieceType.BISHOP, Color.BLACK): '♝',
            (PieceType.KNIGHT, Color.BLACK): '♞',
            (PieceType.PAWN, Color.BLACK): '♟'
        }
        return symbols.get((self.piece_type, self.color), '?')


class ChessEngine:
    """High-performance chess engine using functional programming"""

    # Movement vectors for each piece type
    VECTORS = {
        PieceType.KING: [(i, j) for i in [-1, 0, 1] for j in [-1, 0, 1] if (i, j) != (0, 0)],
        PieceType.QUEEN: [(i, j) for i in range(-7, 8) for j in range(-7, 8)
                          if (i == 0) != (j == 0) or abs(i) == abs(j) and i != 0],
        PieceType.ROOK: [(i, 0) for i in range(-7, 8) if i != 0] +
                        [(0, j) for j in range(-7, 8) if j != 0],
        PieceType.BISHOP: [(i, i) for i in range(-7, 8) if i != 0] +
                          [(i, -i) for i in range(-7, 8) if i != 0],
        PieceType.KNIGHT: [(2, 1), (2, -1), (-2, 1), (-2, -1),
                          (1, 2), (1, -2), (-1, 2), (-1, -2)],
        PieceType.PAWN: []  # Special handling required
    }

    def __init__(self):
        """Initialize chess engine with starting position"""
        self.board: Dict[Position, ChessPiece] = self._create_initial_board()
        self.current_turn: Color = Color.WHITE
        self.move_history: List[Tuple[Position, Position, Optional[ChessPiece]]] = []
        self.castling_rights = {
            (Color.WHITE, 'king'): True,
            (Color.WHITE, 'queen'): True,
            (Color.BLACK, 'king'): True,
            (Color.BLACK, 'queen'): True
        }
        self.en_passant_target: Optional[Position] = None
        self.halfmove_clock = 0
        self.fullmove_number = 1

    @staticmethod
    def _create_initial_board() -> Dict[Position, ChessPiece]:
        """Create initial chess board setup"""
        board = {}
        # Piece setup using functional approach
        piece_order = [PieceType.ROOK, PieceType.KNIGHT, PieceType.BISHOP,
                      PieceType.QUEEN, PieceType.KING, PieceType.BISHOP,
                      PieceType.KNIGHT, PieceType.ROOK]
        # Place major pieces
        board.update({Position(0, i): ChessPiece(piece, Color.BLACK)
                     for i, piece in enumerate(piece_order)})
        board.update({Position(7, i): ChessPiece(piece, Color.WHITE)
                     for i, piece in enumerate(piece_order)})
        # Place pawns
        board.update({Position(1, i): ChessPiece(PieceType.PAWN, Color.BLACK)
                     for i in range(8)})
        board.update({Position(6, i): ChessPiece(PieceType.PAWN, Color.WHITE)
                     for i in range(8)})
        return board

    def _get_piece_moves(self, pos: Position, piece: ChessPiece, include_castling: bool = True) -> Set[Position]:
        """Calculate all possible moves for a piece"""
        moves = set()

        if piece.piece_type == PieceType.PAWN:
            direction = -1 if piece.color == Color.WHITE else 1
            start_row = 6 if piece.color == Color.WHITE else 1

            # Forward moves
            front = pos + (direction, 0)
            if front and front not in self.board:
                moves.add(front)
                if pos.row == start_row:
                    double = pos + (2 * direction, 0)
                    if double and double not in self.board:
                        moves.add(double)

            # Captures
            captures = [pos + (direction, -1), pos + (direction, 1)]
            moves.update(filter(lambda p: p and p in self.board and
                              self.board[p].color != piece.color, captures))

            # En passant
            if self.en_passant_target:
                ep_captures = [pos + (direction, -1), pos + (direction, 1)]
                moves.update(filter(lambda p: p == self.en_passant_target, ep_captures))

        else:
            vectors = self.VECTORS[piece.piece_type]

            if piece.piece_type in [PieceType.KING, PieceType.KNIGHT]:
                # Single-step moves
                potential_moves = map(lambda v: pos + v, vectors)
                moves.update(filter(lambda p: p and (p not in self.board or
                                                    self.board[p].color != piece.color),
                                  potential_moves))
            else:
                # Sliding pieces
                for vector in vectors:
                    current = pos
                    while True:
                        current = current + (vector[0] // max(abs(vector[0]), 1) if vector[0] else 0,
                                           vector[1] // max(abs(vector[1]), 1) if vector[1] else 0)
                        if not current:
                            break
                        if current in self.board:
                            if self.board[current].color != piece.color:
                                moves.add(current)
                            break
                        moves.add(current)

            # Add castling moves for king (only if include_castling is True to prevent recursion)
            if piece.piece_type == PieceType.KING and include_castling and not self._is_in_check(piece.color):
                moves.update(self._get_castling_moves(pos, piece))

        return moves

    def _get_castling_moves(self, king_pos: Position, king: ChessPiece) -> Set[Position]:
        """Get available castling moves"""
        moves = set()
        row = 7 if king.color == Color.WHITE else 0

        # King-side castling
        if self.castling_rights.get((king.color, 'king'), False):
            if all(Position(row, col) not in self.board for col in [5, 6]):
                if not any(self._is_position_attacked(Position(row, col), king.color)
                          for col in [4, 5, 6]):
                    moves.add(Position(row, 6))

        # Queen-side castling
        if self.castling_rights.get((king.color, 'queen'), False):
            if all(Position(row, col) not in self.board for col in [1, 2, 3]):
                if not any(self._is_position_attacked(Position(row, col), king.color)
                          for col in [2, 3, 4]):
                    moves.add(Position(row, 2))

        return moves

    def _is_position_attacked(self, pos: Position, defending_color: Color) -> bool:
        """Check if a position is attacked by the opposing color"""
        attacking_color = Color.BLACK if defending_color == Color.WHITE else Color.WHITE
        # KEY FIX: Pass include_castling=False to prevent infinite recursion
        return any(pos in self._get_piece_moves(attacker_pos, attacker, include_castling=False)
                  for attacker_pos, attacker in self.board.items()
                  if attacker.color == attacking_color)

    def _is_in_check(self, color: Color) -> bool:
        """Check if the king of given color is in check"""
        king_pos = next((pos for pos, piece in self.board.items()
                        if piece.piece_type == PieceType.KING and piece.color == color), None)
        return self._is_position_attacked(king_pos, color) if king_pos else False

    def get_legal_moves(self, pos: Position) -> Set[Position]:
        """Get all legal moves for a piece at given position"""
        if pos not in self.board:
            return set()

        piece = self.board[pos]
        if piece.color != self.current_turn:
            return set()

        # Get pseudo-legal moves
        moves = self._get_piece_moves(pos, piece)

        # Filter moves that would leave king in check or capture opponent's king
        legal_moves = set()
        for move in moves:
            # Don't allow capturing opponent's king (game should end at checkmate)
            target_piece = self.board.get(move)
            if target_piece and target_piece.piece_type == PieceType.KING:
                continue  # Skip this illegal move

            # Make move temporarily
            captured = self.board.get(move)
            self.board[move] = piece
            del self.board[pos]

            # Check if king is safe
            if not self._is_in_check(piece.color):
                legal_moves.add(move)

            # Restore position
            self.board[pos] = piece
            if captured:
                self.board[move] = captured
            else:
                self.board.pop(move, None)

        return legal_moves


    def make_move(self, from_pos: Position, to_pos: Position) -> bool:
        """Execute a move if legal"""
        if to_pos not in self.get_legal_moves(from_pos):
            return False

        piece = self.board[from_pos]
        captured = self.board.get(to_pos)

        # Handle special moves
        self._handle_special_moves(from_pos, to_pos, piece)

        # Make the move
        self.board[to_pos] = piece
        del self.board[from_pos]

        # Update game state
        self.move_history.append((from_pos, to_pos, captured))
        self._update_castling_rights(from_pos, to_pos, piece)
        self._update_en_passant(from_pos, to_pos, piece)
        self.halfmove_clock = 0 if captured or piece.piece_type == PieceType.PAWN else self.halfmove_clock + 1

        if self.current_turn == Color.BLACK:
            self.fullmove_number += 1

        self.current_turn = Color.BLACK if self.current_turn == Color.WHITE else Color.WHITE

        return True

    def _handle_special_moves(self, from_pos: Position, to_pos: Position, piece: ChessPiece):
        """Handle castling, en passant, and promotion"""
        # Castling
        if piece.piece_type == PieceType.KING and abs(from_pos.col - to_pos.col) == 2:
            row = from_pos.row
            if to_pos.col == 6:  # King-side
                self.board[Position(row, 5)] = self.board[Position(row, 7)]
                del self.board[Position(row, 7)]
            else:  # Queen-side
                self.board[Position(row, 3)] = self.board[Position(row, 0)]
                del self.board[Position(row, 0)]

        # En passant capture
        if piece.piece_type == PieceType.PAWN and to_pos == self.en_passant_target:
            capture_row = 3 if piece.color == Color.WHITE else 4
            del self.board[Position(capture_row, to_pos.col)]

        # Pawn promotion (auto-promote to queen for simplicity)
        if piece.piece_type == PieceType.PAWN and to_pos.row in [0, 7]:
            self.board[to_pos] = ChessPiece(PieceType.QUEEN, piece.color)

    def _update_castling_rights(self, from_pos: Position, to_pos: Position, piece: ChessPiece):
        """Update castling rights after a move"""
        if piece.piece_type == PieceType.KING:
            self.castling_rights[(piece.color, 'king')] = False
            self.castling_rights[(piece.color, 'queen')] = False
        elif piece.piece_type == PieceType.ROOK:
            if from_pos.col == 0:
                self.castling_rights[(piece.color, 'queen')] = False
            elif from_pos.col == 7:
                self.castling_rights[(piece.color, 'king')] = False

    def _update_en_passant(self, from_pos: Position, to_pos: Position, piece: ChessPiece):
        """Update en passant target square"""
        if piece.piece_type == PieceType.PAWN and abs(from_pos.row - to_pos.row) == 2:
            self.en_passant_target = Position((from_pos.row + to_pos.row) // 2, from_pos.col)
        else:
            self.en_passant_target = None

    def is_checkmate(self) -> bool:
        """Check if current player is in checkmate"""
        if not self._is_in_check(self.current_turn):
            return False
        # Check if any piece has legal moves
        return not any(self.get_legal_moves(pos)
                      for pos, piece in list(self.board.items())
                      if piece.color == self.current_turn)

    def is_stalemate(self) -> bool:
        """Check if game is in stalemate"""
        if self._is_in_check(self.current_turn):
            return False
        # Check if any piece has legal moves
        return not any(self.get_legal_moves(pos)
                      for pos, piece in list(self.board.items())
                      if piece.color == self.current_turn)

    def is_draw(self) -> bool:
        """Check for draw conditions"""
        # Fifty-move rule
        if self.halfmove_clock >= 100:
            return True

        # Insufficient material
        pieces = list(self.board.values())
        if len(pieces) <= 3:
            piece_types = {p.piece_type for p in pieces}
            # King vs King, King+Bishop vs King, King+Knight vs King
            if piece_types <= {PieceType.KING, PieceType.BISHOP, PieceType.KNIGHT}:
                return True

        return self.is_stalemate()


class ChessGUI:
    """Modern Chess GUI using tkinter with professional design"""

    # Color scheme for modern look
    COLORS = {
        'dark_square': '#779556',
        'light_square': '#EBECD0',
        'highlight': '#F7F769',
        'legal_move': '#646D40',
        'selected': '#BACA2B',
        'check': '#E63946',
        'background': '#2B2D42',
        'text': '#EDF2F4',
        'button': '#8D99AE',
        'button_hover': '#A8B2C7'
    }

    def __init__(self, master: tk.Tk):
        """Initialize the chess GUI"""
        self.master = master
        self.master.title("Professional Chess Game")
        self.master.configure(bg=self.COLORS['background'])
        self.master.resizable(False, False)

        # Set window size and center it
        self.square_size = 80
        window_width = self.square_size * 8 + 300
        window_height = self.square_size * 8 + 100
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.master.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Initialize game engine
        self.engine = ChessEngine()
        self.ai = SimpleAI(self.engine)
        self.selected_square: Optional[Position] = None
        self.legal_moves: Set[Position] = set()

        # Create UI
        self._create_widgets()
        self._draw_board()
        self._draw_pieces()

    def computer_move(self):
        if self.engine.current_turn == Color.BLACK:
            move = self.ai.choose_move()
            if move:
                self.engine.make_move(*move)
                self._refresh_display()
                self._check_game_status()

    def _create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        main_frame = tk.Frame(self.master, bg=self.COLORS['background'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Left panel - Board
        board_frame = tk.Frame(main_frame, bg=self.COLORS['background'])
        board_frame.pack(side=tk.LEFT, padx=(0, 20))

        # Board title
        title = tk.Label(board_frame, text="♔ Professional Chess ♚",
                        font=('Segoe UI', 24, 'bold'),
                        fg=self.COLORS['text'], bg=self.COLORS['background'])
        title.pack(pady=(0, 10))

        # Chess board canvas
        self.canvas = tk.Canvas(board_frame,
                               width=self.square_size * 8,
                               height=self.square_size * 8,
                               highlightthickness=2,
                               highlightbackground=self.COLORS['text'])
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self._on_square_click)

        # Right panel - Game info
        info_frame = tk.Frame(main_frame, bg=self.COLORS['background'], width=240)
        info_frame.pack(side=tk.RIGHT, fill=tk.Y)
        info_frame.pack_propagate(False)

        # Game status
        self.status_label = tk.Label(info_frame,
                                     text=f"{'White' if self.engine.current_turn == Color.WHITE else 'Black'}'s Turn",
                                     font=('Segoe UI', 16, 'bold'),
                                     fg=self.COLORS['text'],
                                     bg=self.COLORS['background'])
        self.status_label.pack(pady=(0, 20))

        # Move history
        history_label = tk.Label(info_frame, text="Move History",
                                font=('Segoe UI', 14, 'bold'),
                                fg=self.COLORS['text'],
                                bg=self.COLORS['background'])
        history_label.pack()

        # History listbox with scrollbar
        history_frame = tk.Frame(info_frame, bg=self.COLORS['background'])
        history_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        scrollbar = tk.Scrollbar(history_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.history_listbox = tk.Listbox(history_frame,
                                          yscrollcommand=scrollbar.set,
                                          font=('Consolas', 10),
                                          bg='#3D3F51',
                                          fg=self.COLORS['text'],
                                          selectbackground=self.COLORS['button'],
                                          height=15)
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.history_listbox.yview)

        # Control buttons
        button_frame = tk.Frame(info_frame, bg=self.COLORS['background'])
        button_frame.pack(pady=20)

        # New Game button
        self.new_game_btn = self._create_button(button_frame, "New Game", self._new_game)
        self.new_game_btn.pack(pady=5)

        # Undo button
        self.undo_btn = self._create_button(button_frame, "Undo Move", self._undo_move)
        self.undo_btn.pack(pady=5)

        # Exit button
        self.exit_btn = self._create_button(button_frame, "Exit", self.master.quit)
        self.exit_btn.pack(pady=5)

    def _create_button(self, parent: tk.Widget, text: str, command: Callable) -> tk.Button:
        """Create a styled button"""
        btn = tk.Button(parent, text=text, command=command,
                       font=('Segoe UI', 11, 'bold'),
                       fg=self.COLORS['text'],
                       bg=self.COLORS['button'],
                       activebackground=self.COLORS['button_hover'],
                       activeforeground=self.COLORS['text'],
                       relief=tk.FLAT,
                       padx=20, pady=8,
                       cursor='hand2')

        # Add hover effects
        btn.bind('<Enter>', lambda e: btn.config(bg=self.COLORS['button_hover']))
        btn.bind('<Leave>', lambda e: btn.config(bg=self.COLORS['button']))

        return btn

    def _draw_board(self):
        """Draw the chess board"""
        self.canvas.delete("square")
        colors = [self.COLORS['light_square'], self.COLORS['dark_square']]

        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                x1 = col * self.square_size
                y1 = row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size

                self.canvas.create_rectangle(x1, y1, x2, y2,
                                            fill=color,
                                            outline="",
                                            tags=("square", f"square_{row}_{col}"))

                # Add coordinate labels
                if col == 0:
                    self.canvas.create_text(5, y1 + self.square_size // 2,
                                          text=str(8 - row),
                                          font=('Arial', 10),
                                          fill='#333',
                                          anchor='w')
                if row == 7:
                    self.canvas.create_text(x1 + self.square_size // 2,
                                          self.square_size * 8 - 5,
                                          text=chr(97 + col),
                                          font=('Arial', 10),
                                          fill='#333',
                                          anchor='s')

    def _draw_pieces(self):
        """Draw all pieces on the board"""
        self.canvas.delete("piece")

        for position, piece in self.engine.board.items():
            x = position.col * self.square_size + self.square_size // 2
            y = position.row * self.square_size + self.square_size // 2

            # Draw piece with shadow effect
            self.canvas.create_text(x + 2, y + 2,
                                   text=piece.symbol,
                                   font=('Arial', int(self.square_size * 0.7)),
                                   fill='#000000',
                                   tags=("piece", "shadow"),
                                   anchor='center')

            self.canvas.create_text(x, y,
                                   text=piece.symbol,
                                   font=('Arial', int(self.square_size * 0.7)),
                                   fill='#FFFFFF' if piece.color == Color.WHITE else '#000000',
                                   tags=("piece", f"piece_{position.row}_{position.col}"),
                                   anchor='center')

    def _highlight_square(self, position: Position, color: str):
        """Highlight a square with given color"""
        x1 = position.col * self.square_size
        y1 = position.row * self.square_size
        x2 = x1 + self.square_size
        y2 = y1 + self.square_size

        self.canvas.create_rectangle(x1 + 2, y1 + 2, x2 - 2, y2 - 2,
                                    fill="",
                                    outline=color,
                                    width=3,
                                    tags="highlight")

    def _show_legal_moves(self, moves: Set[Position]):
        """Display legal moves on the board"""
        for move in moves:
            x = move.col * self.square_size + self.square_size // 2
            y = move.row * self.square_size + self.square_size // 2

            if move in self.engine.board:
                # Capture move - show as ring
                self.canvas.create_oval(x - 25, y - 25, x + 25, y + 25,
                                      fill="",
                                      outline=self.COLORS['legal_move'],
                                      width=3,
                                      tags="move_indicator")
            else:
                # Regular move - show as dot
                self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10,
                                      fill=self.COLORS['legal_move'],
                                      outline="",
                                      tags="move_indicator")

    def _on_square_click(self, event):
        """Handle click on chess board"""
        col = event.x // self.square_size
        row = event.y // self.square_size

        if not (0 <= row < 8 and 0 <= col < 8):
            return

        clicked_pos = Position(row, col)

        if self.selected_square is None:
            # Select a piece
            if clicked_pos in self.engine.board:
                piece = self.engine.board[clicked_pos]
                if piece.color == self.engine.current_turn:
                    self.selected_square = clicked_pos
                    self.legal_moves = self.engine.get_legal_moves(clicked_pos)
                    self._refresh_display()
        else:
            # Try to make a move
            if clicked_pos in self.legal_moves:
                from_pos = self.selected_square
                to_pos = clicked_pos

                if self.engine.make_move(from_pos, to_pos):
                    self._refresh_display()
                    self.master.after(400, self.computer_move)
                    # Update move history
                    move_text = f"{len(self.engine.move_history)}. {from_pos.to_algebraic()} → {to_pos.to_algebraic()}"
                    self.history_listbox.insert(tk.END, move_text)
                    self.history_listbox.see(tk.END)

                    # Check game status
                    self._check_game_status()

            # Clear selection
            self.selected_square = None
            self.legal_moves = set()
            self._refresh_display()

    def _refresh_display(self):
        """Refresh the board display"""
        self.canvas.delete("highlight")
        self.canvas.delete("move_indicator")

        # Highlight selected square
        if self.selected_square:
            self._highlight_square(self.selected_square, self.COLORS['selected'])
            self._show_legal_moves(self.legal_moves)

        # Highlight king in check
        if self.engine._is_in_check(self.engine.current_turn):
            king_pos = next((pos for pos, piece in self.engine.board.items()
                           if piece.piece_type == PieceType.KING and
                           piece.color == self.engine.current_turn), None)
            if king_pos:
                self._highlight_square(king_pos, self.COLORS['check'])

        # Update status
        turn_text = "White" if self.engine.current_turn == Color.WHITE else "Black"
        self.status_label.config(text=f"{turn_text}'s Turn")

        self._draw_pieces()

    def _check_game_status(self):
        """Check and display game status"""
        if self.engine.is_checkmate():
            winner = "Black" if self.engine.current_turn == Color.WHITE else "White"
            messagebox.showinfo("Game Over", f"Checkmate! {winner} wins!")
            self._new_game()
        elif self.engine.is_draw():
            reason = "Stalemate" if self.engine.is_stalemate() else "Draw by fifty-move rule"
            messagebox.showinfo("Game Over", f"{reason}! The game is a draw.")
            self._new_game()
        elif self.engine._is_in_check(self.engine.current_turn):
            self.status_label.config(text=f"{'White' if self.engine.current_turn == Color.WHITE else 'Black'} in Check!")

    def _new_game(self):
        """Start a new game"""
        self.engine = ChessEngine()
        self.ai = SimpleAI(self.engine)
        self.selected_square = None
        self.legal_moves = set()
        self.history_listbox.delete(0, tk.END)
        self._draw_board()
        self._refresh_display()

    def _undo_move(self):
        """Undo the last move"""
        if not self.engine.move_history:
            messagebox.showinfo("No moves", "No moves to undo!")
            return

        # Get last move
        from_pos, to_pos, captured = self.engine.move_history.pop()

        # Restore piece to original position
        self.engine.board[from_pos] = self.engine.board[to_pos]
        del self.engine.board[to_pos]

        # Restore captured piece if any
        if captured:
            self.engine.board[to_pos] = captured

        # Switch turn back
        self.engine.current_turn = Color.BLACK if self.engine.current_turn == Color.WHITE else Color.WHITE

        # Update display
        self.history_listbox.delete(tk.END)
        self._refresh_display()


def main():
    """Main entry point for the chess application"""
    root = tk.Tk()
    app = ChessGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
