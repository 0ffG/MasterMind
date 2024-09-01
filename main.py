class Candidate:
    def __init__(self, val, pscore, nscore):
        self.v = val
        self.p = pscore
        self.n = nscore

    def __str__(self):
        return f"{self.v} ({self.p},{self.n})"

    def check_plus_pos(self, guessval):
        pscore = 0
        for i in range(len(str(self.v))):
            if str(self.v)[i] == str(guessval)[i]:
                pscore += 1
        return pscore

    def check_neg_pos(self, guessval):
        guesStr = str(guessval)
        answerStr = str(self.v)
        incorrectP = 0
        list_A = []
        list_G = []
        list_gt = []
        for i in answerStr:
            list_A.append(i)
        for i in guesStr:
            list_G.append(i)
        for i in range(len(answerStr)):
            if answerStr[i] == guesStr[i]:
                list_A.remove(answerStr[i])
                list_G.remove(guesStr[i])
        for x in list_G:
            if x not in list_gt:
                list_gt.append(x)
        for x in list_gt:
            if x in list_A:
                incorrectP = incorrectP + 1
        return incorrectP

    def cconsistent(self, guess):
        return self.check_plus_pos(guess.v) == guess.p and self.check_neg_pos(guess.v) == guess.n


class CodeMaker:
    def __init__(self, n):
        self.guess_list = []
        self.n = n
        self.start = 10 ** (n - 1)

    # def __str__(self):
    # return f"Guess#{len(self.guess_list)}:".join([str(guess) for guess in self.guess_list])
    def __str__(self):
        guesses = ""
        num = 0
        for guess in self.guess_list:
            guesses += f"Guess#{num + 1}:" + str(guess) + " "
            num += 1
        return guesses

    def add_guess(self, guess):
        self.guess_list.append(guess)

    def consistent(self, candidate):
        for guess in self.guess_list:
            #print(candidate.cconsistent(guess), guess, candidate)
            if not candidate.cconsistent(guess):
                return False
        self.start = candidate.v + 1
        return True

    def propose_guess(self):
        for candidate in range(self.start, 10 ** self.n):
            if self.consistent(Candidate(candidate, 0, 0)):
                return Candidate(candidate, 0, 0)
        return False


import random

random.seed(20)


class CodeBreaker:
    def __init__(self, n):
        self.n = n
        self.secret_code = None

    def generate(self, n):
        self.secret_code = random.randint(10 ** (n - 1), 10 ** n - 1)

    def setscore(self, guess):
        guess.p = guess.check_plus_pos(self.secret_code)
        guess.n = guess.check_neg_pos(self.secret_code)


class MasterMind:
    def __init__(self):
        self.n = int(input())
        self.code_maker = CodeMaker(self.n)
        self.code_breaker = CodeBreaker(self.n)
        self.code_breaker.generate(self.n)
        self.answer = self.code_breaker.secret_code

    def playGame(self):
        while True:
            guess = self.code_maker.propose_guess()
            if not guess:
                print(f"Found secret_code {self.answer} ({self.n},0)")
                break
            self.code_breaker.setscore(guess)
            self.code_maker.add_guess(guess)
            print(self.code_maker)
            # if guess.p == self.code_maker.n:
            #   print(self.code_breaker.generate(self.n))
            #  break


def main():
    my_game = MasterMind()
    my_game.playGame()


if __name__ == "__main__":
    main()

