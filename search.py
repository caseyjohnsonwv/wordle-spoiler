from string import ascii_lowercase

LETTER,WEIGHT = 0,1
class WeightedPrefixTree():
    
    def __init__(self, words):
        freqs = {letter:{depth:0 for depth in range(5)} for letter in ascii_lowercase}
        # calculate weights
        for word in words:
            for depth,letter in enumerate(word):
                freqs[letter][depth] += 1
        # build prefix tree
        self.trie = {}
        for word in words:
            temp_trie = self.trie
            for depth,letter in enumerate(word):
                weight = freqs[letter][depth] + sum(freqs[letter].values())
                temp_trie = temp_trie.setdefault((letter,weight), {})
            temp_trie = temp_trie.setdefault(None,None)

    def size(self):
        return len(self.list_words())

    def list_words(self):
        return self._list_words_(self.trie)
    def _list_words_(self, trie):
        word_list = []
        if not trie:
            return word_list
        for k,v in trie.items():
            if k:
                for el in self._list_words_(v):
                    word_list.append(k[LETTER]+el)
            else:
                word_list.append('')
        return word_list

    def contains(self, word):
        return self._contains_(self.trie, word)
    def _contains_(self, trie, substring):
        if not trie:
            return False
        for k,v in trie.items():
            if not k:
                return True
            elif len(substring) > 0 and k[LETTER] == substring[0]:
                return self._contains_(v, substring[1:])
        return False

    def get_weight(self, word):
        return self._get_weight_(self.trie, word) if self.contains(word) else 0
    def _get_weight_(self, trie, substring):
        for k,v in trie.items():
            if not k:
                return 0
            elif len(substring) > 0 and k[LETTER] == substring[0]:
                return k[WEIGHT] + self._get_weight_(v, substring[1:])

    def remove(self, word):
        self._remove_(self.trie, word)
    def _remove_(self, trie, substring):
        for k,v in trie.items():
            if k and len(substring) > 0 and k[LETTER] == substring[0]:
                self._remove_(v, substring[1:])
                trie[k] = None

    def heaviest_word(self):
        best,heaviest = "",0
        for word in self.list_words():
            weight = self.get_weight(word)
            if weight > heaviest and len(set(word)) == len(word):
                best = word
                heaviest = weight
        return best

    def __repr__(self):
        return str(self.trie)


with open('solutions.txt', 'r') as f:
        solutions = [word.strip() for word in f.readlines()]
# with open('guesses.txt', 'r') as f:
#     guesses = [word.strip() for word in f.readlines()]
# guesses.extend(solutions)
# guesses = list(set(guesses))

tree = WeightedPrefixTree(solutions)
for i in range(10):
    word = tree.heaviest_word()
    tree.remove(word)
    print(word)