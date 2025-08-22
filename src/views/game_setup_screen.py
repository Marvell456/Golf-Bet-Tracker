from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, 
    QComboBox, QPushButton, QGroupBox, QGridLayout, QFormLayout
)
from PyQt5.QtCore import pyqtSignal, Qt


class GameSetupScreen(QWidget):
    # Signal emitted when the user wants to continue to the game
    continue_signal = pyqtSignal()
    
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.init_ui()
        
    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(40, 40, 40, 40)
        
        # Header
        header_label = QLabel("Game Setup")
        header_label.setObjectName("headerLabel")
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label)
        
        # Voor adjustments section
        if self.game.settings.voor_enabled:
            # Explanation card
            explanation_card = QWidget()
            explanation_card.setObjectName("card")
            explanation_layout = QVBoxLayout(explanation_card)
            
            # Title
            title = QLabel("Voor Adjustments")
            title.setObjectName("subHeaderLabel")
            title.setAlignment(Qt.AlignCenter)
            explanation_layout.addWidget(title)
            
            # Detailed explanation
            explanation = QLabel(
                "Voor is a handicap system where players can give strokes to other players.\n\n"
                "How it works:\n"
                "• Each player can give 0-2 strokes to other players\n"
                "• These strokes are subtracted from the receiving player's score\n"
                "• You cannot give strokes to yourself\n\n"
                "Example: If Player 1 gives 2 strokes to Player 2, and Player 2 scores 5 on a hole,\n"
                "their adjusted score would be 3 (5 - 2) when comparing with Player 1."
            )
            explanation.setObjectName("infoLabel")
            explanation.setAlignment(Qt.AlignLeft)
            explanation_layout.addWidget(explanation)
            
            main_layout.addWidget(explanation_card)
            
            # Voor adjustments grid
            voor_group = QGroupBox("Set Voor Adjustments")
            voor_layout = QVBoxLayout()
            
            # Grid for voor adjustments between players
            grid_layout = QGridLayout()
            grid_layout.setSpacing(20)
            
            # Add column headers (players as recipients)
            for col, player_name in enumerate(self.game.players, 1):
                label = QLabel(player_name)
                label.setAlignment(Qt.AlignCenter)
                label.setStyleSheet("""
                    QLabel {
                        font-size: 24px;
                        padding: 10px;
                        font-weight: bold;
                        color: #3498db;
                    }
                """)
                grid_layout.addWidget(label, 0, col)
            
            # Add row headers (players as givers) and spinboxes
            for row, from_player in enumerate(self.game.players, 1):
                # Add row header
                label = QLabel(from_player)
                label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                label.setStyleSheet("""
                    QLabel {
                        font-size: 24px;
                        padding: 10px;
                        font-weight: bold;
                        color: #3498db;
                    }
                """)
                grid_layout.addWidget(label, row, 0)
                
                # Add spinboxes for each combination
                for col, to_player in enumerate(self.game.players, 1):
                    # Can't voor yourself
                    if from_player == to_player:
                        label = QLabel("-")
                        label.setAlignment(Qt.AlignCenter)
                        label.setStyleSheet("""
                            QLabel {
                                font-size: 24px;
                                padding: 10px;
                                color: #95a5a6;
                            }
                        """)
                        grid_layout.addWidget(label, row, col)
                    else:
                        spin_box = QSpinBox()
                        spin_box.setMinimum(0)
                        spin_box.setMaximum(2)
                        spin_box.setValue(0)
                        spin_box.setProperty("from_player", from_player)
                        spin_box.setProperty("to_player", to_player)
                        spin_box.setStyleSheet("""
                            QSpinBox {
                                font-size: 24px;
                                padding: 10px;
                                min-height: 50px;
                            }
                            QSpinBox::up-button, QSpinBox::down-button {
                                width: 40px;
                                height: 40px;
                            }
                        """)
                        grid_layout.addWidget(spin_box, row, col)
            
            voor_layout.addLayout(grid_layout)
            voor_group.setLayout(voor_layout)
            main_layout.addWidget(voor_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        
        continue_button = QPushButton("Continue to Game")
        continue_button.setMinimumWidth(250)
        continue_button.clicked.connect(self.on_continue)
        button_layout.addWidget(continue_button)
        
        main_layout.addLayout(button_layout)
        
        # Set the layout
        self.setLayout(main_layout)
    
    def on_continue(self):
        # Save voor adjustments
        if self.game.settings.voor_enabled:
            for i in range(self.layout().count()):
                widget = self.layout().itemAt(i).widget()
                if isinstance(widget, QGroupBox) and widget.title() == "Set Voor Adjustments":
                    voor_layout = widget.layout()
                    # Find the grid layout
                    for j in range(voor_layout.count()):
                        item = voor_layout.itemAt(j)
                        if isinstance(item, QGridLayout):
                            grid = item
                            # Iterate through all widgets in the grid
                            for k in range(grid.count()):
                                widget = grid.itemAt(k).widget()
                                if isinstance(widget, QSpinBox):
                                    from_player = widget.property("from_player")
                                    to_player = widget.property("to_player")
                                    adjustment = widget.value()
                                    self.game.set_voor_adjustment(from_player, to_player, adjustment)
        
        # Emit signal to continue to the game
        self.continue_signal.emit()