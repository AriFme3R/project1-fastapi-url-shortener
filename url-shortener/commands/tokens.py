from typing import Annotated

import typer
from rich import print

from api.api_v1.auth.services import redis_tokens


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
            if redis_tokens.token_exists(token)
            else "[bold red]does not exist.[/bold red]"
        ),
    )
