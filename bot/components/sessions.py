from aiohttp import ClientSession


def session_factory(*args, **kwargs) -> ClientSession:
    return ClientSession(*args, **kwargs)


async def close_session(session: ClientSession) -> None:
    await session.close()