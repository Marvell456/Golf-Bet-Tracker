from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, 
    QPushButton, QGroupBox, QFormLayout
)
from PyQt5.QtCore import pyqtSignal, Qt


class HoleScreen(QWidget):
    # Signal emitted when the user wants to continue to the next hole
    continue_signal = pyqtSignal()
    
    def __init__(self, game, hole_number):
        super().__init__()
        self.game = game
        self.hole_number = hole_number
        self.player_score_inputs = {}
        self.init_ui()
        
    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header_label = QLabel(f"Hole {self.hole_number}")
        header_label.setObjectName("headerLabel")
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label)
        
        # Card-style form container
        form_container = QWidget()
        form_container.setObjectName("card")
        form_layout = QVBoxLayout(form_container)
        
        # Hole details group
        hole_group = QGroupBox("Hole Details")
        hole_layout = QFormLayout()
        
        # Hole value
        self.hole_value = QSpinBox()
        self.hole_value.setMinimum(1)
        self.hole_value.setMaximum(1000)
        self.hole_value.setValue(10)  # Default value
        hole_layout.addRow("Value:", self.hole_value)
        
        # Par for the hole
        self.hole_par = QSpinBox()
        self.hole_par.setMinimum(1)
        self.hole_par.setMaximum(10)
        self.hole_par.setValue(3)  # Default value
        hole_layout.addRow("Par:", self.hole_par)
        
        hole_group.setLayout(hole_layout)
        form_layout.addWidget(hole_group)
        
        # Player scores group
        scores_group = QGroupBox("Player Scores")
        scores_layout = QFormLayout()
        
        # Add input for each player's score
        for player_name in self.game.players:
            spin_box = QSpinBox()
            spin_box.setMinimum(1)
            spin_box.setMaximum(20)
            spin_box.setValue(self.hole_par.value())  # Default to par
            self.player_score_inputs[player_name] = spin_box
            scores_layout.addRow(f"{player_name}:", spin_box)
            
            # Connect par value changes to update default scores
            self.hole_par.valueChanged.connect(
                lambda value, sb=spin_box: sb.setValue(value) if sb.value() == sb.property("last_par") else None)
            spin_box.setProperty("last_par", self.hole_par.value())
        
        # Update last_par property when par changes
        self.hole_par.valueChanged.connect(
            lambda value: [spin_box.setProperty("last_par", value) for spin_box in self.player_score_inputs.values()])
        
        scores_group.setLayout(scores_layout)
        form_layout.addWidget(scores_group)
        
        main_layout.addWidget(form_container)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        continue_button = QPushButton("Continue")
        continue_button.clicked.connect(self.on_continue)
        button_layout.addWidget(continue_button)
        
        main_layout.addLayout(button_layout)
        
        # Set the layout
        self.setLayout(main_layout)
    
    def on_continue(self):
        # Save hole details
        hole_value = self.hole_value.value()
        hole_par = self.hole_par.value()
        
        # Update the hole in the game
        hole = self.game.holes[self.hole_number]
        hole.value = hole_value
        hole.par = hole_par
        
        # Save player scores
        for player_name, spin_box in self.player_score_inputs.items():
            score = spin_box.value()
            self.game.set_player_score(self.hole_number, player_name, score)
        
        # Emit signal to continue
        self.continue_signal.emit()