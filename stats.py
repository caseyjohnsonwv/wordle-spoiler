from string import ascii_lowercase
import sys

TOP_WORDS_COUNT = int(sys.argv[1]) if len(sys.argv) > 1 else 10

# track position of each letter in solutions
position_frequency = {letter:[0]*5 for letter in ascii_lowercase}
# track number of solutions actually containing each letter
words_containing_letter = {letter:0 for letter in ascii_lowercase}

with open('solutions.txt', 'r') as f:
    solutions = [word.strip() for word in f.readlines()]

print(f"Analyzing {len(solutions)} solutions...")
for word in solutions:
    word_letters = set()
    for i,letter in enumerate(word):
        word_letters.add(letter)
        position_frequency[letter][i] += 1
    for letter in word_letters:
        words_containing_letter[letter] += 1

# get everything down to one number
weighted_appearance_probabilities = {letter:[0]*5 for letter in ascii_lowercase}
for letter,freq in position_frequency.items():
    total_freq = sum(freq)
    for position in range(len(freq)):
        # frequency with which a letter appears in this position
        pct_if_present = freq[position] / total_freq * 100
        # frequency of a letter appearcing in the solution at all
        prob_presence = words_containing_letter[letter] / len(solutions)
        # overall probability that the letter is in this position in the solution
        weighted_appearance_probabilities[letter][position] = pct_if_present * prob_presence

# show me that wap table
for letter,waps in weighted_appearance_probabilities.items():
    wap_strings = '\t|\t'.join([f"{w:.1f}%" for w in waps])
    table_row = f"{letter.upper()}\t|\t{wap_strings}"
    print(table_row)
    print('-'*90)
print('\n')

# assign a score to every valid guess based on the wap table
with open('guesses.txt', 'r') as f:
    guesses = [word.strip() for word in f.readlines()]
guesses.extend(solutions)
guesses = list(set(guesses))

print(f"Analyzing {len(guesses)} valid guesses...")
scores = {word:0 for word in guesses}
for word in scores.keys():
    for i,letter in enumerate(word):
        scores[word] += weighted_appearance_probabilities[letter][i]

# print top N guesses
for word,score in sorted(scores.items(), key=lambda pair:pair[1], reverse=True)[:TOP_WORDS_COUNT]:
    print(f"{word.upper()} ({score:.2f})")

