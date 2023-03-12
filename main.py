import random
errorAttempts = 12
difficultyScaling = {1: (5, 8), 2: (9, 12), 3: (12, 15)}


def random_element(array: list):
    num = random.randrange(0, len(array))
    return array[num]


def get_any_word(difficulty: int):
    wordFile = open('englishwords.txt', 'r')
    lower, upper = difficultyScaling[difficulty]
    wordList = wordFile.readlines()
    wordFile.close()
    words = []
    for i in wordList:
        size = len(i)
        if lower <= size <= upper:
            words.append(i.rstrip('\n'))
    word = random_element(words)
    return word


class WrongGuess(Exception):

    def __init__(self, letter: str):
        self.letter = letter

    def __str__(self):
        return self.letter + ' is not in the word.'


class Hangman:

    def __init__(self, word: str):
        self.word = word.lower()
        self.wordSize = len(word)
        self.lettersToGuess = self.wordSize
        self.letterList = ['_' for _ in range(self.wordSize)]
        self.letterDict = dict()
        self.attempts = errorAttempts

    def initiate_dict(self):
        for i in range(self.wordSize):
            if self.word[i] in self.letterDict:
                self.letterDict[self.word[i]].append(i)
            else:
                self.letterDict[self.word[i]] = [i, ]

    def guess_letter(self, letter):
        if len(letter) > 1:
            raise ValueError('The length of the letter cannot be more than 1.')

        if self.attempts <= 0:
            return -1

        if letter in self.letterList:
            raise KeyError('The letter is already entered.')

        if letter not in self.letterDict:
            self.attempts -= 1
            raise WrongGuess(letter)

        # If the letter is in letterDict:
        for i in self.letterDict[letter]:
            self.letterList[i] = letter
            self.lettersToGuess -= 1

    def return_word(self):
        resultWord = ''
        for i in self.letterList:
            resultWord += i
        return resultWord

    def result(self):
        # 1 if won, 0 if the game is not over, -1 if lost.
        if self.attempts <= 0:
            return -1
        elif self.lettersToGuess <= 0:
            return 1
        return 0


def main():
    print('Hangman')
    while True:
        print('\nChoose your option:\n1. New Game\n2. Exit')
        c = 0
        while c not in (1, 2):
            try:
                c = int(input())
            except ValueError:
                print('Please enter only either 1 or 2.')
            else:
                if c not in (1, 2):
                    print('Please enter only either 1 or 2.')
        if c == 2:
            break
        print()
        difficulty = 0
        print('Choose your difficulty:\n1. Easy\n2. Normal\n3. Hard')
        while difficulty not in (1, 2, 3):
            try:
                difficulty = int(input())
            except ValueError:
                print('Please enter only either 1, 2 or 3.')
            else:
                if c not in (1, 2, 3):
                    print('Please enter only either 1, 2 or 3.')
        word = get_any_word(difficulty)
        hangman = Hangman(word)
        hangman.initiate_dict()
        while True:
            try:
                print()
                print('Attempts remaining:', hangman.attempts)
                res = hangman.result()
                if res == 1:
                    print('You won!')
                    print('You found the word:', hangman.word)
                    break
                elif res == -1:
                    print('You lost!')
                    print('The word was', hangman.word)
                    break
                print(hangman.return_word())
                a = input('Enter your guess: ')
                hangman.guess_letter(a)
            except ValueError as v:
                print(v)
                continue
            except KeyError:
                print("You've already entered this letter.")
                continue
            except WrongGuess as w:
                print(w)
                continue


if __name__ == '__main__':
    main()
