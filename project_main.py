from project_logic import *

# to change the .ui file to .py, put the following in the terminal
# pyuic6 -x .ui -o .py

def main():
    application = QApplication([])
    window = Logic()
    window.show()
    application.exec()


if __name__ == '__main__':
    main()