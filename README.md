# **Web 聊天助手（基于 Flask + corpus JavaScript）**

## **📌 项目简介**

本项目是一个 **网页端智能聊天助手** ，支持 **人机对话** ，可用于 **耳机信息查询、型号对比、价格推荐等功能** 。

前端采用 **原生 HTML + CSS + JavaScript** ，后端使用 **Flask** 提供 API 服务，聊天逻辑由 `response.py` 处理。

---

## **📁 项目结构**

<pre class="!overflow-visible" data-start="324" data-end="610"><div class="contain-inline-size rounded-md border-[0.5px] border-token-border-medium relative bg-token-sidebar-surface-primary dark:bg-gray-950"><div class="flex items-center text-token-text-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-[5px] h-9 bg-token-sidebar-surface-primary dark:bg-token-main-surface-secondary select-none">bash</div><div class="sticky top-9 md:top-[5.75rem]"><div class="absolute bottom-0 right-2 flex h-9 items-center"><div class="flex items-center rounded bg-token-sidebar-surface-primary px-2 font-sans text-xs text-token-text-secondary dark:bg-token-main-surface-secondary"><span class="" data-state="closed"><button class="flex gap-1 items-center select-none px-4 py-1" aria-label="复制"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-xs"><path fill-rule="evenodd" clip-rule="evenodd" d="M7 5C7 3.34315 8.34315 2 10 2H19C20.6569 2 22 3.34315 22 5V14C22 15.6569 20.6569 17 19 17H17V19C17 20.6569 15.6569 22 14 22H5C3.34315 22 2 20.6569 2 19V10C2 8.34315 3.34315 7 5 7H7V5ZM9 7H14C15.6569 7 17 8.34315 17 10V15H19C19.5523 15 20 14.5523 20 14V5C20 4.44772 19.5523 4 19 4H10C9.44772 4 9 4.44772 9 5V7ZM5 9C4.44772 9 4 9.44772 4 10V19C4 19.5523 4.44772 20 5 20H14C14.5523 20 15 19.5523 15 19V10C15 9.44772 14.5523 9 14 9H5Z" fill="currentColor"></path></svg>复制</button></span><span class="" data-state="closed"><button class="flex select-none items-center gap-1"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-xs"><path d="M2.5 5.5C4.3 5.2 5.2 4 5.5 2.5C5.8 4 6.7 5.2 8.5 5.5C6.7 5.8 5.8 7 5.5 8.5C5.2 7 4.3 5.8 2.5 5.5Z" fill="currentColor" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"></path><path d="M5.66282 16.5231L5.18413 19.3952C5.12203 19.7678 5.09098 19.9541 5.14876 20.0888C5.19933 20.2067 5.29328 20.3007 5.41118 20.3512C5.54589 20.409 5.73218 20.378 6.10476 20.3159L8.97693 19.8372C9.72813 19.712 10.1037 19.6494 10.4542 19.521C10.7652 19.407 11.0608 19.2549 11.3343 19.068C11.6425 18.8575 11.9118 18.5882 12.4503 18.0497L20 10.5C21.3807 9.11929 21.3807 6.88071 20 5.5C18.6193 4.11929 16.3807 4.11929 15 5.5L7.45026 13.0497C6.91175 13.5882 6.6425 13.8575 6.43197 14.1657C6.24513 14.4392 6.09299 14.7348 5.97903 15.0458C5.85062 15.3963 5.78802 15.7719 5.66282 16.5231Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path><path d="M14.5 7L18.5 11" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>编辑</button></span></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="!whitespace-pre"><span>📂 项目目录
│── server.py                # Flask 服务器，提供聊天 API，并渲染 HTML 界面
│── response.py              # 处理用户输入，返回 AI 生成的回复
│── Headset assistant.html   # 前端界面，包含聊天 UI
│── headphones.json          # 耳机数据文件（包含型号、参数等）
│── corpus.json              # 预定义的意图数据（用于 NLP 识别）
│── static
    ── script.js             # 存储 JavaScript 逻辑
    ── style.css             # 存储 CSS 修饰器风格
</span></code></div></div></pre>

---

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

---

## **📜 结论**

本项目实现了一个 **基于 Flask +  JavaScript** 的网页端智能聊天助手，支持耳机信息查询、对比、推荐等功能，并采用简洁的 UI 设计，适合进一步扩展功能。

---

## **📄 许可证**

本项目遵循 **MIT License** ，可自由修改和使用。🎉

---

如果你希望对 **界面样式** 或 **功能逻辑** 进行调整，欢迎提出建议！😊🚀
