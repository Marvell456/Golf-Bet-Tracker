from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, 
    QComboBox, QCheckBox, QPushButton, QGroupBox, QFormLayout
)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QIcon


class StartScreen(QWidget):
    # Signal emitted when the user wants to start the game
    start_game_signal = pyqtSignal()
    
    def __init__(self, game_settings):
        super().__init__()
        self.game_settings = game_settings
        self.init_ui()
        
    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(30)  # Increased spacing
        main_layout.setContentsMargins(40, 40, 40, 40)  # Increased margins
        
        # Header
        header_label = QLabel("Golf Helper")
        header_label.setObjectName("headerLabel")
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label)
        
        # Subheader
        sub_header = QLabel("Setup your game")
        sub_header.setObjectName("subHeaderLabel")
        sub_header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(sub_header)
        
        # Card-style form container
        form_container = QWidget()
        form_container.setObjectName("card")
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(25)  # Increased spacing
        form_layout.setContentsMargins(30, 30, 30, 30)  # Increased margins
        
        # Game settings group
        settings_group = QGroupBox("Game Settings")
        settings_layout = QFormLayout()
        settings_layout.setSpacing(20)  # Increased spacing
        settings_layout.setLabelAlignment(Qt.AlignRight)
        
        # Number of players
        self.player_count = QSpinBox()
        self.player_count.setMinimum(2)
        self.player_count.setMaximum(10)
        self.player_count.setValue(self.game_settings.number_of_players)
        settings_layout.addRow("Number of Players:", self.player_count)
        
        # Number of holes
        self.hole_count = QSpinBox()
        self.hole_count.setMinimum(1)
        self.hole_count.setMaximum(18)
        self.hole_count.setValue(self.game_settings.number_of_holes)
        settings_layout.addRow("Number of Holes:", self.hole_count)
        
        # Game mode
        self.game_mode = QComboBox()
        self.game_mode.addItem("Single Winner", "single_winner")
        self.game_mode.addItem("Face to Face", "face_to_face")
        if self.game_settings.game_mode == "face_to_face":
            self.game_mode.setCurrentIndex(1)
        settings_layout.addRow("Game Mode:", self.game_mode)
        
        # Scoring type
        self.scoring_type = QComboBox()
        self.scoring_type.addItem("Par", "par")
        self.scoring_type.addItem("Bogey", "bogey")
        if self.game_settings.scoring_type == "bogey":
            self.scoring_type.setCurrentIndex(1)
        settings_layout.addRow("Scoring Type:", self.scoring_type)
        
        settings_group.setLayout(settings_layout)
        form_layout.addWidget(settings_group)
        
        # Special rules group
        rules_group = QGroupBox("Special Rules")
        rules_layout = QVBoxLayout()
        rules_layout.setSpacing(25)  # Increased spacing
        
        # Buchi enabled
        self.buchi_enabled = QCheckBox("Enable Buchi")
        self.buchi_enabled.setChecked(True)
        self.buchi_enabled.setStyleSheet("""
            QCheckBox {
                font-size: 24px;
                padding: 15px;
            }
            QCheckBox::indicator {
                width: 30px;
                height: 30px;
            }
        """)
        rules_layout.addWidget(self.buchi_enabled)
        
        # Voor enabled
        self.voor_enabled = QCheckBox("Enable Voor")
        self.voor_enabled.setChecked(True)
        self.voor_enabled.setStyleSheet("""
            QCheckBox {
                font-size: 24px;
                padding: 15px;
            }
            QCheckBox::indicator {
                width: 30px;
                height: 30px;
            }
        """)
        rules_layout.addWidget(self.voor_enabled)
        
        rules_group.setLayout(rules_layout)
        form_layout.addWidget(rules_group)
        
        # Add form to main layout
        main_layout.addWidget(form_container)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)  # Increased spacing
        
        start_button = QPushButton("Start Game")
        start_button.setMinimumWidth(200)  # Set minimum width
        start_button.clicked.connect(self.on_start_game)
        button_layout.addWidget(start_button)
        
        main_layout.addLayout(button_layout)
        
        # Set the layout
        self.setLayout(main_layout)
    
    def on_start_game(self):
        # Save all settings
        self.game_settings.number_of_players = self.player_count.value()
        self.game_settings.number_of_holes = self.hole_count.value()
        self.game_settings.game_mode = self.game_mode.currentData()
        self.game_settings.scoring_type = self.scoring_type.currentData()
        self.game_settings.buchi_enabled = self.buchi_enabled.isChecked()
        self.game_settings.voor_enabled = self.voor_enabled.isChecked()
        
        # Emit signal to start the game
        self.start_game_signal.emit()