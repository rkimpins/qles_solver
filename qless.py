import itertools
import board
import queue
from is_word import WordLord


#TODO
#make it use only common not weird words (maybe just not 2 letter words)
#fix repeating problem
#simulate dice roll
#let user input letters

WORD_LORD = WordLord()

def solve_qless(letters):
	size = (len(letters)*2, len(letters)*2) # this is the largest we will ever need the board to be
	stack = []

	visited = []

	add_first_word_boards_to_stack(stack, letters, size)

	while len(stack) > 0:
		letters, current_board = stack.pop()
		if is_valid_board(current_board) and len(letters) == 0:
			yield current_board
		if not is_valid_board(current_board):
			continue
		if is_valid_board(current_board):
			for coord, letter in current_board.iterdata():
				for word in iter_valid_words(letters + letter):
					left_over_letters = subtract_letters(letters, word)
					for r_board in place_word(current_board, coord, word, 'horizontal'):
						if list(r_board.iterdata()) not in visited:
							stack.append((left_over_letters, r_board))
							visited.append(list(r_board.iterdata()))
					for r_board in place_word(current_board, coord, word, 'vertical'):
						if list(r_board.iterdata()) not in visited:
							stack.append((left_over_letters, r_board))
							visited.append(list(r_board.iterdata()))


def print_qless_solutions(letters):
	for b in solve_qless(letters):
		print("SOLVED")
		print_board(b)


def add_first_word_boards_to_stack(board_stack, letters, size):
	start_board = board.Board(size)
	for word in iter_valid_words(letters):
		coord = (size[0]//2, size[1]//2 - len(word)//2)
		new_b = start_board.copy()
		for letter in word:
			new_b[coord] = letter
			coord = (coord[0], coord[1] + 1)
		board_stack.append((subtract_letters(letters, word), new_b))


def iter_valid_words(letters):
	for i in range(2, len(letters) + 1):
		yielded = set()
		for word in itertools.combinations(letters, i):
			annagramed = ''.join(sorted(word))
			for real_word in WORD_LORD.annagrammed_to_words(annagramed):
				if real_word not in yielded:
					yielded.add(real_word)
					yield real_word


def is_word(word):
	return WORD_LORD.is_word(word)


def subtract_letters(letters, subtractor):
	l_letters = list(letters)
	for letter in subtractor:
		if letter in l_letters:
			l_letters.remove(letter)
	return ''.join(l_letters)


def find(word, char):
	return [i for i, letter in enumerate(word) if letter == char]


def place_word(current_board, coord, word, axis):
	assert axis in ['vertical', 'horizontal']
	results = []

	char_positions = find(word, current_board[coord])
	for char_pos in char_positions:
	
		before, after = split_word_by_position(word, char_pos)
		new_board = current_board.copy()

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
	return word[:char_position], word[char_position+1:]


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


def is_valid_board(b):
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
	#print_qless_solutions('ndhgsklpkyee')
	print_qless_solutions('ndhgsklpkyeera')
	#print_qless_solutions('aactm')


if __name__ == '__main__':
	main()
