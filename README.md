# Golf-Bet-Tracker
A Python program to assist golf bet calculations. A golf game is full of bets with its own extensive rules. This program is built to assist golf players in calculating how much every player owes each other in a golf game through score, voor, buchi, etc.

# Feature:
- Payment tracking based on buchi, voor, scoring multipliers (par, boogey, eagle, etc), and par
- Score tracking based on inputted score for each hole
- Full GUI program to ensure easy navigation and usage
- Double window pop-up: full game progress (score, voor, par, payment) and the gameplay, aka inputting scores and continuing the gameplay

# Tech Stack:
- PyQt5

# Screenshots:
![Game Setup](screenshots/Game%20Setup.png)

![Voor Adjustments](screenshots/Voor%20Adjustments.png)

![Gameplay](screenshots/Gameplay.png)

![Buchi Gamepla](screenshots/Buchi%20Gameplay.png)

![Round 1 Results](screenshots/Round%201%20Results.png)

![Live Game Progress](screenshots/Live%20Game%20Progress.png)

![Voor Game Progress](screenshots/Voor%20Game%20Progress.png)

![Buchi Game Progress](screenshots/Buchi%20Game%20Progress.png)

![Payment Game Progress](screenshots/Payment%20Game%20Progress.png)

# Installation & Usage
1. Clone the repository:
   git clone https://github.com/Marvell456/Golf-Bet-Tracker.git

2. Install dependencies:
   pip install -r requirements.txt

3. Run the program:
   python main.py

# Future Improvements
- Add buchi value
- Fix bugs
- Easier GUI navigation
- Downloadable on Android (Maybe using React + Expo)

# Why I Built This
I built this because my Dad wanted an app that could make calculating golf bets easier. He told me about how he and his friends had to calculate one by one, based on his notes after every golf game, to determine how much each person owes each others. It is frustrating, hideous, and time-wasting. Thus, I made him this program so that he can easily input his scores and his friends and output a result for how much each person owes the others. I hope that this will help him save time and effort and focus on having fun with his friends.
