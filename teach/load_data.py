from teach import models
import csv

def load_db():
    with open('duzy_plik.csv', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        for row in reader:
            
            answers = []
            for i in range(len(row)):
                if i == 0:
                    category = models.Category.objects.get(name=row[i])
                elif i == 1:
                    text = row[i]
                elif i == 2:
                    difficulty = row[i]
                else:
                    answers.append(row[i])
            exercise = models.Exercise.objects.create(category=category, description=text, difficulty=difficulty, class_profile="podstawa")
            correct_answer = answers[0]
            models.Answer.objects.create(text=correct_answer, exercise=exercise, correct=True)
            for i in range(1,len(answers)):
                models.Answer.objects.create(text=answers[i], exercise=exercise)
            
                

