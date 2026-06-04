这段代码使用 **FastAPI** 框架实现了一个简单的 WebSocket 聊天应用。下面将重点解释 **WebSocket 接口的实现部分**，并简要说明整体结构。

---

## 一、整体结构概览

- 使用 `FastAPI` 创建一个 Web 应用。
- 提供一个根路径 `/`，返回一个 HTML 页面，其中包含一个表单和 JavaScript 脚本，用于与后端建立 WebSocket 连接并发送/接收消息。
- 定义一个 WebSocket 路由 `/ws`，处理客户端的连接、接收消息并回显。

---

## 二、WebSocket 接口实现详解（核心部分）

```python
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
```

### 1. 路由注册：`@app.websocket("/ws")`

- 使用 `@app.websocket` 装饰器注册一个 WebSocket 路由。
- 当客户端访问 `ws://127.0.0.1:8000/ws` 时，会触发这个函数。

### 2. 参数：`websocket: WebSocket`

- FastAPI 自动注入一个 `WebSocket` 对象，代表当前客户端的连接。
- 通过这个对象可以与客户端进行双向通信。

### 3. 建立连接：`await websocket.accept()`

- 必须调用 `accept()` 方法来接受 WebSocket 握手请求。
- 如果不调用，连接会被拒绝。

### 4. 消息循环：`while True:`

- 一旦连接建立，进入一个无限循环，持续监听客户端发来的消息。
- 这是 WebSocket 长连接的典型模式。

### 5. 接收消息：`await websocket.receive_text()`

- 异步等待客户端发送文本消息。
- 如果客户端断开连接或发送非文本数据（如二进制），可能会抛出异常（实际项目中应加异常处理）。

### 6. 回复消息：`await websocket.send_text(...)`

- 将收到的消息加工后（加上前缀 `"Message text was: "`）再发送回客户端。
- 实现了“回显”功能（echo server）。

> ⚠️ 注意：此代码没有处理连接关闭或异常情况。在生产环境中，应使用 `try...except` 捕获 `WebSocketDisconnect` 等异常以优雅关闭连接。

---

## 三、前端部分简要说明（辅助理解）

HTML 中的 JavaScript：

```javascript
var ws = new WebSocket("ws://127.0.0.1:8000/ws");
ws.onmessage = function(event) {
    // 收到消息后，创建 <li> 显示在页面上
};
function sendMessage(event) {
    ws.send(input.value); // 发送输入框内容
}
```

- 前端通过 `new WebSocket(...)` 连接到 `/ws`。
- 用户输入文本后点击“Send”，调用 `ws.send()` 发送。
- 服务端回传消息后，前端通过 `onmessage` 接收并显示。

---

## 四、运行方式

```python
if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

- 使用 `uvicorn` 启动 ASGI 服务器。
- 监听本地 8000 端口，支持 HTTP 和 WebSocket。

---

## 五、总结（WebSocket 实现要点）

| 步骤 | 说明 |
|------|------|
| 1. 装饰器 | `@app.websocket("/ws")` 定义 WebSocket 路由 |
| 2. 接受连接 | `await websocket.accept()` 完成握手 |
| 3. 接收消息 | `await websocket.receive_text()` 异步等待客户端消息 |
| 4. 发送消息 | `await websocket.send_text(...)` 向客户端推送数据 |
| 5. 持续通信 | 用 `while True` 维持长连接（需异常处理） |

> ✅ 这是一个最简 WebSocket 示例，适合学习原理。实际项目中需加入连接管理、多用户广播、异常处理等机制。