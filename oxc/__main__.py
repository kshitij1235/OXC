from oxc.cli import app
from oxc.oxc import __app_name__

def main():
    '''
    The function that runs the app 
    '''
    app(prog_name=__app_name__)

if __name__ == "__main__":
    main()
