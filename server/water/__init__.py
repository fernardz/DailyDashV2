from .models import Water, Water_Goal

def create_module(app, **kwargs):
    from .routers import router
    app.include_router(router)
