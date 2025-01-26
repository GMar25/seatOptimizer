from flask import Flask

from webserver import user_blueprint, admin_blueprint

app = Flask(__name__)
app.register_blueprint(user_blueprint)
app.register_blueprint(admin_blueprint, url_prefix="/user")

if __name__ == "__main__":
    app.run(debug=True)
app.run(debug=True)
