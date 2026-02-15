#!/usr/bin/env python3
# labyrinth_game/main.py

from __future__ import annotations

from labyrinth_game.player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from labyrinth_game.utils import (
    attempt_open_treasure,
    describe_current_room,
    show_help,
    solve_puzzle,
)


def process_command(game_state: dict, command_line: str) -> None:
    parts = command_line.strip().split()
    if not parts:
        return

    command = parts[0].lower()
    arg = " ".join(parts[1:]).strip().lower()

    match command:
        case "help":
            show_help()

        case "look":
            describe_current_room(game_state)

        case "inventory" | "inv":
            show_inventory(game_state)

        case "go":
            if not arg:
                print("Куда идти? Пример: go north")
                return
            move_player(game_state, arg)

        case "take":
            if not arg:
                print("Что поднять? Пример: take torch")
                return
            take_item(game_state, arg)

        case "use":
            if not arg:
                print("Что использовать? Пример: use torch")
                return
            use_item(game_state, arg)

        case "solve":
            # если мы в сокровищнице — решаем победную логику
            if game_state["current_room"] == "treasure_room":
                attempt_open_treasure(game_state)
                return
            solve_puzzle(game_state)

        case "quit" | "exit":
            game_state["game_over"] = True

        case _:
            print("Неизвестная команда. Введите help для списка команд.")


def main() -> None:
    game_state = {
        "player_inventory": [],
        "current_room": "entrance",
        "game_over": False,
        "steps_taken": 0,
    }

    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)

    while not game_state["game_over"]:
        command_line = get_input("> ")
        process_command(game_state, command_line)

    print("Игра окончена.")


if __name__ == "__main__":
    main()
