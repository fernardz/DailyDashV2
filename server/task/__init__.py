from .models import Task, TaskRecord


def create_module(app, **kwargs):
    from .routers import router
    app.include_router(router)
