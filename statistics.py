import json

with open("questions.json", "r") as file:
    data = json.load(file)

# adds all categories and subcategories in separate sets
cats = set()
subs = set()
for q in data:
    if q["difficulty"] == "1":
        q["sub-category"] = "one"
    cats.add(q["category"])
    subs.add(q["sub-category"])

# the count for each category, stored as a dict
stats_cats = {}
for c in cats:
    a = 0
    for q in data:
        if c == q["category"]:
            a += 1
    stats_cats[c] = a

# the count for each sub-category, stored as a dict
stats_subs = {}
for c in subs:
    a = 0
    for q in data:
        if c == q["sub-category"]:
            a += 1
    stats_subs[c] = a

# count the number of questions for each difficulty and store it in a dict
keys = ["1", "2", "3", "4", "5", "6"]
diff = {key: 0 for key in keys}

for key in diff:
    for q in data:
        if q["difficulty"] == key:
            diff[key] += 1


# open a new txt file and write the two dictionaries (stats for subs/cats) from above
with open("statsquestions.txt", "w") as f:
    f.write("CATEGORIES\n\n")
    for key, value in sorted(stats_cats.items()):
        f.write(f"{key}: {value}\n")

    lines = "-" * 30
    f.write(f"{lines}\n")

    f.write("SUB-CATEGORIES\n\n")
    for key, value in sorted(stats_subs.items()):
        f.write(f"{key}: {value}\n")

    f.write(f"{lines}\n")

    f.write("DIFFICULTY\n\n")
    for key, value in diff.items():
        f.write(f"{key}: {value}\n")

    f.write(f"{lines}\n")

    f.write(f"QUESTIONS: {len(data)}")
