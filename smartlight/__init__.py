from flask import Flask

from smartlight.animations import Animations


# Set up Flask App
app = Flask(__name__)

app.config.from_object('config')

animation_thread = Animations(app=app)

from smartlight.controllers import main
app.register_blueprint(main)

