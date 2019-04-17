<h1 align="center">Woggle</h1>
<p align="center">A Florida State University COP 3035 Project<br>
By Kathryn Crotty, Kyle Frost, Alex Keeney, and Jessica Kent</p>

# Prerequisites
  - Python 3.6+ and Pip
  - Requirements from [requirements.txt](requirements.txt)
  - MySQL local database (or connection to database)
  - virtualenv

# How to Run
  1. Create virtualenv & activate
  2. Install requirements from [requirements.txt](requirements.txt)
  3. Populate MySQL databases using [database.sql](database.sql) (if not connecting to remote)
  4. Create `secrets.py` inside [app/main](app/main) (will __NOT__ run without)
  5. Run server with `python boggle.py`
  6. Open http://localhost:5000

# Plan
## Core
### Rooms
  - Maximum 8 and minimum 2 of players
  - Password protected rooms
  - Server Notifications
    - e.g. "Round is starting...", "That's not a word!", etc
### Gameplay
  - Boggle Pieces Board
    - Rolling randomly
      - Random side of each piece
      - Random placement on 4x4 board
    - Correct choosing logic (e.g. piece has to be next to the next, no doubling up)
  - 1 minute timer to find words
### Scoring
  - Leaderboard
    - Player list with scores
    - Changes after each round
### Word Selection
  - Updating list of words
    - Add words to "box" as players find them
  - Only allow 3+ letter words
  - Check against dictionary
    - Everytime someone submits word, check
  - Show everyone's word lists after each round to show scoring
### Chat
  - Chat system
    - To/From styling
      - Names with messages
  - Include relevant server messages
    - e.g. "User X has entered the room", etc
