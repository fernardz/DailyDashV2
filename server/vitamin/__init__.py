from .models import Vitamin, Vitamin_Goal, VitaminRecord


def create_module(app, **kwargs):
    from .routers import router
    app.include_router(router)
