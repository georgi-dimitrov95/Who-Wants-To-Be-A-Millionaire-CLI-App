# Who Wants To Be a Millionaire
### Video Demo:  <https://www.youtube.com/watch?v=du7IrX6I970>
### Disclaimer: before starting the video lower your volume, the first 5 seconds are rather loud, apologies!
### Developed in February, 2024

## Game description
My final CS50p project is a rendition of the popular "Who Wants To Be a Millionaire" game quiz. The main difference between this project and other similar imitations of the game is that here both the input and the output takes place in the terminal.

The player has to correctly answer a series of multiple-choice questions with increasing difficulty in order to advance to the next level/question. There are 15 questions in total and each of them is worth a specific amount of money. The first question gives a prize of $100 while the final one awards $1,000,000.

After the fifth question awaits a guaranteed prize point, just like in the original game. On the other hand, the second guaranteed prize point is determined by the player and can be chosen only once per game, but on any question the player desires. I believe this adds a bit of a strategic flavor to the game, which in my opinion can be a bit lackluster in that department.

The player is allowed two lifelines that can be used at any point during the game. They can also be used in combination with each other. Each lifeline can only be used once per game. Considering the nature of this simulated game, I have decided to omit two of the classic lifelines - "Phone a friend" & "Ask the audience".
With the abovementioned considerations in mind the two lifelines are:

- **50/50** - removes two wrong answers from the multiple-choice selection, leaving only one wrong answer and the correct one

- **change question** - presents another question with a similar difficulty instead of the initial one

At any point during the game the player can choose to stop playing and walk away with the prize he/she has won at this point.
The answers (A/B/C/D) can be typed both in lower and uppercase, but the other possible options to answer a question should be typed as follows (without the quotes): "50/50", "change question", "walkaway"

## Files overview
- **game_rules.txt** - contains the game rules which are presented to the player at the start of each game
- **questions.json** - the raw file containing all of the questions in a **[{q1}, {q2}, {q3}]** format. Each element (question) in that list contains a few key-value pairs which are then used across the other files/programs. Here is how a question's structure looks like:

```json
{
    "question": "In the story 'Jack and the Beanstalk' what does Jack trade to get the magic beans?",
    "A": "a cow",
    "B": "a hat",
    "C": "a harp",
    "D": "a goose",
    "answer": "A",
    "difficulty": "2",
    "category": "culture",
    "sub-category": "literature",
    "asked": false
}
```
- **statistics.py** - iterates over all of the questions in order to provide a basic report on how many questions there are in **questions.json** as well as the number of questions in each difficulty, category and sub-category. The output of that file can be viewed in **statsquestions.txt**. In total there are:
    - 411 questions
    - 6 difficulties
    - 7 categories
    - 22 sub-categories (not per category, but in total)
- **categorize.py** - the first half of the program opens **questions.json** and creates a few dictionaries, each nested in the previous one: difficulty -> category -> sub-category -> list of questions. This serves as the main structure of the questions. The second half of the program checks each questions's attributes (difficulty, category, sub-category) and adds it to the appropriate list of questions. The final structure, populated with all of the questions can is saved in **struct.json** and will be used in the main program **project.py**. Here is how a cut-down version of this structure looks like (it displays only the first difficulty and a couple categories):

```json
{
  "1": {
    "culture": {
      "literature": ["q1", "q2", "q3"],
      "movies": [],
      "music": []
    },
    "nature": {
      "fauna": [],
      "flora": [],
      "human": []
    }
  }
}
```

## Main program overview

At the start the program welcomes the player and presents the game rules. After that from **struct.json** it loads the categorized questions in memory. Lastly before the game starts it tabulates and displays the virtual table of the game (using the tabulate module) which contains each question number and the corresponding prize.

Afterwards the core game loop is executed, which asks a maximum of 15 questions and for each question does the following operations in order:
- determines the question's difficulty and prize
- after question 5 asks the player to lock a second guaranteed prize point, if it hasn't been done yet
- gets a question from the database loaded in memory
- displays the question using the prettytable module
- prompts for an answer and validates it
- checks if the answer is correct and in the process activates a lifeline if chosen
    - if the answer is correct it moves to the next iteration of the core game loop and updates the variables containing info about the money won, used lifelines and guaranteed prize points
       - Here each question's "asked" value is changed to True so the question doesn't get asked again in the current game or in a sequential one
       - After each 15 consecutive games, each question is reset to "not asked" because otherwise the program will run out of questions for some of the difficulty tiers
    - if the answer is incorrect/walkaway the core game loop breaks, the player wins the appropritate prize and is prompted to start a new game or exit the program






