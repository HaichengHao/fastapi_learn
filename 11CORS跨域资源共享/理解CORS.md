CORS（**Cross-Origin Resource Sharing**，跨域资源共享）是一种 **浏览器安全机制**，用于控制一个网页是否可以向 **不同源（origin）** 的服务器发起请求并读取响应。

---

### 🌐 什么是“同源”？

两个 URL 被认为是 **同源**，当且仅当它们的以下三个部分完全相同：

- **协议（Protocol）**：如 `http` 或 `https`
- **域名（Host）**：如 `example.com`
- **端口（Port）**：如 `80`、`3000`、`65533`

✅ 同源示例：
- `https://api.example.com:443` 和 `https://api.example.com` → 同源（443 是 HTTPS 默认端口）
  
❌ 跨域（不同源）示例：
- `http://localhost:3000` vs `http://localhost:65533` → **端口不同，跨域**
- `http://localhost:3000` vs `https://localhost:3000` → **协议不同，跨域**
- `http://localhost:3000` vs `http://127.0.0.1:3000` → **域名不同（localhost ≠ 127.0.0.1），跨域**

> 💡 注意：`localhost` 和 `127.0.0.1` 在 DNS 上解析为同一 IP，但浏览器视为 **不同源**！

---

### 🔒 为什么要有 CORS？

这是为了防止 **恶意网站窃取用户数据**。例如：

- 用户登录了银行网站 `bank.com`
- 恶意网站 `evil.com` 尝试用 JavaScript 向 `bank.com/api/transfer` 发起请求
- 如果没有 CORS，浏览器会携带用户的 cookie 自动发送请求 → 可能转账成功！

CORS 通过要求 **目标服务器明确允许** 来阻止这类攻击。

---

### ⚙️ CORS 是如何工作的？

#### 1. **简单请求（Simple Request）**
满足以下条件的请求属于“简单请求”，浏览器直接发送，**不发预检**：
- 方法：`GET`、`POST`、`HEAD`
- Headers 只包含：
  - `Accept`
  - `Accept-Language`
  - `Content-Language`
  - `Content-Type`（仅限 `application/x-www-form-urlencoded`、`multipart/form-data`、`text/plain`）

✅ 浏览器会自动在请求中带上 `Origin` 头，如：
```http
Origin: http://localhost:3000
```

✅ 服务器必须在响应中包含：
```http
Access-Control-Allow-Origin: http://localhost:3000
# 或（开发时常用，但不安全）
Access-Control-Allow-Origin: *
```

否则浏览器会 **拦截响应**，前端 JS 拿不到数据（即使 HTTP 状态是 200）。

---

#### 2. **预检请求（Preflight Request）**
如果你的请求 **不符合简单请求条件**（比如 `Content-Type: application/json`、自定义 header、`PUT`/`DELETE` 方法等），浏览器会先发一个 **`OPTIONS` 请求** 进行“预检”。

例如你的代码：
```js
fetch('http://127.0.0.1:65533/info', {
  method: 'GET',
  headers: { 'Content-Type': 'application/json' } // ← 触发预检！
})
```

虽然方法是 `GET`，但因为设置了 `Content-Type: application/json`（不属于简单类型），所以会先发：

```http
OPTIONS /info HTTP/1.1
Origin: http://localhost:6342
Access-Control-Request-Method: GET
Access-Control-Request-Headers: content-type
```

✅ 服务器必须正确响应这个 `OPTIONS` 请求，并返回：
```http
HTTP/1.1 200 OK
Access-Control-Allow-Origin: http://localhost:6342
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type
Access-Control-Max-Age: 86400
```

然后浏览器才会发送真正的 `GET` 请求。

---

### ❌ 常见错误

| 错误信息 | 原因 |
|--------|------|
| `No 'Access-Control-Allow-Origin' header present` | 服务器没返回 CORS 头 |
| `The value of the 'Access-Control-Allow-Origin' header is invalid` | 返回了多个 origin 或格式错误 |
| `Request header field X is not allowed` | `Access-Control-Allow-Headers` 没包含该 header |

---

### ✅ 如何解决 CORS？

- **后端**：配置 CORS 中间件（如 FastAPI 的 `CORSMiddleware`）
- **开发阶段**：可临时允许所有来源（`allow_origins=["*"]`）
- **生产环境**：严格指定可信来源（如 `["https://yourdomain.com"]`）

> ⚠️ 注意：`allow_credentials=True` 时不能使用 `*`，必须指定具体域名。

---

### 🧪 举个例子（FastAPI）

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:6342"],  # 前端地址
    allow_methods=["*"],
    allow_headers=["*"],
)
```

这样就能让 `http://localhost:6342` 成功调用你的 API。

---

### 总结

> **CORS 不是后端功能，而是浏览器的安全策略**。  
> 后端只需正确设置响应头，告诉浏览器：“我信任这个来源，允许它读取我的数据”。

如果你控制后端，就配置 CORS；如果只做前端，需联系后端开发者开启 CORS 支持。