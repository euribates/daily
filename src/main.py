#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import datetime
import os
import re
from subprocess import call

from rich.console import Console
import typer


SOURCE = Path.home() / Path('Dropbox/parcan')
EDITOR = os.environ.get('EDITOR', 'vim')  # that easy!

console = Console()


def hoy():
    return datetime.date.today()


def get_current_note_path():
    f = hoy()
    filename = f'journal-{f.year:04d}-{f.month:02d}-{f.day:02d}.md'
    return SOURCE / filename


app = typer.Typer()


@app.command()
def today():
    pat_note = re.compile(r"\[(.)\] (.+)")
    note = get_current_note_path()
    print(f"Tareas para hoy ({hoy()})")
    if note.exists():
        with open(note, 'r', encoding='utf-8') as f_in:
            for line in f_in:
                _match = pat_note.match(line)
                if _match:
                    if _match.group(1) in {'x', 'X'}:
                        markup = 'yellow'
                        emoji = ':white_heavy_check_mark:'
                    else:
                        markup = 'bold green'
                        emoji = ':white_large_square:'
                    titulo = _match.group(2)
                    console.print(
                        emoji,
                        f"[{markup}]{titulo}[/{markup}]",
                        sep=' ',
                        )



@app.command()
def done(task_name: str):
    note = get_current_note_path()
    with open(note, 'a', encoding='utf-8') as f_out:
        f_out.write(f'[x] {task_name}')


@app.command()
def todo(task_name: str):
    note = get_current_note_path()
    with open(note, 'a', encoding='utf-8') as f_out:
        print(f'\n[ ] {task_name}', file=f_out)


@app.command()
def edit():
    note = get_current_note_path()
    call([EDITOR, note])


if __name__ == "__main__":
    app()
