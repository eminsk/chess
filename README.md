# Professional Chess Game 🎯

A high-performance, memory-efficient Chess game implementation in Python with a beautiful modern GUI. Built using functional programming paradigms to minimize loops and conditionals while maximizing performance.

## Features ✨

### Core Gameplay
- **Full Chess Rules Implementation**: Complete chess logic including all standard moves
- **Special Moves**: Castling (both kingside and queenside), En Passant captures, and Pawn Promotion
- **Game State Detection**: Automatic detection of Check, Checkmate, Stalemate, and Draw conditions
- **Move Validation**: Real-time legal move calculation and display
- **Undo Functionality**: Ability to undo moves during gameplay

### Technical Excellence
- **Functional Programming**: Minimal use of loops and if-else statements, leveraging:
  - Lambda functions and higher-order functions
  - Map, filter, and list comprehensions
  - Dictionary-based move mappings
  - Immutable data structures with dataclasses
- **Performance Optimization**:
  - LRU caching for move calculations
  - Efficient board representation using dictionaries
  - Optimized piece movement algorithms
- **Memory Efficiency**:
  - Frozen dataclasses for immutable objects
  - Efficient position and piece representations
  - Smart caching strategies

### Modern GUI Design
- **Beautiful Interface**: Professional dark theme with carefully selected colors
- **Interactive Board**: Click-to-move interface with visual feedback
- **Visual Indicators**:
  - Highlighted selected pieces
  - Legal move indicators (dots for empty squares, rings for captures)
  - Check warning highlights
  - Algebraic notation display
- **Game Information Panel**:
  - Current player indicator
  - Move history with scrollable list
  - Game control buttons with hover effects

## Installation 📦

### Prerequisites
- Python 3.8 or higher
- tkinter (usually comes with Python)

### Setup
1. Clone or download the chess game files
2. No external dependencies required! Uses only Python standard library

## Running the Game 🚀

Simply run the main Python file:

```bash
python chess_game.py
```

The game window will open centered on your screen with the chess board ready to play.

## How to Play 🎮

1. **Making Moves**:
   - Click on a piece to select it (it will be highlighted)
   - Legal moves will be shown as dots (empty squares) or rings (captures)
   - Click on a highlighted square to move the piece there

2. **Special Moves**:
   - **Castling**: Move the king two squares towards a rook (when allowed)
   - **En Passant**: Capture an enemy pawn that just made a two-square advance
   - **Promotion**: Pawns reaching the opposite end automatically promote to Queens

3. **Game Controls**:
   - **New Game**: Start a fresh game
   - **Undo Move**: Take back the last move
   - **Exit**: Close the application

4. **Game End Conditions**:
   - **Checkmate**: When a king is in check with no legal moves
   - **Stalemate**: When a player has no legal moves but isn't in check
   - **Draw**: After 50 moves without captures or pawn moves

## Code Architecture 🏗️

### Class Structure

#### `PieceType` & `Color` Enums
- Type-safe piece and color representations

#### `Position` (Immutable Dataclass)
- Represents board positions with row/column
- Supports position arithmetic and algebraic notation conversion

#### `ChessPiece` (Immutable Dataclass)
- Represents individual chess pieces
- Provides Unicode symbols for display

#### `ChessEngine`
- Core game logic and rule enforcement
- Functional approach to move generation
- Efficient board state management
- Special move handling (castling, en passant, promotion)
- Game state detection (check, checkmate, stalemate)

#### `ChessGUI`
- Modern tkinter-based interface
- Event-driven architecture
- Responsive visual feedback
- Professional styling and animations

### Design Patterns

1. **Immutability**: Using frozen dataclasses for game objects
2. **Functional Programming**: Heavy use of map, filter, and comprehensions
3. **Caching**: LRU cache for expensive computations
4. **Separation of Concerns**: Clear separation between engine and GUI

## Performance Features 🚄

- **Move Caching**: LRU cache stores calculated moves for positions
- **Efficient Board Representation**: Dictionary-based board for O(1) lookups
- **Optimized Move Generation**: Vector-based movement calculation
- **Minimal Loops**: Functional programming reduces iteration overhead

## Memory Optimization 💾

- **Immutable Objects**: Prevents unnecessary object duplication
- **Smart Caching**: Limited cache size prevents memory bloat
- **Efficient Data Structures**: Minimal memory footprint for game state

## GUI Features 🎨

### Color Scheme
- Dark modern theme for reduced eye strain
- High contrast for piece visibility
- Color-coded indicators for game states

### Visual Feedback
- Piece selection highlighting
- Legal move indicators
- Check warnings
- Smooth hover effects on buttons

## Future Enhancements 🔮

Potential improvements for future versions:
- AI opponent with adjustable difficulty
- Game save/load functionality
- PGN import/export
- Time controls
- Online multiplayer
- Sound effects
- Multiple themes
- Chess puzzles mode
- Opening book integration
- Analysis mode with engine evaluation

## Technical Notes 📝

The implementation prioritizes:
1. **Code Quality**: Clean, professional, well-documented code
2. **Performance**: Optimized algorithms and data structures
3. **User Experience**: Intuitive interface with visual feedback
4. **Maintainability**: Modular design for easy enhancement

## License 📄

This is a professional implementation created for educational and entertainment purposes.

## Author ✍️

Developed as a demonstration of professional Python programming with emphasis on functional programming paradigms, performance optimization, and modern GUI design.

---

Enjoy playing this beautiful, efficient implementation of the classic game of Chess! ♔♕♖♗♘♙