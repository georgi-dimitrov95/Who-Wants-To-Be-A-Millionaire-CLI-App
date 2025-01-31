import json
import project
import pytest

with open("struct.json", "r") as file:
    questions = json.load(file)

table = project.create_table()
test_table = [[1, '$100'], [2, '$200'], [3, '$300'], [4, '$500'], [5, '$1,000'], [6, '$2,000'], [7, '$4,000'], [8, '$8,000'], [9, '$16,000'], [10, '$32,000'], [11, '$64,000'], [12, '$125,000'], [13, '$250,000'], [14, '$500,000'], [15, '$1,000,000']]

locked_no = {"amount": 0, "locked": False}
locked_yes = {"amount": 32000, "locked": True}

question = {
          "question": "In Greek mythology, what is the name of Zeus' father?",
          "A": "Apollo",
          "B": "Cronus",
          "C": "Prometheus",
          "D": "Hercules",
          "answer": "B",
          "difficulty": "1",
          "category": "one",
          "sub-category": "sub-one",
          "asked": False
        }

def test_check_answer():
    assert project.check_answer("walkaway", question, questions, 1) == True
    assert project.check_answer("A", question, questions, 1) == {"question": question, "correct/false": False}
    assert project.check_answer("B", question, questions, 1) == {"question": question, "correct/false": True}
    assert project.check_answer("C", question, questions, 1) == {"question": question, "correct/false": False}
    assert project.check_answer("D", question, questions, 1) == {"question": question, "correct/false": False}

    assert project.check_answer("a", question, questions, 1) == {"question": question, "correct/false": False}
    assert project.check_answer("b", question, questions, 1) == {"question": question, "correct/false": True}
    assert project.check_answer("c", question, questions, 1) == {"question": question, "correct/false": False}
    assert project.check_answer("d", question, questions, 1) == {"question": question, "correct/false": False}


def test_virtual_table():
    assert project.virtual_table(table) == test_table


def test_lock_money():
    assert project.lock_money({"amount": 0, "locked": False}, "y", 32000) == locked_yes
    assert project.lock_money({"amount": 0, "locked": False}, "y", 32000) != locked_no
    assert project.lock_money({"amount": 0, "locked": False}, "n", 0) == locked_no
    assert project.lock_money({"amount": 0, "locked": False}, "n", 32000) == locked_no


def test_fifty_fifty():
    correct_answer = project.fifty_fifty(question)

    white = 0
    for c in correct_answer:
        if c == "asked":
            continue
        if correct_answer[c].isspace():
            white +=1

    assert correct_answer["answer"] not in ["A", "C", "D"]
    assert white == 2






