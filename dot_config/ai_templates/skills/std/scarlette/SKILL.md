---
name: starlette
description: >
  Build async Python web applications and APIs with Starlette 1.0, the lightweight ASGI
  framework. Use this skill when creating HTTP endpoints, WebSocket servers, middleware,
  routing, static file serving, templates, authentication, background tasks, configuration,
  testing, or any ASGI application. Triggers on mentions of Starlette, ASGI framework,
  async web Python, or when building APIs that need routing, middleware, WebSocket support,
  or server-sent events with Python's async ecosystem. Also use when the user mentions
  FastAPI internals, since FastAPI is built on Starlette.
---

# Starlette 1.0 -- Complete Reference

Starlette 1.0.0 is a lightweight ASGI framework/toolkit for async web services in Python.
Requires Python >= 3.10. Core dependency: `anyio` (supports both asyncio and trio).

---

## Quick Start

```bash
uv init myapp && cd myapp
uv add starlette uvicorn
```

Create `app.py`:

```python
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route


async def homepage(request: Request) -> JSONResponse:
    return JSONResponse({"hello": "world"})


app = Starlette(routes=[
    Route("/", homepage),
])
```

Run:

```bash
uv run uvicorn app:app --reload
```

Starlette can also be used as a bare ASGI toolkit without the framework class:

```python
from starlette.responses import PlainTextResponse


async def app(scope, receive, send):
    assert scope["type"] == "http"
    response = PlainTextResponse("Hello, world!")
    await response(scope, receive, send)
```

Both sync and async endpoint functions are supported. Sync functions automatically
run in a thread pool so they don't block the event loop:

```python
def sync_homepage(request: Request) -> JSONResponse:
    # Runs in threadpool automatically -- safe to call blocking I/O here
    return JSONResponse({"sync": True})
```

---

## 1. Application Setup

### Full Application

```python
import contextlib
from typing import AsyncIterator, TypedDict

import httpx
from starlette.applications import Starlette
from starlette.config import Config
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Mount, Route, WebSocketRoute
from starlette.staticfiles import StaticFiles
from starlette.websockets import WebSocket


# --- Configuration ---
config = Config(".env")
DEBUG = config("DEBUG", cast=bool, default=False)
SECRET_KEY = config("SECRET_KEY", default="change-me-in-production")


# --- Lifespan (startup / shutdown) ---
class AppState(TypedDict):
    http_client: httpx.AsyncClient


@contextlib.asynccontextmanager
async def lifespan(app: Starlette) -> AsyncIterator[AppState]:
    async with httpx.AsyncClient() as client:
        yield {"http_client": client}


# --- Endpoints ---
async def homepage(request: Request) -> PlainTextResponse:
    return PlainTextResponse("Hello, world!")


async def user_detail(request: Request) -> PlainTextResponse:
    username = request.path_params["username"]
    return PlainTextResponse(f"Hello, {username}!")


async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()
    await websocket.send_text("Connected!")
    await websocket.close()


# --- Routes ---
routes = [
    Route("/", homepage),
    Route("/users/{username}", user_detail),
    WebSocketRoute("/ws", websocket_endpoint),
    Mount("/static", StaticFiles(directory="static"), name="static"),
]

# --- Middleware (execution order: top to bottom) ---
middleware = [
    Middleware(CORSMiddleware, allow_origins=["*"]),
    Middleware(SessionMiddleware, secret_key=SECRET_KEY),
]

# --- App ---
app = Starlette(
    debug=DEBUG,
    routes=routes,
    middleware=middleware,
    lifespan=lifespan,
)
```

### Application State

```python
# Global mutable state on the app instance
app.state.ADMIN_EMAIL = "admin@example.org"

# Access from any endpoint via request.app
async def homepage(request: Request) -> PlainTextResponse:
    admin = request.app.state.ADMIN_EMAIL
    return PlainTextResponse(f"Admin: {admin}")
```

### Dynamic Registration (alternative to declarative routes)

```python
app.add_middleware(CORSMiddleware, allow_origins=["*"])
app.add_route("/health", health_check, methods=["GET"])
app.add_exception_handler(404, custom_404_handler)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.host("api.example.com", api_app, name="api")
```

---

## 2. Configuration

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

```shell
# .env
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
SECRET_KEY=43n080musdfjt54t-09sdgr
ALLOWED_HOSTS=127.0.0.1, localhost
```

**Precedence**: environment variable > .env file > default > raises KeyError.

### Secret (Hidden in Tracebacks)

```python
secret = Secret("my-api-key")
repr(secret)   # Secret('**********')  -- safe in logs/tracebacks
str(secret)    # "my-api-key"          -- explicit str() to reveal
bool(secret)   # True                  -- empty string is False
```

### Prefixed Environment Variables

```python
import os
os.environ["MYAPP_DEBUG"] = "yes"

config = Config(env_prefix="MYAPP_")
debug = config("DEBUG")  # reads MYAPP_DEBUG -> "yes"
```

### Custom .env Encoding

```python
config = Config(".env", encoding="latin-1")
```

### Environment Protection (for Testing)

```python
from starlette.config import environ

# Must set BEFORE any config reads occur
environ["DEBUG"] = "TRUE"
environ["TESTING"] = "1"
# After a key is read by Config, writing to it raises EnvironError
```

---

## 3. Lifespan (Startup / Shutdown)

### Basic Lifespan

```python
import contextlib
from starlette.applications import Starlette

@contextlib.asynccontextmanager
async def lifespan(app):
    # Startup: runs before the first request is served
    print("Starting up...")
    yield
    # Shutdown: runs after all connections close and background tasks complete
    print("Shutting down...")

app = Starlette(routes=routes, lifespan=lifespan)
```

### Typed Lifespan State (Share Resources with Requests)

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
    # Dict-style access (type-safe when using Request[AppState])
    client = request.state["http_client"]
    resp = await client.get("https://httpbin.org/get")
    return PlainTextResponse(resp.text)


app = Starlette(routes=[Route("/proxy", proxy)], lifespan=lifespan)
```

**Shallow copy semantics**: state is shallow-copied per request. Mutable objects
(lists, dicts) are shared across concurrent requests; immutable values are isolated.

### Testing with Lifespan

```python
from starlette.testclient import TestClient

def test_with_lifespan():
    with TestClient(app) as client:  # triggers startup
        response = client.get("/proxy")
        assert response.status_code == 200
    # shutdown runs when context manager exits
```

---

## 4. Routing

### HTTP Routes with Path Parameters

```python
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Route


async def user_detail(request: Request) -> PlainTextResponse:
    user_id = request.path_params["user_id"]
    return PlainTextResponse(f"User {user_id}")


routes = [
    Route("/", homepage),
    Route("/users/{user_id:int}", user_detail, methods=["GET"]),
    Route("/files/{filepath:path}", serve_file),
    Route("/items/{item_id:uuid}", item_detail),
    Route("/price/{amount:float}", show_price),
]
```

**Built-in path convertors**: `str` (default -- any non-slash chars), `int`, `float`, `uuid`, `path` (any chars including slashes).

### Custom Path Convertor

```python
from datetime import datetime
from starlette.convertors import Convertor, register_url_convertor


class DateTimeConvertor(Convertor[datetime]):
    regex = r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}"

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
    Mount("/api/v1", routes=[
        Route("/items", items_list),
    ]),
]
```

### Mount Sub-Applications

```python
routes = [
    Mount("/static", app=StaticFiles(directory="static"), name="static"),
    Mount("/admin", app=admin_app),  # any ASGI app
]
```

### Host-Based Routing

```python
from starlette.routing import Host

routes = [
    Host("api.example.org", app=api_app, name="api"),
    Host("{subdomain}.example.org", app=subdomain_app, name="subdomain"),
]
```

Port is stripped for matching. Host patterns support path-style parameters.

### Reverse URL Lookups

```python
# From request (returns full URL with scheme and host)
url = request.url_for("user_detail", username="tom")

# Nested mount names use colon separator
url = request.url_for("users:user_detail", username="tom")

# Static file URL
url = request.url_for("static", path="/css/style.css")

# Without request context (returns URLPath -- path only, no host/scheme)
path = app.url_path_for("user_detail", username="tom")

# Convert URLPath to absolute URL
absolute = path.make_absolute_url(base_url="https://example.com")
```

### Route Priority

First match wins. Place specific routes before parameterized ones:

```python
routes = [
    Route("/users/me", current_user),       # specific -- checked first
    Route("/users/{username}", user_detail), # parameterized -- checked second
]
```

### Router (Lightweight, Without App Middleware)

```python
from starlette.routing import Router

router = Router(
    routes=[Route("/", homepage)],
    redirect_slashes=True,  # /users/ redirects to /users
)
```

---

## 5. Requests

### Properties

```python
from starlette.requests import Request

async def handler(request: Request):
    request.method              # "GET", "POST", etc.
    request.url                 # URL object (str-like): "https://example.com/path?q=1"
    request.url.path            # "/path"
    request.url.scheme          # "https"
    request.url.port            # 443
    request.base_url            # URL for the app root (scheme + host + root_path)
    request.headers             # Headers -- case-insensitive, immutable multi-dict
    request.headers["content-type"]
    request.headers.getlist("x-forwarded-for")
    request.query_params        # QueryParams -- immutable multi-dict
    request.query_params["q"]
    request.query_params.getlist("tag")
    request.path_params         # dict[str, Any] from route convertors
    request.cookies             # dict[str, str]
    request.client              # Address(host, port) or None
    request.app                 # the Starlette/Router instance
    request.state               # State object for per-request data
    request.session             # dict -- requires SessionMiddleware
    request.user                # BaseUser -- requires AuthenticationMiddleware
    request.auth                # AuthCredentials -- requires AuthenticationMiddleware
```

### Body Access

```python
# Full body as bytes (cached after first call)
body: bytes = await request.body()

# JSON (cached after first call)
data: Any = await request.json()

# Streaming body (for large payloads -- cannot use body()/json() after)
async for chunk in request.stream():
    process(chunk)

# Form data -- usable as EITHER await OR async context manager
# As context manager (recommended -- auto-closes upload files):
async with request.form() as form:
    username = form["username"]        # str field
    upload = form["file"]              # UploadFile
    contents = await upload.read()

# As awaitable (caller must close):
form = await request.form()
try:
    username = form["username"]
finally:
    await request.close()

# Form with custom limits
async with request.form(
    max_files=100,              # default 1000
    max_fields=500,             # default 1000
    max_part_size=5*1024*1024,  # default 1MB
) as form:
    ...
```

**Requires**: `uv add python-multipart` for `request.form()`.

### UploadFile

```python
async with request.form() as form:
    upload = form["file"]

    # Properties
    upload.filename       # str | None -- "photo.jpg"
    upload.content_type   # str | None -- "image/jpeg" (from Content-Type header)
    upload.size           # int | None -- file size in bytes
    upload.headers        # Headers -- all headers for this part

    # Async I/O methods
    content = await upload.read(size=-1)  # read all or N bytes
    await upload.seek(0)                  # rewind
    await upload.write(b"data")           # write (for in-memory modification)
    await upload.close()                  # explicit close
```

### Request State

```python
import time

# Middleware sets state
request.state.start_time = time.time()

# Endpoint reads it
elapsed = time.time() - request.state.start_time

# Dict-style access works too
request.state["key"] = "value"
val = request.state["key"]
```

### Disconnect Detection

```python
import asyncio

async def long_poll(request: Request):
    while not await request.is_disconnected():
        await asyncio.sleep(1)
    return Response("Client left")
```

### Server Push (HTTP/2 -- requires server support)

```python
async def homepage(request: Request):
    await request.send_push_promise("/static/style.css")  # no-op if unsupported
    return HTMLResponse('<html><head><link rel="stylesheet" href="/static/style.css"/></head></html>')
```

---

## 6. Responses

### Response Types

```python
from starlette.responses import (
    Response, PlainTextResponse, HTMLResponse,
    JSONResponse, RedirectResponse, StreamingResponse, FileResponse,
)

# Plain text
PlainTextResponse("Hello")

# HTML
HTMLResponse("<h1>Hello</h1>")

# JSON
JSONResponse({"key": "value"})
JSONResponse({"error": "not found"}, status_code=404)

# Generic (specify media_type)
Response(b"\x89PNG...", media_type="image/png")

# Redirect (default 307 Temporary Redirect)
RedirectResponse(url="/new-location")
RedirectResponse(url="/permanent", status_code=301)

# Empty (no body, no content-type)
Response(status_code=204)
```

### Custom JSON Serialization

```python
import orjson
from starlette.responses import JSONResponse


class OrjsonResponse(JSONResponse):
    media_type = "application/json"

    def render(self, content) -> bytes:
        return orjson.dumps(content)
```

### Custom Response Type

```python
from starlette.responses import Response


class XMLResponse(Response):
    media_type = "application/xml"
    charset = "utf-8"
```

### Streaming Response

```python
import asyncio
from starlette.responses import StreamingResponse


async def number_stream():
    for i in range(100):
        yield f"data: {i}\n"
        await asyncio.sleep(0.1)


async def stream_endpoint(request: Request):
    return StreamingResponse(number_stream(), media_type="text/plain")
```

Both sync iterables and async iterables/generators work.

### File Response (with Range Request Support)

```python
from starlette.responses import FileResponse

# Download (Content-Disposition: attachment)
FileResponse("report.pdf")

# Inline display in browser
FileResponse("image.png", filename="photo.png", content_disposition_type="inline")

# Custom media type
FileResponse("data.bin", media_type="application/octet-stream")
```

Automatically handles: `Accept-Ranges`, single/multi-range requests (206),
`If-Range`/`If-None-Match` conditionals (304), ETag, Last-Modified, HEAD requests.

### Cookies

```python
response = JSONResponse({"ok": True})

response.set_cookie(
    key="session_id",
    value="abc123",
    max_age=3600,               # seconds until expiry
    expires=None,               # datetime | str | int | None
    path="/",                   # cookie path scope (None omits Path)
    domain=None,                # ".example.com"
    secure=True,                # HTTPS only
    httponly=True,               # no JavaScript access
    samesite="lax",             # "lax" | "strict" | "none" | None (omit attr)
    # partitioned=True,         # Python 3.14+ only -- CHIPS partitioned cookies
)

response.delete_cookie(key="session_id", path="/")
```

### Response Headers

```python
response = JSONResponse({"data": 1})
response.headers["X-Request-Id"] = "abc-123"
response.headers.append("X-Multi", "value1")
response.headers.append("X-Multi", "value2")
```

---

## 7. Endpoints (Class-Based Views)

### HTTPEndpoint

```python
from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route


class UserEndpoint(HTTPEndpoint):
    async def get(self, request: Request) -> JSONResponse:
        return JSONResponse([{"name": "Alice"}, {"name": "Bob"}])

    async def post(self, request: Request) -> JSONResponse:
        data = await request.json()
        return JSONResponse(data, status_code=201)

    async def delete(self, request: Request) -> JSONResponse:
        return JSONResponse({"deleted": True})


# Pass the CLASS (not instance) to Route
routes = [Route("/users", UserEndpoint)]
```

Unhandled methods return 405 Method Not Allowed with `Allow` header.

### WebSocketEndpoint

```python
from starlette.endpoints import WebSocketEndpoint
from starlette.routing import WebSocketRoute
from starlette.websockets import WebSocket


class EchoEndpoint(WebSocketEndpoint):
    encoding = "text"  # "text" | "bytes" | "json" | None

    async def on_connect(self, websocket: WebSocket) -> None:
        await websocket.accept()

    async def on_receive(self, websocket: WebSocket, data: str) -> None:
        await websocket.send_text(f"Echo: {data}")

    async def on_disconnect(self, websocket: WebSocket, close_code: int) -> None:
        pass


routes = [WebSocketRoute("/ws", EchoEndpoint)]
```

---

## 8. Middleware

### Declaring Middleware

```python
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

middleware = [
    # Outermost -- processed first on request, last on response
    Middleware(TrustedHostMiddleware, allowed_hosts=["example.com", "*.example.com"]),
    Middleware(HTTPSRedirectMiddleware),
    Middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]),
    Middleware(GZipMiddleware, minimum_size=1000, compresslevel=9),
    Middleware(SessionMiddleware, secret_key="use-a-real-secret-here"),
    # Innermost
]

app = Starlette(routes=routes, middleware=middleware)
```

**Execution order**: `ServerErrorMiddleware` (auto) -> user middleware top-to-bottom -> `ExceptionMiddleware` (auto) -> Router -> Endpoint.

### CORSMiddleware

```python
Middleware(CORSMiddleware,
    allow_origins=["https://example.com"],
    allow_origin_regex=r"https://.*\.example\.org",  # use tight patterns, not ".*"
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
    allow_credentials=True,
    allow_private_network=True,   # Private Network Access (PNA)
    expose_headers=["X-Request-Id"],
    max_age=600,                  # preflight cache in seconds
)
```

To apply CORS headers to error responses too, wrap outside Starlette:

```python
app = Starlette(routes=routes)
app = CORSMiddleware(app=app, allow_origins=["*"])
```

**Warning**: Overly permissive `allow_origin_regex` (e.g., `".*"`) can allow
any origin. Always use fullmatch patterns like `r"https://.*\.example\.org"`.

### SessionMiddleware

```python
Middleware(SessionMiddleware,
    secret_key="use-a-real-secret",  # required
    session_cookie="session",         # cookie name
    max_age=14 * 24 * 60 * 60,       # 2 weeks; None = browser session cookie
    same_site="lax",                  # "lax" | "strict" | "none"
    path="/",
    https_only=False,                 # True sets Secure flag
    domain=None,                      # ".example.com"
)
```

Session cookies are always HttpOnly (not accessible from JavaScript).
The `Set-Cookie` header is only sent when the session is modified, not on read-only access.

```python
async def handler(request: Request):
    request.session["user"] = "alice"           # set
    username = request.session.get("user")      # get
    request.session.pop("user", None)           # remove
    request.session.clear()                     # clear all
```

**Requires**: `uv add itsdangerous`

### GZipMiddleware

```python
Middleware(GZipMiddleware,
    minimum_size=500,     # skip compression below this (bytes)
    compresslevel=9,      # 1 = fastest, 9 = smallest
)
```

Skips compression when: Content-Encoding already set, Content-Type is `text/event-stream`, or response uses `http.response.pathsend`.

### TrustedHostMiddleware

```python
Middleware(TrustedHostMiddleware,
    allowed_hosts=["example.com", "*.example.com"],
    www_redirect=True,  # redirect example.com -> www.example.com
)
```

### HTTPSRedirectMiddleware

```python
Middleware(HTTPSRedirectMiddleware)
# http -> https, ws -> wss (307 Temporary Redirect)
```

### BaseHTTPMiddleware (Custom Request/Response Middleware)

```python
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        start = time.time()
        response = await call_next(request)
        response.headers["X-Process-Time"] = f"{time.time() - start:.4f}"
        return response
```

With constructor parameters:

```python
class CustomHeaderMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, header_value: str = "default"):
        super().__init__(app)
        self.header_value = header_value

    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        response.headers["X-Custom"] = self.header_value
        return response

Middleware(CustomHeaderMiddleware, header_value="production")
```

**Caveat**: BaseHTTPMiddleware prevents `contextvars.ContextVar` changes from
propagating upward through the middleware stack. Use pure ASGI middleware if you
need contextvar propagation.

### Pure ASGI Middleware (Maximum Control)

```python
from starlette.types import ASGIApp, Message, Receive, Scope, Send


class PureASGIMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                from starlette.datastructures import MutableHeaders
                headers = MutableHeaders(scope=message)
                headers.append("X-Custom", "value")
            await send(message)

        await self.app(scope, receive, send_wrapper)
```

**Key patterns for pure ASGI middleware**:

Wrap `receive` to inspect/modify request body:
```python
async def __call__(self, scope, receive, send):
    if scope["type"] != "http":
        await self.app(scope, receive, send)
        return

    body_size = 0

    async def counting_receive():
        nonlocal body_size
        message = await receive()
        body_size += len(message.get("body", b""))
        return message

    await self.app(scope, counting_receive, send)
```

Wrap `send` to inspect/modify response:
```python
async def __call__(self, scope, receive, send):
    if scope["type"] != "http":
        await self.app(scope, receive, send)
        return

    async def send_with_headers(message):
        if message["type"] == "http.response.start":
            from starlette.datastructures import MutableHeaders
            headers = MutableHeaders(scope=message)
            headers["X-Added"] = "value"
        await send(message)

    await self.app(scope, receive, send_with_headers)
```

Short-circuit with an early response:
```python
async def __call__(self, scope, receive, send):
    if scope["type"] == "http" and URL(scope=scope).path == "/blocked":
        response = PlainTextResponse("Blocked", status_code=403)
        await response(scope, receive, send)
        return
    await self.app(scope, receive, send)
```

Inject data into scope for downstream access:
```python
import uuid

async def __call__(self, scope, receive, send):
    scope["request_id"] = str(uuid.uuid4())
    await self.app(scope, receive, send)
```

**Statelessness rule**: per-connection state must live in `__call__`, not on `self`.

### Middleware on Individual Routes

```python
routes = [
    Route("/compressed", handler, middleware=[Middleware(GZipMiddleware)]),
    Mount("/api", routes=api_routes, middleware=[Middleware(AuthMiddleware)]),
]
router = Router(routes=routes, middleware=[Middleware(LoggingMiddleware)])
```

Route-level middleware is NOT wrapped in `ExceptionMiddleware` -- exceptions
propagate directly.

---

## 9. Exception Handling

### Registering Handlers

```python
from starlette.exceptions import HTTPException, WebSocketException
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse
from starlette.websockets import WebSocket


async def not_found(request: Request, exc: HTTPException) -> HTMLResponse:
    return HTMLResponse("<h1>Page Not Found</h1>", status_code=404)


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        {"detail": exc.detail},
        status_code=exc.status_code,
        headers=exc.headers,
    )


async def ws_exception_handler(websocket: WebSocket, exc: WebSocketException) -> None:
    await websocket.close(code=1008)


async def global_error_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse({"detail": "Internal server error"}, status_code=500)


exception_handlers = {
    404: not_found,                         # by status code
    HTTPException: http_exception_handler,  # by exception class
    WebSocketException: ws_exception_handler,
    Exception: global_error_handler,        # catch-all for unhandled errors
}

app = Starlette(routes=routes, exception_handlers=exception_handlers)
```

### Raising Exceptions

```python
from starlette.exceptions import HTTPException, WebSocketException

# In endpoints or route handlers (not middleware):
raise HTTPException(status_code=404, detail="Item not found")
raise HTTPException(status_code=401, headers={"WWW-Authenticate": "Bearer"})

# In WebSocket handlers:
raise WebSocketException(code=1008, reason="Policy violation")
```

`HTTPException` raised in a WebSocket handler before `accept()` sends a proper
HTTP error response (not a WebSocket close frame).

### Middleware Stack and Errors

- **Handled exceptions** (`HTTPException`): caught by `ExceptionMiddleware`, converted to responses
- **Unhandled exceptions**: bubble up to `ServerErrorMiddleware`, which returns 500 or debug traceback
- `debug=True` overrides 500 handlers with interactive traceback pages

---

## 10. WebSockets

### Function-Based Handler

```python
from starlette.websockets import WebSocket, WebSocketDisconnect


async def websocket_handler(websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        while True:
            text = await websocket.receive_text()
            await websocket.send_text(f"Echo: {text}")
    except WebSocketDisconnect:
        print("Client disconnected")
```

### Send and Receive Methods

```python
await websocket.send_text("hello")
await websocket.send_bytes(b"\x00\x01")
await websocket.send_json({"key": "value"})             # text frame (default)
await websocket.send_json({"key": "value"}, mode="binary")  # binary frame

text: str = await websocket.receive_text()
data: bytes = await websocket.receive_bytes()
obj: Any = await websocket.receive_json()
obj: Any = await websocket.receive_json(mode="binary")
```

### Async Iterators (Auto-Handle Disconnect)

```python
async def echo(websocket: WebSocket) -> None:
    await websocket.accept()
    async for message in websocket.iter_text():
        await websocket.send_text(f"Echo: {message}")
    # Loop exits cleanly on WebSocketDisconnect

# Also: websocket.iter_bytes(), websocket.iter_json()
```

### Subprotocol and Accept Headers

```python
await websocket.accept(
    subprotocol="graphql-ws",
    headers=[(b"x-request-id", b"abc123")],
)
```

### Rejection (Denial Response)

```python
from starlette.responses import JSONResponse

async def auth_ws(websocket: WebSocket) -> None:
    token = websocket.query_params.get("token")
    if not valid_token(token):
        # Send a full HTTP response instead of upgrading
        await websocket.send_denial_response(
            JSONResponse({"error": "unauthorized"}, status_code=401)
        )
        return
    await websocket.accept()
    ...
```

### WebSocket Properties

Same as Request: `websocket.url`, `websocket.headers`, `websocket.query_params`,
`websocket.path_params`, `websocket.client`, `websocket.cookies`, `websocket.state`.

---

## 11. Static Files

```python
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

routes = [
    Mount("/static", app=StaticFiles(directory="static"), name="static"),
]
```

### HTML Mode (SPA / Directory Index)

```python
# Auto-serves index.html for directories; serves 404.html on not found
Mount("/", app=StaticFiles(directory="public", html=True))
```

### Package Static Files

```python
StaticFiles(packages=["bootstrap4"])                      # "statics" subdir (default)
StaticFiles(packages=[("bootstrap4", "static")])          # custom subdir
StaticFiles(directory="static", packages=["bootstrap4"])  # combine
```

### All Options

```python
StaticFiles(
    directory="static",
    packages=None,
    html=False,            # serve index.html for directories
    check_dir=True,        # validate directory exists on startup
    follow_symlink=False,  # follow symbolic links
)
```

Handles ETag, If-None-Match (304), If-Modified-Since, Content-Type detection, path traversal prevention.

---

## 12. Templates

```python
from starlette.requests import Request
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


async def homepage(request: Request):
    return templates.TemplateResponse(request, "index.html", {"title": "Home"})


routes = [
    Route("/", homepage),
    Mount("/static", StaticFiles(directory="static"), name="static"),
]
```

**Requires**: `uv add jinja2`

### url_for in Templates

Automatically available in every template:

```html
<link href="{{ url_for('static', path='/css/style.css') }}" rel="stylesheet" />
<a href="{{ url_for('user_detail', username='tom') }}">Profile</a>
```

### Custom Filters

```python
templates = Jinja2Templates(directory="templates")
templates.env.filters["markdown"] = lambda text: markdown.markdown(text)
```

### Context Processors

```python
def global_context(request: Request) -> dict:
    return {"app_name": "MyApp", "current_user": request.user}

templates = Jinja2Templates(
    directory="templates",
    context_processors=[global_context],  # sync only, not async
)
```

### Custom Jinja2 Environment

```python
import jinja2

env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"), autoescape=True)
templates = Jinja2Templates(env=env)
```

When using `directory=`, autoescape is enabled by default for `.html`, `.htm`, `.xml`.

### Testing Templates

```python
def test_homepage():
    client = TestClient(app)
    response = client.get("/")
    assert response.template.name == "index.html"
    assert "title" in response.context
```

---

## 13. Authentication

### Backend Implementation

```python
import base64
import binascii

from starlette.authentication import (
    AuthCredentials, AuthenticationBackend, AuthenticationError, SimpleUser,
)
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import Request


class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn):
        if "Authorization" not in conn.headers:
            return None  # unauthenticated -- sets UnauthenticatedUser

        auth = conn.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() != "basic":
                return None
            decoded = base64.b64decode(credentials).decode("ascii")
        except (ValueError, UnicodeDecodeError, binascii.Error):
            raise AuthenticationError("Invalid basic auth credentials")

        username, _, password = decoded.partition(":")
        # Verify password here...
        return AuthCredentials(["authenticated", "admin"]), SimpleUser(username)


middleware = [
    Middleware(AuthenticationMiddleware, backend=BasicAuthBackend()),
]
```

### Using Auth in Endpoints

```python
async def homepage(request: Request):
    if request.user.is_authenticated:
        return PlainTextResponse(f"Hello, {request.user.display_name}")
    return PlainTextResponse("Hello, anonymous")
```

### Checking Scopes Programmatically

```python
from starlette.authentication import has_required_scope

async def handler(request: Request):
    if has_required_scope(request, ["admin"]):
        ...  # admin-only logic
```

### @requires Decorator

```python
from starlette.authentication import requires

@requires("authenticated")
async def dashboard(request: Request):
    ...

@requires(["authenticated", "admin"])
async def admin_panel(request: Request):
    ...

@requires("authenticated", status_code=404)   # hide existence of page
async def hidden_page(request: Request):
    ...

@requires("authenticated", redirect="login")  # preserves ?next= for return URL
async def protected(request: Request):
    ...

# On class-based endpoints
class Dashboard(HTTPEndpoint):
    @requires("authenticated")
    async def get(self, request: Request):
        ...
```

### Custom Auth Error Handler

```python
from starlette.responses import JSONResponse

def on_auth_error(request, exc):
    return JSONResponse({"error": str(exc)}, status_code=401)

Middleware(AuthenticationMiddleware, backend=BasicAuthBackend(), on_error=on_auth_error)
```

---

## 14. Background Tasks

### Single Task

```python
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse


async def send_welcome_email(to_address: str) -> None:
    ...  # async I/O here


async def signup(request: Request) -> JSONResponse:
    data = await request.json()
    task = BackgroundTask(send_welcome_email, to_address=data["email"])
    return JSONResponse({"status": "ok"}, background=task)
```

### Multiple Tasks

```python
from starlette.background import BackgroundTasks


async def signup(request: Request) -> JSONResponse:
    data = await request.json()
    tasks = BackgroundTasks()
    tasks.add_task(send_welcome_email, to_address=data["email"])
    tasks.add_task(send_admin_notification, username=data["username"])
    tasks.add_task(log_signup, data=data)  # sync functions work too (run in threadpool)
    return JSONResponse({"status": "ok"}, background=tasks)
```

Tasks execute sequentially in order. If one raises an exception, subsequent tasks are skipped.

---

## 15. Testing

### TestClient (Synchronous, Built on httpx)

```python
from starlette.testclient import TestClient

client = TestClient(app)

# HTTP methods
response = client.get("/")
response = client.post("/users", json={"name": "Alice"})
response = client.put("/users/1", json={"name": "Bob"})
response = client.patch("/users/1", json={"name": "Charlie"})
response = client.delete("/users/1")

# Assertions
assert response.status_code == 200
assert response.json() == {"hello": "world"}
assert response.headers["content-type"] == "application/json"

# Form data
response = client.post("/form", data={"field": "value"})

# File uploads
with open("test.txt", "rb") as f:
    response = client.post("/upload", files={"file": f})

# Custom headers
response = client.get("/", headers={"Authorization": "Bearer token123"})

# Disable redirect following
response = client.get("/redirect", follow_redirects=False)

# Test 500 responses (default raises the exception in test)
client = TestClient(app, raise_server_exceptions=False)
response = client.get("/error")
assert response.status_code == 500
```

**Requires**: `uv add httpx`

### Lifespan Testing

```python
def test_with_lifespan():
    with TestClient(app) as client:  # triggers startup
        response = client.get("/")
        assert response.status_code == 200
    # shutdown runs on exit
```

### WebSocket Testing

```python
def test_websocket():
    client = TestClient(app)
    with client.websocket_connect("/ws") as ws:
        ws.send_text("hello")
        data = ws.receive_text()
        assert data == "Echo: hello"

    # With subprotocols
    with client.websocket_connect("/ws", subprotocols=["graphql-ws"]) as ws:
        ws.send_json({"type": "connection_init"})
        msg = ws.receive_json()
        ws.close(code=1000)
```

### Async Testing (with httpx directly)

```python
from httpx import ASGITransport, AsyncClient


async def test_async():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/")
        assert response.status_code == 200
```

### Backend Selection

```python
with TestClient(app, backend="trio") as client:       # use trio instead of asyncio
    ...
with TestClient(app, backend_options={"use_uvloop": True}) as client:
    ...
```

---

## 16. API Schemas (OpenAPI)

```python
from starlette.requests import Request
from starlette.routing import Route
from starlette.schemas import SchemaGenerator

schemas = SchemaGenerator(
    {"openapi": "3.0.0", "info": {"title": "My API", "version": "1.0"}}
)


async def list_users(request: Request):
    """
    responses:
      200:
        description: A list of users.
        examples:
          [{"username": "tom"}]
    """
    ...


async def openapi_schema(request: Request):
    return schemas.OpenAPIResponse(request=request)


routes = [
    Route("/users", list_users, methods=["GET"]),
    Route("/schema", openapi_schema, include_in_schema=False),
]
```

**Requires**: `uv add pyyaml`

Schema content is parsed from YAML in endpoint docstrings (after an optional `---` separator).

---

## 17. Data Structures Reference

### URL

```python
from starlette.datastructures import URL

url = URL("https://user:pass@example.com:8080/path?q=1#frag")
url.scheme       # "https"
url.hostname     # "example.com"
url.port         # 8080
url.path         # "/path"
url.query        # "q=1"
url.fragment     # "frag"
url.username     # "user"
url.password     # "pass"
url.netloc       # "user:pass@example.com:8080"
url.is_secure    # True (https or wss)

# Immutable modifications (return new URL)
url.replace(hostname="other.com", port=443)
url.include_query_params(page=2, sort="name")
url.replace_query_params(q="new-search")
url.remove_query_params(["q", "page"])
```

### Headers / MutableHeaders

```python
from starlette.datastructures import Headers, MutableHeaders

headers = Headers({"content-type": "text/html", "x-custom": "value"})
headers["Content-Type"]       # case-insensitive: "text/html"
headers.getlist("x-custom")   # ["value"]

mutable = headers.mutablecopy()
mutable["X-New"] = "val"
mutable.append("X-Multi", "a")
mutable.add_vary_header("Accept-Encoding")
mutable |= {"X-Extra": "merged"}
del mutable["X-New"]
```

### QueryParams

```python
from starlette.datastructures import QueryParams

params = QueryParams("page=1&tag=python&tag=async")
params["page"]            # "1"
params.getlist("tag")     # ["python", "async"]
params.multi_items()      # [("page", "1"), ("tag", "python"), ("tag", "async")]
str(params)               # "page=1&tag=python&tag=async"
```

### MultiDict / ImmutableMultiDict

```python
from starlette.datastructures import MultiDict

md = MultiDict([("key", "a"), ("key", "b"), ("other", "c")])
md["key"]            # "a" (first value)
md.getlist("key")    # ["a", "b"]
md.multi_items()     # all pairs including duplicates
md.append("key", "d")
md.poplist("key")    # ["a", "b", "d"]
```

### State

```python
from starlette.datastructures import State

state = State()
state.counter = 0       # attribute access
state["counter"] = 1    # dict access
del state.counter
len(state)              # 0
```

### FormData

```python
from starlette.datastructures import FormData, UploadFile

# Immutable multi-dict of str | UploadFile values
# Returned by request.form()
form = FormData([("field", "value"), ("file", upload_file_instance)])
form["field"]         # "value"
form.getlist("field") # ["value"]
form.multi_items()    # all key-value pairs
await form.close()    # closes all UploadFile instances
```

### URLPath

```python
from starlette.datastructures import URLPath

# Returned by url_path_for() -- a str subclass with extra metadata
path = URLPath("/users/tom", protocol="http", host="example.com")
str(path)                                      # "/users/tom"
path.make_absolute_url("https://example.com")  # URL("https://example.com/users/tom")
```

### Secret / CommaSeparatedStrings / Address

```python
from starlette.datastructures import Secret, CommaSeparatedStrings, Address

secret = Secret("key")              # repr hides value, str reveals it
hosts = CommaSeparatedStrings("a, b, c")  # list(hosts) == ["a", "b", "c"]
addr = Address(host="127.0.0.1", port=8000)
```

---

## 18. Concurrency Utilities

### run_in_threadpool

```python
from starlette.concurrency import run_in_threadpool

async def handler(request: Request):
    # Run blocking code without blocking the event loop
    result = await run_in_threadpool(blocking_function, arg1, arg2)
    return JSONResponse({"result": result})
```

### iterate_in_threadpool

```python
from starlette.concurrency import iterate_in_threadpool

async def handler(request: Request):
    sync_iter = range(100)
    async for item in iterate_in_threadpool(sync_iter):
        ...
```

### Thread Pool Tuning

Sync endpoints, FileResponse, UploadFile, and sync BackgroundTasks all run in
anyio's default thread pool (40 concurrent threads).

```python
import anyio.to_thread

limiter = anyio.to_thread.current_default_thread_limiter()
limiter.total_tokens = 100  # increase for high-concurrency sync workloads
```

---

## 19. Status Codes

```python
from starlette import status

# HTTP
status.HTTP_200_OK                     # 200
status.HTTP_201_CREATED                # 201
status.HTTP_204_NO_CONTENT             # 204
status.HTTP_301_MOVED_PERMANENTLY      # 301
status.HTTP_302_FOUND                  # 302
status.HTTP_304_NOT_MODIFIED           # 304
status.HTTP_307_TEMPORARY_REDIRECT     # 307
status.HTTP_308_PERMANENT_REDIRECT     # 308
status.HTTP_400_BAD_REQUEST            # 400
status.HTTP_401_UNAUTHORIZED           # 401
status.HTTP_403_FORBIDDEN              # 403
status.HTTP_404_NOT_FOUND              # 404
status.HTTP_405_METHOD_NOT_ALLOWED     # 405
status.HTTP_409_CONFLICT               # 409
status.HTTP_422_UNPROCESSABLE_CONTENT  # 422
status.HTTP_429_TOO_MANY_REQUESTS      # 429
status.HTTP_500_INTERNAL_SERVER_ERROR  # 500

# WebSocket
status.WS_1000_NORMAL_CLOSURE         # 1000
status.WS_1001_GOING_AWAY             # 1001
status.WS_1008_POLICY_VIOLATION       # 1008
status.WS_1011_INTERNAL_ERROR         # 1011
```

---

## 20. Database and GraphQL

Starlette is database-agnostic. Recommended async-compatible libraries:

- **SQLAlchemy** 2.0+ (native async support)
- **SQLModel** (SQLAlchemy + Pydantic)
- **Tortoise ORM** (Django-inspired async ORM)
- **Piccolo** (async ORM and query builder)

Use the lifespan handler to manage database connection pools.

GraphQL support was removed in Starlette 0.17. Use third-party libraries:
**Strawberry**, **Ariadne**, **starlette-graphene3**, or **tartiflette-asgi**.

---

## 21. WSGI Compatibility (Deprecated)

```python
from starlette.middleware.wsgi import WSGIMiddleware
from starlette.routing import Mount


def legacy_wsgi_app(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/plain")])
    return [b"Hello from WSGI"]


routes = [
    Mount("/legacy", app=WSGIMiddleware(legacy_wsgi_app)),
]
```

`WSGIMiddleware` is deprecated in Starlette 1.0. Migrate to the `a2wsgi` package.

---

## Common Patterns

### REST API

```python
import contextlib

from starlette.applications import Starlette
from starlette.endpoints import HTTPEndpoint
from starlette.exceptions import HTTPException
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

ITEMS: dict[int, dict] = {}


@contextlib.asynccontextmanager
async def lifespan(app):
    ITEMS[1] = {"id": 1, "name": "Widget"}
    yield
    ITEMS.clear()


class ItemList(HTTPEndpoint):
    async def get(self, request: Request) -> JSONResponse:
        return JSONResponse(list(ITEMS.values()))

    async def post(self, request: Request) -> JSONResponse:
        data = await request.json()
        item_id = max(ITEMS.keys(), default=0) + 1
        ITEMS[item_id] = {"id": item_id, **data}
        return JSONResponse(ITEMS[item_id], status_code=201)


class ItemDetail(HTTPEndpoint):
    async def get(self, request: Request) -> JSONResponse:
        item_id = request.path_params["item_id"]
        if item_id not in ITEMS:
            raise HTTPException(status_code=404, detail="Item not found")
        return JSONResponse(ITEMS[item_id])

    async def put(self, request: Request) -> JSONResponse:
        item_id = request.path_params["item_id"]
        if item_id not in ITEMS:
            raise HTTPException(status_code=404, detail="Item not found")
        data = await request.json()
        ITEMS[item_id] = {"id": item_id, **data}
        return JSONResponse(ITEMS[item_id])

    async def delete(self, request: Request) -> JSONResponse:
        item_id = request.path_params["item_id"]
        if item_id not in ITEMS:
            raise HTTPException(status_code=404, detail="Item not found")
        del ITEMS[item_id]
        return JSONResponse({"deleted": item_id})


routes = [
    Route("/items", ItemList),
    Route("/items/{item_id:int}", ItemDetail),
]

app = Starlette(
    routes=routes,
    middleware=[Middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])],
    lifespan=lifespan,
)
```

### Server-Sent Events (SSE)

```python
import asyncio

from starlette.requests import Request
from starlette.responses import StreamingResponse


async def event_generator():
    count = 0
    while True:
        count += 1
        yield f"data: {count}\n\n"
        await asyncio.sleep(1)


async def sse_endpoint(request: Request) -> StreamingResponse:
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
```

### File Upload with Background Processing

```python
from starlette.background import BackgroundTask
from starlette.requests import Request
from starlette.responses import JSONResponse


async def process_file(content: bytes, filename: str) -> None:
    ...


async def upload(request: Request) -> JSONResponse:
    async with request.form() as form:
        file = form["file"]
        content = await file.read()
        filename = file.filename

    task = BackgroundTask(process_file, content=content, filename=filename)
    return JSONResponse(
        {"filename": filename, "size": len(content)},
        background=task,
    )
```

### Multi-Tenant with Host Routing

```python
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Host, Route, Router


async def tenant_home(request: Request) -> PlainTextResponse:
    tenant = request.path_params["tenant"]
    return PlainTextResponse(f"Welcome to {tenant}")


routes = [
    Host("{tenant}.myapp.com", app=Router(routes=[
        Route("/", tenant_home),
    ]), name="tenant"),
]
```

---

## Why uv

Starlette itself uses uv. The repo has a committed `uv.lock`, all dev scripts use
`uv run` and `uv sync`, and `pyproject.toml` declares `required-version = ">=0.8.6"`
under `[tool.uv]`. The maintainer (Kludex) chose uv for the project's own workflow.

Always use `uv` instead of `pip` or `python3` when working with Starlette:

```bash
# Project setup
uv init myproject && cd myproject
uv add starlette uvicorn

# Install all optional deps at once
uv add starlette[full]

# Run the dev server
uv run uvicorn app:app --reload

# Run tests (matching Starlette's own scripts/test)
uv run pytest
```

**Why this matters:**

- **Matches upstream.** Starlette's `scripts/install` is `uv sync --frozen`.
  Their test runner is `uv run coverage run -m pytest`. Using uv means your
  local workflow mirrors the project's CI.
- **Speed.** `uv add starlette[full]` resolves and installs in under a second.
  pip takes 5-15x longer on the same dependency set.
- **Deterministic lockfile.** `uv.lock` pins exact versions across all platforms.
  `pip freeze` is a weaker, platform-specific guarantee.
- **Implicit venv management.** `uv run uvicorn app:app` creates and reuses a
  virtual environment automatically. No `python -m venv .venv && source .venv/bin/activate`
  ceremony.
- **Full compatibility.** uv reads standard `pyproject.toml` and `requirements.txt`.
  Nothing changes about how Starlette declares its dependencies.

On macOS, avoid calling `python3` directly. Use `uv run` which manages the
interpreter and virtual environment for you.

## Dependencies

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
| Install all | `uv add starlette[full]` |

## ASGI Servers

```bash
uv run uvicorn myapp:app --reload   # recommended
uv run daphne myapp:app
uv run hypercorn myapp:app
```
