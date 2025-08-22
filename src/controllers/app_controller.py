from PyQt5.QtWidgets import QMainWindow

from src.models.game import Game, GameSettings
from src.views.start_screen import StartScreen
from src.views.game_setup_screen import GameSetupScreen
from src.views.hole_screen import HoleScreen
from src.views.buchi_screen import BuchiScreen
from src.views.results_screen import ResultsScreen
from src.views.final_results_screen import FinalResultsScreen
from src.views.progress_window import ProgressWindow


class AppController:
    def __init__(self):
        self.main_window = QMainWindow()
        self.main_window.setWindowTitle("Golf Helper")
        self.main_window.setMinimumSize(1200, 800)
        
        self.game_settings = GameSettings()
        self.game = None
        self.progress_window = None
        
        # Initialize screens (they'll be created when needed)
        self.start_screen = None
        self.game_setup_screen = None
        self.hole_screen = None
        self.buchi_screen = None
        self.results_screen = None
        self.final_results_screen = None

    def show_start_screen(self):
        """Show the initial game setup screen."""
        self.start_screen = StartScreen(self.game_settings)
        self.start_screen.start_game_signal.connect(self.on_start_game)
        
        self.main_window.setCentralWidget(self.start_screen)
        self.main_window.show()

    def on_start_game(self):
        """Handler for when the user wants to start a new game."""
        # Initialize the game with current settings
        self.game = Game(self.game_settings)
        
        # Add players
        for i in range(1, self.game_settings.number_of_players + 1):
            player_name = f"Player {i}"
            self.game.add_player(player_name)
        
        # Create and show progress window
        self.progress_window = ProgressWindow(self.game)
        self.progress_window.show()
        
        # Show game setup screen for voor adjustments if needed
        if self.game_settings.voor_enabled:
            self.show_game_setup_screen()
        else:
            # Skip to first hole if voor not enabled
            self.show_next_hole()

    def show_game_setup_screen(self):
        """Show the game setup screen for voor adjustments."""
        self.game_setup_screen = GameSetupScreen(self.game)
        self.game_setup_screen.continue_signal.connect(self.show_next_hole)
        
        self.main_window.setCentralWidget(self.game_setup_screen)

    def show_next_hole(self):
        """Show the screen for the next hole."""
        current_hole = self.game.current_hole
        
        # Check if we've completed all holes
        if current_hole > self.game_settings.number_of_holes:
            self.show_final_results()
            return
            
        # Create a new hole in the game
        self.game.add_hole(current_hole, 0, 0)  # Default values will be set by user
        
        # Show the hole screen
        self.hole_screen = HoleScreen(self.game, current_hole)
        self.hole_screen.continue_signal.connect(self.on_hole_completed)
        
        self.main_window.setCentralWidget(self.hole_screen)

    def on_hole_completed(self):
        """Handler for when a hole is completed."""
        # Show buchi screen if enabled
        if self.game.settings.buchi_enabled:
            self.show_buchi_screen(self.game.current_hole)
        else:
            # Calculate payments for the current hole
            self.game.calculate_payments_for_hole(self.game.current_hole)
            # Show results screen
            self.results_screen = ResultsScreen(self.game, self.game.current_hole)
            self.results_screen.continue_signal.connect(self.on_results_acknowledged)
            self.main_window.setCentralWidget(self.results_screen)
        
        # Update progress window
        if hasattr(self, 'progress_window'):
            self.progress_window.update_table()

    def show_buchi_screen(self, hole_number):
        """Show the buchi selection screen."""
        self.buchi_screen = BuchiScreen(self.game, hole_number)
        self.buchi_screen.continue_signal.connect(lambda: self.on_buchi_completed(hole_number))
        
        self.main_window.setCentralWidget(self.buchi_screen)

    def on_buchi_completed(self, hole_number):
        """Handler for when buchi selections are completed."""
        # Calculate payments for this hole (including buchi)
        self.game.calculate_payments_for_hole(hole_number)
        
        # Show results screen
        self.results_screen = ResultsScreen(self.game, hole_number)
        self.results_screen.continue_signal.connect(self.on_results_acknowledged)
        self.main_window.setCentralWidget(self.results_screen)
        
        # Update progress window
        if hasattr(self, 'progress_window'):
            self.progress_window.update_table()

    def show_hole_results(self, hole_number):
        """Show the results for a specific hole."""
        self.results_screen = ResultsScreen(self.game, hole_number)
        self.results_screen.continue_signal.connect(self.on_continue_to_next_hole)
        
        self.main_window.setCentralWidget(self.results_screen)

    def on_continue_to_next_hole(self):
        """Handler for continuing to the next hole."""
        # Increment current hole
        self.game.current_hole += 1
        self.show_next_hole()

    def show_final_results(self):
        """Show the final results screen."""
        # Calculate all payments and optimize them
        self.game.calculate_all_payments()
        
        self.final_results_screen = FinalResultsScreen(self.game)
        self.final_results_screen.new_game_signal.connect(self.on_new_game)
        
        self.main_window.setCentralWidget(self.final_results_screen)

    def on_new_game(self):
        """Handler for starting a new game."""
        # Close progress window if it exists
        if self.progress_window:
            self.progress_window.close()
            self.progress_window = None
            
        # Reset game settings and show start screen
        self.game_settings = GameSettings()
        self.show_start_screen()

    def on_results_acknowledged(self):
        """Handler for when the user acknowledges the results."""
        # Move to next hole
        self.game.current_hole += 1
        
        # Show next hole or final results
        if self.game.current_hole <= self.game_settings.number_of_holes:
            self.show_next_hole()
        else:
            self.show_final_results()
            
        # Update progress window
        if hasattr(self, 'progress_window'):
            self.progress_window.update_table()