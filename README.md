Простой чат на Flask с использованием WebSockets (Flask-SocketIO). Теперь поддерживает трех пользователей, а также возможность вручную добавлять новых пользователей в коде.  

## 🚀 Установка и запуск  

### 1. Клонирование репозитория  
```bash
git clone https://github.com/Antongo22/SimpleWebsocketChat.git
cd SimpleWebsocketChat
```  

### 2. Установка зависимостей  
Убедитесь, что у вас установлен Python 3, затем установите необходимые пакеты:  
```bash
pip install flask flask-socketio flask-login eventlet
```  

### 3. Запуск сервера  
```bash
python app.py
```  

### 4. Открытие чата в браузере  
Перейдите по адресу:  
```
http://127.0.0.1:5000
```  

## 🔑 Доступные пользователи  
| Логин  | Пароль   |  
|--------|---------|  
| user1  | password1 |  
| user2  | password2 |  
| user3  | password3 |  

## 🌟 Новые возможности  
- **Добавление пользователей вручную**: теперь можно легко расширять список пользователей, редактируя словарь `users` в `app.py`.  
- **Глобальный чат** для всех пользователей.  
- **Личные чаты**: каждый пользователь может отправлять сообщения конкретному собеседнику.  
- **Автоматическая отправка сообщений без перезагрузки страницы**.  

## 🔧 Как добавить новых пользователей?  
Чтобы добавить нового пользователя, откройте `app.py` и добавьте его в словарь `users`:  

```python
users = {
    "user1": "password1",
    "user2": "password2",
    "user3": "password3",
    "new_user": "new_password"  # Новый пользователь
}
```  

После этого новый пользователь сможет войти в чат.  

## 📂 Структура проекта  
```
SimpleWebsocketChat/
│── app.py            # Основной серверный файл
│── templates/
│   ├── login.html    # Страница авторизации
│   ├── chat.html     # Чат
│── README.md         # Документация
```  

## 📌 Будущие улучшения  
- 📦 **Сохранение сообщений в БД** (SQLite/PostgreSQL)  
- 🔒 **Регистрация новых пользователей через интерфейс**  
- 🏠 **Создание чат-комнат (групповые чаты)**  

---  

**Автор:** Антон Алейниченко  

