from pathlib import Path

import typer
from alembic import command, config

app = typer.Typer()


def get_alembic_config() -> config.Config:
    return config.Config(str(Path(__file__).parent.parent / 'alembic.ini'))


@app.command()
def migrate(message: str | None = None):
    """Alias for 'alembic revision --autogenerate [-m <message>]'"""
    command.revision(get_alembic_config(), message=message, autogenerate=True)


@app.command()
def upgrade(revision: str = 'head'):
    """Alias for 'alembic upgrade <revision>'"""
    command.upgrade(get_alembic_config(), revision=revision)


if __name__ == "__main__":
    app()
