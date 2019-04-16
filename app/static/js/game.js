var socket;
$(document).ready(function() {
  if (Notification.permission != 'granted') {
    try {
        Notification.requestPermission().then(function(result){ console.log(result); });
    } catch (error) {
        if (error instanceof TypeError) {
            Notification.requestPermission(function(result) {
                console.log(result);
            });
        } else {
            throw error;
        }
    }
  }
  socket = io.connect('//' + document.domain + ':' + location.port + '/game');
  socket.on('connect', function() {
    socket.emit('joined', {});
  });

  socket.on('set_storage', function(data) {
    sessionStorage.setItem('you', data.user);
  });

  socket.on('update_leaderboard', function(data){
    var leaderboard = $('#leaderboard-table');
    leaderboard.empty();
    leaderboard.append('<tr><th style="text_align:left;padding-left:30px;" colspan="2">Players</th><th style="text-align:center">Score</th></tr>');
    for (var i = 0; i < data.users.length; i++) {
      leaderboard.append('<tr><td class="user-icon"><img class="p-icon" src="' + head_image_url + '"></td><td class="player-name">' + data.users[i][0] + '</td><td class="player-score">' + data.users[i][1] + '</td></tr>');
    }
    if (data.users.length > 1) {
      $('#start-game-button').prop('disabled', false);
    } else {
      $('#start-game-button').prop('disabled', true);
    }
  });

  socket.on('new_chat', function(data) {
    var chatContainer = document.getElementById('chat-messages-container'),
        chatList = $('#chat-messages-list'),
        chatItem = document.createElement('li'),
        chatName = document.createElement('div'),
        chatMsg = document.createElement('div'),
        chatSender = (sessionStorage.getItem('you') == data.user) ? 'me' : 'other';

    var chatItems = $('#chat-messages-list li'), lastItem = chatItems.last();

    var game = $('#main-container');
    var notification = $('.serverNotification');

    var userJoinedMessage = data.message.substr(data.length - 20);
    var userLeftMessage = data.message.substr(data.length - 18);

    if (lastItem) {
      var lastUser = lastItem.find('.username'),
        lastMsg = lastItem.find('.msg');
      if (lastUser.text() == data.user) {
        lastMsg.append('<br/><br/>' + data.message);
      } else {
          if (data.user == "SERVER") {
            if (userJoinedMessage == "has joined the game.") {
              // joined game
            } else if (userLeftMessage == "has left the game.") {
              // left game
            }
            notification.remove();
            chatList.append('<li class="server"><div class="msg">' + data.message + '</div></li>');
            game.append('<div class="serverNotification server-notify-show">' + data.message + '</div>');
            setTimeout(function() {
              $('.serverNotification').removeClass("server-notify-show").addClass("server-notify-hide");
            }, 3000);
            console.log("SERVER Sent Message");
          } else {
            chatList.append('<li class="' + chatSender + '"><div class="username slide-up-from-bottom">'+ data.user + '</div><div class="msg slide-up-from-bottom">' + data.message + '</div></li>');
          }
      }
    } else {
      if (data.user == "SERVER") {
          notification.remove();
          chatList.append('<li class="server"><div class="msg">' + data.message + '</div></li>');
          game.append('<div class="serverNotification server-notify-show">' + data.message + '</div>');
          setTimeout(function() {
            $('.serverNotification').removeClass("server-notify-show").addClass("server-notify-hide");
          }, 3000);
          console.log("SERVER Sent Message");
      } else {
          console.log("Send message");
          chatList.append('<li class="' + chatSender + '"><div class="username slide-up-from-bottom">'+ data.user + '</div><div class="msg slide-up-from-bottom">' + data.message + '</div></li>');
      }
    }
    chatContainer.scrollTop = chatContainer.scrollHeight;

    if (data.user != 'SERVER') {
      $.titleAlert("New chat from " + data.user, {
        requireBlur: true,
        stopOnFocus: true
      });

      if (Notification.permission == 'granted') {
        var notification = new Notification('New chat from ' + data.user, {
          body: data.message
        });
      }
    }
  });

  socket.on('update_timer', function(data) {
    if (!$('#timer').is(":visible")) {
      $('#timer').toggle();
    }
    $('#timer').text(data.timer);
    if (parseInt(data.timer.slice(-2)) < 10 && data.timer != '01:00') {
      $('#timer').css('color', 'red');
    } else {
      $('#timer').css('color', 'black');
    }
  });

  socket.on('word_success', function(data) {
    console.log(data);
    var wordList = $('#word-list-container');

    wordList.append('<div class="word-list-word">' + data.word + '</div>');
    socket.emit('add_word', data.user, data.word);
  });

  socket.on('rolled_die', function(data) {
    // Start the game
    console.log(data);

    var newGameBoard = $('<div />', {
      'id': 'game-board'
    });
    //newGameBoard.empty();

    for (var i = 0; i < data.dice.length; i++) {
      newGameBoard.append('<button class="letter">' + data.dice[i] + '</button>')
    }

    $("#board-wrap").append(newGameBoard);
    $("#board-wrap").append("<br>")
    $("#board-wrap").append('<div id="output-container"><div id="output"></div></div><br id="output-break" /><button id="clear-all">Submit</button>');
    $("#board-wrap").fadeIn(400, function() {
      reset();
      setBoggleBoardVariables();
    });
  });

  socket.on('play_error', function(data) {
    var game = $('#main-container');
    var notification = $('.serverNotification');

    notification.remove();
    game.append('<div class="serverNotification playError server-notify-show">' + data.error + '</div>');
    setTimeout(function() {
      $('.serverNotification').removeClass("server-notify-show").addClass("server-notify-hide");
    }, 3000);
  });

  socket.on('get_ready_front', function(data) {
    var start = $("#start-game-button");
    var flashInterval = setInterval(function () {
      start.css("background-color", function () {
        this.switch = !this.switch
        return this.switch ? "#f48221" : "#ffcd9e"
      });
    }, 100);
    start.prop('disabled', true);
    start.text("Ready...");
    setTimeout(function() {
      start.text("Set...");
      setTimeout(function() {
        start.text("Go!");
        setTimeout(function() {
          start.fadeOut(400, function() {
            if (data.user == sessionStorage.getItem('you')) {
              socket.emit('start_timer', {});
            }
            window.clearInterval(flashInterval);
          });
        }, 1000);
      }, 1000);
    }, 1000);

    console.log('Start button pressed!');
  });

  socket.on('end_game', function(data) {
    $("#board-wrap").fadeOut(400, function() {
      if (data.sender == sessionStorage.getItem('you')) {
        console.log("i am " + sessionStorage.getItem('you') + " and i am calling end_game_words.");
        socket.emit('end_game_words', {});
      }
      // $("#output-container").remove();
      // $("#output-break").remove();
      // $("#clear-all").remove();
      $("#board-wrap").empty();
    });
    $("#timer").fadeOut();
  });

  socket.on('all_word_lists', function(data) {
    console.log(data);

    var endWordsContainer = $('#end-word-lists-container');
    endWordsContainer.empty();

    for (var key in data) {
      var newDiv = $("<div />", {
        "class": "end-word-list"
      });
      newDiv.append('<div class="end-word-list-owner">' + key + ', round score: ' + data[key][2] + '</div><hr>');
      for (var i in data[key][0]) {
        if (!data[key][1].includes(data[key][0][i])) {
          newDiv.append('<div class="word-list-word" style="text-decoration: line-through;color: red;">' + data[key][0][i] + '</div>');
        } else {
          newDiv.append('<div class="word-list-word">' + data[key][0][i] + '</div>');
        }
      }

      endWordsContainer.append(newDiv);
      endWordsContainer.append("<br>");
    }

    $("#end-word-lists-container").fadeIn();

    setTimeout(function() {
      $("#end-word-lists-container").fadeOut(400, function() {
        $("#start-game-button").text("Start");
        $("#start-game-button").fadeIn();
        $("#start-game-button").prop("style", false);
        $("#word-list-container").empty();
      });
    }, 10000);
  });

  $('#start-game-button').click(function() {
    socket.emit('get_ready', sessionStorage.getItem('you'));
  });

  $('#chat-form').submit(function() {
    var message = $('#chat-input').val();
    socket.emit('send_chat', sessionStorage.getItem('you'), message);
    $('#chat-input').val('');
    return false;
  });
});

window.onbeforeunload = function () {
  socket.emit('leave', {'user': sessionStorage.getItem('you')}, function() {
    socket.disconnect();
  });
  //return false;
}
