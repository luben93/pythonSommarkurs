# Programmeringsteknik webbkurs KTH P-Uppgift
# Titel: Minröjning
# Tobias Brodd
# 12 augusti 2015

# Det här är ett minröjningsprogram likt MSröj där användaren ska utforska ett område (en matris) och se upp för miner som ligger utplacerade på några av rutorna.

import random
import time
import os
# ---------- Klasser ----------

# En klass som beskriver en spelar:
#   name - spelarens namn
#   score - spelarens poäng

class Player:
    # Skapar en ny spelare
    def __init__ (self, name):
        self.name = name
        self.score = 0
        self.mine = False
        self.flagged_mines = 0

    # Returnerar spelarens info
    def __str__ (self):
        if self.mine == False:
            return "Grattis! Du löste hela matrisen! " + self.name + " fick " + str(self.score) + " poäng!"
        else:
            return "Du trampade tyvärr på en mina! " + self.name + " fick inga poäng. Antal flaggade minor: " + str(self.flagged_mines)

    # Räknar ut spelarens poäng
    def score_method(self, time_total, opened_boxes):
        self.score += int((opened_boxes/time_total)*10000)
        return self.score
    
# En klass som beskriver en topplista
class High_scores:
    # Skapar en topplista
    def __init__ (self, filename, path):
        if os.path.exists(path):
            self.scores = []
            with open(filename, "r") as file:
                for line in file:
                    self.scores.append(line)
                i = 0
                while i < len(self.scores):
                    for name_score in self.scores:
                        name_score = name_score.strip().split(" ", -1)
                        score = int(name_score[1])
                        name = name_score[0]
                        self.scores[i] = name, score
                        i += 1
                self.scores = sorted(self.scores, key=lambda name_score: name_score[1], reverse=True)
        else:
            self.scores = []
            with open(filename, "w") as file:
                file.write(self.scores)
                
    # Sparar topplistan som en fil
    def save_file(self, filename, high_scores, name, score):
        with open(filename, "w") as file:
            i = 0
            for name_score in self.scores[:10]:
                file.write(" ".join(str(part) for part in name_score) + "\n")
                i += 1

    # Visar topplistan:
    def show_high_scores(self, high_scores):
        print("Antal tävlande:", len(high_scores.scores[:10]))
        i = 1
        for score in self.scores[:10]:
            print(str(i) + ":", score[0] + ":", score[1])
            i += 1
        time.sleep(1.0)

    # Sparar spelarens poäng i topplistan
    def save_list(self, high_scores, name, score):
        player_score = (name + ":", score)
        self.scores.append(player_score)
        self.scores = sorted(self.scores, key=lambda name_score: name_score[1], reverse=True)

# En klass som beskriver en ruta/rutorna:
#   self.boxes - rutans grundvärde

class Boxes:
    # Skapar en ruta/rutorna
    def __init__ (self, choice_y_axis, choice_x_axis):
        self.boxes = choice_y_axis*choice_x_axis*["|*|"]

    # Slumpar fram ett antal koordinater och ger dem en mina (M)
    def random_method(self, choice_y_axis, choice_x_axis):
        valid = False
        while valid == False:
            try:
                valid_mine_number = False
                while valid_mine_number == False:
                    try:
                        mines = abs(int(input("Hur många minor vill du ha i matrisen? ")))
                        if mines < choice_y_axis*choice_x_axis and mines != 0:
                            valid_mine_number = True
                        else:
                            print("Du kan inte ha lika många minor som du har rutor i matrisen! Inte heller fler eller noll stycken!")
                            valid_mine_number = False
                    except NameError:
                        print("Försök igen!")
                        valid_mine_number = False
                    random_list = ["00"]
                    random_y = mines*[None]
                    random_x = mines*[None]
                    i = 0
                    while i < mines:
                        repeat_random = True
                        while repeat_random == True:
                            random_y[i] = random.randint(0, choice_y_axis-1)
                            random_x[i] = random.randint(0, choice_x_axis-1)
                            random_mine = str(random_y[i]) + str(random_x[i])
                            if i == 0:
                                random_list[0] = random_mine
                                repeat_random = False
                            else:
                                same = False
                                for mine in random_list[:(i+1)]:
                                    if mine == random_mine:
                                        repeat_random = True
                                        same = True
                                if same == False:
                                    repeat_random = False
                                    random_list.append(random_mine)
                        i += 1
                valid = True
                return random_y, random_x, mines
            except ValueError:
                valid = False

    # Kollar valet av ruta
    def check(self, matrix, choice_y, choice_x, choice_y_axis, choice_x_axis, flagged):
        if matrix[choice_y][choice_x] == "M":
            self.boxes[choice_y+choice_x+choice_y*(choice_x_axis-1)] = "|M|"
            return True, matrix, 0
        else:
            mine_number = 0
            border_mine_list = [None]
            n = -1
            while n < 2:
                m = -1
                while m < 2:
                    if n == 0 and m == 0 or choice_y+n == -1 or choice_x+m == -1:
                        pass
                    else:
                        try:
                            border_mine_list.append(matrix[choice_y+n][choice_x+m])
                        except IndexError:
                            pass
                    m += 1
                n += 1
            for box in border_mine_list:
                if box == "M":
                    mine_number += 1
            if mine_number != 0:
                self.boxes[choice_y+choice_x+choice_y*(choice_x_axis-1)] = "|"+str(mine_number)+"|"
            else:
                if flagged == True:
                    self.boxes[choice_y+choice_x+choice_y*(choice_x_axis-1)] = "|E|"
                else:
                    self.check_empty(matrix, choice_y, choice_x, choice_x_axis)
            return False, matrix, mine_number

    # Lägger till eller tar bort en flagga
    def flagged_method(self, flag_y, flag_x, choice_y_axis, choice_x_axis, flagged, matrix, player):
        if flagged == True:
            state, matrix, mine_number = self.check(matrix, flag_y, flag_x, choice_y_axis, choice_x_axis, flagged)
            if matrix[flag_y][flag_x] == "M":
                self.boxes[flag_y+flag_x+flag_y*(choice_x_axis-1)] = "|F|"
                matrix[flag_y][flag_x] = "M"
                player.flagged_mines += 1
            else:
                self.boxes[flag_y+flag_x+flag_y*(choice_x_axis-1)] = "|F|"
                matrix[flag_y][flag_x] = "|*|"
        else:
            if matrix[flag_y][flag_x] == "M":
                self.boxes[flag_y+flag_x+flag_y*(choice_x_axis-1)] = "|*|"
                matrix[flag_y][flag_x] = "M"
            else:
                self.boxes[(flag_y)+(flag_x)+(flag_y)*(choice_x_axis-1)] = "|*|"

    # Öppnar upp alla tomma rutor samt kanten vid minorna
    def check_empty(self, matrix, y, x, choice_x_axis):
        try:
            if self.boxes[y+x+y*(choice_x_axis-1)] == "|*|":
                mine_number = 0
                border_list = []
                n = -1
                while n < 2:
                    m = -1
                    while m < 2:
                        if y+n < 0 or x+m < 0 or y < 0 or x < 0:
                            pass
                        elif n == 0 and m == 0:
                            pass
                        else:
                            try:
                                border_list.append(str(matrix[y+n][x+m]) + " " + str(y+n) + " " + str(x+m))
                            except IndexError:
                                pass
                        m += 1
                    n += 1
                for box in border_list:
                    if box[0] == "M":
                        mine_number += 1
                if mine_number != 0:
                    self.boxes[y+x+y*(choice_x_axis-1)] = "|"+str(mine_number)+"|"
                else:
                    self.boxes[y+x+y*(choice_x_axis-1)] = "|E|"
                    for box in border_list:
                        coordinate_y = int(box[4])
                        coordinate_x = int(box[6])
                        self.check_empty(matrix, coordinate_y, coordinate_x, choice_x_axis)
        except IndexError:
            pass
        
# ---------- Funktioner ----------

# En funktion som visar info samt spelreglerna:
def show_info_rules():
    print("Hej och välkommen till Minesweeper!")
    time.sleep(0.5)
    print("Regler::\n Du kommer först få välja storleken på din spelplan (max 10x10 rutor). Sedan får du bestämma antalet minor du vill ha på speplplanen. Därefter startar spelet och du får välja mellan att gå till en ruta eller lägga till en flagga. Har du redan lagt till en flagga och ångrar dig så kan du alltid ta bort den. När du har gått till alla rutor på spelplanen utan att ha trampat på en mina så har du klarat spelet! Du kan även klara spelet genom att flagga de rutor där det finns minor. Poängen du får när du har klarat spelet ges av antal steg du har tagit och tiden det tog att klara det. Lycka till!:\n")
    time.sleep(1.0)
    name = input("Vänligen ange ert namn: ")
    return name

# En funktion som returnerar valet av storleken av spelplanen:
def choice_matrix():
    valid = False
    while valid == False:
        try:
            valid_matrix = False
            while valid_matrix == False:
                choice_y_axis = abs(int(input("Hur många rader vill du ha i din matris? ")))
                if choice_y_axis > 10:
                    print("Du kan endast välja en matris på max 10*10 rutor!")
                    valid_matrix = False
                else:
                    valid_matrix = True
                if valid_matrix == True:
                    choice_x_axis = abs(int(input("Hur många rutor vill du ha på varje rad? ")))
                    if choice_x_axis > 10:
                        print("Du kan endast välja en matris på max 10*10 rutor!")
                        valid_matrix = False
                    else:
                        valid_matrix = True
            return choice_y_axis, choice_x_axis
        except ValueError:
            print("Förösk igen!")
            valid = False

# En funktion som skapar samt skriver ut en matris:
def matrix_func(matrix, choice_y_axis, choice_x_axis, boxes, random_y, random_x, mines, answer_continue, opened_boxes):
    if answer_continue == False:
        i = 0
        while i < mines:
            boxes.boxes[random_y[i]+random_x[i]+random_y[i]*(choice_x_axis-1)] = "|M|"
            i += 1
    n = 0
    k = 0
    letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    matrix = [[boxes.boxes[box+choice_x_axis*row] for box in range(choice_x_axis)] for row in range(choice_y_axis)]
    n = 0
    for row in matrix:
        print(letters[n] + ":", "-".join(row))
        n += 1
    mines_solved = 0
    mine_coordinates_list = mines*[None]
    i = 0
    while i < mines:
        matrix[random_y[i]][random_x[i]] = "M"
        mine_coordinates_list[i] = matrix[random_y[i]][random_x[i]]
        if matrix[random_y[i]][random_x[i]] == "M" and boxes.boxes[random_y[i]+random_x[i]+random_y[i]*(choice_x_axis-1)] == "|F|":
            mines_solved += 1
        i += 1
    if mines_solved == len(mine_coordinates_list) or opened_boxes == (choice_y_axis*choice_x_axis)-len(mine_coordinates_list):
        return matrix, letters, True
    else:
        return matrix, letters, False

# En funktion som returnerar spelarens val:
def choice_box(letters, choice_x_axis, boxes):
    try:
        valid_box = False
        while valid_box == False:
            choice_y = input("Välj rad: ")
            choice_y = choice_y.upper()
            n = 0
            while n < 10:
                if choice_y == letters[n] or choice_y == str(n+1):
                    choice_y = n
                else:
                    n += 1
            choice_x = abs(int(input("Välj ruta i raden " + letters[choice_y] + ": "))-1)
            if boxes.boxes[choice_y+choice_x+choice_y*(choice_x_axis-1)] != "|*|":
                print("Du har redan varit på denna ruta!")
                valid_box = False
            elif choice_y == "" or choice_x == "":
                return False, 0, 0
            else:
                valid_box = True
                return True, choice_y, choice_x
    except ValueError:
        return False, 0, 0

# En funktion som returnerar spelarens val av flaggning
def choice_flag(choice_x_axis, boxes, letters):
    try:
        valid_flag = False
        while valid_flag == False:
            choice = input("Vill du ta bort en flagga eller lägga till en? ")
            if choice.startswith("l"):
                flag_y = abs(int(input("Välj rad: "))-1)
                flag_x = abs(int(input("Välj ruta i raden " + letters[flag_y] + " som ska flaggas: "))-1)
                if boxes.boxes[flag_y+flag_x+flag_y*(choice_x_axis-1)] != "|*|":
                    print("Du kan inte lägga till en flagga på denna ruta!")
                    valid_flag = False
                elif flag_y == "" or flag_x == "":
                    return False, 0, 0, 0
                else:
                    valid_flag = True
                    return False, flag_y, flag_x, True
            else:
                flag_y = abs(int(input("Välj rad i vilken flaggan ska tas bort: "))-1)
                flag_x = abs(int(input("Välj ruta i raden " + letters[flag_y] + " där flaggan ska tas bort: "))-1)
                if boxes.boxes[flag_y+flag_x+flag_y*(choice_x_axis-1)] != "|F|":
                    print("Du kan inte ta bort en flagga från denna ruta!")
                    valid_flag = False
                elif flag_y == "" or flag_x == "":
                    return False, 0, 0, 0
                else:
                    valid_flag = True
                    return False, flag_y, flag_x, False
    except ValueError:
        return False, 0, 0, 0
    except IndexError:
        return False, 0, 0, 0
# En funktion som returnerar spelarens val (gå eller flagga)
def choice_func():
        choice = input("Vill du gå till en ruta eller vill du flagga en ruta? ")
        choice = choice.lower()
        return choice

def mine_number_fake_func(y, x, choice_x_axis, boxes):
    mine_number_fake = 1
    while mine_number_fake < 9:
        if boxes.boxes[y+x+y*(choice_x_axis-1)] == "|"+str(mine_number_fake)+"|":
            mine_number_fake = 10
            return True
        else:
            mine_number_fake += 1
    if mine_number_fake == 9:
        return False

# ---------- Huvudprogram ----------
def main_program():
    FILENAME = "high_scores.txt"
    PATH = (os.path.dirname(os.path.abspath(FILENAME)) + "/" + FILENAME)
    high_scores = High_scores(FILENAME, PATH)
    try_again = "ja"
    while try_again.startswith("j"):
        name = show_info_rules()
        player = Player(name)
        choice_y_axis, choice_x_axis = choice_matrix()
        boxes = Boxes(choice_y_axis, choice_x_axis)
        matrix = choice_y_axis*[None]
        print("---"*choice_x_axis)
        random_y, random_x, mines = boxes.random_method(choice_y_axis, choice_x_axis)
        answer_continue = True
        opened_boxes = 0
        start = time.time()
        while answer_continue == True:
            matrix, letters, solved = matrix_func(matrix, choice_y_axis, choice_x_axis, boxes, random_y, random_x, mines, answer_continue, opened_boxes)
            valid = False
            flagged = False
            while valid == False:
                choice = choice_func()
                if choice.startswith("f"):
                    flagged = True
                if choice.startswith("f") or choice.startswith("t"):
                    valid, flag_y, flag_x, flagged = choice_flag(choice_x_axis, boxes, letters)
                    boxes.flagged_method(flag_y, flag_x, choice_y_axis, choice_x_axis, flagged, matrix, player)
                    matrix, letters, solved = matrix_func(matrix, choice_y_axis, choice_x_axis, boxes, random_y, random_x, mines, answer_continue, opened_boxes)
                    if solved == True:
                        valid = True
                elif choice.startswith("g"):
                    valid, choice_y, choice_x = choice_box(letters, choice_x_axis, boxes)
                    if valid == True:
                        state, matrix, mine_number = boxes.check(matrix, choice_y, choice_x, choice_y_axis, choice_x_axis, flagged)
                else:
                    print("Försök igen!")
                    valid = False
            if state == False:
                print("Du klarade dig!")
                opened_boxes += 1
                answer_continue = True
                if solved == True:
                    answer_continue = False
            else:
                player.mine = True
                answer_continue = False
        stop = time.time()
        time_total = stop - start
        score = player.score_method(time_total, opened_boxes)
        print(player)
        matrix, letters, solved_flagged = matrix_func(matrix, choice_y_axis, choice_x_axis, boxes, random_y, random_x, mines, answer_continue, opened_boxes)
        high_scores.save_list(high_scores, name, score)
        high_scores.save_file(FILENAME, high_scores, name, score)
        high_scores.show_high_scores(high_scores)
        try_again = input("Vill du försöka igen? ")
        try_again = try_again.lower()
    time.sleep(0.5)
    print("Tack för att du använde mitt program!")

# ---------- Programmet ----------
main_program()
