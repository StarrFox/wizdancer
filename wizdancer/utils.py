import asyncio
import ctypes

user32 = ctypes.windll.user32


async def maybe_find_window_by_name(parent, name):
    for child in await parent.children():
        if await child.name() == name:
            return child
    return None


async def wait_for_window_by_path(parent, *path):
    window = parent
    for name in path:
        while (maybe_window := await maybe_find_window_by_name(window, name)) is None:
            pass
        window = maybe_window
    return window


async def post_keys(client, keys):
    for key in keys:
        user32.PostMessageW(client.window_handle, 0x100, ord(key), 0)
        user32.PostMessageW(client.window_handle, 0x101, ord(key), 0)