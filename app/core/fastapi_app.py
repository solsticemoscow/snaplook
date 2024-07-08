from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse


from app.api.router import router as api_router


def create_application():
    app = FastAPI(title='Snap Look')
    app.include_router(router=api_router)

    @app.get('/')
    async def redirect():
        response = RedirectResponse(url='http://localhost:8444/docs')
        return response

    return app

app = create_application()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

def get_application():
    global app
    if app is None:
        app = create_application()
    return app
