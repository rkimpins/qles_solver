import itertools
from PIL.Image import new
import board
import queue
from is_word import WordLord

WORD_LORD = WordLord()

# generate all the words we can, for each word
# for each position along the word, generate the words we can build off of that
# repeat this process 
# If we aren't able to create any new words, we return


def import_words():
	filename = 'words.txt'
	with open(filename, 'r') as f:
		words = [line.strip() for line in f.readlines()]
	return words


def is_word(word):
	return WORD_LORD.is_word(word)


def iter_valid_words(letters):
	# generate all the words we can given the set of letters
	for i in range(2, len(letters) + 1):
		yielded = set()
		for word in itertools.combinations(letters, i):
			annagramed = ''.join(sorted(word))
			for real_word in WORD_LORD.annagrammed_to_words(annagramed):
				#print('SET:')
				#for x in yielded:
				#	print(f'{x}-', end='')
				#print('')
				#print(f'{real_word=}')
				if real_word not in yielded:
					yielded.add(real_word)
					yield real_word
			#if is_word(joined_word) and joined_word not in yielded:
			#	yielded.add(joined_word)
			#	yield joined_word


def valid_board_state(b):
	return True


def solve_qless(letters):
	size = (20, 20)
	q = queue.Queue()
	b = board.Board(size)

	q.put((letters, b))

	while not q.empty():
		# get next item
		# if not valid, continue
		# if it is valid and out of letters, print!!
		# if valid and letters left, generate all the words we can with the letters left
		letters, b = q.get()
		#print_board(b)
		if valid_board_state(b) and len(letters) == 0:
			print("SOLVED")
			print_board(b)
		if not valid_board_state(b):
			continue
		if valid_board_state(b):
			if number_of_letters_on_board(b) == 0:
				for word in iter_valid_words(letters):
					new_b = b.copy()
					coord = (size[0]//2, size[1]//2)
					new_b[coord] = word[0]
					new_b = place_word(new_b, coord, word[1:], 'horizontal')[0]
					q.put((subtract_letters(letters, word), new_b))
				continue
			for coord in find_all_filled_coords(b):
				new_letters = letters + b[coord]
				for word in iter_valid_words(letters):
					# place word
					left_over_letters = subtract_letters(letters, word)
					for r_board in place_word(b, coord, word, 'horizontal'):
						q.put((left_over_letters, r_board))
					for r_board in place_word(b, coord, word, 'vertical'):
						q.put((left_over_letters, r_board))

def subtract_letters(letters, subtractor):
	for char in subtractor:
		letters = letters.replace(char, '')
	return letters

def place_word(b, coord, word, axis):
	assert axis in ['vertical', 'horizontal']
	results = []

	#TODO we will deal with multiple cases later
	char_pos = word.find(b[coord])
	#char_positions = find(word, b[coord])
	#if len(char_positions) == 1:
	#	char_pos = char_positions[0]
	#else:
	#	char_pos = char_positions[0]
	
	before, after = split_word_by_position(word, char_pos)
	new_board = b.copy()

	overlapped = False
	for index, letter in enumerate(before):
		if axis == 'vertical':
			coord_negative = coord[0] - index - 1, coord[1]
		if axis == 'horizontal':
			coord_negative = coord[0], coord[1] - index - 1

		if new_board[coord_negative] is not board.Empty:
			overlapped = True
			break
		new_board[coord_negative] = letter
	if overlapped:
		return []
	overlapped = False

	for index, letter in enumerate(after):
		if axis == 'vertical':
			coord_positive = coord[0] + index + 1, coord[1]
		if axis == 'horizontal':
			coord_positive = coord[0], coord[1] + index + 1
		if new_board[coord_positive] is not board.Empty:
			overlapped = True
		new_board[coord_positive] = letter
	
	if overlapped:
		return []
	results.append(new_board)
	
	return results


def number_of_letters_on_board(b):
	return len(list(b.iterdata()))


def split_word_by_position(word, char_position):
	return word[:char_position], word[char_position:]

def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]


def find_all_filled_coords(b):
	for coord in b:
		if b[coord] is not board.Empty:
			yield coord

def capture_words(b, coord):
	words = []
	word = b[coord]

	new_coord = coord
	while(True):
		new_coord = (new_coord[0] - 1, new_coord[1])
		if b[new_coord] is board.Empty:
			break
		word = b[new_coord] + word
	new_coord = coord
	while(True):
		new_coord = (new_coord[0] + 1, new_coord[1])
		if b[new_coord] is board.Empty:
			break
		word = word + b[new_coord]
	words.append(word)

	word = b[coord]
	new_coord = coord
	while(True):
		new_coord = (new_coord[0], new_coord[1] - 1)
		if b[new_coord] is board.Empty:
			break
		word = b[new_coord] + word
	new_coord = coord
	while(True):
		new_coord = (new_coord[0], new_coord[1] + 1)
		if b[new_coord] is board.Empty:
			break
		word = word + b[new_coord]
	words.append(word)
	return words


def valid_board_state(b):
	for coord, data in b.iterdata():
		for word in capture_words(b, coord):
			if len(word) > 1 and not is_word(word):
				return False
	return True


def print_board(b):
	row = 0
	for coord in b:
		if coord[0] != row:
			print('|')
			row = coord[0]
			#print('-' * 50)
		if b[coord] is not board.Empty:
			print(f'|{b[coord]}', end='')
		else:
			print('|.', end='')
	print('|')

def boards_equal(b1, b2):
	for coord, data in b1.iterdata():
		if b2[coord] != data:
			return False
	return True

def main():
	#counter = 0
	#for iter in iter_valid_words('ndhgsklpkyee'):
		#if counter % 100 == 0:
		#print(iter)
		#counter += 1
	solve_qless('ndhgsklpkyee')


if __name__ == '__main__':
	main()