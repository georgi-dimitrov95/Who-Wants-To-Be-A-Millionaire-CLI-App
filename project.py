import sys
import json
import random
from tabulate import tabulate
from prettytable import PrettyTable

walkaway = False
lifelines = {"50/50": False, "change question": False, "double dip": False}
rules = ""

def main():
    global walkaway, lifelines, rules

    # welcomes the player and presents the game rules
    print('\nHello and welcome to my "Who Wants To Be A Millionaire" game!')
    with open("game_rules.txt", "r") as file:
         rules = file.read()
    print(rules)

    # loads the categorized questions in memory
    with open("struct.json", "r") as file:
        questions = json.load(file)

    # reverses the list in order to look like WWTBAM's graphic and tabulates it
    table = create_table()
    wwtbam_table = virtual_table(table)
    print(tabulate(wwtbam_table[::-1], tablefmt="heavy_grid", numalign="left"))

    # number of consecutive games played
    games = 0
    # starts consecutive games without exiting the program
    while True:
        start_game()

        # resets each question to "not asked" after every 15 consecutive games (because we will run out of questions for some of the difficulty tiers)
        if games > 0 and games % 15 == 0:
            questions = reset_questions(questions)

        # resets the amounts/values of the variables used for the lifelines and the money & walkaway prizes
        walkaway = False
        lifelines = {"50/50": False, "change question": False, "double dip": False}
        money_won = 0
        money_locked = {"amount": 0, "locked": False}

        # the core game loop - asks a maximum of 15 questions
        for i in range(1, 16):
            # determines the question's difficulty and prize
            tier = str(table[i][0])
            prize = table[i][1]

            if i == 6:
                money_locked["amount"] = 1000
                print(f"\nCongratulations! You have reached the first guaranteed prize point. No matter how your game goes from now on, you will win a guaranteed prize of ${money_locked['amount']}!\nRemember that before each of the following questions you will be asked if you'd like to lock the question as your second guaranteed prize point. You can do that only once per game so use it wisely. Good luck!")
            # after question 5 asks the player to lock a 2nd fixed sum, if it hasn't been done yet
            if money_locked["locked"] == False:
                if i > 5:
                    ask_lock = input("\nWould you like to lock the following question as your second guaranteed prize point? Type y/n: ")
                    money_locked = lock_money(money_locked, ask_lock, prize)

            print(f"\nQuestion {i} for ${prize}")
            # gets a question from the database
            question = get_question(questions, tier)
            question = tab_answers(question)
            # displays the question
            print(tabulate_question(question))
            # prompts for an answer and validates it
            answer = prompt_and_validate_answer()

            # activates a certain lifeline if chosen and checks if the following answer is correct
            question_and_answer = check_answer(answer, question, questions, tier)
            print(f'\nThe correct answer is {question_and_answer["question"]["answer"]}.')

            if question_and_answer["walkaway"] == True:
                print(f"\nCongratulations! You played well and won ${money_won}!")
                break
            elif question_and_answer["correct/false"] == True:
                money_won = prize
                if i == 16:
                    print(f"Congratulations on your impeccable game! You have won the grand prize of ${money_won}!")
                    break
                else:
                    print("\nCorrect answer! Onto the next question.")
            else:
                print(f"\nThank you for the game! You have won ${money_locked['amount']}!")
                break

        games += 1


def start_game():
   # asks if the player wants to start a game (returns None if "y")
    while True:
        try:
            start = input("\nWould you like to start a new game? Please press y/n: ")
            if start.lower() not in ["y", "n"]:
                raise ValueError
        except ValueError:
            print('Please input a valid answer - either "y" or "n" (without the quotes)')
            continue
        else:
            if start.lower() == "y":
                return
            else:
                sys.exit("\nThanks for stopping by. Have a great day!\n")


def create_table():
    # creates a dictionary qt = {question number: [difficulty, prize money]}
    prizes = [100, 200, 300, 500, 1000, 2000, 4000, 8000, 16000, 32000, 64000, 125000, 250000, 500000, 1000000]
    qt = {}
    # we start from difficulty 1 for the first five questions, for the last 10 questions we have 5 difficulties
    tier = 1
    for i in range(1, 16):
        # increments the difficulty on every odd question number after the 5th question - (6, 8, 10, 12, 14)
        if i > 5 and i % 2 == 0:
            tier += 1

        # adds the list = [difficulty, prize money] to each question number
        qt[i] = [None, None]
        qt[i][0] = tier
        qt[i][1] = prizes[i - 1]
    return qt


def virtual_table(data):
    # creates a table with columns: question - prize
    tabs = []
    for d in data:
        tab = [d, "${:,}".format(data[d][1])]
        tabs.append(tab)
    return tabs


def get_question(q, difficulty):
    # we start with 0 questions found and we try to find one and return it
    while True:
        # chooses a random category
        randcat = random.choice(list(q[difficulty].keys()))

        # uses randcat to enter the category's dict and choose a random sub-category
        randsub = random.choice(list(q[difficulty][randcat].keys()))

        # checks if the sub-category is empty or if the question was already asked
        # (if not, we pick a random question from the sub-category list of questions)
        try:
            randq = random.choice(q[difficulty][randcat][randsub])
            if randq["asked"] is True:
                print("c")
                raise IndexError
        except IndexError:
            continue
        else:
            randq["asked"] = True
            return randq


def tabulate_question(quest):
    # makes a list with the question's answers so it can be presented as a table
    first_row = [f"A: {quest['A']}", f"B: {quest['B']}"]
    second_row = [f"C: {quest['C']}", f"D: {quest['D']}"]

    # tabulates the question and answers
    table = PrettyTable()
    table.header = False
    table.title = quest["question"]
    table.add_row(first_row, divider=True)
    table.add_row(second_row)
    return table


def prompt_and_validate_answer():
    # list of valid answers
    answers = ["a", "b", "c", "d", "walkaway", "50/50", "change question"]

    # prompts the user for an answer and checks if it is a valid one
    while True:
        try:
            answer = input("Answer: ")
            if answer.lower() not in answers:
                raise NameError
        except NameError:
            print("Please input a valid answer. The possible ones are A / B / C / D / walkaway / 50/50 / change question ")
            continue
        else:
            return answer


def check_answer(answer, quest, questions, tier):
    global walkaway, lifelines
    # activates the "50/50" lifeline if it hasn't been used yet
    # either way it prompts again for an answer
    # revursively calls the function at the end
    if answer == "50/50":
        if lifelines[answer] == False:
            lifelines[answer] = True
            print("\n" + str(tabulate_question(fifty_fifty(quest))))
        else:
            print("You can use that lifeline only once per game")
        answer = prompt_and_validate_answer()
        return check_answer(answer, quest, questions, tier)
    # activates the "change question" lifeline if it hasn't been used yet
    # either way it prompts again for an answer
    # revursively calls the function at the end
    elif answer == "change question":
        if lifelines[answer] == False:
            lifelines[answer] = True
            quest = get_question(questions, tier)
            quest = tab_answers(quest)
            print("\n" + str(tabulate_question(quest)))
        else:
            print("You can use that lifeline only once per game")
        answer = prompt_and_validate_answer()
        return check_answer(answer, quest, questions, tier)
    elif answer == "walkaway":
        return {"question": quest, "correct/false": answer.upper() == quest["answer"], "walkaway": True}
    else:
        return {"question": quest, "correct/false": answer.upper() == quest["answer"], "walkaway": False}


def lock_money(money_locked_dict, prompt, money):
    # locks the desired question as a 2nd fixed sum
    if prompt == "y":
        money_locked_dict["amount"] = money
        money_locked_dict["locked"] = True
    return money_locked_dict


def fifty_fifty(quest):
    # determines which is the correct answer letter and removes it from the list of possible answers
    answers = ["A", "B", "C", "D"]
    anscopy = ["A", "B", "C", "D"]
    for a in anscopy:
        if a == quest["answer"]:
            answers.remove(a)

    # we are left with a list of 3 wrong answers and we randomly pick two of them
    # after that we go to the according key-value pair and set it to ""
    elim_answers = random.sample(answers, 2)
    for e in elim_answers:
        quest[e] = " " * len(quest[e])

    return quest


def reset_questions(quests):
    for diff in quests.keys():
        for cat in quests[diff].keys():
            for sub in quests[diff][cat].keys():
                if len(quests[diff][cat][sub]) == 0:
                    continue
                for q in quests[diff][cat][sub]:
                    q["asked"] = False
    return quests


def tab_answers(quest):
    # adds white spaces to each answer so all of them are the same length (so they look good in the prettytable format)
    lengths = [len(quest["A"]), len(quest["B"]), len(quest["C"]), len(quest["D"])]
    answers = ["A", "B", "C", "D"]

    for q in quest:
        for a in answers:
            if a == q:
                whites = max(lengths) - len(quest[a])
                quest[a] += (" " * whites)

    return quest


if __name__ == "__main__":
    main()
