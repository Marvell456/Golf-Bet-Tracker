from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QHBoxLayout, QHeaderView, QTabWidget
from PyQt5.QtCore import Qt

class ProgressWindow(QWidget):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.setWindowTitle("Game Progress")
        self.setMinimumSize(1600, 900)
        
        # Create layout
        layout = QVBoxLayout()
        layout.setSpacing(30)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Title and explanation
        title_layout = QVBoxLayout()
        title = QLabel("Game Progress")
        title.setObjectName("headerLabel")
        title.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title)
        
        explanation = QLabel(
            "This window shows the current state of the game.\n"
            "Use the tabs below to view different aspects of the game."
        )
        explanation.setObjectName("infoLabel")
        explanation.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(explanation)
        
        layout.addLayout(title_layout)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Scores tab
        scores_tab = QWidget()
        scores_layout = QVBoxLayout(scores_tab)
        self.scores_table = self.create_scores_table()
        scores_layout.addWidget(self.scores_table)
        self.tab_widget.addTab(scores_tab, "Scores")
        
        # Voor tab (if enabled)
        if self.game.settings.voor_enabled:
            voor_tab = QWidget()
            voor_layout = QVBoxLayout(voor_tab)
            self.voor_table = self.create_voor_table()
            voor_layout.addWidget(self.voor_table)
            self.tab_widget.addTab(voor_tab, "Voor Adjustments")
        
        # Buchi tab (if enabled)
        if self.game.settings.buchi_enabled:
            buchi_tab = QWidget()
            buchi_layout = QVBoxLayout(buchi_tab)
            self.buchi_table = self.create_buchi_table()
            buchi_layout.addWidget(self.buchi_table)
            self.tab_widget.addTab(buchi_tab, "Buchi")
        
        # Payments tab
        payments_tab = QWidget()
        payments_layout = QVBoxLayout(payments_tab)
        self.payments_table = self.create_payments_table()
        payments_layout.addWidget(self.payments_table)
        self.tab_widget.addTab(payments_tab, "Payments")
        
        layout.addWidget(self.tab_widget)
        
        self.setLayout(layout)
        self.update_all_tables()
    
    def create_scores_table(self):
        table = QTableWidget()
        table.setColumnCount(len(self.game.players) + 1)  # +1 for hole number
        table.setHorizontalHeaderLabels(["Hole"] + list(self.game.players.keys()))
        self.setup_table_style(table)
        return table
    
    def create_voor_table(self):
        table = QTableWidget()
        table.setColumnCount(len(self.game.players) + 1)  # +1 for hole number
        table.setHorizontalHeaderLabels(["Hole"] + list(self.game.players.keys()))
        self.setup_table_style(table)
        return table
    
    def create_buchi_table(self):
        table = QTableWidget()
        table.setColumnCount(len(self.game.players) + 1)  # +1 for hole number
        table.setHorizontalHeaderLabels(["Hole"] + list(self.game.players.keys()))
        self.setup_table_style(table)
        return table
    
    def create_payments_table(self):
        table = QTableWidget()
        table.setColumnCount(4)  # Hole, From, To, Amount
        table.setHorizontalHeaderLabels(["Hole", "From", "To", "Amount"])
        self.setup_table_style(table)
        return table
    
    def setup_table_style(self, table):
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setVisible(False)
        table.setShowGrid(True)
        table.setAlternatingRowColors(True)
        table.setStyleSheet("""
            QTableWidget {
                font-size: 24px;
                gridline-color: #bdc3c7;
            }
            QTableWidget::item {
                padding: 15px;
                min-height: 60px;
            }
            QHeaderView::section {
                font-size: 26px;
                font-weight: bold;
                background-color: #e8e8e8;
                padding: 20px;
                border: 2px solid #dcdde1;
            }
        """)
    
    def update_all_tables(self):
        self.update_scores_table()
        if self.game.settings.voor_enabled:
            self.update_voor_table()
        if self.game.settings.buchi_enabled:
            self.update_buchi_table()
        self.update_payments_table()
    
    def update_scores_table(self):
        self.scores_table.setRowCount(0)
        
        # Add rows for each hole
        for hole_num in range(1, self.game.settings.number_of_holes + 1):
            row_position = self.scores_table.rowCount()
            self.scores_table.insertRow(row_position)
            
            # Add hole number
            hole_item = QTableWidgetItem(str(hole_num))
            hole_item.setTextAlignment(Qt.AlignCenter)
            self.scores_table.setItem(row_position, 0, hole_item)
            
            # Add scores for each player
            for col, player in enumerate(self.game.players, 1):
                score = self.game.get_player_score(hole_num, player)
                if score is not None:
                    # Calculate adjusted score if voor is enabled
                    if self.game.settings.voor_enabled:
                        adjusted_score = self.game.get_adjusted_score(player, hole_num)
                        if adjusted_score != score:
                            score_text = f"{score} ({adjusted_score})"
                        else:
                            score_text = str(score)
                    else:
                        score_text = str(score)
                else:
                    score_text = "-"
                
                score_item = QTableWidgetItem(score_text)
                score_item.setTextAlignment(Qt.AlignCenter)
                self.scores_table.setItem(row_position, col, score_item)
        
        # Add total row
        self.add_total_row(self.scores_table)
    
    def update_voor_table(self):
        self.voor_table.setRowCount(0)
        
        # Add rows for each hole
        for hole_num in range(1, self.game.settings.number_of_holes + 1):
            row_position = self.voor_table.rowCount()
            self.voor_table.insertRow(row_position)
            
            # Add hole number
            hole_item = QTableWidgetItem(str(hole_num))
            hole_item.setTextAlignment(Qt.AlignCenter)
            self.voor_table.setItem(row_position, 0, hole_item)
            
            # Add voor adjustments for each player
            for col, player in enumerate(self.game.players, 1):
                adjustments = []
                for opponent in self.game.players:
                    if opponent != player:
                        adjustment = self.game.players[player].voor_adjustments.get(opponent, 0)
                        if adjustment > 0:
                            adjustments.append(f"{opponent}: -{adjustment}")
                
                if adjustments:
                    text = "\n".join(adjustments)
                else:
                    text = "-"
                
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignCenter)
                self.voor_table.setItem(row_position, col, item)
    
    def update_buchi_table(self):
        self.buchi_table.setRowCount(0)
        
        # Add rows for each hole
        for hole_num in range(1, self.game.settings.number_of_holes + 1):
            row_position = self.buchi_table.rowCount()
            self.buchi_table.insertRow(row_position)
            
            # Add hole number
            hole_item = QTableWidgetItem(str(hole_num))
            hole_item.setTextAlignment(Qt.AlignCenter)
            self.buchi_table.setItem(row_position, 0, hole_item)
            
            # Add buchi status for each player
            for col, player in enumerate(self.game.players, 1):
                participated = self.game.players[player].buchi_participations.get(hole_num, False)
                won = self.game.players[player].buchi_wins.get(hole_num, False)
                
                if participated:
                    text = "✓" if won else "✗"
                else:
                    text = "-"
                
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignCenter)
                self.buchi_table.setItem(row_position, col, item)
    
    def update_payments_table(self):
        self.payments_table.setRowCount(0)
        row = 0
        
        # Add payments for each hole
        for hole_num in range(1, self.game.settings.number_of_holes + 1):
            hole = self.game.holes.get(hole_num)
            if hole and hole.payments:
                for from_player, to_players in hole.payments.items():
                    for to_player, amount in to_players.items():
                        self.payments_table.insertRow(row)
                        
                        # Hole number
                        hole_item = QTableWidgetItem(str(hole_num))
                        hole_item.setTextAlignment(Qt.AlignCenter)
                        self.payments_table.setItem(row, 0, hole_item)
                        
                        # From player
                        from_item = QTableWidgetItem(from_player)
                        from_item.setTextAlignment(Qt.AlignCenter)
                        self.payments_table.setItem(row, 1, from_item)
                        
                        # To player
                        to_item = QTableWidgetItem(to_player)
                        to_item.setTextAlignment(Qt.AlignCenter)
                        self.payments_table.setItem(row, 2, to_item)
                        
                        # Amount
                        amount_item = QTableWidgetItem(str(amount))
                        amount_item.setTextAlignment(Qt.AlignCenter)
                        self.payments_table.setItem(row, 3, amount_item)
                        
                        row += 1
    
    def add_total_row(self, table):
        total_row = table.rowCount()
        table.insertRow(total_row)
        
        # Add "Total" label
        total_label = QTableWidgetItem("Total")
        total_label.setTextAlignment(Qt.AlignCenter)
        total_label.setBackground(Qt.lightGray)
        table.setItem(total_row, 0, total_label)
        
        # Add totals for each player
        for col, player in enumerate(self.game.players, 1):
            total = self.game.get_total_score(player)
            if total is not None:
                # Calculate adjusted total if voor is enabled
                if self.game.settings.voor_enabled:
                    adjusted_total = self.game.get_adjusted_total_score(player)
                    if adjusted_total != total:
                        total_text = f"{total} ({adjusted_total})"
                    else:
                        total_text = str(total)
                else:
                    total_text = str(total)
            else:
                total_text = "-"
            
            total_item = QTableWidgetItem(total_text)
            total_item.setTextAlignment(Qt.AlignCenter)
            total_item.setBackground(Qt.lightGray)
            table.setItem(total_row, col, total_item)
    
    def update_table(self):
        """Update all tables with current game data"""
        self.update_all_tables() 