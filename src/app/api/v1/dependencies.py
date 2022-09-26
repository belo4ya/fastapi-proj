from app.core.db import async_session_factory, SessionT


async def get_session() -> SessionT:
    async with async_session_factory() as session:
        yield session
