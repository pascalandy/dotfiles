---
name: starlette
description: >
  Build async Python web applications and APIs with Starlette 1.0, the lightweight ASGI
  framework. Use this skill when creating HTTP endpoints, WebSocket servers, middleware,
  routing, static file serving, templates, authentication, background tasks, configuration,
  testing, or any ASGI application. Triggers on mentions of Starlette, ASGI framework,
  async web Python, or when building APIs that need routing, middleware, WebSocket support,
  or server-sent events with Python's async ecosystem.
---

# Starlette 1.0 -- Complete Reference Skill

Starlette 1.0.0 is a lightweight ASGI framework/toolkit for building async web services in Python.
It requires Python >= 3.10 and depends on `anyio` (asyncio + trio support).

## Installation

```bash
pip install starlette          # core only
pip install starlette[full]    # all optional deps (httpx, jinja2, python-multipart, itsdangerous, pyyaml)
```

Run with any ASGI server:
```bash
pip install uvicorn
uvicorn myapp:app
```

---

## 1. Application

### Minimal App (Framework Mode)

```python
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

async def homepage(request):
    return JSONResponse({"hello": "world"})

app = Starlette(debug=True, routes=[
    Route("/", homepage),
])
```

### Minimal App (Toolkit / Bare ASGI Mode)

```python
from starlette.responses import PlainTextResponse

async def app(scope, receive, send):
    assert scope["type"] == "http"
    response = PlainTextResponse("Hello, world!")
    await response(scope, receive, send)
```

### Full Application with All Features

```python
import contextlib
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import PlainTextResponse, JSONResponse
from starlette.routing import Route, Mount, WebSocketRoute
from starlette.staticfiles import StaticFiles

@contextlib.asynccontextmanager
async def lifespan(app):
    print("Startup")
    yield
    print("Shutdown")

def homepage(request):
    return PlainTextResponse("Hello, world!")

async def user(request):
    username = request.path_params["username"]
    return PlainTextResponse(f"Hello, {username}!")

async def websocket_endpoint(websocket):
    await websocket.accept()
    await websocket.send_text("Hello, websocket!")
    await websocket.close()

routes = [
    Route("/", homepage),
    Route("/user/{username}", user),
    WebSocketRoute("/ws", websocket_endpoint),
    Mount("/static", StaticFiles(directory="static"), name="static"),
]

middleware = [
    Middleware(CORSMiddleware, allow_origins=["*"]),
    Middleware(SessionMiddleware, secret_key="secret"),
]

app = Starlette(
    debug=True,
    routes=routes,
    middleware=middleware,
    lifespan=lifespan,
)
```

### Application State

```python
# Store global state
app.state.ADMIN_EMAIL = "admin@example.org"

# Access from endpoint
async def homepage(request):
    admin = request.app.state.ADMIN_EMAIL
    return PlainTextResponse(f"Admin: {admin}")
```

---

## 2. Routing

### HTTP Routes with Path Parameters

```python
from starlette.routing import Route, Mount, Router
from starlette.responses import PlainTextResponse

async def user(request):
    user_id = request.path_params["user_id"]
    return PlainTextResponse(f"User {user_id}")

routes = [
    Route("/", homepage),
    Route("/users/{user_id:int}", user, methods=["GET"]),
    Route("/files/{filepath:path}", serve_file),
    Route("/items/{item_id:uuid}", item_detail),
    Route("/price/{amount:float}", price),
]
```

**Built-in path convertors**: `str` (default), `int`, `float`, `uuid`, `path`.

### Custom Path Convertor

```python
from datetime import datetime
from starlette.convertors import Convertor, register_url_convertor

class DateTimeConvertor(Convertor):
    regex = "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}"

    def convert(self, value: str) -> datetime:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")

    def to_string(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%dT%H:%M:%S")

register_url_convertor("datetime", DateTimeConvertor())

# Usage: Route("/events/{when:datetime}", event_handler)
```

### Nested Routes (Mount)

```python
from starlette.routing import Mount, Route

routes = [
    Route("/", homepage),
    Mount("/users", routes=[
        Route("/", users_list, methods=["GET", "POST"]),
        Route("/{username}", user_detail),
    ]),
    Mount("/api", routes=[
        Mount("/v1", routes=[
            Route("/items", items_v1),
        ]),
    ]),
]
```

### Mount Sub-Applications

```python
from starlette.staticfiles import StaticFiles

routes = [
    Mount("/static", app=StaticFiles(directory="static"), name="static"),
    Mount("/api", app=api_app),  # another ASGI app
]
```

### Host-Based Routing

```python
from starlette.routing import Host, Route

routes = [
    Host("api.example.org", app=api_app, name="api"),
    Host("{subdomain}.example.org", app=subdomain_app, name="subdomain"),
]

app = Starlette(routes=routes)
# Or add dynamically:
app.host("www.example.org", site_app, name="main_site")
```

### Reverse URL Lookups

```python
# From request context
url = request.url_for("user_detail", username="tom")  # full URL

# Nested mount names use colon separator
url = request.url_for("users:user_detail", username="tom")

# Static file URL
url = request.url_for("static", path="/css/style.css")

# Without request (path only, no host/scheme)
path = app.url_path_for("user_detail", username="tom")
```

### WebSocket Routes

```python
from starlette.routing import WebSocketRoute

async def ws_echo(websocket):
    await websocket.accept()
    async for message in websocket.iter_text():
        await websocket.send_text(f"Echo: {message}")
    await websocket.close()

routes = [
    WebSocketRoute("/ws", ws_echo),
    WebSocketRoute("/ws/{room}", ws_room),
]
```

### Route Priority

First match wins. Put specific routes before parameterized routes:

```python
routes = [
    Route("/users/me", current_user),       # specific first
    Route("/users/{username}", user_detail), # parameterized second
]
```

### Router (Lightweight, No Middleware Wrapping)

```python
from starlette.routing import Router, Route

router = Router(routes=[
    Route("/", homepage),
    Route("/about", about),
])
```

---

## 3. Requests

### Request Properties

```python
from starlette.requests import Request

async def handler(request: Request):
    # Method
    method = request.method  # "GET", "POST", etc.

    # URL
    url = request.url              # URL object (string-like)
    path = request.url.path        # "/users/123"
    scheme = request.url.scheme    # "https"
    port = request.url.port        # 443

    # Headers (case-insensitive, immutable)
    content_type = request.headers["content-type"]
    all_values = request.headers.getlist("x-custom")

    # Query parameters (immutable multi-dict)
    search = request.query_params["search"]
    all_tags = request.query_params.getlist("tag")

    # Path parameters
    user_id = request.path_params["user_id"]

    # Client address
    if request.client:
        host = request.client.host
        port = request.client.port

    # Cookies
    session_id = request.cookies.get("session_id")

    # Application reference
    app = request.app
```

### Request Body

```python
# Full body as bytes
body = await request.body()

# JSON
data = await request.json()

# Streaming body
async for chunk in request.stream():
    process(chunk)

# Form data (URL-encoded or multipart)
async with request.form() as form:
    username = form["username"]          # string field
    upload = form["file"]               # UploadFile object
    filename = upload.filename
    contents = await upload.read()

# Form with limits
async with request.form(max_files=100, max_fields=500, max_part_size=5*1024*1024) as form:
    ...
```

### UploadFile

```python
async with request.form() as form:
    upload = form["file"]
    # Properties
    upload.filename       # "photo.jpg" or None
    upload.content_type   # "image/jpeg" or None
    upload.size           # int or None
    upload.headers        # Headers object

    # Async file operations
    content = await upload.read()
    await upload.seek(0)
    await upload.write(b"extra data")
    await upload.close()
```

### Request State

```python
# Middleware can set state
request.state.start_time = time.time()

# Endpoints can read it
elapsed = time.time() - request.state.start_time

# Dict-style access also works
request.state["key"] = "value"
```

### Disconnect Detection

```python
async def long_poll(request):
    while not await request.is_disconnected():
        await asyncio.sleep(1)
    return Response("Done")
```

### Server Push (HTTP/2)

```python
async def homepage(request):
    await request.send_push_promise("/static/style.css")
    return HTMLResponse('<html><head><link rel="stylesheet" href="/static/style.css"/></head></html>')
```

---

## 4. Responses

### Basic Responses

```python
from starlette.responses import (
    Response, HTMLResponse, PlainTextResponse,
    JSONResponse, RedirectResponse, StreamingResponse, FileResponse,
)

# Plain text
Response("Hello", media_type="text/plain")
PlainTextResponse("Hello")

# HTML
HTMLResponse("<h1>Hello</h1>")

# JSON
JSONResponse({"key": "value"})
JSONResponse({"error": "not found"}, status_code=404)

# Redirect (default 307 Temporary)
RedirectResponse(url="/new-location")
RedirectResponse(url="/permanent", status_code=301)

# Empty response
Response(status_code=204)
```

### Custom JSON Serialization (orjson, etc.)

```python
import orjson
from starlette.responses import JSONResponse

class OrjsonResponse(JSONResponse):
    def render(self, content) -> bytes:
        return orjson.dumps(content)
```

### Streaming Response

```python
import asyncio
from starlette.responses import StreamingResponse

async def slow_numbers(minimum, maximum):
    yield "<html><body><ul>"
    for number in range(minimum, maximum + 1):
        yield f"<li>{number}</li>"
        await asyncio.sleep(0.5)
    yield "</ul></body></html>"

async def app(scope, receive, send):
    response = StreamingResponse(slow_numbers(1, 10), media_type="text/html")
    await response(scope, receive, send)
```

### File Response (with Range Request Support)

```python
from starlette.responses import FileResponse

# Download with Content-Disposition: attachment
FileResponse("report.pdf")

# Inline display
FileResponse("image.png", filename="photo.png", content_disposition_type="inline")

# Custom media type
FileResponse("data.bin", media_type="application/octet-stream")
```

FileResponse automatically handles:
- `Accept-Ranges: bytes` header
- Single and multi-range requests (206 Partial Content)
- `If-Range` / `If-None-Match` conditional requests
- ETag and Last-Modified headers
- HEAD requests (headers only, no body)

### Cookies

```python
response = JSONResponse({"status": "ok"})

# Set cookie
response.set_cookie(
    key="session",
    value="abc123",
    max_age=3600,           # seconds
    expires=None,           # datetime, str, or int
    path="/",
    domain="example.com",
    secure=True,
    httponly=True,
    samesite="lax",         # "lax", "strict", "none"
)

# Delete cookie
response.delete_cookie(key="session", path="/")
```

### Response Headers

```python
response = JSONResponse({"data": 1})
response.headers["X-Custom"] = "value"
response.headers.append("X-Multi", "value1")
response.headers.append("X-Multi", "value2")
```

---

## 5. WebSockets

### Function-Based WebSocket

```python
from starlette.websockets import WebSocket

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # Send
    await websocket.send_text("Hello")
    await websocket.send_bytes(b"\x00\x01")
    await websocket.send_json({"type": "greeting"})

    # Receive
    text = await websocket.receive_text()
    data = await websocket.receive_bytes()
    obj = await websocket.receive_json()

    # Close
    await websocket.close(code=1000, reason="Done")
```

### Async Iterators

```python
async def echo(websocket: WebSocket):
    await websocket.accept()
    async for message in websocket.iter_text():
        await websocket.send_text(f"Echo: {message}")

async def binary_echo(websocket: WebSocket):
    await websocket.accept()
    async for data in websocket.iter_bytes():
        await websocket.send_bytes(data)

async def json_echo(websocket: WebSocket):
    await websocket.accept()
    async for obj in websocket.iter_json():
        await websocket.send_json({"received": obj})
```

### WebSocket Properties

```python
async def handler(websocket: WebSocket):
    url = websocket.url
    headers = websocket.headers
    query_params = websocket.query_params
    path_params = websocket.path_params
    client = websocket.client  # Address(host, port)
    cookies = websocket.cookies
```

### Subprotocol and Headers

```python
async def handler(websocket: WebSocket):
    await websocket.accept(
        subprotocol="graphql-ws",
        headers=[(b"x-custom", b"value")],
    )
```

### Denial Response (Reject Before Accept)

```python
from starlette.responses import Response

async def auth_ws(websocket: WebSocket):
    if not is_authorized(websocket):
        await websocket.send_denial_response(
            Response("Unauthorized", status_code=401)
        )
        return
    await websocket.accept()
    ...
```

Or raise HTTPException before accept (returns proper HTTP error):

```python
from starlette.exceptions import HTTPException

async def handler(websocket: WebSocket):
    raise HTTPException(status_code=401, detail="Unauthorized")
```

---

## 6. Endpoints (Class-Based Views)

### HTTP Endpoint

```python
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse, PlainTextResponse

class UserEndpoint(HTTPEndpoint):
    async def get(self, request):
        users = [{"name": "Alice"}, {"name": "Bob"}]
        return JSONResponse(users)

    async def post(self, request):
        data = await request.json()
        return JSONResponse(data, status_code=201)

    async def put(self, request):
        data = await request.json()
        return JSONResponse(data)

    async def delete(self, request):
        return PlainTextResponse("Deleted", status_code=204)

# Register as route endpoint class (not instance)
routes = [Route("/users", UserEndpoint)]
```

Unhandled methods automatically return 405 Method Not Allowed with `Allow` header.

### WebSocket Endpoint

```python
from starlette.endpoints import WebSocketEndpoint
from starlette.routing import WebSocketRoute

class EchoEndpoint(WebSocketEndpoint):
    encoding = "text"  # "text", "bytes", "json", or None

    async def on_connect(self, websocket):
        await websocket.accept()

    async def on_receive(self, websocket, data):
        await websocket.send_text(f"Echo: {data}")

    async def on_disconnect(self, websocket, close_code):
        print(f"Disconnected with code {close_code}")

routes = [WebSocketRoute("/ws", EchoEndpoint)]
```

---

## 7. Middleware

### Adding Middleware

```python
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.sessions import SessionMiddleware

middleware = [
    Middleware(TrustedHostMiddleware, allowed_hosts=["example.com", "*.example.com"]),
    Middleware(HTTPSRedirectMiddleware),
    Middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]),
    Middleware(GZipMiddleware, minimum_size=1000, compresslevel=9),
    Middleware(SessionMiddleware, secret_key="super-secret"),
]

app = Starlette(routes=routes, middleware=middleware)
```

**Execution order**: ServerErrorMiddleware -> user middleware (top-to-bottom) -> ExceptionMiddleware -> Router -> Endpoint.

### CORSMiddleware

```python
Middleware(CORSMiddleware,
    allow_origins=["https://example.com"],    # or ["*"] for all
    allow_origin_regex=r"https://.*\.example\.org",
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
    allow_credentials=True,
    allow_private_network=True,  # Private Network Access (PNA)
    expose_headers=["X-Custom-Header"],
    max_age=600,  # preflight cache seconds
)
```

For CORS on error responses, wrap outside Starlette:

```python
app = Starlette(routes=routes)
app = CORSMiddleware(app=app, allow_origins=["*"])
```

### SessionMiddleware

```python
Middleware(SessionMiddleware,
    secret_key="secret",
    session_cookie="session",  # cookie name
    max_age=14 * 24 * 60 * 60,  # 2 weeks; None for browser session
    same_site="lax",    # "lax", "strict", "none"
    path="/",
    https_only=False,   # True = Secure flag
    domain=None,        # ".example.com"
)

# In endpoint
async def handler(request):
    request.session["user"] = "alice"
    username = request.session.get("user")
    request.session.clear()
```

### GZipMiddleware

```python
Middleware(GZipMiddleware,
    minimum_size=500,     # bytes; skip compression below this
    compresslevel=9,      # 1 (fastest) to 9 (smallest)
)
```

Skips compression when Content-Encoding already set or Content-Type is `text/event-stream`.

### TrustedHostMiddleware

```python
Middleware(TrustedHostMiddleware,
    allowed_hosts=["example.com", "*.example.com"],
    www_redirect=True,  # redirect bare domain to www
)
```

### HTTPSRedirectMiddleware

```python
Middleware(HTTPSRedirectMiddleware)
# Redirects http -> https, ws -> wss (307)
```

### BaseHTTPMiddleware (Custom Middleware)

```python
from starlette.middleware.base import BaseHTTPMiddleware

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        import time
        start = time.time()
        response = await call_next(request)
        elapsed = time.time() - start
        response.headers["X-Process-Time"] = str(elapsed)
        return response

middleware = [Middleware(TimingMiddleware)]
```

With constructor parameters:

```python
class CustomHeaderMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, header_value="Example"):
        super().__init__(app)
        self.header_value = header_value

    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Custom"] = self.header_value
        return response

Middleware(CustomHeaderMiddleware, header_value="MyValue")
```

**Limitation**: BaseHTTPMiddleware prevents `contextvars.ContextVar` changes from propagating upward.

### Pure ASGI Middleware (Maximum Control)

```python
from starlette.types import ASGIApp, Scope, Receive, Send, Message

class PureASGIMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # Modify response headers
        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                from starlette.datastructures import MutableHeaders
                headers = MutableHeaders(scope=message)
                headers.append("X-Custom", "value")
            await send(message)

        await self.app(scope, receive, send_wrapper)
```

### ASGI Middleware Patterns

**Redirect middleware**:
```python
from starlette.datastructures import URL
from starlette.responses import RedirectResponse

class RedirectsMiddleware:
    def __init__(self, app, path_mapping: dict):
        self.app = app
        self.path_mapping = path_mapping

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        url = URL(scope=scope)
        if url.path in self.path_mapping:
            url = url.replace(path=self.path_mapping[url.path])
            response = RedirectResponse(url, status_code=301)
            await response(scope, receive, send)
            return
        await self.app(scope, receive, send)
```

**Request body logging**:
```python
class BodySizeLogger:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        body_size = 0
        async def logging_receive():
            nonlocal body_size
            message = await receive()
            body_size += len(message.get("body", b""))
            if not message.get("more_body", False):
                print(f"Request body size: {body_size}")
            return message
        await self.app(scope, logging_receive, send)
```

**Transaction ID injection**:
```python
import uuid

class TransactionIDMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        scope["transaction_id"] = uuid.uuid4()
        await self.app(scope, receive, send)
```

**Monitoring / timing**:
```python
import time

class MonitoringMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        start = time.time()
        try:
            await self.app(scope, receive, send)
        except Exception:
            raise
        finally:
            elapsed = time.time() - start
            print(f"Request took {elapsed:.3f}s")
```

### Middleware on Individual Routes

```python
from starlette.middleware import Middleware
from starlette.middleware.gzip import GZipMiddleware

routes = [
    Route("/compressed", endpoint=handler, middleware=[Middleware(GZipMiddleware)]),
    Mount("/api", routes=api_routes, middleware=[Middleware(AuthMiddleware)]),
]

# Or on Router
router = Router(routes=routes, middleware=[Middleware(GZipMiddleware)])
```

Route-level middleware is NOT wrapped in exception handling middleware (unlike app-level).

---

## 8. Static Files

### Basic Static File Serving

```python
from starlette.staticfiles import StaticFiles
from starlette.routing import Mount

routes = [
    Mount("/static", app=StaticFiles(directory="static"), name="static"),
]
```

### HTML Mode (SPA / Directory Index)

```python
# Serves index.html for directories, custom 404.html on not found
Mount("/", app=StaticFiles(directory="public", html=True))
```

### Package Static Files

```python
# From Python package's "statics" subdirectory (default)
StaticFiles(packages=["bootstrap4"])

# Custom subdirectory within package
StaticFiles(packages=[("bootstrap4", "static")])

# Combine with local directory
StaticFiles(directory="static", packages=["bootstrap4"])
```

### Options

```python
StaticFiles(
    directory="static",
    packages=None,
    html=False,
    check_dir=True,        # validate directory exists on init
    follow_symlink=False,  # follow symbolic links
)
```

Handles ETag, If-None-Match (304), If-Modified-Since, Content-Type auto-detection.

---

## 9. Templates

### Jinja2 Templates

```python
from starlette.templating import Jinja2Templates
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

templates = Jinja2Templates(directory="templates")

async def homepage(request):
    return templates.TemplateResponse(request, "index.html", {"title": "Home"})

routes = [
    Route("/", homepage),
    Mount("/static", StaticFiles(directory="static"), name="static"),
]
```

In templates, `url_for` is automatically available:
```html
<link href="{{ url_for('static', path='/css/style.css') }}" rel="stylesheet" />
<a href="{{ url_for('user_detail', username='tom') }}">Tom</a>
```

### Custom Filters

```python
templates = Jinja2Templates(directory="templates")
templates.env.filters["markdown"] = lambda text: markdown.markdown(text)
```

### Context Processors

```python
from starlette.requests import Request

def global_context(request: Request) -> dict:
    return {"app_name": "MyApp", "user": request.user}

templates = Jinja2Templates(
    directory="templates",
    context_processors=[global_context],
)
```

### Custom Jinja2 Environment

```python
import jinja2

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader("templates"),
    autoescape=True,
)
templates = Jinja2Templates(env=env)
```

Autoescape is enabled by default for `.html`, `.htm`, `.xml` when using `directory`.

### Testing Templates

```python
def test_homepage():
    client = TestClient(app)
    response = client.get("/")
    assert response.template.name == "index.html"
    assert "title" in response.context
```

---

## 10. Authentication

### Authentication Backend

```python
import base64
import binascii
from starlette.authentication import (
    AuthCredentials, AuthenticationBackend, AuthenticationError, SimpleUser
)
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware

class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn):
        if "Authorization" not in conn.headers:
            return None  # unauthenticated

        auth = conn.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() != "basic":
                return None
            decoded = base64.b64decode(credentials).decode("ascii")
        except (ValueError, UnicodeDecodeError, binascii.Error):
            raise AuthenticationError("Invalid credentials")

        username, _, password = decoded.partition(":")
        # Verify password here...
        return AuthCredentials(["authenticated", "admin"]), SimpleUser(username)

middleware = [
    Middleware(AuthenticationMiddleware, backend=BasicAuthBackend()),
]
```

### Using Auth in Endpoints

```python
async def homepage(request):
    if request.user.is_authenticated:
        return PlainTextResponse(f"Hello, {request.user.display_name}")
    return PlainTextResponse("Hello, anonymous")

# Check auth scopes
from starlette.authentication import has_required_scope
if has_required_scope(request, ["admin"]):
    ...
```

### @requires Decorator

```python
from starlette.authentication import requires

@requires("authenticated")
async def dashboard(request):
    return PlainTextResponse("Dashboard")

@requires(["authenticated", "admin"])
async def admin_panel(request):
    return PlainTextResponse("Admin")

# Custom status code
@requires("authenticated", status_code=404)
async def hidden_page(request):
    ...

# Redirect to login
@requires("authenticated", redirect="login")
async def protected(request):
    ...

# On class-based endpoints
class Dashboard(HTTPEndpoint):
    @requires("authenticated")
    async def get(self, request):
        ...
```

### Custom Auth Error Handler

```python
def on_auth_error(request, exc):
    return JSONResponse({"error": str(exc)}, status_code=401)

Middleware(AuthenticationMiddleware,
    backend=BasicAuthBackend(),
    on_error=on_auth_error,
)
```

---

## 11. Exception Handling

### Custom Exception Handlers

```python
from starlette.exceptions import HTTPException, WebSocketException
from starlette.requests import Request
from starlette.websockets import WebSocket
from starlette.responses import JSONResponse, HTMLResponse

# By status code
async def not_found(request: Request, exc: HTTPException):
    return HTMLResponse("<h1>404</h1>", status_code=404)

async def server_error(request: Request, exc: HTTPException):
    return HTMLResponse("<h1>500</h1>", status_code=500)

# By exception class
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        {"detail": exc.detail},
        status_code=exc.status_code,
        headers=exc.headers,
    )

# WebSocket exception handler
async def ws_exception_handler(websocket: WebSocket, exc: WebSocketException):
    await websocket.close(code=1008)

# Global error handler
async def global_error(request: Request, exc: Exception):
    return JSONResponse({"detail": "Internal error"}, status_code=500)

exception_handlers = {
    404: not_found,
    500: server_error,
    HTTPException: http_exception_handler,
    WebSocketException: ws_exception_handler,
    Exception: global_error,
}

app = Starlette(routes=routes, exception_handlers=exception_handlers)
```

### Raising Exceptions

```python
from starlette.exceptions import HTTPException, WebSocketException

# HTTP
raise HTTPException(status_code=404, detail="Not found")
raise HTTPException(status_code=401, headers={"WWW-Authenticate": "Bearer"})

# WebSocket
raise WebSocketException(code=1008, reason="Policy violation")
```

---

## 12. Background Tasks

### Single Task

```python
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse

async def send_email(to_address: str):
    ...

async def signup(request):
    data = await request.json()
    task = BackgroundTask(send_email, to_address=data["email"])
    return JSONResponse({"status": "ok"}, background=task)
```

### Multiple Tasks

```python
from starlette.background import BackgroundTasks

async def signup(request):
    data = await request.json()
    tasks = BackgroundTasks()
    tasks.add_task(send_welcome_email, to_address=data["email"])
    tasks.add_task(send_admin_notification, username=data["username"])
    tasks.add_task(log_signup, data=data)  # sync functions work too
    return JSONResponse({"status": "ok"}, background=tasks)
```

Tasks execute sequentially. If one raises, subsequent tasks are skipped.

---

## 13. Lifespan (Startup / Shutdown)

### Basic Lifespan

```python
import contextlib
from starlette.applications import Starlette

@contextlib.asynccontextmanager
async def lifespan(app):
    # Startup
    print("Starting up...")
    yield
    # Shutdown
    print("Shutting down...")

app = Starlette(routes=routes, lifespan=lifespan)
```

### Lifespan State (Share Resources with Requests)

```python
import contextlib
from typing import AsyncIterator, TypedDict
import httpx
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Route

class AppState(TypedDict):
    http_client: httpx.AsyncClient

@contextlib.asynccontextmanager
async def lifespan(app: Starlette) -> AsyncIterator[AppState]:
    async with httpx.AsyncClient() as client:
        yield {"http_client": client}

async def proxy(request: Request) -> PlainTextResponse:
    # Attribute-style access
    client = request.state.http_client
    # Or dict-style access (type-safe with Request[AppState])
    client = request.state["http_client"]
    resp = await client.get("https://httpbin.org/get")
    return PlainTextResponse(resp.text)

app = Starlette(
    routes=[Route("/proxy", proxy)],
    lifespan=lifespan,
)
```

State is **shallow-copied** per request. Mutable objects (lists, dicts) are shared; immutable values are isolated.

---

## 14. Configuration

### Config from .env Files

```python
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

config = Config(".env")

DEBUG = config("DEBUG", cast=bool, default=False)
DATABASE_URL = config("DATABASE_URL")
SECRET_KEY = config("SECRET_KEY", cast=Secret)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=CommaSeparatedStrings)
```

`.env` file:
```
DEBUG=True
DATABASE_URL=postgresql://user:pass@localhost:5432/db
SECRET_KEY=super-secret-key
ALLOWED_HOSTS=127.0.0.1, localhost
```

**Precedence**: Environment variable > .env file > default > error.

### Secret (Hides in Tracebacks)

```python
from starlette.datastructures import Secret

secret = Secret("my-api-key")
repr(secret)   # Secret('**********')
str(secret)    # "my-api-key"
bool(secret)   # True
```

### Prefixed Environment Variables

```python
import os
os.environ["APP_DEBUG"] = "yes"

config = Config(env_prefix="APP_")
debug = config("DEBUG")  # reads APP_DEBUG -> "yes"
```

### Environment Protection

```python
from starlette.config import environ

# Set BEFORE importing settings modules
environ["DEBUG"] = "TRUE"
environ["TESTING"] = "1"

# After a key is read, modifying it raises EnvironError
```

---

## 15. Data Structures

### URL

```python
from starlette.datastructures import URL

url = URL("https://user:pass@example.com:8080/path?q=1#frag")
url.scheme      # "https"
url.hostname    # "example.com"
url.port        # 8080
url.path        # "/path"
url.query       # "q=1"
url.fragment    # "frag"
url.username    # "user"
url.password    # "pass"
url.is_secure   # True

# Immutable modifications
url2 = url.replace(hostname="other.com", port=443)
url3 = url.include_query_params(page=2)
url4 = url.replace_query_params(q="new")
url5 = url.remove_query_params(["q"])
```

### Headers

```python
from starlette.datastructures import Headers, MutableHeaders

headers = Headers({"content-type": "text/html", "x-custom": "value"})
headers["Content-Type"]     # "text/html" (case-insensitive)
headers.getlist("x-custom") # ["value"]

mutable = headers.mutablecopy()
mutable["X-New"] = "val"
mutable.append("X-Multi", "a")
mutable.append("X-Multi", "b")
mutable.add_vary_header("Accept-Encoding")

# Merge
mutable |= {"X-Extra": "merged"}
```

### QueryParams

```python
from starlette.datastructures import QueryParams

params = QueryParams("page=1&tag=python&tag=async")
params["page"]           # "1"
params.getlist("tag")    # ["python", "async"]
params.multi_items()     # [("page", "1"), ("tag", "python"), ("tag", "async")]
str(params)              # "page=1&tag=python&tag=async"
```

### MultiDict / ImmutableMultiDict

```python
from starlette.datastructures import MultiDict, ImmutableMultiDict

md = MultiDict([("key", "a"), ("key", "b"), ("other", "c")])
md["key"]           # "a" (first value)
md.getlist("key")   # ["a", "b"]
md.multi_items()    # [("key", "a"), ("key", "b"), ("other", "c")]
md.append("key", "d")
md.poplist("key")   # ["a", "b", "d"]
```

### State

```python
from starlette.datastructures import State

state = State()
state.counter = 0
state["counter"] = 1
del state.counter
len(state)
```

### CommaSeparatedStrings

```python
from starlette.datastructures import CommaSeparatedStrings

hosts = CommaSeparatedStrings("127.0.0.1, localhost, example.com")
list(hosts)  # ["127.0.0.1", "localhost", "example.com"]
```

---

## 16. Testing

### TestClient (Synchronous)

```python
from starlette.testclient import TestClient

client = TestClient(app)
response = client.get("/")
assert response.status_code == 200
assert response.json() == {"hello": "world"}

# POST with JSON
response = client.post("/users", json={"name": "Alice"})

# POST with form data
response = client.post("/upload", data={"field": "value"})

# File upload
with open("test.txt", "rb") as f:
    response = client.post("/upload", files={"file": f})

# Multiple files
files = {"file1": open("a.txt", "rb"), "file2": ("name.png", open("b.png", "rb"), "image/png")}
response = client.post("/upload", files=files)

# Custom headers
response = client.get("/", headers={"Authorization": "Bearer token123"})
client.headers = {"Authorization": "Bearer token123"}

# Don't follow redirects
response = client.get("/redirect", follow_redirects=False)
```

### Testing with Lifespan

```python
def test_with_lifespan():
    with TestClient(app) as client:  # triggers startup
        response = client.get("/")
        assert response.status_code == 200
    # shutdown runs here
```

### Testing Error Responses

```python
client = TestClient(app, raise_server_exceptions=False)
response = client.get("/error")
assert response.status_code == 500
```

### WebSocket Testing

```python
def test_websocket():
    client = TestClient(app)
    with client.websocket_connect("/ws") as ws:
        ws.send_text("hello")
        data = ws.receive_text()
        assert data == "Echo: hello"

    with client.websocket_connect("/ws", subprotocols=["graphql-ws"]) as ws:
        ws.send_json({"type": "connection_init"})
        msg = ws.receive_json()
        ws.close(code=1000)
```

### Async Testing (with httpx)

```python
from httpx import AsyncClient, ASGITransport

async def test_async():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/")
        assert response.status_code == 200
```

### Backend Selection (asyncio vs trio)

```python
with TestClient(app, backend="trio") as client:
    ...

with TestClient(app, backend_options={"use_uvloop": True}) as client:
    ...
```

---

## 17. API Schemas (OpenAPI)

### Schema from Docstrings

```python
from starlette.schemas import SchemaGenerator
from starlette.routing import Route

schemas = SchemaGenerator(
    {"openapi": "3.0.0", "info": {"title": "My API", "version": "1.0"}}
)

async def list_users(request):
    """
    responses:
      200:
        description: A list of users.
        examples:
          [{"username": "tom"}]
    """
    ...

async def openapi_schema(request):
    return schemas.OpenAPIResponse(request=request)

routes = [
    Route("/users", list_users, methods=["GET"]),
    Route("/schema", openapi_schema, include_in_schema=False),
]
```

---

## 18. Thread Pool

Sync endpoints, FileResponse, UploadFile, and sync BackgroundTasks run in a thread pool
(default 40 concurrent threads via anyio).

```python
import anyio.to_thread

# Increase thread pool size
limiter = anyio.to_thread.current_default_thread_limiter()
limiter.total_tokens = 100
```

### run_in_threadpool

```python
from starlette.concurrency import run_in_threadpool

async def handler(request):
    result = await run_in_threadpool(blocking_function, arg1, arg2)
    return JSONResponse({"result": result})
```

---

## 19. WSGI Compatibility

```python
from starlette.middleware.wsgi import WSGIMiddleware

# Wrap a Flask/Django WSGI app
def flask_app(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/plain")])
    return [b"Hello from WSGI"]

routes = [
    Mount("/legacy", app=WSGIMiddleware(flask_app)),
]
```

Note: `WSGIMiddleware` is deprecated in 1.0. Use `a2wsgi` package instead.

---

## 20. Status Codes

```python
from starlette import status

status.HTTP_200_OK            # 200
status.HTTP_201_CREATED       # 201
status.HTTP_204_NO_CONTENT    # 204
status.HTTP_301_MOVED_PERMANENTLY  # 301
status.HTTP_307_TEMPORARY_REDIRECT # 307
status.HTTP_400_BAD_REQUEST   # 400
status.HTTP_401_UNAUTHORIZED  # 401
status.HTTP_403_FORBIDDEN     # 403
status.HTTP_404_NOT_FOUND     # 404
status.HTTP_422_UNPROCESSABLE_CONTENT  # 422
status.HTTP_500_INTERNAL_SERVER_ERROR  # 500

# WebSocket
status.WS_1000_NORMAL_CLOSURE    # 1000
status.WS_1001_GOING_AWAY        # 1001
status.WS_1008_POLICY_VIOLATION  # 1008
```

---

## Common Patterns

### Full REST API Example

```python
import contextlib
from starlette.applications import Starlette
from starlette.endpoints import HTTPEndpoint
from starlette.exceptions import HTTPException
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.routing import Route

ITEMS: dict[int, dict] = {}

@contextlib.asynccontextmanager
async def lifespan(app):
    ITEMS[1] = {"id": 1, "name": "Widget"}
    yield
    ITEMS.clear()

class ItemList(HTTPEndpoint):
    async def get(self, request):
        return JSONResponse(list(ITEMS.values()))

    async def post(self, request):
        data = await request.json()
        item_id = max(ITEMS.keys(), default=0) + 1
        ITEMS[item_id] = {"id": item_id, **data}
        return JSONResponse(ITEMS[item_id], status_code=201)

class ItemDetail(HTTPEndpoint):
    async def get(self, request):
        item_id = request.path_params["item_id"]
        if item_id not in ITEMS:
            raise HTTPException(status_code=404, detail="Item not found")
        return JSONResponse(ITEMS[item_id])

    async def put(self, request):
        item_id = request.path_params["item_id"]
        if item_id not in ITEMS:
            raise HTTPException(status_code=404, detail="Item not found")
        data = await request.json()
        ITEMS[item_id] = {"id": item_id, **data}
        return JSONResponse(ITEMS[item_id])

    async def delete(self, request):
        item_id = request.path_params["item_id"]
        if item_id not in ITEMS:
            raise HTTPException(status_code=404, detail="Item not found")
        del ITEMS[item_id]
        return JSONResponse({"deleted": item_id})

routes = [
    Route("/items", ItemList),
    Route("/items/{item_id:int}", ItemDetail),
]

middleware = [
    Middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"]),
]

app = Starlette(routes=routes, middleware=middleware, lifespan=lifespan)
```

### Server-Sent Events (SSE)

```python
import asyncio
from starlette.responses import StreamingResponse

async def event_stream():
    count = 0
    while True:
        count += 1
        yield f"data: Event {count}\n\n"
        await asyncio.sleep(1)

async def sse_endpoint(request):
    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )
```

### File Upload with Background Processing

```python
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse

async def process_file(content: bytes, filename: str):
    # Heavy processing in background
    ...

async def upload(request):
    async with request.form() as form:
        upload = form["file"]
        content = await upload.read()
        filename = upload.filename

    task = BackgroundTask(process_file, content=content, filename=filename)
    return JSONResponse({"filename": filename, "size": len(content)}, background=task)
```

### Multi-Tenant with Host Routing

```python
from starlette.routing import Host, Route, Mount

async def tenant_home(request):
    subdomain = request.path_params["tenant"]
    return PlainTextResponse(f"Welcome to {subdomain}")

routes = [
    Host("{tenant}.myapp.com", app=Router(routes=[
        Route("/", tenant_home),
    ]), name="tenant"),
]
```

---

## Dependencies & Compatibility

| Feature | Required Package |
|---|---|
| Core | `anyio>=3.6.2,<5` |
| TestClient | `httpx>=0.27.0,<0.29.0` |
| Templates | `jinja2` |
| Form parsing | `python-multipart>=0.0.18` |
| Sessions | `itsdangerous` |
| Schema YAML | `pyyaml` |
| Python | `>=3.10` |
| Async backends | `asyncio` (default), `trio` |

## ASGI Servers

- **uvicorn** (recommended): `uvicorn myapp:app --reload`
- **daphne**: `daphne myapp:app`
- **hypercorn**: `hypercorn myapp:app`
