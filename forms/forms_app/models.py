

from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.name + "@(" + str(self.pk) + ")"


class Form(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + "@(" + str(self.pk) + ")"


# there could be following types of questions: dropdown, checkbox, radio button, text
class Question(models.Model):
    text = models.CharField(max_length=100)
    type = models.CharField(max_length=30)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)

    def __str__(self):
        return self.text + "@(" + str(self.pk) + ")"

    def get_type(self):
        return self.type


# Optional choices sent along with questions of type dropdown, checkbox, radio button
class Choice(models.Model):
    text = models.CharField(max_length=1024)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.text + "@(" + str(self.pk) + ")"

# User-given answers to questions
class Answer(models.Model):
    text = models.CharField(max_length=1024)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.text + "@(" + str(self.pk) + ")"

