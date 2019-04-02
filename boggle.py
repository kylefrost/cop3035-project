from gevent import monkey
monkey.patch_all()
from app import gen_app, socketio

# Generate main application object
app = gen_app(debug=True)

if __name__ == '__main__':
    # Run program on localhost
    socketio.run(app, host='0.0.0.0')
