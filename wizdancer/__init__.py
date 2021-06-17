import asyncio

from pymem.exception import MemoryReadError
from wizwalker import HookAlreadyActivated, HookNotActive, HookNotReady
from wizwalker.memory import HookHandler, SimpleHook

_dance_moves_transtable = str.maketrans("abcd", "WDSA")


class DanceGameMovesHook(SimpleHook):
    pattern = rb"\x48\x8B\xF8\x48\x39\x70\x10"
    instruction_length = 7
    exports = [("dance_game_moves", 8)]
    noops = 2

    async def bytecode_generator(self, packed_exports):
        return (
            b"\x48\x8B\xF8"
            b"\x48\x8B\x00"
            b"\x48\xA3" + packed_exports[0][1] +
            b"\x48\x8B\xC7"
            b"\x48\x39\x70\x10"
        )


async def activate_dance_game_moves_hook(
    self, *, wait_for_ready: bool = False, timeout: float = None
):
    if self._check_if_hook_active(DanceGameMovesHook):
        raise HookAlreadyActivated("DanceGameMovesHook")

    await self._check_for_autobot()

    hook = DanceGameMovesHook(self)
    await hook.hook()

    self._active_hooks.append(hook)
    self._base_addrs["dance_game_moves"] = hook.dance_game_moves

    if wait_for_ready:
        await self._wait_for_value(hook.dance_game_moves, timeout)
HookHandler.activate_dance_game_moves_hook = activate_dance_game_moves_hook


async def deactivate_dance_game_moves_hook(self):
    if not self._check_if_hook_active(DanceGameMovesHook):
        raise HookNotActive("DanceGameMovesHook")

    hook = await self._get_hook_by_type(DanceGameMovesHook)
    self._active_hooks.remove(hook)
    await hook.unhook()

    del self._base_addrs["dance_game_moves"]
HookHandler.deactivate_dance_game_moves_hook = deactivate_dance_game_moves_hook


async def read_current_dance_game_moves(self) -> str:
    try:
        addr = self._base_addrs["dance_game_moves"]
    except KeyError:
        raise HookNotActive("DanceGameMovesHook")

    try:
        moves = await self.read_bytes(addr, 8)
    except MemoryReadError:
        raise HookNotReady("DanceGameMovesHook")
    return moves.partition(b"\0")[0].decode().translate(_dance_moves_transtable)
HookHandler.read_current_dance_game_moves = read_current_dance_game_moves