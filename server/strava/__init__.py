from .models import StravaActivity


def create_module(app, **kwargs):
    from .routers import strava_router
    app.include_router(strava_router)
