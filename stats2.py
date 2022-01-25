from string import ascii_lowercase
import sys

TOP_WORDS_COUNT = int(sys.argv[1]) if len(sys.argv) > 1 else 10

# track position of each letter in solutions
position_frequency = {letter:[0]*5 for letter in ascii_lowercase}
# track number of solutions actually containing each letter
words_containing_letter = {letter:0 for letter in ascii_lowercase}

with open('solutions.txt', 'r') as f:
    solutions = [word.strip() for word in f.readlines()]

with open('guesses.txt', 'r') as f:
    guesses = [word.strip() for word in f.readlines()]
guesses.extend(solutions)
guesses = list(set(guesses))

# brute force compare every guess to every solution
guess_scores = {guess:0 for guess in guesses}
for guess in guesses:
    for solution in solutions:
        for i,letter in enumerate(guess):
            if solution[i] == letter:
                guess_scores[guess] += 3
            elif letter in solution:
                guess_scores[guess] += 1

for guess,score in sorted(guess_scores.items(), key=lambda pair:pair[1], reverse=True)[:TOP_WORDS_COUNT]:
    print(f"{str(guess).upper()}: {score}")


