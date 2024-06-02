from filemod import *
from typer import echo
from typing import *
import os 
from colorama import Fore , init , Style
import os
from filemod import delete_specific_line

class color_text:
    
    @staticmethod
    def color_print(content : str , 
                prefix_text : str = None,
                color=None) -> None:
        """
        This code prints the text in color 
        using colorma

        rules  
        ------
        - if color is None then it will be set to white
        """
        if color is None : color = Fore.WHITE
        init(convert=True)
        echo(f'{prefix_text} {color}{content}{Style.RESET_ALL}')
        init(convert=False)

    @staticmethod
    def color_writer(content : str , 
                    prefix_text : str = None,
                    color=None) -> None:
        """
        This code prints the text in color 
        using colorma

        rules  
        ------
        - if color is None then it will be set to white
        """
        if color is None : color = Fore.WHITE
        string = f'{prefix_text} {color}{content}'
    
        return string 
    
class content_operations : 
    @staticmethod
    def format_comment(comment:str,flag="None") -> str:
        """
        format the passed comment

        contains 
        --------
            - stripping the white spaces 
            - removing the extra before comment
        """

        return comment[comment.find(f"[{flag}]"):].strip()
    
    @staticmethod
    def get_content(target):
        """
        It gets the content from any file with
        data in it(auto generated) and returns in list
        """
        lines = []
        try:        

            with open(target,encoding='UTF-8') as file:
                lines = file.readlines() 
            return list(map(str.strip, lines))

        except Exception as e : 
            return False

class file_operations:

    @staticmethod
    def scan():
        '''
        scan files which are in the scope *NOT IGNORED FILES*
        '''
        top_directory = os.getcwd()
        skip_entries = set()

        try:
            with open(".ignore_scan", "r") as f:
                for line in f:
                    skip_entries.add(line.strip())
        #if user chose not to include a .ignore_scan file
        except FileNotFoundError: 
            pass

        for root, dirs, files in os.walk(top_directory):
            # Remove ignored directories from dirs list
            dirs[:] = [dir_ for dir_ in dirs if dir_ not in skip_entries]

            for file in files:
                if file not in skip_entries:
                    yield os.path.join(root, file)
                    
    @staticmethod
    def remove_comment(file,line_number):
        return delete_specific_line(file, line_number)

    @staticmethod
    def smart_delete(filename):
        line=0 
        try:
            with open(filename, "r") as f:
                contents = f.readlines()
            # remove the line item from list, by line number, starts from 0
            contents.pop(line-1)

            with open(filename, "w") as f:
                contents = "".join(contents)
                f.write(contents)
            return True
        except FileNotFoundError:
            return False
        

