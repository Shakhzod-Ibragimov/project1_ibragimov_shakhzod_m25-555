# labyrinth_game/player_actions.py
from __future__ import annotations

from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room, random_event


def get_input(prompt: str = "> ") -> str:
  """Read user input safely; return 'quit' on Ctrl+C/Ctrl+D."""
    try:
        return input(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def show_inventory(game_state: dict) -> None:
    """Print player's inventory."""
    inventory = game_state["player_inventory"]
    if not inventory:
        print("Инвентарь пуст.")
        return
    print("Ваш инвентарь:", ", ".join(inventory))


def move_player(game_state: dict, direction: str) -> None:
 """Move player to another room if possible and update steps."""
    current_room = game_state["current_room"]
    room_data = ROOMS[current_room]
    exits = room_data["exits"]

    if direction not in exits:
        print("Нельзя пойти в этом направлении.")
        return

    next_room = exits[direction]

    # проверка на вход в treasure_room
    if next_room == "treasure_room":
        if "treasure_key" in game_state["player_inventory"]:
            print("Вы используете найденный ключ,"
" чтобы открыть путь в комнату сокровищ."
)
        else:
            print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
            return

    game_state["current_room"] = next_room
    game_state["steps_taken"] += 1

    describe_current_room(game_state)
    random_event(game_state)


def take_item(game_state: dict, item_name: str) -> None:
    """Take an item from the room into the player's inventory."""
    current_room = game_state["current_room"]
    room_items = ROOMS[current_room]["items"]

    if item_name == "treasure_chest":
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return

    if item_name not in room_items:
        print("Такого предмета здесь нет.")
        return

    room_items.remove(item_name)
    game_state["player_inventory"].append(item_name)
    print(f"Вы подняли: {item_name}")


def use_item(game_state: dict, item_name: str) -> None:
    """Use an item from inventory and apply its effect."""
    inventory = game_state["player_inventory"]

    if item_name not in inventory:
        print("У вас нет такого предмета.")
        return

    if item_name == "torch":
        print("Вы зажигаете факел. Вокруг становится светлее.")
        return

    if item_name == "sword":
        print("Вы крепко сжимаете меч. Вам становится увереннее.")
        return

    if item_name == "bronze_box":
        if "rusty_key" not in inventory:
            inventory.append("rusty_key")
            print("Вы открываете бронзовую шкатулку и находите rusty_key!")
        else:
            print("Шкатулка пуста.")
        return

    print("Вы не знаете, как это использовать.")
