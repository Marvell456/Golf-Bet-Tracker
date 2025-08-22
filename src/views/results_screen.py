from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGroupBox, QGridLayout, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import pyqtSignal, Qt


class ResultsScreen(QWidget):
    # Signal emitted when the user wants to continue to the next hole
    continue_signal = pyqtSignal()
    
    def __init__(self, game, hole_number):
        super().__init__()
        self.game = game
        self.hole_number = hole_number
        self.hole = game.holes[hole_number]
        self.init_ui()
        
    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header_label = QLabel(f"Results for Hole {self.hole_number}")
        header_label.setObjectName("headerLabel")
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label)
        
        # Card-style form container
        results_container = QWidget()
        results_container.setObjectName("card")
        results_layout = QVBoxLayout(results_container)
        
        # Hole info
        hole_info = QLabel(f"Value: {self.hole.value}, Par: {self.hole.par}")
        hole_info.setAlignment(Qt.AlignCenter)
        results_layout.addWidget(hole_info)
        
        # Scores table
        scores_group = QGroupBox("Scores")
        scores_layout = QVBoxLayout()
        
        scores_table = QTableWidget()
        scores_table.setColumnCount(2)
        scores_table.setHorizontalHeaderLabels(["Player", "Score"])
        scores_table.setRowCount(len(self.game.players))
        scores_table.horizontalHeader().setStretchLastSection(True)
        
        for i, (player_name, score) in enumerate(self.hole.player_scores.items()):
            # Player name
            player_item = QTableWidgetItem(player_name)
            scores_table.setItem(i, 0, player_item)
            
            # Score
            score_item = QTableWidgetItem(str(score))
            scores_table.setItem(i, 1, score_item)
        
        scores_layout.addWidget(scores_table)
        scores_group.setLayout(scores_layout)
        results_layout.addWidget(scores_group)
        
        # Payments table
        if self.hole.payments:
            payments_group = QGroupBox("Payments")
            payments_layout = QVBoxLayout()
            
            payments_table = QTableWidget()
            payments_table.setColumnCount(3)
            payments_table.setHorizontalHeaderLabels(["From", "To", "Amount"])
            
            # Count total payments
            payment_count = 0
            for from_player, to_players in self.hole.payments.items():
                payment_count += len(to_players)
            
            payments_table.setRowCount(payment_count)
            
            # Fill payments table
            row = 0
            for from_player, to_players in self.hole.payments.items():
                for to_player, amount in to_players.items():
                    # From player
                    from_item = QTableWidgetItem(from_player)
                    payments_table.setItem(row, 0, from_item)
                    
                    # To player
                    to_item = QTableWidgetItem(to_player)
                    payments_table.setItem(row, 1, to_item)
                    
                    # Amount
                    amount_item = QTableWidgetItem(str(amount))
                    payments_table.setItem(row, 2, amount_item)
                    
                    row += 1
            
            payments_layout.addWidget(payments_table)
            payments_group.setLayout(payments_layout)
            results_layout.addWidget(payments_group)
        else:
            no_payments = QLabel("No payments for this hole")
            no_payments.setAlignment(Qt.AlignCenter)
            results_layout.addWidget(no_payments)
        
        # Buchi results if applicable
        if self.game.settings.buchi_enabled and self.hole.buchi_participants:
            buchi_group = QGroupBox("Buchi Results")
            buchi_layout = QVBoxLayout()
            
            # Participants
            participants_label = QLabel("Participants: " + ", ".join(self.hole.buchi_participants))
            buchi_layout.addWidget(participants_label)
            
            # Winners
            if self.hole.buchi_winners:
                winners_label = QLabel("Winners: " + ", ".join(self.hole.buchi_winners))
                buchi_layout.addWidget(winners_label)
            else:
                winners_label = QLabel("No winners (or all won)")
                buchi_layout.addWidget(winners_label)
            
            buchi_group.setLayout(buchi_layout)
            results_layout.addWidget(buchi_group)
        
        main_layout.addWidget(results_container)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        next_hole_button = QPushButton("Next Hole")
        next_hole_button.clicked.connect(self.on_continue)
        button_layout.addWidget(next_hole_button)
        
        main_layout.addLayout(button_layout)
        
        # Set the layout
        self.setLayout(main_layout)
    
    def on_continue(self):
        # Emit signal to continue to the next hole
        self.continue_signal.emit()