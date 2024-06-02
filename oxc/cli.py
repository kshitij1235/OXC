import typer
import os 
from oxc.core import *
from oxc.oxc import __app_name__,__version__
from typing import *
from oxc.dependency import *
from oxc.dependency import _version_callback
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

import pytn
#region backup
from tabulate import tabulate   
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
            print(backup_comment)
            Backup.copy_files_to_backup(core.file_operations.scan(),backup_comment)
            typer.echo("Back created")
        except Exception as e : 
            typer.echo(f"failed to create backup {e}")
        finally:typer.Exit(1)
    if scan : 
        
        files = os.listdir("./.oxc/backup/")
        data=[[index+1,pytn.extract_values(f"./.oxc/backup/{file_name}/backup.oxc")[3],*file_name.split("_")] for index ,file_name in enumerate(files)]
        typer.echo(tabulate(data, headers=["id", "backup", "date","Time"]))

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


