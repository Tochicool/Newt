import pickle
import random

import app.userInput as input

questions = []

class Question():

    hint = "No hint available"
    marks = 0
    maxMarks = 0
    isMarked = False
    topics = []
    diagram = None
    response = None

    def __init__(self, prompt, answer, topic=None):
        self.prompt = prompt
        self.answer = answer
        questions.append(self)

    def mark(self, response):
        if self.answer == response:
            return self.marks
        else:
            return 0

    def __repr__(self):
        return self.prompt


class MultipleChoice(Question):
    marks = maxMarks = 2

    def __init__(self, prompt, answer, redHerrings):
        Question.__init__(self, prompt, answer)
        self.redHerrings = redHerrings
        self.options = redHerrings+[answer]
        random.shuffle(self.options)

    def mark(self, response):
        if self.isMarked:
            return True
        if self.answer == response:
            self.response = response
            return True
        elif self.marks > 1:
            self.marks -= 1
            return -1
        else:
            self.marks -= 1
            self.response = response
            return False


class Qualitative(Question):
    marks = maxMarks = 2
    
    def __init__(self, prompt, answer):
        Question.__init__(self, prompt, answer)
        
        i = 0
        self.keywords = []

        for char in self.answer:
            if char == "[":
                i += 1
            elif char == "]":
                i -= 1
            if not -1 < i < 2:
                break

        if i == 0:
            keyword = ""
            for char in self.answer:
                if char == "[":
                    keyword = ""
                elif char == "]":
                    self.keywords.append(keyword)
                else:
                    keyword += char

        self.answer = input.normalise(self.answer)
        self.marks = max(1, len(self.keywords))
    
    def mark(self, response, tolerance=0.5):

        if self.isMarked:
            return self.marks

        self.response = input.normalise(response)

        if len(self.keywords) > 0:
            for keyword in self.keywords:
                if not input.soundex(keyword) in input.soundex(self.response):
                    self.marks -= 1
                    for word in self.response.split(" "):
                        if input.isTypo(word, keyword):
                            self.marks += 1
                            break
        match = 0
        total = 0
        for goal in set(self.answer.split(" ")):
            for word in set(self.response.split(" ")):
                if input.isTypo(word, goal) or input.soundex(word) == input.soundex(goal):
                    match += 1
            total += 1

        self.marks = min(self.marks, int(match*self.marks/total + tolerance))
        return max(0, self.maxMarks)


class Quantitative(Question):

    def __init__(self, prompt, answer, working=None, diagram=None):
        Question.__init__(self, prompt, answer)

        if working is not None:
            self.marks = len(working)

    def mark(self, response):
        if abs(response - self.answer) < 0.01:
            return self.marks
        sf = input.getSF(self.answer)
        while sf > 0:
            if input.roundSF(response, sf) == response:
                return self.marks-1
            sf -= 1


class Quiz():

    index = 0
    completed = False

    def __init__(self, questionSet, timed=True, showHints=True):
        self.questionSet = questionSet
        if timed:
            self.time = int(60*sum([question.marks for question in questionSet]))
        else:
            self.time = '\u221E' # Lemniscate
        self.showHints = showHints

    def score(self):
        return sum([question.marks for question in self.questionSet if question.isMarked])

    def maxScore(self):
        return sum([question.maxMarks for question in self.questionSet])

    def numberAnswered(self):
        number = 0
        for question in self.questionSet:
            if question.isMarked:
                number += 1
        return number

    def save(self, quizFile):
        pickle.dump(self, quizFile, pickle.HIGHEST_PROTOCOL)

    def load(self, quizFile):
        return pickle.load(quizFile)



definitionsTXT = open('data/definitions.txt', 'r', encoding='utf-8')
topic = 0
prompt=""
answer=""
for line in definitionsTXT:
    if line[0] == "#":
        topic += 1
        continue
    if topic > 0:
        if ":" in line:
            prompt = "Define "+line.split(":")[0]
            answer += line.split(":")[1]
        elif line == "\n" and prompt != "" and answer != "":
            Qualitative(prompt, answer).topics = [topic]
            prompt = ""
            answer = ""
definitionsTXT.close()

multipleChoiceTXT = open('data/multipleChoice.txt', 'r', encoding='utf-8')
topic=0
state=1
prompt=""
answer=""
redHerrings=[]
for line in multipleChoiceTXT:
    if line[0] == "#":
        topic += 1
        continue
    if topic > 0:
        if not "\n" == line:
            if state == 1:
                prompt += line[:-1]
            elif state == 2:
                answer = line[:-1]
                state += 1
            elif state == 3:
                redHerrings.append(line[:-1])
        elif state == 1:
            state += 1
        elif prompt != "" and answer != "":
            MultipleChoice(prompt, answer, redHerrings).topics = [topic]
            state = 1
            prompt = ""
            answer = ""
            redHerrings = []
multipleChoiceTXT.close()

qualitativeTXT = open('data/qualitative.txt', 'r', encoding='utf-16')
topic=0
state=1
prompt=""
answer=""
marks=1
for line in qualitativeTXT:
    if line[0] == "#":
        topic += 1
        continue
    if topic > 0:
        if "\n" == line and state == 2:
            question = Qualitative(prompt, answer)
            question.topics = [topic]
            question.marks = question.maxMarks = marks
            state = 1
            prompt = ""
            answer = ""
            marks = 1
        elif line[0].isnumeric() and state == 1:
            marks = int(line[0])
            state = 2
        elif state == 1:
            prompt += line
        elif state == 2:
            answer += line
qualitativeTXT.close()

#for question in questions:
# print(questions.index(question), question.answer)
