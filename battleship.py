from tkinter import *
from easygui import *
import random
import time as ti
from datetime import datetime, timedelta
import sys

#Main game function
#Основная функция
def battleship():
    root_1 = Tk()
    root_2 = Tk()
    root_3 = Tk()
    root_1.title("Battleship(Your Canvas)")
    root_2.title("Battleship(Opponent's Canvas)")
    root_3.title("Layout")
    scene_1 = Canvas(root_1, bg = "white", width = 550, height = 550)
    scene_2 = Canvas(root_2, bg = "white", width = 550, height = 550)

    board_size = 10
    letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    cell_hor_positions = {}
    numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    show_opponent = False
    cell_vert_positions = {}
    your_shipoccupied_cells = []
    your_ship_positions = []
    your_score = [0]
    opponents_shipoccupied_cells = []
    opponents_ship_positions = []
    opponents_score = [0]
    your_similarity = []
    opponents_similarity = []

    width = 500
    height = 500
    border = 5
    i = 0
    time_start = datetime.now()
    scoreboard = open("scoreboard.txt", "a", encoding = "UTF-8")
    database = open("database.txt", "a", encoding = "UTF-8")

    #Function that counts how much time have passed since game start
    #Функция, которая высчитывает время, прошедшее с момента начала игры
    def time_score():
        time_end = datetime.now()
        passed = time_end - time_start
        result = passed / timedelta(seconds=1)
        return str(round(result, 6))

    #Function that opens an end option menu and depending on player's choice does it
    #Функция, создающая меню после окончания игры(после проигрыша или выигрыша) и в зависимости от выбора игрока выполняет это.
    def end_option():
        choice = buttonbox("What would you like to do next?", choices = ["New Game", "View Scoreboard", "Quit"])
        if choice == "New Game":
            battleship()
        elif choice == "View Scoreboard":
            file = open("scoreboard.txt", encoding = "UTF-8")
            scores = ""
            place = 1
            for each in file:
                scores += str(place) + ". " + each
                place += 1
            file.close()
            if buttonbox("Scoreboard (Nickname - Time)\n\n" + scores, title = "Scoreboard", choices = ["Back"]) == "Back":
                 end_option()
        else:
            sys.exit("Game Over")

    #Function that is updating a scoreboard by overwriting it each time when player saves his final time
    #Функция, перезаписывающая таблицу рекордов, тем самым обновляя ее, каждый раз, когда игрок сохраняет свой результат
    def update_scoreboard():
        open('scoreboard.txt', 'w').close()
        data = open("database.txt", encoding = "UTF-8")
        base = {}
        names = []

        for each in data:
            if each[-1] == "\n":
                result = each[:-1].split(" ")
                names.append(result[0])
            else:
                result = each.split(" ")
                names.append(result[0])
            base[result[0]] = result[1]

        while len(names) > 0:
            best = None
            for each in names:
                if best == None:
                    best = float(base[each])
                else:
                    if float(base[each]) < best:
                        best = float(base[each])
                        
            scoreboard.write(list(base.keys())[list(base.values()).index(str(best))] + "  -  " + str(round(best, 2)) + "\n")
            names.remove(list(base.keys())[list(base.values()).index(str(best))])
        scoreboard.close()

    #Function that checks who is attacking and depending on it checking whether he hit, missed or eliminated all enemies and won
    #Функция, проверяющая кто атакует(игрок или компьютер), после чего проверяет попал ли атакующий, не попал или же выйграл (уничтожил все корабли)
    def attack(button, ship_positions):
        if ship_positions == opponents_ship_positions:
            if button in ship_positions:
                your_score.append(your_score[-1] + 1)

                if your_score[-1] == 20:
                    final_time = time_score()
                    msgbox("Congratulations, you eliminated all enemies!\n" +
                           "Your final time is " + str(round(float(final_time), 2)) + " seconds")

                    if buttonbox("Would you like to save your result?", choices = ["yes", "no"]) == "yes":
                        nickname = enterbox("Please enter your name/nickname: ")
                        database.write(nickname + " " + final_time + "\n")
                        database.close()
                        update_scoreboard()
                        print("Saved")

                    scene_2.create_line(cell_hor_positions[letters.index(button[0])], cell_vert_positions[numbers.index(button[1:])], cell_hor_positions[letters.index(button[0]) + 1], cell_vert_positions[numbers.index(button[1:]) + 1], width = 3, fill = "red")
                    scene_2.create_line(cell_hor_positions[letters.index(button[0]) + 1], cell_vert_positions[numbers.index(button[1:])], cell_hor_positions[letters.index(button[0])], cell_vert_positions[numbers.index(button[1:]) + 1], width = 3, fill = "red")
                    ti.sleep(1)
                    root_1.destroy()
                    root_2.destroy()
                    root_3.destroy()
                    end_option()
                else:
                    print("Nice, you hit the enemy!\n")
                    scene_2.create_line(cell_hor_positions[letters.index(button[0])], cell_vert_positions[numbers.index(button[1:])], cell_hor_positions[letters.index(button[0]) + 1], cell_vert_positions[numbers.index(button[1:]) + 1], width = 3, fill = "red")
                    scene_2.create_line(cell_hor_positions[letters.index(button[0]) + 1], cell_vert_positions[numbers.index(button[1:])], cell_hor_positions[letters.index(button[0])], cell_vert_positions[numbers.index(button[1:]) + 1], width = 3, fill = "red")
                    print("It's your turn again:")
                return True
            else:
                print("You missed.\n")
                scene_2.create_oval(cell_hor_positions[letters.index(button[0])] + 20, cell_vert_positions[numbers.index(button[1:])] + 20, cell_hor_positions[letters.index(button[0])] + 30, cell_vert_positions[numbers.index(button[1:])] + 30, fill = "black")
                return False
        else:
            if button in ship_positions:
                opponents_score.append(opponents_score[-1] + 1)

                if opponents_score[-1] == 20:
                    msgbox("Unfortunately you lost. Game Over.\n")
                    scene_1.create_line(cell_hor_positions[letters.index(button[0])], cell_vert_positions[numbers.index(button[1:])], cell_hor_positions[letters.index(button[0]) + 1], cell_vert_positions[numbers.index(button[1:]) + 1], width = 3, fill = "red")
                    scene_1.create_line(cell_hor_positions[letters.index(button[0]) + 1], cell_vert_positions[numbers.index(button[1:])], cell_hor_positions[letters.index(button[0])], cell_vert_positions[numbers.index(button[1:]) + 1], width = 3, fill = "red")
                    root_1.destroy()
                    root_2.destroy()
                    root_3.destroy()
                    end_option()
                else:
                    print("Oh no, you got hit!\n")
                    scene_1.create_line(cell_hor_positions[letters.index(button[0])], cell_vert_positions[numbers.index(button[1:])], cell_hor_positions[letters.index(button[0]) + 1], cell_vert_positions[numbers.index(button[1:]) + 1], width = 3, fill = "red")
                    scene_1.create_line(cell_hor_positions[letters.index(button[0]) + 1], cell_vert_positions[numbers.index(button[1:])], cell_hor_positions[letters.index(button[0])], cell_vert_positions[numbers.index(button[1:]) + 1], width = 3, fill = "red")
                    print("Computer's turn again:")
                    return True
            else:
                print("Your opponent missed.\n")
                scene_1.create_oval(cell_hor_positions[letters.index(button[0])] + 20, cell_vert_positions[numbers.index(button[1:])] + 20, cell_hor_positions[letters.index(button[0])] + 30, cell_vert_positions[numbers.index(button[1:])] + 30, fill = "black")
                return False

    #Function that calculates cells near ship where other ships can not be placed, so each ship has a gap cell on the every side
    #Фунуция, высчитывающая клетки, находящиеся рядом с кораблем, куда другие коради не могут быть поставлены, так чтобы у каждого корабля с каждой стороны была одна клетка пустая
    def space(position, ship_positions_list, occupied_cells):
        first = []
        first.append(position)
        ship_positions_list.append(position)

        try:
            first.append(position[0] + str(int(position[1:]) + 1))
        except:
            None
        try:
            first.append(position[0] + str(int(position[1:]) - 1))
        except:
            None
        try:
            first.append(letters[letters.index(position[0]) + 1] + position[1:])
        except:
            None
        try:
            first.append(letters[letters.index(position[0]) - 1] + position[1:])
        except:
            None
        try:
            first.append(letters[letters.index(position[0]) + 1] + str(int(position[1:]) + 1))
        except:
            None
        try:
            first.append(letters[letters.index(position[0]) + 1] + str(int(position[1:]) - 1))
        except:
            None
        try:
            first.append(letters[letters.index(position[0]) - 1] + str(int(position[1:]) + 1))
        except:
            None
        try:
            first.append(letters[letters.index(position[0]) - 1] + str(int(position[1:]) - 1))
        except:
            None
            
        for each in first:
            if each not in occupied_cells:
                occupied_cells.append(each)

    #Function that calculates all directions, in which specific ship can be created and then returns it as a list
    #Фунуция, высчитывающая все направления для конкретного корабля, в которых этот корабль может быть построен и возвращает список с этими направлениями
    def filter_possible_directions(start_cell, ship_length):
        directions = ["up", "down", "right", "left"]
        hor_index = letters.index(start_cell[0]) + 1
        vert_index = numbers.index(start_cell[1:]) + 1

        if ship_length > hor_index:
            directions.remove("left")
        if ship_length > 10-hor_index:
            directions.remove("right")
        if ship_length > vert_index:
            directions.remove("up")
        if ship_length > 10-vert_index:
            directions.remove("down")
        return directions

    #Function that calculates all cells of specific ship, where it will be created
    #Функция, высчитывающая все клетки конкретного корабля, где он будет создан
    def find_available_cells(occupied_cells, ship_length, ship_positions_list):
        cells = []
        start_cell = random.choice(letters) + random.choice(numbers)

        while start_cell in occupied_cells:
            start_cell = random.choice(letters) + random.choice(numbers)
            if start_cell not in occupied_cells:
                break
        directions = filter_possible_directions(start_cell, ship_length)
        r_direction = random.choice(directions)

        for i in range(ship_length):
            if r_direction == "left":
                cells.append(letters[letters.index(start_cell[0])-i] + numbers[numbers.index(start_cell[1:])])
            if r_direction == "up":
                cells.append(letters[letters.index(start_cell[0])] + numbers[numbers.index(start_cell[1:])-i])
            if r_direction == "right":
                cells.append(letters[letters.index(start_cell[0])+i] + numbers[numbers.index(start_cell[1:])])
            if r_direction == "down":
                cells.append(letters[letters.index(start_cell[0])] + numbers[numbers.index(start_cell[1:])+i])

        for cell in cells:
            if cell in occupied_cells:
                return find_available_cells(occupied_cells, ship_length, ship_positions_list)
        return cells

    #Function that randomly creates a ship, depending on the arguments that were given to it
    #Функция, случайным образом создающая корабль, на основании данных аргументов
    def r_ship(scene, ship_length, ship_positions_list, occupied_cells, color_outline, color_fill):
        cells = find_available_cells(occupied_cells, ship_length, ship_positions_list)
        exception_cells = []
        to_remove = []

        for cell in cells:
            space(cell, ship_positions_list, occupied_cells)

        for cell in cells:
            if cell[1:] == "10":
                exception_cells.append(cell[0])
                to_remove.append(cell)

        cells.sort()
        exception_cells.sort()

        for cell in to_remove:
            cells.remove(cell)
        for cell in exception_cells:
            cells.append(cell + "10")
            
        scene.create_rectangle(cell_hor_positions[letters.index(cells[0][0])], cell_vert_positions[numbers.index(cells[0][1:])],
                    cell_hor_positions[letters.index(cells[len(cells)-1][0])+1], cell_vert_positions[numbers.index(cells[len(cells)-1][1:])+1],
                    outline = color_outline, width = 1, fill = color_fill)

    #Function where a scenario of what will happen when a specific button was pressed is written
    #Функция, где прописан сценарий того, что случится после нажатия кнопки
    def callback(buttonname):
        if buttonname in your_similarity:
            print("That spot was chosen earlier, please choose another one.\n")
        else:
            your_similarity.append(buttonname)
            print("You have chosen " + str(buttonname) + "\n")
            
            if your_score[-1] != 20 and not attack(buttonname, opponents_ship_positions):
                print("Computer's turn:")

                r_cell = random.choice(letters) + random.choice(numbers)
                while True:
                    if r_cell in opponents_similarity:
                        r_cell = random.choice(letters) + random.choice(numbers)
                    else:
                        break

                opponents_similarity.append(r_cell)
                print("Computer have chosen " + str(r_cell) + "\n")

                while attack(r_cell, your_ship_positions):
                    r_cell = random.choice(letters) + random.choice(numbers)
                    while True:
                        if r_cell in opponents_similarity:
                            r_cell = random.choice(letters) + random.choice(numbers)
                        else:
                            break

                    print("Computer have chosen " + str(r_cell) + "\n")
                    opponents_similarity.append(r_cell)

                print("Now it's your turn:")

    #In that loop a game field for a player's canvas is being drawn
    #В этом цикле риссуется поле игрока
    for each in range(11):
        scene_1.create_line(border + i, border, border + i, height + border, fill = "purple")
        scene_1.create_line(border, border + i, width + border, border + i, fill = "purple")
        i += 50

        if each == 10:
            y = 25
            for ea in numbers:
                scene_1.create_text(i - 20, border + y, text = ea,font = ("Helvetica", 25), fill = "purple")
                y += 50
                if ea == numbers[-1]:
                    y = 25

            for ea in letters:
                scene_1.create_text(border + y, i - 20, text = ea,font = ("Helvetica", 25), fill = "purple")
                y += 50
            i = 0

    #In that loop a game field for a opponent's canvas is being drawn
    #В этом цикле риссуется поле компьютера
    for each in range(11):
        scene_2.create_line(border + i, border, border + i, height + border, fill = "mediumblue")
        scene_2.create_line(border, border + i, width + border, border + i, fill = "mediumblue")
        i += 50

        if each == 10:
            y = 25
            for ea in numbers:
                scene_2.create_text(i - 20, border + y, text = ea,font = ("Helvetica", 25), fill = "mediumblue")
                y += 50
                if ea == numbers[-1]:
                    y = 25

            for ea in letters:
                scene_2.create_text(border + y, i - 20, text = ea,font = ("Helvetica", 25), fill = "mediumblue")
                y += 50
            i = 0

    #In that loop all button are being created and configured
    #В этом цикле создаются и конфигурируются все кнопки
    for n in numbers:
        for l in letters:
            Button(root_3, text = l + n, bg = "SteelBlue2", font = ("default", 18), activebackground = "white",
                   command = lambda button_name = str(l+n): callback(button_name)).grid(row = numbers.index(n)+1, column = letters.index(l)+1, sticky = W+E+N+S)

    #In that loop all horisontal cordinates of all cells are calculated and listed in a dictionary, where a key is an index of a cell and as a value it is a cordinate
    #В этом цикле высчитываются горизонтальные кординаты клеток и заносятся в словарь, где ключем являются индексы клеток, а значением кординаты
    for i in range(board_size+1):
        if i == 0:
            cell_hor_positions[i] = border
        else:
            cell_hor_positions[i] = cell_hor_positions[i - 1] + 50

    #In that loop all vertical cordinates of all cells are calculated and listed in a dictionary, where a key is an index of a cell and as a value it is a cordinate
    #В этом цикле высчитываются вертикальные кординаты клеток и заносятся в словарь, где ключем являются индексы клеток, а значением кординаты
    for i in range(board_size+1):
        if i == 0:
            cell_vert_positions[i] = border
        else:
            cell_vert_positions[i] = cell_vert_positions[i - 1] + 50

    #Here r_ship function is being called a specific amount of times to create all player ships
    #Сдесь создаются все корабли игрока посредством функции r_ship
    r_ship(scene_1, 4, your_ship_positions, your_shipoccupied_cells, "blue violet", "thistle")
    for each in range(2):
        r_ship(scene_1, 3, your_ship_positions, your_shipoccupied_cells, "blue violet", "thistle")
    for each in range(3):
        r_ship(scene_1, 2, your_ship_positions, your_shipoccupied_cells, "blue violet", "thistle")
    for each in range(4):
        r_ship(scene_1, 1, your_ship_positions, your_shipoccupied_cells, "blue violet", "thistle")

    # Here r_ship function is being called a specific amount of times to create all player ships
    # Сдесь создаются все корабли компьютера посредством функции r_ship
    c_outline = "steelblue" if show_opponent else ""
    c_fill = "lightblue" if show_opponent else ""

    r_ship(scene_2, 4, opponents_ship_positions, opponents_shipoccupied_cells, c_outline, c_fill)
    for each in range(2):
        r_ship(scene_2, 3, opponents_ship_positions, opponents_shipoccupied_cells, c_outline, c_fill)
    for each in range(3):
        r_ship(scene_2, 2, opponents_ship_positions, opponents_shipoccupied_cells, c_outline, c_fill)
    for each in range(4):
        r_ship(scene_2, 1, opponents_ship_positions, opponents_shipoccupied_cells, c_outline, c_fill)
 
    print("You start, choose the spot!")

    scene_1.pack()
    scene_2.pack()
    mainloop()
#To start whole programm battleship function is called here
#Для выполнения всей программы, которая является по сути одной функцией она же и вызывается(battleship)
battleship()