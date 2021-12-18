class WordLord:
	def __init__(self):
		self.anagram_dict = {}
		with open('words.txt', 'r') as f:
			for word in f.readlines():
				word = word.strip()
				anagrammed = ''.join(sorted(word))
				if anagrammed in self.anagram_dict:
					self.anagram_dict[anagrammed].append(word)
				else:
					self.anagram_dict[anagrammed] = [word]
		#self.word_dict = {}
		#for letter1 in 'abcdefghijklmnopqrstuvwxyz':
		#	self.word_dict[letter1] = {}
		#	for letter2 in 'abcdefghijklmnopqrstuvwxyz':
		#		self.word_dict[letter1][letter2] = []
		
		#with open('words.txt', 'r') as f:
		#	for word in f.readlines():
		#		word = word.strip()
		#		self.word_dict[word[0]][word[1]].append(word)

	def is_word(self, word):
		anagrammed = ''.join(sorted(word))
		return word in self.anagram_dict.get(anagrammed, [])
		#if len(word) < 2:
		#	return False
		#return word in self.word_dict[word[0]][word[1]]
	def is_annagrammed_word(self, annagrammed):
		return annagrammed in self.anagram_dict

	def annagrammed_to_words(self, annagrammed):
		return self.anagram_dict.get(annagrammed, [])
