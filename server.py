from flask import Flask, request, jsonify, send_from_directory
from response import process_message

app = Flask(__name__)


# 根路由，返回前端 HTML 文件
@app.route('/')
def index():
    return send_from_directory('.', 'Headset assistant.html')


# 聊天接口
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message', '')
    reply = process_message(user_input)
    return jsonify({'reply': reply})


if __name__ == '__main__':
    app.run(debug=True)
