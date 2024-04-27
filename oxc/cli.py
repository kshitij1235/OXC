import typer
import os 
from oxc.core import *
from oxc.oxc import __app_name__,__version__
from typing import *
from oxc.dependency import _version_callback,scan_flags,files_in_scope,create_workspace,copy_files_to_backup
from oxc import core

app = typer.Typer()





# scann all the files 
@app.command()
def scan(
        flag: str = typer.Option(
            str,
            "--flag",
            "-f",
            help="Show all the comments with flag fixme in it"
        ),
) -> None:

    # this code srape all the flags of the comment 
    if flag  != '':
        scan_flags(flag)

    else :
        typer.echo('''Options must be used ''')
        typer.echo('''eg : --status , --flag [ARG]''')
        raise typer.Exit(1)
    
@app.command()
def status()->None : 
    # show the number of files are 
    # in the scope of the application 
    files_in_scope()


#region backup

@app.command()
def backup(backup_comment: str = typer.Option(
            str,
            "--comment",
            "-c",
            help="backup"
        ),
        scan :str = typer.Option(
            None,
            "--scan",
            "-s",
            help="show the available backups"
        )
        
)-> None :
    
    if backup_comment:
        try : 
            copy_files_to_backup(core.scan())
            typer.echo("Back created")
        except Exception as e : 
            typer.echo(f"failed to create backup {e}")
        finally:typer.Exit(1)

#endregion

@app.command()
def create(
        create: Optional[bool] = typer.Option(
            default = None,
            help="create a working dir",
            is_eager=True,
        )
)-> None :
    if create_workspace() :
        ... 
    else : 
        typer.echo("worspace already initiated")
        typer.Exit(1)
        
@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return


