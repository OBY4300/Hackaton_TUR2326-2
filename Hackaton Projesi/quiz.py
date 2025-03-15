class Question:
    def __init__(self, text, options, correct_option):
        self.text = text
        self.option = options
        self.correct_option = correct_option

class Quiz:
    def __init__(self):
        self.questions = []

    def add_question(self, question):
        self.questions.append(question)