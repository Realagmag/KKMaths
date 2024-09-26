from teach import models
import csv
import random


def load_db():
    with open("teach/duzy_plik.csv", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        next(reader)
        for row in reader:
            answers_correct_dict = {}
            for i in range(len(row)):
                if i == 0:
                    category = models.Category.objects.get(name=row[i])
                elif i == 1:
                    text = row[i]
                elif i == 2:
                    difficulty = row[i]
                elif i == 3:
                    answers_correct_dict[row[i]] = True
                else:
                    answers_correct_dict[row[i]] = False

            exercise = models.Exercise.objects.create(
                category=category,
                description=text,
                difficulty=difficulty,
                class_profile="podstawa",
            )
            answers = list(answers_correct_dict.keys())
            random.shuffle(answers)
            for i in range(len(answers)):
                models.Answer.objects.create(
                    text=answers[i],
                    exercise=exercise,
                    correct=answers_correct_dict.get(answers[i]),
                )
