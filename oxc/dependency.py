from oxc.oxc import __app_name__ , __version__
from oxc.core import *
from colorama import Fore, Style
import typer
import ctypes 
import os 
import colorama




def _version_callback(value: bool) -> None:
    '''
    fetch the app name and the version 
    '''
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()
    
def files_in_scope():
    for files in file_operations.scan():
        typer.echo(f'{Fore.GREEN}{files}{Style.RESET_ALL}')
        
def color_rules(flag:str) -> colorama.Fore:
    if flag == "FIXME":
        return Fore.YELLOW
    if flag == "TODO":
        return Fore.BLUE
    if flag == "ERROR":
        return Fore.RED
    if flag == "DONE":
        return Fore.GREEN
    
    return Fore.WHITE


import inquirer
def comment_options(inputs:list)->str:
    '''
    Servers the bunch of selectable 
    options with the help of inquirer package
    '''
    inputs.insert(0,"quit")
    opt = [inquirer.Checkbox("comments",message ="comments",
                  choices=inputs,
                  carousel=True)
            ]
    
    return inquirer.prompt(opt)

def scan_flags(flag):
    """
    This functions scan the files which are in the scope 
    and compares the flags
    """
    found = False
    files = file_operations.scan()
    # scanned_files = {}
    options = []
    for file_ in files:
        with open(file_) as file:
            for lines_number , line in enumerate(file,1):
                if f"[{flag}]" in line:
                    
                    # scanned_files[lines_number-1] = {
                    #     "line":lines_number,
                    #     "file":file_,
                    # }
                                      
                    options.append(color_text.color_writer(content=content_operations.format_comment(line,flag=flag),
                                prefix_text=f"{file_}:{lines_number}",
                                color=color_rules(flag))
                    )
                    # color_print(content=format_comment(line,flag=flag),
                    #             prefix_text=f"#{lines_number-1} {file_}:{lines_number}",
                    #             color=color_rules(flag))
                    found = True


    # line_to_delete = input("remove comment : ")
    # delete = scanned_files.get(int(line_to_delete))
    # remove_comment(delete.get("file"),
    #                delete.get("line"))
    if found is False:            
        color_text.color_print(content="Nothing to logged with this tags")
        return False
    
    comment_options(options)

def create_workspace()->bool:

    try : 
        os.makedirs(".oxc")
        FILE_ATTRIBUTE_HIDDEN = 0x02
        ret = ctypes.windll.kernel32.SetFileAttributesW(".oxc", 
                                    FILE_ATTRIBUTE_HIDDEN)
        os.mkdir(".oxc/backups")
        os.mkdir(".oxc/logs")
        return True
    except Exception as e :
        print(e)
        return False
    


#region backup components

import shutil
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor



def copy_file(file_path, destination_folder):
    file_name = os.path.basename(file_path)
    destination_path = os.path.join(destination_folder, file_name)
    shutil.copy(file_path, destination_path)


class Backup:

    @staticmethod
    def get_latest_backup()->str:
        ...

    @staticmethod
    def copy_files_to_backup(file_list,backup_comment="")->bool:

        try: 
            backup_folder = ".oxc/backup"
            backup_folder_path = os.path.join(backup_folder, datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
            os.makedirs(backup_folder_path)

            with ThreadPoolExecutor() as executor:
                executor.map(lambda file_path: copy_file(file_path, backup_folder_path), file_list)

            backup_details = (
                "{ \n" +
                f"backup : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n" +
                f"comment : {backup_comment} \n" +
                "}"
            )
            oxc_conf_path = os.path.join(backup_folder_path, 'backup.oxc')

            with open(oxc_conf_path, 'w') as oxc_conf_file:
                oxc_conf_file.write(backup_details)
        except Exception as e:
            print(e)
            return False

        return True


#endregion