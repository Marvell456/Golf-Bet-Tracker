from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGroupBox, QGridLayout, QTableWidget, QTableWidgetItem, QTabWidget
)
from PyQt5.QtCore import pyqtSignal, Qt


class FinalResultsScreen(QWidget):
    # Signal emitted when the user wants to start a new game
    new_game_signal = pyqtSignal()
    
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.init_ui()
        
    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header_label = QLabel("Final Results")
        header_label.setObjectName("headerLabel")
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label)
        
        # Tabs for different result views
        tabs = QTabWidget()
        
        # Tab for hole-by-hole results
        hole_tab = QWidget()
        hole_layout = QVBoxLayout(hole_tab)
        self.create_hole_by_hole_view(hole_layout)
        tabs.addTab(hole_tab, "Hole by Hole")
        
        # Tab for player summary
        player_tab = QWidget()
        player_layout = QVBoxLayout(player_tab)
        self.create_player_summary_view(player_layout)
        tabs.addTab(player_tab, "Player Summary")
        
        # Tab for final payments
        payments_tab = QWidget()
        payments_layout = QVBoxLayout(payments_tab)
        self.create_final_payments_view(payments_layout)
        tabs.addTab(payments_tab, "Final Payments")
        
        main_layout.addWidget(tabs)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        new_game_button = QPushButton("New Game")
        new_game_button.clicked.connect(self.on_new_game)
        button_layout.addWidget(new_game_button)
        
        main_layout.addLayout(button_layout)
        
        # Set the layout
        self.setLayout(main_layout)
    
    def create_hole_by_hole_view(self, layout):
        """Create the hole-by-hole results view."""
        # Scrollable container for all holes
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        # Add a section for each hole
        for hole_number, hole in sorted(self.game.holes.items()):
            hole_group = QGroupBox(f"Hole {hole_number}")
            hole_layout = QVBoxLayout()
            
            # Hole info
            hole_info = QLabel(f"Value: {hole.value}, Par: {hole.par}")
            hole_layout.addWidget(hole_info)
            
            # Scores table
            scores_table = QTableWidget()
            scores_table.setColumnCount(2)
            scores_table.setHorizontalHeaderLabels(["Player", "Score"])
            scores_table.setRowCount(len(hole.player_scores))
            
            for i, (player, score) in enumerate(hole.player_scores.items()):
                player_item = QTableWidgetItem(player)
                scores_table.setItem(i, 0, player_item)
                
                score_item = QTableWidgetItem(str(score))
                scores_table.setItem(i, 1, score_item)
            
            hole_layout.addWidget(scores_table)
            
            # Payments if any
            if hole.payments:
                payments_label = QLabel("Payments:")
                hole_layout.addWidget(payments_label)
                
                payments_table = QTableWidget()
                payments_table.setColumnCount(3)
                payments_table.setHorizontalHeaderLabels(["From", "To", "Amount"])
                
                # Count total payments
                payment_count = 0
                for from_player, to_players in hole.payments.items():
                    payment_count += len(to_players)
                
                payments_table.setRowCount(payment_count)
                
                # Fill payments table
                row = 0
                for from_player, to_players in hole.payments.items():
                    for to_player, amount in to_players.items():
                        payments_table.setItem(row, 0, QTableWidgetItem(from_player))
                        payments_table.setItem(row, 1, QTableWidgetItem(to_player))
                        payments_table.setItem(row, 2, QTableWidgetItem(str(amount)))
                        row += 1
                
                hole_layout.addWidget(payments_table)
            else:
                no_payments = QLabel("No payments for this hole")
                hole_layout.addWidget(no_payments)
            
            hole_group.setLayout(hole_layout)
            scroll_layout.addWidget(hole_group)
        
        layout.addWidget(scroll_content)
    
    def create_player_summary_view(self, layout):
        """Create the player summary view."""
        # Calculate total scores and payments for each player
        player_summary = {}
        
        for player_name in self.game.players:
            # Initialize summary
            player_summary[player_name] = {
                "total_score": 0,
                "paid": 0,
                "received": 0,
                "net": 0
            }
            
            # Sum up scores
            for hole_number, hole in self.game.holes.items():
                if player_name in hole.player_scores:
                    player_summary[player_name]["total_score"] += hole.player_scores[player_name]
            
            # Calculate payments
            for hole_number, hole in self.game.holes.items():
                # Payments made
                if player_name in hole.payments:
                    for recipient, amount in hole.payments[player_name].items():
                        player_summary[player_name]["paid"] += amount
                
                # Payments received
                for payer, recipients in hole.payments.items():
                    if player_name in recipients:
                        player_summary[player_name]["received"] += recipients[player_name]
            
            # Calculate net
            player_summary[player_name]["net"] = player_summary[player_name]["received"] - player_summary[player_name]["paid"]
        
        # Create summary table
        summary_table = QTableWidget()
        summary_table.setColumnCount(5)
        summary_table.setHorizontalHeaderLabels(["Player", "Total Score", "Paid", "Received", "Net"])
        summary_table.setRowCount(len(player_summary))
        
        for i, (player, data) in enumerate(player_summary.items()):
            summary_table.setItem(i, 0, QTableWidgetItem(player))
            summary_table.setItem(i, 1, QTableWidgetItem(str(data["total_score"])))
            summary_table.setItem(i, 2, QTableWidgetItem(str(data["paid"])))
            summary_table.setItem(i, 3, QTableWidgetItem(str(data["received"])))
            
            net_item = QTableWidgetItem(str(data["net"]))
            # Color net item based on value
            if data["net"] > 0:
                net_item.setBackground(Qt.green)
            elif data["net"] < 0:
                net_item.setBackground(Qt.red)
            
            summary_table.setItem(i, 4, net_item)
        
        layout.addWidget(summary_table)
    
    def create_final_payments_view(self, layout):
        """Create the final payments view."""
        if not self.game.final_payments:
            no_payments = QLabel("No final payments to settle")
            layout.addWidget(no_payments)
            return
        
        # Final payments table
        payments_table = QTableWidget()
        payments_table.setColumnCount(3)
        payments_table.setHorizontalHeaderLabels(["From", "To", "Amount"])
        
        # Count total payments
        payment_count = 0
        for payer, recipients in self.game.final_payments.items():
            payment_count += len(recipients)
        
        payments_table.setRowCount(payment_count)
        
        # Fill payments table
        row = 0
        for payer, recipients in self.game.final_payments.items():
            for recipient, amount in recipients.items():
                payments_table.setItem(row, 0, QTableWidgetItem(payer))
                payments_table.setItem(row, 1, QTableWidgetItem(recipient))
                payments_table.setItem(row, 2, QTableWidgetItem(str(amount)))
                row += 1
        
        layout.addWidget(payments_table)
    
    def on_new_game(self):
        # Emit signal to start a new game
        self.new_game_signal.emit()