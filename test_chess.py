"""
Test script for the Professional Chess Game
Tests core functionality without GUI
"""

from chess_game import ChessEngine, Position, ChessPiece, PieceType, Color


def test_initial_setup():
    """Test that the board is set up correctly"""
    engine = ChessEngine()
    
    # Test white pieces
    assert engine.board[Position(7, 0)].piece_type == PieceType.ROOK
    assert engine.board[Position(7, 0)].color == Color.WHITE
    assert engine.board[Position(7, 4)].piece_type == PieceType.KING
    assert engine.board[Position(7, 4)].color == Color.WHITE
    
    # Test black pieces
    assert engine.board[Position(0, 0)].piece_type == PieceType.ROOK
    assert engine.board[Position(0, 0)].color == Color.BLACK
    assert engine.board[Position(0, 4)].piece_type == PieceType.KING
    assert engine.board[Position(0, 4)].color == Color.BLACK
    
    # Test pawns
    for i in range(8):
        assert engine.board[Position(6, i)].piece_type == PieceType.PAWN
        assert engine.board[Position(6, i)].color == Color.WHITE
        assert engine.board[Position(1, i)].piece_type == PieceType.PAWN
        assert engine.board[Position(1, i)].color == Color.BLACK
    
    print("✓ Initial board setup is correct")


def test_pawn_moves():
    """Test pawn movement"""
    engine = ChessEngine()
    
    # Test white pawn can move 1 or 2 squares initially
    legal_moves = engine.get_legal_moves(Position(6, 4))  # e2 pawn
    assert Position(5, 4) in legal_moves  # e3
    assert Position(4, 4) in legal_moves  # e4
    
    # Make a move
    assert engine.make_move(Position(6, 4), Position(4, 4))  # e2-e4
    
    # Now it's black's turn
    assert engine.current_turn == Color.BLACK
    
    # Black pawn can also move 1 or 2 squares
    legal_moves = engine.get_legal_moves(Position(1, 4))  # e7 pawn
    assert Position(2, 4) in legal_moves  # e6
    assert Position(3, 4) in legal_moves  # e5
    
    print("✓ Pawn movement works correctly")


def test_knight_moves():
    """Test knight movement"""
    engine = ChessEngine()
    
    # Test white knight moves
    legal_moves = engine.get_legal_moves(Position(7, 1))  # b1 knight
    assert Position(5, 0) in legal_moves  # a3
    assert Position(5, 2) in legal_moves  # c3
    assert len(legal_moves) == 2  # Only 2 moves available initially
    
    # Move knight
    assert engine.make_move(Position(7, 1), Position(5, 2))  # Nc3
    
    print("✓ Knight movement works correctly")


def test_castling():
    """Test castling"""
    engine = ChessEngine()
    
    # Clear path for kingside castling
    engine.make_move(Position(6, 4), Position(4, 4))  # e4
    engine.make_move(Position(1, 4), Position(3, 4))  # e5
    engine.make_move(Position(7, 6), Position(5, 5))  # Nf3
    engine.make_move(Position(0, 6), Position(2, 5))  # Nf6
    engine.make_move(Position(7, 5), Position(6, 4))  # Be2
    engine.make_move(Position(0, 5), Position(1, 4))  # Be7
    
    # Now white can castle kingside
    king_moves = engine.get_legal_moves(Position(7, 4))
    assert Position(7, 6) in king_moves  # Kingside castling
    
    # Perform castling
    initial_rook_pos = Position(7, 7)
    assert engine.board[initial_rook_pos].piece_type == PieceType.ROOK
    
    assert engine.make_move(Position(7, 4), Position(7, 6))  # O-O
    
    # Check that king and rook moved correctly
    assert engine.board[Position(7, 6)].piece_type == PieceType.KING
    assert engine.board[Position(7, 5)].piece_type == PieceType.ROOK
    assert initial_rook_pos not in engine.board
    
    print("✓ Castling works correctly")


def test_check_detection():
    """Test check detection"""
    engine = ChessEngine()
    
    # Create a simple check scenario
    # Clear some pieces for demonstration
    engine.board = {
        Position(7, 4): ChessPiece(PieceType.KING, Color.WHITE),
        Position(0, 4): ChessPiece(PieceType.KING, Color.BLACK),
        Position(1, 4): ChessPiece(PieceType.ROOK, Color.BLACK),
    }
    engine.current_turn = Color.BLACK
    
    # Move rook to check white king
    assert engine.make_move(Position(1, 4), Position(7, 4)) == False  # Can't capture king
    engine.make_move(Position(1, 4), Position(6, 4))  # Move to e2 instead
    
    # White king should now be in check
    engine.current_turn = Color.WHITE
    assert engine._is_in_check(Color.WHITE)
    
    print("✓ Check detection works correctly")


def test_algebraic_notation():
    """Test algebraic notation conversion"""
    assert Position(0, 0).to_algebraic() == "a8"
    assert Position(0, 7).to_algebraic() == "h8"
    assert Position(7, 0).to_algebraic() == "a1"
    assert Position(7, 7).to_algebraic() == "h1"
    assert Position(4, 4).to_algebraic() == "e4"
    
    print("✓ Algebraic notation works correctly")


def test_piece_symbols():
    """Test piece Unicode symbols"""
    white_king = ChessPiece(PieceType.KING, Color.WHITE)
    black_queen = ChessPiece(PieceType.QUEEN, Color.BLACK)
    
    assert white_king.symbol == '♔'
    assert black_queen.symbol == '♛'
    
    print("✓ Piece symbols work correctly")


def test_position_arithmetic():
    """Test position arithmetic"""
    pos = Position(4, 4)
    
    # Test valid moves
    new_pos = pos + (1, 0)
    assert new_pos == Position(5, 4)
    
    new_pos = pos + (-1, 1)
    assert new_pos == Position(3, 5)
    
    # Test out of bounds
    new_pos = pos + (10, 0)
    assert new_pos is None
    
    new_pos = pos + (0, -5)
    assert new_pos is None
    
    print("✓ Position arithmetic works correctly")


def run_all_tests():
    """Run all tests"""
    print("\n🎯 Running Professional Chess Game Tests\n")
    print("-" * 40)
    
    test_initial_setup()
    test_pawn_moves()
    test_knight_moves()
    test_castling()
    test_check_detection()
    test_algebraic_notation()
    test_piece_symbols()
    test_position_arithmetic()
    
    print("-" * 40)
    print("\n✅ All tests passed successfully!")
    print("\nThe chess game is working correctly.")
    print("You can now run 'python chess_game.py' to play!")


if __name__ == "__main__":
    run_all_tests()