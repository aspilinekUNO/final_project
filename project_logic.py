from PyQt6.QtWidgets import *
from project_gui import *
import csv

class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # set all input boxes invisible by default
        self.frame_score1.setVisible(False)
        self.frame_score2.setVisible(False)
        self.frame_score3.setVisible(False)
        self.frame_score4.setVisible(False)
        self.label_error.setVisible(False)
        self.label_success.setVisible(False)

        self.button_submit.clicked.connect(lambda : self.submit())
    
    def submit(self):
        try:
            self.label_success.setVisible(False)
            name = self.input_name.text()
            # name cannot be left blank
            if len(name) == 0:
                raise NameError
            score_num = int(self.input_attempt_num.text())

            # no amount of attempts outside of 1-4
            if score_num <= 0 or score_num > 4:
                raise ValueError
            
            # disallow changing number of attempts before submitting
            # will retain name and attempts num but not any of the score info
            if (score_num == 1) and self.frame_score2.isVisible():
                raise IndexError
            elif (score_num == 2) and ((not self.frame_score2.isVisible()) or self.frame_score3.isVisible()):
                raise IndexError
            elif (score_num == 3) and ((not self.frame_score3.isVisible()) or self.frame_score4.isVisible()):
                raise IndexError
            elif (score_num == 4) and (not self.frame_score4.isVisible()) and self.frame_score1.isVisible():
                raise IndexError
            
        except NameError:
            self.label_success.setVisible(False)
            self.label_error.setVisible(True)
            self.label_error.setText('Name cannot be blank')
        except ValueError:
            self.label_success.setVisible(False)
            self.label_error.setVisible(True)
            self.label_error.setText('Score amount must be an integer between 1 and 4')
        except IndexError:
            self.clear_score_input()
            self.set_scores_visible(score_num)
        except:
            self.label_success.setVisible(False)
            self.label_error.setVisible(True)
            self.label_error.setText('An error has occurred')
        else:
            self.label_error.setVisible(False)
            # if any score input is visible, submit will check for valid list of scores
            # will not be looking for scores if they haven't had a chance to enter them
            if self.frame_score1.isVisible():
                score_list = self.accept_scores(score_num)

                # writing to the csv file
                # will create a header if the file doesn't already exist
                if score_list[0] != -1:
                    try:
                        with open('grades.csv', 'x', newline='') as file:
                            csv_writer = csv.writer(file)
                            header = ['Name', 'Score 1', 'Score 2', 'Score 3', 'Score 4', 'Final']
                            csv_writer.writerow(header)
                            score_list.append(max(score_list))
                            score_list.insert(0, name)
                            csv_writer.writerow(score_list)
                    except FileExistsError:
                        with open('grades.csv', 'a', newline='') as file:
                            csv_writer = csv.writer(file)
                            score_list.append(max(score_list))
                            score_list.insert(0, name)
                            csv_writer.writerow(score_list)

                    self.clear_screen()
                    self.label_success.setVisible(True)
                    self.label_success.setText(f'Score(s) for {name} have been submitted!')
            # prevents score boxes from reappearing once scores are submitted
            if not self.label_success.isVisible():
                self.set_scores_visible(score_num)
    
    # set visibility for score input boxes
    def set_scores_visible(self, score_num):
        if score_num == 1:
            self.frame_score1.setVisible(True)
            self.frame_score2.setVisible(False)
            self.frame_score3.setVisible(False)
            self.frame_score4.setVisible(False)
        elif score_num == 2:
            self.frame_score1.setVisible(True)
            self.frame_score2.setVisible(True)
            self.frame_score3.setVisible(False)
            self.frame_score4.setVisible(False)
        elif score_num == 3:
            self.frame_score1.setVisible(True)
            self.frame_score2.setVisible(True)
            self.frame_score3.setVisible(True)
            self.frame_score4.setVisible(False)
        elif score_num == 4:
            self.frame_score1.setVisible(True)
            self.frame_score2.setVisible(True)
            self.frame_score3.setVisible(True)
            self.frame_score4.setVisible(True)
    
    def clear_score_input(self):
        self.input_score1.clear()
        self.input_score2.clear()
        self.input_score3.clear()
        self.input_score4.clear()
        self.label_error.setVisible(False)
        self.label_success.setVisible(False)
    
    # clear all fields and turn scores invisible
    def clear_screen(self):
        self.input_name.clear()
        self.input_attempt_num.clear()
        self.input_score1.clear()
        self.input_score2.clear()
        self.input_score3.clear()
        self.input_score4.clear()
        self.frame_score1.setVisible(False)
        self.frame_score2.setVisible(False)
        self.frame_score3.setVisible(False)
        self.frame_score4.setVisible(False)
        self.label_error.setVisible(False)
        self.label_success.setVisible(False)

# put scores into a list
# will catch no input, str input, float input, negative input, greater than 100

    def accept_scores(self, score_num):
        score_list = [0, 0, 0, 0]
        if score_num == 1:
            try:
                score1 = int(self.input_score1.text())
                score_list = [score1, 0, 0, 0]
                if (score1 < 0) or (score1 > 100):
                    raise ValueError
            except:
                score_list[0] = -1
                self.label_error.setVisible(True)
                self.label_error.setText('Score must be an integer between 0 and 100')
            return score_list
        
        elif score_num == 2:
            try:
                score1 = int(self.input_score1.text())
                score2 = int(self.input_score2.text())
                score_list = [score1, score2, 0, 0]
                for num in score_list:
                    if num == '':
                        raise IndexError
                    if (num < 0) or (num > 100):
                        raise ValueError
            except IndexError:
                self.label_error.setVisible(True)
                self.label_error.setText('Scores cannot be blank')
            except:
                score_list[0] = -1
                self.label_error.setVisible(True)
                self.label_error.setText('Score must be an integer between 0 and 100')
            return score_list
        
        elif score_num == 3:
            try:
                score1 = int(self.input_score1.text())
                score2 = int(self.input_score2.text())
                score3 = int(self.input_score3.text())
                score_list = [score1, score2, score3, 0]
                for num in score_list:
                    if num == '':
                        raise IndexError
                    if (num < 0) or (num > 100):
                        raise ValueError
            except IndexError:
                self.label_error.setVisible(True)
                self.label_error.setText('Scores cannot be blank')
            except:
                score_list[0] = -1
                self.label_error.setVisible(True)
                self.label_error.setText('Score must be an integer between 0 and 100')
            return score_list
        
        elif score_num == 4:
            try:
                score1 = int(self.input_score1.text())
                score2 = int(self.input_score2.text())
                score3 = int(self.input_score3.text())
                score4 = int(self.input_score4.text())
                score_list = [score1, score2, score3, score4]
                for num in score_list:
                    if (num < 0) or (num > 100):
                        raise ValueError
            except:
                score_list[0] = -1
                self.label_error.setVisible(True)
                self.label_error.setText('Score must be an integer between 0 and 100')
            return score_list