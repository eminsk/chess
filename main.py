#!/usr/bin/env python3
"""
Professional Chess Game - Main Entry Point

Choose between single-player (vs AI) or multiplayer (two players) mode.
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Import the game modules directly
try:
    from chess_game import ChessGUI as SinglePlayerGUI
    from chess_multiplayer import ChessGUI as MultiPlayerGUI
except ImportError as e:
    print(f"Error importing game modules: {e}")
    sys.exit(1)


class GameSelector:
    """Game mode selector GUI"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Professional Chess Game")
        self.root.geometry("400x300")
        self.root.configure(bg='#2B2D42')
        self.root.resizable(False, False)
        
        # Center window
        self.center_window()
        
        # Create UI
        self.create_widgets()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        """Create the selector interface"""
        # Title
        title = tk.Label(
            self.root,
            text="♔ Professional Chess ♚",
            font=('Segoe UI', 24, 'bold'),
            fg='#EDF2F4',
            bg='#2B2D42'
        )
        title.pack(pady=30)
        
        # Subtitle
        subtitle = tk.Label(
            self.root,
            text="Choose Your Game Mode",
            font=('Segoe UI', 14),
            fg='#A8B2C7',
            bg='#2B2D42'
        )
        subtitle.pack(pady=10)
        
        # Button frame
        button_frame = tk.Frame(self.root, bg='#2B2D42')
        button_frame.pack(pady=30)
        
        # Single player button
        single_btn = self.create_button(
            button_frame,
            "🤖 Single Player vs AI",
            "Play against computer opponent",
            self.start_single_player
        )
        single_btn.pack(pady=10)
        
        # Multiplayer button
        multi_btn = self.create_button(
            button_frame,
            "👥 Two Player Mode",
            "Play with a friend locally",
            self.start_multiplayer
        )
        multi_btn.pack(pady=10)
        
        # Exit button
        exit_btn = self.create_button(
            button_frame,
            "❌ Exit",
            "Close the application",
            self.root.quit,
            width=25
        )
        exit_btn.pack(pady=20)
    
    def create_button(self, parent, text, tooltip, command, width=30):
        """Create a styled button with tooltip"""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=('Segoe UI', 12, 'bold'),
            fg='#EDF2F4',
            bg='#8D99AE',
            activebackground='#A8B2C7',
            activeforeground='#EDF2F4',
            relief=tk.FLAT,
            padx=20,
            pady=10,
            width=width,
            cursor='hand2'
        )
        
        # Hover effects
        btn.bind('<Enter>', lambda e: btn.config(bg='#A8B2C7'))
        btn.bind('<Leave>', lambda e: btn.config(bg='#8D99AE'))
        
        # Tooltip (simple implementation)
        def show_tooltip(event):
            # Simple tooltip using window title (basic implementation)
            self.root.title(f"Professional Chess Game - {tooltip}")
        
        def hide_tooltip(event):
            self.root.title("Professional Chess Game")
        
        btn.bind('<Enter>', lambda e: [btn.config(bg='#A8B2C7'), show_tooltip(e)])
        btn.bind('<Leave>', lambda e: [btn.config(bg='#8D99AE'), hide_tooltip(e)])
        
        return btn
    
    def start_single_player(self):
        """Launch single player mode"""
        self.launch_game_direct(SinglePlayerGUI, "Single Player vs AI")
    
    def start_multiplayer(self):
        """Launch multiplayer mode"""
        self.launch_game_direct(MultiPlayerGUI, "Two Player Mode")
    
    def launch_game_direct(self, game_class, game_name):
        """Launch the specified game directly"""
        try:
            # Close selector window
            self.root.destroy()
            
            # Create new root window for the game
            game_root = tk.Tk()
            
            # Launch the game
            game_app = game_class(game_root)
            game_root.mainloop()
            
        except Exception as e:
            messagebox.showerror(
                "Launch Error",
                f"Failed to launch {game_name}:\n{str(e)}"
            )
    
    def run(self):
        """Start the selector"""
        self.root.mainloop()


def main():
    """Main entry point"""
    try:
        selector = GameSelector()
        selector.run()
    except KeyboardInterrupt:
        print("\nGame selector closed by user.")
    except Exception as e:
        print(f"Error starting game selector: {e}")


if __name__ == "__main__":
    main()