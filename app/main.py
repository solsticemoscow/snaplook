import uvicorn

from app.core.fastapi_app import get_application


app = get_application()


if __name__ == "__main__":

    uvicorn.run(app, host="127.0.0.1", port=8444)

