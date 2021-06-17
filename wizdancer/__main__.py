import asyncio

from wizwalker import ClientHandler

from .utils import *


async def ignore_pet_level_up(client, pet_game_window):
    level_up_window = await maybe_find_window_by_name(
        pet_game_window, "PetLevelUpWindow"
    )
    if not level_up_window:
        return

    close_button = await wait_for_window_by_path(
        level_up_window, "wndPetLevelBkg", "btnPetLevelClose"
    )
    await client.mouse_handler.click_window(close_button)
    await asyncio.sleep(0.125)


async def main():
    async with ClientHandler() as handler:
        client = handler.get_new_clients()[0]

        await client.activate_hooks()
        await client.mouse_handler.activate_mouseless()
        await client.hook_handler.activate_dance_game_moves_hook()

        while True:
            world_view = await wait_for_window_by_path(
                client.root_window, "WorldView"
            )

            track_window = await maybe_find_window_by_name(world_view, "PetGameTracks")
            if not track_window:
                while True:
                    window = await wait_for_window_by_path(
                        world_view,
                        "NPCRangeWin",
                        "wndTitleBackground",
                        "NPCRangeTxtTitle"
                    )
                    if await window.maybe_text() == "Dance Game":
                        break
                    await asyncio.sleep(1)
                await post_keys(client, "X")

                track_window = await wait_for_window_by_path(
                    world_view, "PetGameTracks"
                )

            track_button = await wait_for_window_by_path(
                track_window, "wndBkgTracks", "wndTracks", "btnTrack1"
            )
            await asyncio.sleep(2)
            await client.mouse_handler.click_window(track_button)
            await asyncio.sleep(0.125)
            play_button = await wait_for_window_by_path(track_window, "btnNext")
            await client.mouse_handler.click_window(play_button)
            await asyncio.sleep(0.125)

            pet_game_window = await wait_for_window_by_path(
                world_view, "PetGameSplash", ""
            )

            action_window = await wait_for_window_by_path(
                pet_game_window,
                "PetGameDance",
                "wndControls",
                "wndActionBkg",
                "txtAction"
            )
            for _ in range(5):
                while await action_window.maybe_text() == "<center>Go!":
                    await asyncio.sleep(0.125)
                while await action_window.maybe_text() != "<center>Go!":
                    await asyncio.sleep(0.125)
                await post_keys(
                    client, await client.hook_handler.read_current_dance_game_moves()
                )
            await asyncio.sleep(3)

            await ignore_pet_level_up(client, pet_game_window)

            reward_window = await wait_for_window_by_path(
                pet_game_window, "PetGameRewards"
            )

            next_button = await wait_for_window_by_path(reward_window, "btnNext")
            await client.mouse_handler.click_window(next_button)
            await asyncio.sleep(0.125)

            snack_button = await wait_for_window_by_path(
                reward_window, "wndBkgBottom", "wndCards", "chkSnackCard0"
            )
            await client.mouse_handler.click_window(snack_button)
            await asyncio.sleep(0.125)
            await client.mouse_handler.click_window(next_button)
            await asyncio.sleep(0.25)

            await ignore_pet_level_up(client, pet_game_window)

            back_button = await wait_for_window_by_path(reward_window, "btnBack")
            await client.mouse_handler.click_window(back_button)
            await asyncio.sleep(3)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
