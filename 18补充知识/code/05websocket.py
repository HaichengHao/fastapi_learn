"""
@File    :05websocket.py
@Editor  : 百年
@Date    :2026/6/4 17:49 
"""
import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://127.0.0.1:8000/ws"); 
            ws.onmessage = function(event) {   //收到消息后,创建<li>显示在页面上
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)  //发送输入内容
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")   #tips:当客户端访问 ws://127.0.0.1:8000/ws 时，会触发这个函数。
async def websocket_endpoint(websocket: WebSocket):   #tips:FastAPI 自动注入一个 WebSocket 对象，代表当前客户端的连接。通过这个对象可以与客户端进行双向通信

    await websocket.accept()
    '''
       必须调用 accept() 方法来接受 WebSocket 握手请求。
       如果不调用，连接会被拒绝。
    '''

    '''
    一旦连接建立，进入一个无限循环，持续监听客户端发来的消息。
    这是 WebSocket 长连接的典型模式'''
    while True:
        data = await websocket.receive_text() #tips:异步等待客户端发送文本消息。如果客户端断开连接或发送非文本数据（如二进制），可能会抛出异常（实际项目中应加异常处理）
        await websocket.send_text(f"Message text was: {data}")
        '''
        将收到的消息加工后（加上前缀 "Message text was: "）再发送回客户端。
实现了“回显”功能（echo server）'''
if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)