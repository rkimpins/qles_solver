class WordLord:
	def __init__(self):
		self.anagram_dict = {}
	
	def load_words(self, word_pack='word_packs/top_25000.txt'):
		self.anagram_dict = {}
		with open(word_pack, 'r') as f:
			for word in f.readlines():
				word = word.strip()
				anagrammed = ''.join(sorted(word))
				if anagrammed in self.anagram_dict:
					self.anagram_dict[anagrammed].append(word)
				else:
					self.anagram_dict[anagrammed] = [word]

	def is_word(self, word):
		anagrammed = ''.join(sorted(word))
		return word in self.anagram_dict.get(anagrammed, [])

	def is_annagrammed_word(self, annagrammed):
		return annagrammed in self.anagram_dict

	def annagrammed_to_words(self, annagrammed):
		return self.anagram_dict.get(annagrammed, [])
