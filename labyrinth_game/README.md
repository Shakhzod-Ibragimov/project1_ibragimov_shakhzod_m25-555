# Labyrinth Game

Консольная игра-лабиринт на Python: комнаты, предметы, загадки, случайные события и победа через открытие сундука.

## Установка

```bash
make install
# или
poetry install

# Запуск
make project
# или
poetry run project

# Команды в игре

look — осмотреть текущую комнату
go <direction> — перейти (north/south/east/west)
north/south/east/west — перейти одной командой без go
take <item> — поднять предмет
use <item> — использовать предмет
inventory — показать инвентарь
solve — решить загадку / открыть сундук
help — список команд
quit — выход

#Демонстрация (asciinema)

[![asciinema](https://asciinema.org/a/1lvJ7ZoNCLgCRn6L.svg)](https://asciinema.org/a/1lvJ7ZoNCLgCRn6L)
