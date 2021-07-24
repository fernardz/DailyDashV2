from .models import Water, Water_Goal

def create_module(app, **kwargs):
    from .routers import water_router, water_goal_router
    app.include_router(water_router)
    app.include_router(water_goal_router)
