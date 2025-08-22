class Player:
    def __init__(self, name):
        self.name = name
        self.scores = {}  # hole_number: score
        self.voor_adjustments = {}  # player_name: adjustment
        self.buchi_participations = {}  # hole_number: boolean
        self.buchi_wins = {}  # hole_number: boolean

    def add_score(self, hole_number, score):
        self.scores[hole_number] = score

    def add_voor_adjustment(self, player_name, adjustment):
        self.voor_adjustments[player_name] = adjustment

    def set_buchi_participation(self, hole_number, participated):
        self.buchi_participations[hole_number] = participated

    def set_buchi_win(self, hole_number, won):
        self.buchi_wins[hole_number] = won

    def get_adjusted_score(self, hole_number, opponent_name):
        """Get score adjusted by voor."""
        score = self.scores.get(hole_number, 0)
        voor_adjustment = self.voor_adjustments.get(opponent_name, 0)
        return score - voor_adjustment


class GameSettings:
    def __init__(self):
        self.number_of_players = 2
        self.number_of_holes = 9
        self.game_mode = "single_winner"  # or "face_to_face"
        self.buchi_enabled = False
        self.scoring_type = "par"  # or "bogey"
        self.voor_enabled = False


class HoleData:
    def __init__(self, hole_number, value=0, par=0):
        self.hole_number = hole_number
        self.value = value
        self.par = par
        self.player_scores = {}  # player_name: score
        self.buchi_participants = []
        self.buchi_winners = []
        self.payments = {}  # from_player: {to_player: amount}

    def add_player_score(self, player_name, score):
        self.player_scores[player_name] = score

    def add_buchi_participant(self, player_name):
        if player_name not in self.buchi_participants:
            self.buchi_participants.append(player_name)

    def add_buchi_winner(self, player_name):
        if player_name not in self.buchi_winners:
            self.buchi_winners.append(player_name)

    def record_payment(self, from_player, to_player, amount):
        if from_player not in self.payments:
            self.payments[from_player] = {}
        
        # Add to existing payment if it exists, otherwise create new one
        if to_player in self.payments[from_player]:
            self.payments[from_player][to_player] += amount
        else:
            self.payments[from_player][to_player] = amount


class Game:
    def __init__(self, settings):
        self.settings = settings
        self.players = {}  # player_name: Player object
        self.holes = {}  # hole_number: HoleData
        self.current_hole = 1
        self.final_payments = {}  # from_player: {to_player: amount}

    def add_player(self, player_name):
        self.players[player_name] = Player(player_name)

    def add_hole(self, hole_number, value, par):
        self.holes[hole_number] = HoleData(hole_number, value, par)

    def set_player_score(self, hole_number, player_name, score):
        if hole_number in self.holes and player_name in self.players:
            self.holes[hole_number].add_player_score(player_name, score)
            self.players[player_name].add_score(hole_number, score)

    def set_voor_adjustment(self, player_name, opponent_name, adjustment):
        if player_name in self.players and opponent_name in self.players:
            self.players[player_name].add_voor_adjustment(opponent_name, adjustment)

    def set_buchi_participation(self, hole_number, player_name, participated):
        if hole_number in self.holes and player_name in self.players:
            self.players[player_name].set_buchi_participation(hole_number, participated)
            if participated:
                self.holes[hole_number].add_buchi_participant(player_name)

    def set_buchi_win(self, hole_number, player_name, won):
        if hole_number in self.holes and player_name in self.players:
            self.players[player_name].set_buchi_win(hole_number, won)
            if won:
                self.holes[hole_number].add_buchi_winner(player_name)

    def calculate_payments_for_hole(self, hole_number):
        """Calculate payments for a specific hole based on game rules."""
        if hole_number not in self.holes:
            return
            
        hole = self.holes[hole_number]
        
        # First calculate main game payments
        if self.settings.game_mode == "single_winner":
            self._calculate_single_winner_payments(hole)
        else:  # face_to_face
            self._calculate_face_to_face_payments(hole)
            
        # Then calculate buchi payments if enabled
        if self.settings.buchi_enabled and hole.buchi_participants:
            self._calculate_buchi_payments(hole)

    def _calculate_single_winner_payments(self, hole):
        """Calculate payments for Single Winner mode."""
        scores = {}
        
        # Get adjusted scores considering voor
        for player_name in self.players:
            min_score = float('inf')
            for opponent_name in self.players:
                if player_name != opponent_name:
                    adjusted_score = self.players[player_name].get_adjusted_score(
                        hole.hole_number, opponent_name)
                    min_score = min(min_score, adjusted_score)
            
            scores[player_name] = min_score if min_score != float('inf') else hole.player_scores.get(player_name, 0)
        
        # Find the minimum score
        min_score = min(scores.values()) if scores else 0
        winners = [p for p, s in scores.items() if s == min_score]
        
        # If there's more than one winner, no payments
        if len(winners) > 1:
            return
            
        winner = winners[0]
        winner_score = min_score
        
        # Calculate payment multiplier based on score relative to par
        multiplier = 1
        print(f"Winner score: {winner_score}, Par: {hole.par}")  # Debug log
        if winner_score == 1:  # Hole in one
            multiplier = 8
            print("Hole in one - 8x multiplier")  # Debug log
        elif winner_score == hole.par - 2:  # 2 below par
            multiplier = 4
            print("2 below par - 4x multiplier")  # Debug log
        elif winner_score == hole.par - 1:  # 1 below par
            multiplier = 2
            print("1 below par - 2x multiplier")  # Debug log
        elif winner_score == hole.par:  # At par
            multiplier = 1
            print("At par - 1x multiplier")  # Debug log
        elif winner_score > hole.par:
            if self.settings.scoring_type == "par":
                # Above par in par mode - no payments
                print("Above par in par mode - no payment")  # Debug log
                return
            else:  # bogey mode
                multiplier = 0.5
                print("Above par in bogey mode - 0.5x multiplier")  # Debug log
            
        # Record payments
        for player_name, score in scores.items():
            if player_name != winner and score > winner_score:
                payment = hole.value * multiplier
                print(f"Payment from {player_name} to {winner}: {payment} (value: {hole.value}, multiplier: {multiplier})")  # Debug log
                hole.record_payment(player_name, winner, payment)

    def _calculate_face_to_face_payments(self, hole):
        """Calculate payments for Face to Face mode."""
        # Get all players and their scores
        players = list(self.players.keys())
        scores = {player: hole.player_scores.get(player, 0) for player in players}
        
        # Process each player only once
        for i in range(len(players)):
            player1 = players[i]
            player1_score = scores[player1]
            
            # Compare with remaining players
            for j in range(i + 1, len(players)):
                player2 = players[j]
                player2_score = scores[player2]
                
                # Adjust scores based on voor
                adjusted_player1_score = self.players[player1].get_adjusted_score(
                    hole.hole_number, player2)
                adjusted_player2_score = self.players[player2].get_adjusted_score(
                    hole.hole_number, player1)
                
                # Skip if scores are equal after adjustment
                if adjusted_player1_score == adjusted_player2_score:
                    continue
                
                # Determine winner and loser
                if adjusted_player1_score < adjusted_player2_score:
                    winner, loser = player1, player2
                    winner_score = player1_score
                else:
                    winner, loser = player2, player1
                    winner_score = player2_score
                
                # Calculate payment amount
                multiplier = 1
                print(f"Winner score: {winner_score}, Par: {hole.par}")  # Debug log
                if winner_score == 1:  # Hole in one
                    multiplier = 8
                    print("Hole in one - 8x multiplier")  # Debug log
                elif winner_score == hole.par - 2:  # 2 below par
                    multiplier = 4
                    print("2 below par - 4x multiplier")  # Debug log
                elif winner_score == hole.par - 1:  # 1 below par
                    multiplier = 2
                    print("1 below par - 2x multiplier")  # Debug log
                elif winner_score == hole.par:  # At par
                    multiplier = 1
                    print("At par - 1x multiplier")  # Debug log
                elif winner_score > hole.par:
                    if self.settings.scoring_type == "par":
                        # Above par in par mode - no payments
                        print("Above par in par mode - no payment")  # Debug log
                        continue
                    else:  # bogey mode
                        multiplier = 0.5
                        print("Above par in bogey mode - 0.5x multiplier")  # Debug log
                
                payment = hole.value * multiplier
                print(f"Payment from {loser} to {winner}: {payment} (value: {hole.value}, multiplier: {multiplier})")  # Debug log
                
                # Clear any existing payment between these players before recording new one
                if loser in hole.payments and winner in hole.payments[loser]:
                    del hole.payments[loser][winner]
                
                hole.record_payment(loser, winner, payment)

    def _calculate_buchi_payments(self, hole):
        """Calculate Buchi payments."""
        # If all or none of the participants won, no payments
        if not hole.buchi_winners or len(hole.buchi_winners) == len(hole.buchi_participants):
            return
            
        # Calculate payments from losers to winners
        losers = [p for p in hole.buchi_participants if p not in hole.buchi_winners]
        
        for loser in losers:
            for winner in hole.buchi_winners:
                # Pay only the hole value for buchi winners
                hole.record_payment(loser, winner, hole.value)

    def calculate_all_payments(self):
        """Calculate payments for all holes and optimize final payments."""
        # Calculate payments for each hole
        for hole_number in self.holes:
            self.calculate_payments_for_hole(hole_number)
            
        # Initialize final payments
        for player in self.players:
            self.final_payments[player] = {}
        
        # Sum up all payments across holes
        for hole_number, hole in self.holes.items():
            for payer, recipients in hole.payments.items():
                for recipient, amount in recipients.items():
                    if recipient not in self.final_payments[payer]:
                        self.final_payments[payer][recipient] = 0
                    self.final_payments[payer][recipient] += amount
        
        # Optimize payments
        self._optimize_payments()

    def _optimize_payments(self):
        """Optimize payments to minimize transactions."""
        # Create a copy of current payments
        optimized_payments = {}
        for payer in self.final_payments:
            optimized_payments[payer] = self.final_payments[payer].copy()
        
        # Find reciprocal payments and cancel them out
        for payer, recipients in list(optimized_payments.items()):
            for recipient, amount in list(recipients.items()):
                # Check if recipient also pays the payer
                if recipient in optimized_payments and payer in optimized_payments[recipient]:
                    reciprocal_amount = optimized_payments[recipient][payer]
                    
                    # If amounts are equal, cancel both
                    if amount == reciprocal_amount:
                        del optimized_payments[payer][recipient]
                        del optimized_payments[recipient][payer]
                    # If payer pays more
                    elif amount > reciprocal_amount:
                        optimized_payments[payer][recipient] -= reciprocal_amount
                        del optimized_payments[recipient][payer]
                    # If recipient pays more
                    else:
                        optimized_payments[recipient][payer] -= amount
                        del optimized_payments[payer][recipient]
        
        # Update final payments
        self.final_payments = optimized_payments
        
        # Remove empty payment entries
        for payer in list(self.final_payments.keys()):
            if not self.final_payments[payer]:
                del self.final_payments[payer]

    def get_hole_par(self, hole_number):
        """Get the par for a specific hole"""
        if hole_number in self.holes:
            return self.holes[hole_number].par
        return None

    def get_player_score(self, hole_number, player_name):
        """Get a player's score for a specific hole"""
        if hole_number in self.holes and player_name in self.players:
            return self.holes[hole_number].player_scores.get(player_name)
        return None

    def get_total_score(self, player_name):
        """Get a player's total score across all holes"""
        if player_name not in self.players:
            return None
            
        total = 0
        for hole_number in range(1, self.settings.number_of_holes + 1):
            score = self.get_player_score(hole_number, player_name)
            if score is not None:
                total += score
        return total

    def get_adjusted_total_score(self, player_name):
        """Get a player's total score adjusted by voor across all holes"""
        if player_name not in self.players or not self.settings.voor_enabled:
            return self.get_total_score(player_name)
            
        total = 0
        for hole_number in range(1, self.settings.number_of_holes + 1):
            score = self.get_player_score(hole_number, player_name)
            if score is not None:
                # Find minimum adjusted score against all opponents
                min_adjusted = float('inf')
                for opponent in self.players:
                    if opponent != player_name:
                        adjusted = self.players[player_name].get_adjusted_score(hole_number, opponent)
                        min_adjusted = min(min_adjusted, adjusted)
                if min_adjusted != float('inf'):
                    total += min_adjusted
                else:
                    total += score
        return total

    def get_adjusted_score(self, player_name, hole_number):
        """Get a player's score adjusted by voor for a specific hole"""
        if not self.settings.voor_enabled or player_name not in self.players:
            return self.get_player_score(hole_number, player_name)
            
        score = self.get_player_score(hole_number, player_name)
        if score is None:
            return None
            
        # Find minimum adjusted score against all opponents
        min_adjusted = float('inf')
        for opponent in self.players:
            if opponent != player_name:
                adjusted = self.players[player_name].get_adjusted_score(hole_number, opponent)
                min_adjusted = min(min_adjusted, adjusted)
                
        return min_adjusted if min_adjusted != float('inf') else score