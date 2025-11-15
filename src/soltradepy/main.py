import logging
import os

import typer
from rich.logging import RichHandler

from soltradepy.application.coin_info_job import cli as coin_info_cli
from soltradepy.application.coins_count_job import cli as coins_count_cli
from soltradepy.application.create_db import cli as create_db_cli
from soltradepy.application.generate_proxies import cli as generate_proxies_cli
from soltradepy.application.moralis_job import cli as moralis_job_cli
from soltradepy.application.updt_21w import cli as updt_21w_cli
from soltradepy.application.updt_cf import cli as updt_cf
from soltradepy.application.updt_funding import cli as updt_funding_cli
from soltradepy.application.updt_funding_amount import cli as updt_funding_amount_cli
from soltradepy.application.updt_uri import cli as updt_uri
from soltradepy.application.updt_usdc import cli as updt_usdt_cli

handler = RichHandler(rich_tracebacks=True, markup=True)
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[handler],
)


log = logging.getLogger("rich")

app = typer.Typer(help="Soltradepy Application Menu")

COMMANDS = [
    ("Create DB", create_db_cli),
    ("Coin Info Job", coin_info_cli),
    ("Coins Count Job", coins_count_cli),
    ("Generate Proxies", generate_proxies_cli),
    ("Moralis Job", moralis_job_cli),
    ("Update Funding", updt_funding_cli),
    ("Update cf_clearance", updt_cf),
    ("Update metadata uri", updt_uri),
    ("Update USDC", updt_usdt_cli),
    ("Update Funding Amount", updt_funding_amount_cli),
    ("Update Isma Status", updt_21w_cli),
    ("Change Moralis API Key", None),  # Nueva opción
]

ENV_FILE = os.path.join(os.path.dirname(__file__), "..", "..", ".env")


def change_moralis_api_key():
    typer.echo("=== Change Moralis API Key ===")
    new_key = typer.prompt("Enter new Moralis API Key")
    # Leer el archivo .env y reemplazar la línea correspondiente
    if not os.path.exists(ENV_FILE):
        typer.echo(f"Could not find .env file at {ENV_FILE}")
        return
    with open(ENV_FILE) as f:
        lines = f.readlines()
    found = False
    for i, line in enumerate(lines):
        if line.startswith("MORALIS_API_KEY="):
            lines[i] = f"MORALIS_API_KEY={new_key}\n"
            found = True
            break
    if not found:
        lines.append(f"MORALIS_API_KEY={new_key}\n")
    with open(ENV_FILE, "w") as f:
        f.writelines(lines)
    typer.echo("Moralis API Key updated successfully.")


def menu():
    typer.echo("=== Soltradepy Application Menu ===")
    for idx, (name, _) in enumerate(COMMANDS, 1):
        typer.echo(f"{idx}. {name}")
    typer.echo("0. Exit")
    choice = typer.prompt("Select an option", type=int)
    if choice == 0:
        typer.echo("Bye!")
        raise typer.Exit()
    if 1 <= choice <= len(COMMANDS):
        name, command = COMMANDS[choice - 1]
        if name == "Change Moralis API Key":
            change_moralis_api_key()
        else:
            command()
    else:
        typer.echo("Invalid option")
        raise typer.Exit(code=1)


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        menu()


if __name__ == "__main__":
    app()
