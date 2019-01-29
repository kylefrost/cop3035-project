<h1 align="center">Boggle Web</h1>
<p align="center">A Florida State University COP 3035 Project<br>
By Kathryn Cotty, Kyle Frost, Alex Keeney, and Jessica Kent</p>

## Prerequisites
  - Python 3.6+ and Pip
  - Requirements from [requirements.txt](requirements.txt)
  - MySQL local database (or connection to database)
  - virtualenv

## How to Run
  1. Create virtualenv & activate
  2. Install requirements from [requirements.txt](requirements.txt)
  3. Populate MySQL databases using [database.sql](database.sql) (if not connecting to remote)
  4. Create `secrets.py` inside [app/main](app/main) (will __NOT__ run without)
  5. Run server with `python boggle.py`
  6. Open http://localhost:5000

## Todo
### Core Gameplay
  - Maximum and minimum number of players
  - Password protected games
  - Play vs. computer
  - Settings (play to N, etc)
  - Boggle Pieces Board
    - Rolling randomly
      - Random side of each piece
      - Random placement on 4x4 board
    - Correct choosing logic (e.g. piece has to be next to the next, no doubling up)
  - Chat system
    - Typing indicator
    - To/From styling
      - Names with messages
      - Users can choose colors??
  - Leaderboard
    - Player list with scores
    - Current player indicator
  - Theme customization
    - Night/Day Switch
      - Manual switch
      - Based on location sunset data
    - Custom colored board
      - Person starting/hosting game picks theme?
  - __*TBD*__
