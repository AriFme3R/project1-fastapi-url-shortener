from typing import Annotated

import typer
from rich import print
from rich.markdown import Markdown

from api.api_v1.auth.services import redis_tokens as tokens


app = typer.Typer(
    name="token",
    help="Tokens management.",
    no_args_is_help=True,
    rich_markup_mode="rich",
)


@app.command(help="Check if the passed token is valid - exists or not.")
def check(
    token: Annotated[
        str,
        typer.Argument(
            help="The token to check",
        ),
    ],
):
    print(
        f"Token [bold]{token}[/bold]",
        (
            "[bold green]exists.[/bold green]"
            if tokens.token_exists(token)
            else "[bold red]does not exist.[/bold red]"
        ),
    )


@app.command(name="list", help="Get tokens list")
def list_tokens():
    print(Markdown("# Available API tokens"))
    print(Markdown("\n- ".join([""] + tokens.get_tokens())))
    print()


@app.command(help="Create new token and save it.")
def create():
    token = tokens.generate_and_save_token()
    print(f"[bold]Token - [green]{token}[/green] successfully created[/bold]")


@app.command(help="Add token to storage.")
def add(
    token: Annotated[
        str,
        typer.Argument(help="Token to add"),
    ],
):
    if not tokens.token_exists(token):
        tokens.add_token(token)
        print(f"[bold]Token - [green]{token}[/green] added[/bold]")
        return

    print(f"[bold]Token - [red]{token}[/red] exists[/bold]")


@app.command(help="Remove token from storage.")
def rm(
    token: Annotated[
        str,
        typer.Argument(help="Token to remove"),
    ],
):
    if not tokens.token_exists(token):
        print(f"[bold]Token - [red]{token}[/red] does not exist[/bold]")
        return

    tokens.delete_token(token)
    print(f"[bold]Token - [green]{token}[/green] removed[/bold]")
