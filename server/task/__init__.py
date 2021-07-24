from .models import Task, TaskRecord


def create_module(app, **kwargs):
    #from .routers import router
    from .routers import task_record_router, task_router
    app.include_router(task_record_router)
    app.include_router(task_router)
