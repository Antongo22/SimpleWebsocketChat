from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, send, emit
from functools import wraps

app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecretkey"
socketio = SocketIO(app)

# Демо-база пользователей (логины и пароли)
users = {
    "user1": "password1",
    "user2": "password2",
    "user3": "password3"
}

# Хранение сообщений в памяти
global_messages = []  # Глобальный чат
private_messages = {}  # Личные сообщения {("user1", "user2"): ["msg1", "msg2"]}

# Хранение WebSocket-сессий пользователей
user_sessions = {}

# Декоратор авторизации
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# Главная страница
@app.route("/")
def index():
    return redirect(url_for("login"))

# Логин
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            session["username"] = username
            return redirect(url_for("chat"))

    return render_template("login.html")

# Выход
@app.route("/logout")
@login_required
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

# Страница чата
@app.route("/chat")
@login_required
def chat():
    username = session["username"]
    return render_template(
        "chat.html",
        username=username,
        users=[user for user in users.keys() if user != username],
        global_messages=global_messages
    )

# WebSocket: подключение
@socketio.on("connect")
def handle_connect():
    username = session.get("username")
    if username:
        user_sessions[username] = request.sid
        print(f"{username} подключился. SID: {request.sid}")

# WebSocket: обработка сообщений
@socketio.on("message")
@login_required
def handle_message(data):
    sender = session["username"]
    msg_type = data["type"]
    message = data["message"]

    if msg_type == "global":
        full_msg = f"{sender}: {message}"
        global_messages.append(full_msg)
        send(full_msg, broadcast=True)  # Всем отправляем

    elif msg_type == "private":
        recipient = data["recipient"]
        if recipient in users:
            full_msg = f"(ЛС от {sender}): {message}"

            # Определяем ключ для хранения сообщений (сортируем пользователей, чтобы ключ был универсальным)
            chat_key = tuple(sorted([sender, recipient]))
            if chat_key not in private_messages:
                private_messages[chat_key] = []
            private_messages[chat_key].append(full_msg)

            # Отправляем только отправителю и получателю
            if recipient in user_sessions:
                emit("private_message", {"sender": sender, "message": full_msg}, to=user_sessions[recipient])
            emit("private_message", {"sender": sender, "message": full_msg}, to=request.sid)

# WebSocket: запрос истории личных сообщений
@socketio.on("request_private_history")
@login_required
def send_private_history(data):
    sender = session["username"]
    recipient = data["recipient"]

    chat_key = tuple(sorted([sender, recipient]))
    history = private_messages.get(chat_key, [])

    emit("private_history", {"recipient": recipient, "messages": history}, to=request.sid)

# WebSocket: отключение
@socketio.on("disconnect")
def handle_disconnect():
    username = session.get("username")
    if username and username in user_sessions:
        print(f"{username} отключился.")
        del user_sessions[username]

if __name__ == "__main__":
    socketio.run(app, debug=True)
ы