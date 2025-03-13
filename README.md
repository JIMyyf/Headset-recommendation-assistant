# **Web 聊天助手（基于 Flask 框架）**

## **📌 项目简介**

本项目是一个 **网页端智能聊天助手** ，支持 **人机对话** ，可用于 **耳机信息查询、型号对比、价格推荐等功能** 。

前端采用 **原生 HTML + CSS + JavaScript** ，后端使用 **Flask** 提供 API 服务，聊天逻辑由 `response.py` 处理。

---

## **📁 项目结构**

📂 项目目录
```
├── corpus.json
├── headphones.json
├── Headset assistant.html
├── LICENSE
├── README.md
├── response.py
├── server.py
└── static
    ├── script.js
    └── style.css
```

## **🌍 功能介绍**

✔ **支持网页端聊天交互**

✔ **查询耳机详细信息** （输入耳机型号，例如 `AirPods Pro 2 介绍`）

✔ **对比两个耳机型号** （输入 `AirPods Pro 2 和 Sony XM5 有什么区别？`）

✔ **按价格推荐耳机** （输入 `推荐 2000 元以内的降噪耳机`）

✔ **按功能推荐耳机** （输入 `推荐适合运动的无线耳机`）

✔ **支持 Enter 键发送消息**

✔ **后端 Flask 提供 API，前端 fetch 交互**

✔ **纯净聊天界面，无多余 UI 组件**

---

## **🛠️ 安装与运行**

### **1️⃣ 安装 Python 依赖**

确保你已经安装了 **Python 3** ，然后安装 Flask：

```bash
pip install flask
```

### **2️⃣ 运行 Flask 服务器**

```bash
python server.py
```

如果成功启动，终端会显示：

```bash
 * Serving Flask app 'server'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 112-562-914
```

### **3️⃣ 访问前端界面**

打开浏览器，输入：

```bash
 http://127.0.0.1:5000
```

即可看到聊天界面，输入消息开始交互。

---

## **🖥️ 前端（HTML + JavaScript）**

**前端采用了** ：

- **纯 HTML + CSS** 进行 UI 设计
- **JavaScript fetch API** 进行 AJAX 请求
- **CSS 响应式布局** 让聊天界面更简洁

---

## **🚀 后端（Flask 服务器）**

**server.py** 负责：

- 提供 `/chat` 接口，接收前端消息并返回 AI 回复
- 提供 `index.html`，渲染聊天页面

---

## **🎯 处理逻辑（response.py）**

**response.py** 负责：

- **解析用户输入**
- **识别用户意图**
- **匹配耳机信息**
- **返回聊天回复**

---

## **📸 项目截图**

🎨 **纯净聊天界面，无多余元素**

---

## **📌 未来改进方向**

✅ **增加更强的 NLP 解析能力**

✅ **支持 WebSocket 让对话更流畅**

✅ **添加语音识别，实现语音输入**

✅ **支持数据库存储聊天记录**

✅ **增加其他的功能为用户提供更周到的服务**

---

## **📜 结论**

本项目实现了一个 **基于 Flask +  JavaScript** **+ HTML** 的网页端智能聊天助手，支持耳机信息查询、对比、推荐等功能，并采用简洁的 UI 设计，适合进一步扩展功能。

---

## **📄 许可证**

本项目遵循 **MIT License** ，可自由修改和使用。🎉

---

如果你希望对 **界面样式** 或 **功能逻辑** 进行调整，欢迎提出建议！😊🚀
