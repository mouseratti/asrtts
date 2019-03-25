from s_o.recognizer.main import main
from sys import exit

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print("Error in main: {}".format(e))
        exit(8)