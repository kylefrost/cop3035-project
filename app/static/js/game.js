var socket;
$(document).ready(function() {
  socket = io.connect('//' + document.domain + ':' + location.port + '/game');
  socket.on('connect', function() {
    socket.emit('joined', {});
  });

  socket.on('set_storage', function(data) {
    sessionStorage.setItem('you', data.user);
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
  });

  socket.on('update_timer', function(data) {
    console.log('received data');
    console.log(data);
    $('#timer').text(data.timer);
  });

  $('#start-button').click(function() {
    socket.emit('start_timer', {});
    console.log('Start button pressed!');
  });

  $('#chat-form').submit(function() {
    var message = $('#chat-input').val();
    socket.emit('send_chat', sessionStorage.getItem('you'), message);
    $('#chat-input').val('');
    return false;
  });
});

function leave_room() {
  socket.emit('leave', {}, function() {
    socket.disconnect();
    window.location.href = "{{ url_for('main.index') }}";
  });
}
