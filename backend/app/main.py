import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.events import router as events_router
from app.core.config import get_settings
from app.core.exceptions import http_exception_handler, unhandled_exception_handler, validation_exception_handler
from app.core.logging import RequestIdMiddleware, configure_logging
from app.db.bootstrap import init_events_storage
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

settings = get_settings()
configure_logging(settings.log_level)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    init_events_storage()
    yield

app = FastAPI(
    title="OverThere Events API",
    description="Technical challenge API for events listing and detail.",
    version="0.1.0",
    lifespan=app_lifespan,
    docs_url=None,
    redoc_url=None,
)

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

app.add_middleware(RequestIdMiddleware)

allowed_origins = [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", include_in_schema=False)
def root_redirect_to_docs() -> RedirectResponse:
        return RedirectResponse(url="/docs", status_code=307)


@app.get("/docs", include_in_schema=False)
def custom_swagger_ui() -> HTMLResponse:
        swagger_page = get_swagger_ui_html(
                openapi_url=app.openapi_url,
                title=f"{app.title} - Swagger UI",
                swagger_ui_parameters={
                        "layout": "BaseLayout",
                        "docExpansion": "list",
                        "displayRequestDuration": True,
                        "filter": True,
                        "tryItOutEnabled": True,
                },
        )

        theme_assets = """
<style>
    .theme-toggle {
        align-items: center;
        background: transparent;
        border: 1px solid #8a8a8a;
        border-radius: 4px;
        color: #ffffff;
        cursor: pointer;
        display: inline-flex;
        height: 32px;
        justify-content: center;
        margin-left: 12px;
        width: 32px;
    }

    .theme-toggle svg {
        fill: currentColor;
        height: 16px;
        width: 16px;
    }

    body.theme-dark {
        background: #0f172a;
        color: #e5e7eb;
    }

    body.theme-dark .swagger-ui,
    body.theme-dark .swagger-ui .wrapper,
    body.theme-dark .swagger-ui .information-container,
    body.theme-dark .swagger-ui .scheme-container,
    body.theme-dark .swagger-ui section.models,
    body.theme-dark .swagger-ui .model-container,
    body.theme-dark .swagger-ui .opblock-tag,
    body.theme-dark .swagger-ui .response-col_status,
    body.theme-dark .swagger-ui .response-col_description {
        color: #e5e7eb;
    }

    body.theme-dark .swagger-ui .scheme-container,
    body.theme-dark .swagger-ui section.models,
    body.theme-dark .swagger-ui .opblock,
    body.theme-dark .swagger-ui .model-box,
    body.theme-dark .swagger-ui .responses-inner {
        background: #111827;
        box-shadow: none;
    }

    body.theme-dark .swagger-ui .topbar,
    body.theme-dark .swagger-ui .opblock .opblock-summary {
        background: #0b1220;
    }

    body.theme-dark .swagger-ui input,
    body.theme-dark .swagger-ui select,
    body.theme-dark .swagger-ui textarea {
        background: #0b1220;
        color: #e5e7eb;
    }
</style>
<script>
    (function () {
        var storageKey = "swagger-ui-theme";

        function moonIcon() {
            return '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.25a.75.75 0 0 1 .75.75 8.25 8.25 0 0 0 8.25 8.25.75.75 0 0 1 .53 1.28A10.5 10.5 0 1 1 11.47 2.47a.75.75 0 0 1 .53-.22z"></path></svg>';
        }

        function sunIcon() {
            return '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 6.75a5.25 5.25 0 1 1 0 10.5 5.25 5.25 0 0 1 0-10.5zM12 0a.75.75 0 0 1 .75.75V3a.75.75 0 0 1-1.5 0V.75A.75.75 0 0 1 12 0zm0 21a.75.75 0 0 1 .75.75V24a.75.75 0 0 1-1.5 0v-2.25A.75.75 0 0 1 12 21zM24 12a.75.75 0 0 1-.75.75H21a.75.75 0 0 1 0-1.5h2.25A.75.75 0 0 1 24 12zM3 12a.75.75 0 0 1-.75.75H0a.75.75 0 0 1 0-1.5h2.25A.75.75 0 0 1 3 12zM20.49 2.45a.75.75 0 0 1 1.06 0l1.59 1.59a.75.75 0 0 1-1.06 1.06l-1.59-1.59a.75.75 0 0 1 0-1.06zM2.86 20.08a.75.75 0 0 1 1.06 0l1.59 1.59a.75.75 0 1 1-1.06 1.06L2.86 21.14a.75.75 0 0 1 0-1.06zM23.14 20.08a.75.75 0 0 1 0 1.06l-1.59 1.59a.75.75 0 1 1-1.06-1.06l1.59-1.59a.75.75 0 0 1 1.06 0zM5.51 2.45a.75.75 0 0 1 0 1.06L3.92 5.1a.75.75 0 0 1-1.06-1.06l1.59-1.59a.75.75 0 0 1 1.06 0z"></path></svg>';
        }

        function applyTheme(theme) {
            var isDark = theme === "dark";
            document.body.classList.toggle("theme-dark", isDark);

            var button = document.getElementById("theme-toggle");
            if (button) {
                button.innerHTML = isDark ? sunIcon() : moonIcon();
                button.setAttribute("aria-label", isDark ? "Cambiar a tema claro" : "Cambiar a tema oscuro");
                button.setAttribute("title", isDark ? "Cambiar a tema claro" : "Cambiar a tema oscuro");
            }
        }

        function mountButton() {
            var topbarWrapper = document.querySelector(".swagger-ui .topbar .wrapper");
            if (!topbarWrapper || document.getElementById("theme-toggle")) {
                return;
            }

            var button = document.createElement("button");
            button.id = "theme-toggle";
            button.className = "theme-toggle";
            button.type = "button";
            button.addEventListener("click", function () {
                var isDark = document.body.classList.contains("theme-dark");
                var nextTheme = isDark ? "light" : "dark";
                localStorage.setItem(storageKey, nextTheme);
                applyTheme(nextTheme);
            });

            topbarWrapper.appendChild(button);

            var savedTheme = localStorage.getItem(storageKey) || "light";
            applyTheme(savedTheme);
        }

        function initThemeToggle() {
            var attempts = 0;
            var timer = setInterval(function () {
                attempts += 1;
                mountButton();
                if (document.getElementById("theme-toggle") || attempts > 40) {
                    clearInterval(timer);
                }
            }, 100);
        }

        if (document.readyState === "loading") {
            document.addEventListener("DOMContentLoaded", initThemeToggle);
        } else {
            initThemeToggle();
        }
    })();
</script>
"""

        html = swagger_page.body.decode("utf-8").replace("</body>", f"{theme_assets}</body>")
        return HTMLResponse(content=html, status_code=200)


app.include_router(events_router)
logger.info("FastAPI app initialized")
