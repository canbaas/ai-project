# 🎮 Chess Game - Python Flask Web Application

A fully functional, interactive chess game built with Python Flask and deployed as a web application.

## ✨ Features

- ✅ **Complete Chess Rules** - All pieces move according to official chess rules
- ✅ **Turn-Based Gameplay** - Alternates between White and Black players
- ✅ **Visual Move Indicators** - Green dots for valid moves, red borders for captures
- ✅ **Piece Selection** - Click to select and see all possible moves
- ✅ **Captured Pieces Tracker** - View all captured pieces for both players
- ✅ **Pawn Promotion** - Pawns automatically promote to queens when reaching the end
- ✅ **Game Over Detection** - Win by capturing the opponent's king
- ✅ **New Game Button** - Reset and start fresh anytime
- ✅ **Modern UI** - Clean, responsive design with beautiful gradients

## 🎯 How to Play

1. **Select a Piece**: Click on any piece of your color (White starts first)
2. **See Valid Moves**: Green dots appear on empty squares, red borders on enemy pieces
3. **Make Your Move**: Click on a highlighted square to move there
4. **Capture Pieces**: Move to a square with a red border to capture
5. **Win the Game**: Capture your opponent's king to win!

## 🚀 How to Run Locally

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation Steps

1. **Clone the repository**:
```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
cd YOUR-REPO-NAME
```

2. **Install Flask**:
```bash
pip install flask
```

3. **Run the application**:
```bash
python app.py
```

4. **Open in browser**:
```
http://localhost:5000
```

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with modern gradients and animations
- **Game Logic**: Pure JavaScript with complete chess rules implementation

## 📋 Project Structure
```
chess-game/
│
├── app.py              # Flask application with embedded HTML/CSS/JS
└── README.md           # Project documentation
```

## 🎨 Features Breakdown

### Chess Pieces
- ♔ King - Moves one square in any direction
- ♕ Queen - Moves any number of squares in any direction
- ♜ Rook - Moves horizontally or vertically
- ♝ Bishop - Moves diagonally
- ♞ Knight - Moves in L-shape (2+1 squares)
- ♟ Pawn - Moves forward, captures diagonally

### Special Rules Implemented
- Pawn double move from starting position
- Pawn promotion to queen
- Piece capture mechanics
- Turn-based player switching

## 📸 Screenshots

*Game in progress with valid moves highlighted*

## 🌐 Live Demo

[Play the game online](#) *(Add your deployment link here)*

## 👨‍💻 Development

This project was created as an educational assignment to demonstrate:
- Web application development with Flask
- Interactive UI/UX design
- Game logic implementation
- Clean, maintainable code structure

## 📝 Future Enhancements

- [ ] Check and checkmate detection
- [ ] Castling move
- [ ] En passant capture
- [ ] Move history/undo feature
- [ ] AI opponent
- [ ] Multiplayer online mode
- [ ] Timer/clock feature
- [ ] Save and load games

## 📄 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Suggestions and improvements are welcome! Feel free to fork this repository and submit pull requests.

## 📧 Contact

Created as a project assignment.

---

**⭐ If you like this project, please give it a star!**
