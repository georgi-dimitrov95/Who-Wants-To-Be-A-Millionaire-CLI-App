import json

# opens the initial file with all of the questions
with open("questions.json", "r") as file:
    questions = json.load(file)


# list of categories -> subcategories
culture = ["literature", "movies", "music"]
history = ["ancient", "medieval", "modern", "people", "politics"]
nature = ["flora", "fauna", "human"]
misc = [" ", "art/fashion", "count", "food", "religion/mythology", "sport", "tech", "usa"]



# adds each difficulty, category and sub-category in separate list/sets and sort the sets
keys = [1, 2, 3, 4, 5, 6]
cats = set()
subs = set()

for q in questions:
    cats.add(q["category"])
    subs.add(q["sub-category"])

cats = sorted(cats)
subs = sorted(subs)


# dict for difficulties
difficulties = {key: {} for key in keys}

# dict for categories
categories = {cat: {} for cat in cats}

# dict for sub-categories
subcategories = {sub: {} for sub in subs}


# creates a list of dictionaries sorted by: difficulty -> category -> sub-category
# and stiches all of the above dicts together
for diff in difficulties:
    for cat in categories:
        difficulties[diff][cat] = {}
        for sub in subcategories:
                if cat == "culture" and sub in culture:
                    difficulties[diff][cat][sub] = []
                elif cat == "history" and sub in history:
                    difficulties[diff][cat][sub] = []
                elif cat == "nature" and sub in nature:
                    difficulties[diff][cat][sub] = []
                elif cat == "misc" and sub in misc:
                    difficulties[diff][cat][sub] = []
                elif cat == "one" and sub == "sub-one":
                    difficulties[diff][cat][sub] = []
                elif cat == "science" and sub == "sub-science":
                    difficulties[diff][cat][sub] = []
                elif cat == "geography" and sub == "sub-geography":
                    difficulties[diff][cat][sub] = []
                else:
                    pass

# checks each questions's attributes and adds it to the appropriate difficulty -> category -> sub
for q in questions:
    for diff in difficulties:
        for cat in categories:
            for sub in subcategories:
                if int(q["difficulty"]) == diff:
                    if q["category"] == cat:
                        if q["sub-category"] == sub:
                            difficulties[diff][cat][sub].append(q)


# writes the final data to a file
with open("struct.json", "w") as f:
    json.dump(difficulties, f, indent=2)




