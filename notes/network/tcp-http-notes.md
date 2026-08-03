# TCP/IP & HTTP 复习笔记

> 配合 mini-http-server 项目写的，把课本知识和代码对应起来

## TCP 三次握手（socket编程对应）

写服务器的时候才真正理解了三次握手：

```
客户端                   服务器
  |                        |
  |------ SYN ----------->|  socket()
  |                        |  bind()
  |                        |  listen()  ← 到这步为止
  |<----- SYN+ACK --------|  
  |------ ACK ----------->|  accept()  ← 三次握手完成，返回fd
  |                        |
  |------ 数据交互 ------->|  recv()/send()
```

对应的代码：

```c
int fd = socket(AF_INET, SOCK_STREAM, 0);  // 创建socket
bind(fd, &addr, sizeof(addr));              // 绑定地址
listen(fd, 10);                             // 开始监听
int client = accept(fd, NULL, NULL);        // 接受连接
```

**注意点**：
- `listen` 的第二个参数是已完成队列的大小（不是总连接数）
- `accept` 是阻塞的，会一直等直到有新连接
- 三次握手是内核完成的，`accept` 只是从已完成队列取一个

## HTTP 协议解析

请求报文格式：

```
GET /index.html HTTP/1.1\r\n        ← 请求行(方法+路径+版本)
Host: localhost:8080\r\n            ← 首部字段
Connection: keep-alive\r\n
\r\n                                 ← 空行（分隔首部和主体）
                                     ← 主体（GET没有，POST有）
```

**容易忽略的点**：
- 行末是 `\r\n` 不是 `\n`（RFC规定）
- 首部和主体之间有一个**空行** `\r\n\r\n`
- `Content-Length` 告诉服务器主体有多长（不然不知道读多少）

## 四次挥手

```
主动关闭方              被动关闭方
  |------ FIN ----------->|
  |<----- ACK ------------|   ← 半关闭状态
  |<----- FIN ------------|
  |------ ACK ----------->|   ← 完全关闭
```

- `close(fd)` 触发四次挥手
- 如果忘了 close，fd 会泄漏（pthread_detach 前要注意）

## 端口复用 SO_REUSEADDR

```c
int opt = 1;
setsockopt(fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
```

不加这个的话，关了服务器马上重启会报 "Address already in use"
因为TCP要等2MSL（大约2分钟）才释放端口

## 网络字节序

网络字节序 = 大端。x86是小端，所以要用 htons/htonl 转换：

```c
addr.sin_port = htons(8080);        // host to network short
addr.sin_addr.s_addr = htonl(INADDR_ANY);  // host to network long
```

## 多线程 vs 多路复用

| 方案 | 并发模型 | 适合场景 |
|------|---------|---------|
| pthread | 每连接一线程 | 连接数少 |
| 线程池 | 复用线程 | 中等并发 |
| select/poll | 单线程轮询 | 几百连接 |
| epoll | 事件驱动 | 高并发(C10k) |

这次项目用的是线程池方案，对学习来说够了。
epoll的原理看了，但还没实现（TODO）。

## 实际遇到的问题

1. 浏览器发两个请求 — Chrome默认会同时请求 `/favicon.ico`
2. send不保证发完 — 返回值 < 要发的字节数就要循环
3. fread二进制 — Windows下`"r"`和`"rb"`不一样，图片必须`"rb"`

---

*配合 [mini-http-server](https://github.com/KimserUM/mini-http-server) 食用*
