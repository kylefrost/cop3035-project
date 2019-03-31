var socket;
$(document).ready(function() {
  socket = io.connect('//' + document.domain + ':' + location.port + '/game');
  socket.on('connect', function() {
    socket.emit('joined', {});
  });


  socket.on('status', function(data) {
    $('#game').val($('#game').val() + data.msg + '\n');
    $('#game').scrollTop($('#game')[0].scrollHeight);
  });

  socket.on('message', function(data) {
    $('#game').val($('#game').val() + data.msg + '\n');
    $('#game').scrollTop($('#game')[0].scrollHeight);
  });

  $('#chat-form').submit(function() {
    var message = $('#chat-input').val();
    socket.emit('send_chat', message);
    $('chat-input').val('');
    return false;
  });

  $('#text').keypress(function(e) {
    var code = e.keyCode || e.which;
    if (code == 13) {
      text = $('#text').val();
      $('#text').val('');
      socket.emit('send_chat', {msg: text});
    }
  });
});

function leave_room() {
  socket.emit('leave', {}, function() {
    socket.disconnect();
    window.location.href = "{{ url_for('main.index') }}";
  });
}
