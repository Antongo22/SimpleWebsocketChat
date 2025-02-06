from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, send
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Настройки SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Настройки Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Список пользователей (логин: пароль)
USERS = {
    "user1": "password1",
    "user2": "password2"
}

# Класс пользователя
class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(username):
    if username in USERS:
        return User(username)
    return None

# Главная страница (авторизация)
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in USERS and USERS[username] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for("chat"))

    return render_template("login.html")

# Чат (доступен только авторизованным пользователям)
@app.route("/chat")
@login_required
def chat():
    return render_template("chat.html", username=current_user.id)

# Выход из системы
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# Обработчик сообщений по WebSocket
@socketio.on("message")
@login_required
def handle_message(msg):
    full_msg = f"{current_user.id}: {msg}"
    send(full_msg, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, debug=True)
