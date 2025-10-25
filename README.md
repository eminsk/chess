# Professional Chess Game 🎯

A high-performance, memory-efficient Chess game implementation in Python with a beautiful modern GUI. Built using functional programming paradigms to minimize loops and conditionals while maximizing performance.

## Game Versions 🎮

This project includes two versions of the chess game:

### 1. **chess_game.py** - Single Player vs AI
- Play against a computer opponent
- AI automatically plays as Black
- Simple AI that evaluates captures and makes strategic moves
- Perfect for practicing your chess skills

### 2. **chess_multiplayer.py** - Two Player Mode  
- Play with a friend on the same computer
- Hot-seat multiplayer gameplay
- Both players take turns using the same interface
- Ideal for local multiplayer sessions

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

### 🚀 Quick Install (Recommended)

#### Option 1: Download Pre-built Executables
**No Python installation required!**

1. Go to [Releases](https://github.com/eminsk/chess/releases)
2. Download the latest version for your platform:
   - **Windows**: `ChessGame-Windows-v*.zip`
   - **Linux**: `ChessGame-Linux-v*.zip`
   - **macOS**: `ChessGame-macOS-v*.zip`
3. Extract and run - that's it! 🎉

#### Option 2: Run from Source
**For developers and Python users**

##### Prerequisites
- Python 3.8 or higher
- tkinter (usually comes with Python)
- Git (for cloning the repository)

##### Setup
```bash
git clone https://github.com/eminsk/chess.git
cd chess
python main.py
```

### 🔧 For Developers

Want to contribute or modify the code?

```bash
git clone https://github.com/eminsk/chess.git
cd chess
uv sync  # Install dependencies
python main.py  # Run from source
```

Executables are automatically built by GitHub Actions - no need to build locally!

### Project Structure
```
professional-chess-game/
├── chess_game.py          # Single player vs AI
├── chess_multiplayer.py   # Two player mode
├── main.py               # Entry point selector
├── test_chess.py         # Unit tests
├── README.md             # This documentation
├── pyproject.toml        # Project configuration
└── .gitignore           # Git ignore rules
```

## Running the Game 🚀

### Quick Start (Recommended)
```bash
python main.py
```
This will open a game mode selector where you can choose between single-player and multiplayer modes.

### Direct Launch
Choose your preferred game mode:

#### Single Player vs AI
```bash
python chess_game.py
```

#### Two Player Mode
```bash
python chess_multiplayer.py
```

The game window will open centered on your screen with the chess board ready to play.

## How to Play 🎮

### Game Mode Selection (main.py)
When you run `python main.py`, you'll see a beautiful selector interface with three options:
- **🤖 Single Player vs AI**: Challenge the computer opponent
- **👥 Two Player Mode**: Play with a friend on the same computer  
- **❌ Exit**: Close the application

### Gameplay

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

## Releases & Downloads 📦

### 🎯 Latest Release
[![GitHub release](https://img.shields.io/github/v/release/eminsk/chess)](https://github.com/eminsk/chess/releases/latest)
[![GitHub downloads](https://img.shields.io/github/downloads/eminsk/chess/total)](https://github.com/eminsk/chess/releases)

### 🔄 Automatic Releases
This project features automatic releases:
- **Auto-versioning**: New releases are created automatically when the version in `pyproject.toml` is updated
- **Multi-platform builds**: Each release includes executables for Windows, Linux, and macOS
- **Continuous integration**: GitHub Actions automatically builds and tests the code
- **Zero-dependency executables**: No need to install Python or any dependencies

### 📋 Release Contents
Each release includes:
- **Standalone executables** for all major platforms
- **Portable packages** - just extract and run
- **Source code** for developers
- **Comprehensive documentation**

### 🛠️ Development Builds
Want to try the latest features? Development builds are created automatically on every commit to the main branch.

## License 📄

MIT License - see [LICENSE](LICENSE) file for details.

This is a professional implementation created for educational and entertainment purposes.

## Author ✍️

Developed as a demonstration of professional Python programming with emphasis on functional programming paradigms, performance optimization, and modern GUI design.

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
```bash
git clone https://github.com/eminsk/chess.git
cd chess
python -m pip install -e .
```

### Running Tests
```bash
python -m pytest test_chess.py
```

---

Enjoy playing this beautiful, efficient implementation of the classic game of Chess! ♔♕♖♗♘♙