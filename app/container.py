from dishka import make_async_container
from app.providers import (
    SessionProvider,
    TaskRepositoryProvider,
    TaskServiceProvider,
)

container = make_async_container(
    SessionProvider(),
    TaskRepositoryProvider(),
    TaskServiceProvider(),
)
