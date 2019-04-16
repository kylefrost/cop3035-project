

function reset() {
  delete(magicNumber);
  delete(output);
  delete(gameBoard);
  delete(tiles);
  delete(clearAll);
  delete(indexTiles);
  delete(clearActiveTiles);
  delete(disableTiles);
  delete(validateTile);
  delete(enableSurroundingTiles);
  delete(clicker);
  delete(submitWord);
}

function setBoggleBoardVariables() {
  delete(magicNumber);
  delete(output);
  delete(gameBoard);
  delete(tiles);
  delete(clearAll);
  delete(indexTiles);
  delete(clearActiveTiles);
  delete(disableTiles);
  delete(validateTile);
  delete(enableSurroundingTiles);
  delete(clicker);
  delete(submitWord);
  
  var magicNumber,
      output,
      gameBoard,
      tiles,
      clearAll,
      indexTiles,
      clearActiveTiles,
      disableTiles,
      validateTile,
      enableSurroundingTiles,
      clicker,
      submitWord;

  var magicNumber = 4;

  var output = document.getElementById('output');
  var gameBoard = document.getElementById('game-board');
  var tiles = gameBoard.querySelectorAll('button');

  var clearAll = document.getElementById('clear-all');

  var indexTiles = function () {
    for (var i=0; i < tiles.length; i++) {
      tiles[i].attributes.index = i;
    }
  };

  indexTiles();

  var clearActiveTiles = function() {
    for (var i = 0; i < tiles.length; i++) {
     tiles[i].disabled = false; tiles[i].classList.remove('active');
    }
  }

  var disableTiles = function() {
    for (var i = 0; i < tiles.length; i++) {
      tiles[i].disabled = true;
    }
  }

  var validateTile = function (index, direction) {
    if (index < 0 || index >= magicNumber * magicNumber || tiles[index].classList.contains('active')) return;
    if (direction === 'left' && (index+1) % 4 === 0) return;
    if (direction === 'right' && index % 4 === 0) return;
    tiles[index].disabled = false;
  };

  var enableSurroundingTiles = function (tile) {
    var index = tile.attributes.index;
    var up = index - magicNumber;
    var down = index + magicNumber;
    validateTile(up, 'up');
    validateTile(down, 'down');

    validateTile(index - 1, 'left');
    validateTile(up - 1, 'left');
    validateTile(down - 1, 'left');

    validateTile(index + 1, 'right');
    validateTile(up + 1, 'right');
    validateTile(down + 1, 'right');
  };

  var clicker = function(e) {
    var tile = e.target;
    if (tile.tagName !== 'BUTTON' || tile.classList.contains('active')) {
      return;
    }
    output.innerHTML = output.innerHTML + tile.innerHTML;
    tile.classList.add('active');
    disableTiles();
    enableSurroundingTiles(tile);
  };

  var submitWord = function () {
    socket.emit('new_user_word', sessionStorage.getItem('you'), output.innerHTML);
    output.innerHTML = '';
    clearActiveTiles();
  };

  gameBoard.addEventListener('click', clicker);

  clearAll.addEventListener('click', submitWord);
}
