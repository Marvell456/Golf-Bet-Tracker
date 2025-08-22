from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox,
    QPushButton, QGroupBox, QFormLayout, QMessageBox
)
from PyQt5.QtCore import pyqtSignal, Qt


class BuchiScreen(QWidget):
    # Signal emitted when the user wants to continue
    continue_signal = pyqtSignal()
    
    def __init__(self, game, hole_number):
        super().__init__()
        self.game = game
        self.hole_number = hole_number
        self.participant_checkboxes = {}
        self.winner_checkboxes = {}
        self.init_ui()
        
    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header_label = QLabel(f"Buchi for Hole {self.hole_number}")
        header_label.setObjectName("headerLabel")
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label)
        
        # Card-style form container
        form_container = QWidget()
        form_container.setObjectName("card")
        form_layout = QVBoxLayout(form_container)
        
        # Buchi participants group
        participants_group = QGroupBox("Who played Buchi?")
        participants_layout = QVBoxLayout()
        
        # Add checkbox for each player
        for player_name in self.game.players:
            checkbox = QCheckBox(player_name)
            self.participant_checkboxes[player_name] = checkbox
            participants_layout.addWidget(checkbox)
        
        participants_group.setLayout(participants_layout)
        form_layout.addWidget(participants_group)
        
        # Buchi winners group (initially hidden, will be shown if needed)
        self.winners_group = QGroupBox("Who won Buchi?")
        self.winners_layout = QVBoxLayout()
        
        # Winners will be added dynamically based on participants
        self.winners_group.setLayout(self.winners_layout)
        self.winners_group.hide()  # Hide initially
        form_layout.addWidget(self.winners_group)
        
        # Connect participant checkboxes to update winners
        for checkbox in self.participant_checkboxes.values():
            checkbox.stateChanged.connect(self.update_winner_options)
        
        main_layout.addWidget(form_container)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        continue_button = QPushButton("Continue")
        continue_button.clicked.connect(self.on_continue)
        button_layout.addWidget(continue_button)
        
        main_layout.addLayout(button_layout)
        
        # Set the layout
        self.setLayout(main_layout)
    
    def update_winner_options(self):
        """Update the winner options based on selected participants."""
        # Clear existing winner checkboxes
        for i in reversed(range(self.winners_layout.count())):
            widget = self.winners_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        
        self.winner_checkboxes = {}
        
        # Get participants
        participants = [name for name, cb in self.participant_checkboxes.items() if cb.isChecked()]
        
        # If there are participants, show the winners group
        if len(participants) >= 2:
            # Add checkbox for each participant
            for player_name in participants:
                checkbox = QCheckBox(player_name)
                self.winner_checkboxes[player_name] = checkbox
                self.winners_layout.addWidget(checkbox)
            
            self.winners_group.show()
        else:
            self.winners_group.hide()
    
    def on_continue(self):
        # Save buchi participants
        participants = []
        for player_name, checkbox in self.participant_checkboxes.items():
            participated = checkbox.isChecked()
            self.game.set_buchi_participation(self.hole_number, player_name, participated)
            if participated:
                participants.append(player_name)
        
        # Save buchi winners if there are participants
        if len(participants) >= 2:
            winners = []
            for player_name, checkbox in self.winner_checkboxes.items():
                if checkbox.isChecked():
                    self.game.set_buchi_win(self.hole_number, player_name, True)
                    winners.append(player_name)
            
            # Validate: either all win or some win
            if len(winners) == len(participants) or len(winners) == 0:
                QMessageBox.warning(
                    self, "Invalid Selection", 
                    "Either some players must win (not all) or no one wins."
                )
                return
        
        # Emit signal to continue
        self.continue_signal.emit()