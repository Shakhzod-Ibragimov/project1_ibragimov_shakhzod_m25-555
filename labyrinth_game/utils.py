# labyrinth_game/utils.py

from __future__ import annotations

import math

from labyrinth_game.constants import ROOMS

EVENT_PROBABILITY_MODULO = 10
RANDOM_EVENTS_COUNT = 3

TRAP_DAMAGE_MODULO = 10
TRAP_DEATH_THRESHOLD = 3


def pseudo_random(seed: int, modulo: int) -> int:
    if modulo <= 0:
        return 0
    x = math.sin(seed * 12.9898) * 43758.5453
    frac = x - math.floor(x)
    return int(frac * modulo)


def trigger_trap(game_state: dict) -> None:
    print("Ловушка активирована! Пол стал дрожать...")

    inv = game_state["player_inventory"]
    steps = game_state["steps_taken"]

    if inv:
        idx = pseudo_random(steps, len(inv))
        lost = inv.pop(idx)
        print(f"Вы потеряли предмет: {lost}")
        return

    roll = pseudo_random(steps, TRAP_DAMAGE_MODULO)  # 0..9
    if roll < TRAP_DEATH_THRESHOLD:
        print("Вы не успели увернуться... Поражение.")
        game_state["game_over"] = True
    else:
        print("Вам удалось уцелеть и избежать худшего.")


def describe_current_room(game_state: dict) -> None:
    room_name = game_state["current_room"]
    room = ROOMS[room_name]

    print(f"\n== {room_name.upper()} ==")
    print(room["description"])

    items = room["items"]
    if items:
        print("Заметные предметы:", ", ".join(items))

    exits = room["exits"]
    if exits:
        print("Выходы:", ", ".join(exits.keys()))

    if room["puzzle"] is not None:
        print('Кажется, здесь есть загадка (используйте команду solve).')


def show_help(commands: dict) -> None:
    print("\nДоступные команды:")
    for cmd, desc in commands.items():
        # позиционирование слева + 16 пробелов
        print(f"  {cmd:<16} {desc}")


def solve_puzzle(game_state: dict) -> None:
    room_name = game_state["current_room"]
    room = ROOMS[room_name]

    if room["puzzle"] is None:
        print("Загадок здесь нет.")
        return

    question, answer = room["puzzle"]
    print(question)
    user_answer = input("Ваш ответ: ").strip().lower()
    correct = str(answer).strip().lower()

    if user_answer == correct:
        print("Верно! Загадка решена.")
        room["puzzle"] = None  # нельзя решить дважды

        # простая награда-пример: в hall после загадки появляется ключ
        if room_name == "hall" and "treasure_key" not in game_state["player_inventory"]:
            game_state["player_inventory"].append("treasure_key")
            print("Вы получаете награду: treasure_key!")
        return

    print("Неверно. Попробуйте снова.")


def attempt_open_treasure(game_state: dict) -> None:
    room_name = game_state["current_room"]
    room = ROOMS[room_name]

    if room_name != "treasure_room":
        print("Здесь нет сундука с сокровищами.")
        return

    if "treasure_chest" not in room["items"]:
        print("Сундук уже открыт.")
        return

    inventory = game_state["player_inventory"]
    if "treasure_key" in inventory:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        room["items"].remove("treasure_chest")
        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
        return

    choice = input("Сундук заперт. Ввести код? (да/нет): ").strip().lower()
    if choice != "да":
        print("Вы отступаете от сундука.")
        return

    if room["puzzle"] is None:
        print("Кодовая защита отключена, но ключа всё равно нет.")
        return

    _, correct_code = room["puzzle"]
    code = input("Введите код: ").strip().lower()

    if code == str(correct_code).strip().lower():
        print("Код верный. Замок щёлкает. Сундук открыт!")
        room["items"].remove("treasure_chest")
        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
    else:
        print("Код неверный.")


def random_event(game_state: dict) -> None:
    steps = game_state["steps_taken"]

    # событие с низкой вероятностью (1 из 10)
    if pseudo_random(steps, EVENT_PROBABILITY_MODULO) != 0:
        return

    event_type = pseudo_random(steps + 1, RANDOM_EVENTS_COUNT)  # 0..2
    room_name = game_state["current_room"]
    room = ROOMS[room_name]

    if event_type == 0:
        print("Находка! Вы замечаете на полу монетку.")
        if "coin" not in room["items"]:
            room["items"].append("coin")
        return

    if event_type == 1:
        print("Вы слышите странный шорох где-то рядом...")
        if "sword" in game_state["player_inventory"]:
            print("Вы достаёте меч — существо отступает.")
        return

    # event_type == 2: ловушка по условию
    if room_name == "trap_room" and "torch" not in game_state["player_inventory"]:
        print("Опасность! Без факела в этой комнате легко ошибиться...")
        trigger_trap(game_state)
