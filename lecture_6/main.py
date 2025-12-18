from fastapi import FastAPI

from book_api.main import app as books_app
from healthcheck import app as health_app

app = FastAPI(title="Combined App")

# Include routes from books_app under /api prefix
app.mount("/api", books_app)

# healthcheck remains at the root
# To keep /healthcheck working as before, simply mount the routes of health_app inside the main app
for route in health_app.routes:
    app.router.routes.append(route)
