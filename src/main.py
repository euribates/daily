#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import datetime
import os
import re
from typing import List
from subprocess import call

from rich.console import Console
import typer


SOURCE = Path.home() / Path('Dropbox/parcan')
EDITOR = os.environ.get('EDITOR', 'vim')  # that easy!


def hoy() -> datetime.date:
    return datetime.date.today()


def parse_fecha(s) -> datetime.date:
    if '-' in s:
        year, month, day = [int(_) for _ in s.split('-')]
    else:
        day, month, year = [int(s) for _ in s.split('/')]
    return datetime.date(year, month, day)


def get_current_note_path(f: datetime.date = None) -> Path:
    f = f or hoy()
    filename = f'journal-{f.year:04d}-{f.month:02d}-{f.day:02d}.md'
    return SOURCE / filename


def list_tasks(note: str):
    console = Console()
    pat_note = re.compile(r"\[(.)\] (.+)")
    pat_comilla = re.compile(r"`(.+?)`")
    if note.exists():
        with open(note, 'r', encoding='utf-8') as f_in:
            index = 0
            for line in f_in:
                _match = pat_note.match(line)
                if _match:
                    checkbox, titulo = _match.groups()
                    if checkbox in {'x', 'X'}:
                        markup = '[yellow]'
                        emoji = ':white_heavy_check_mark:'
                    elif checkbox == '>':
                        markup = '[orange1]'
                        emoji = ':right_arrow:'
                    else:
                        markup = '[bold green]'
                        emoji = ':white_large_square:'
                    titulo = pat_comilla.sub(
                        lambda m: f"[bold]{m.group(1)}[/bold]",
                        titulo,
                    )
                    console.print(
                            f'{index:>4}',
                        emoji,
                        markup,
                        titulo,
                    )
                    index += 1


app = typer.Typer(no_args_is_help=True)

@app.command()
def at(fecha:str):
    fecha = parse_fecha(fecha)
    note = get_current_note_path(fecha)
    print(f"Tareas para {fecha}")
    list_tasks(note)


@app.command()
def today():
    '''Tareas para hoy.
    '''
    note = get_current_note_path()
    print(f"Tareas para hoy ({hoy()})")
    list_tasks(note)


@app.command()
def yesterday():
    '''Tareas de ayer.
    '''
    ayer = datetime.date.today() - datetime.timedelta(days=1)
    note = get_current_note_path(ayer)
    print(f"Tareas para ayer ({ayer})")
    list_tasks(note)


@app.command()
def done(words: List[str] = typer.Argument(...)):
    note = get_current_note_path()
    task_name = ' '.join(words)
    with open(note, 'a', encoding='utf-8') as f_out:
        f_out.write(f'[x] {task_name}\n')


@app.command()
def todo(words: List[str] = typer.Argument(...)):
    note = get_current_note_path()
    task_name = ' '.join(words)
    with open(note, 'a', encoding='utf-8') as f_out:
        print(f'\n[ ] {task_name}\n', file=f_out)


@app.command()
def edit(fecha: str = None):
    f = hoy() if fecha is None else parse_fecha(fecha)
    note = get_current_note_path(f)
    call([EDITOR, note])


if __name__ == "__main__":
    app()
