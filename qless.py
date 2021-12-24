import itertools
import board
import queue
import argparse
from is_word import WordLord


WORD_LORD = WordLord()

def solve_qless(letters, max_returns=float('inf'), word_pack='word_pack/top_25000.txt'):

	size = (len(letters)*2, len(letters)*2) # handles worst case word placement
	stack = []

	visited = []
	solutions_returned = 0

	WORD_LORD.load_words(word_pack=word_pack)

	add_first_word_boards_to_stack(stack, letters, size)

	while len(stack) > 0 and solutions_returned < max_returns:
		letters, current_board = stack.pop()
		if is_valid_board(current_board) and len(letters) == 0:
			yield current_board
			solutions_returned += 1
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


def print_qless_solutions(letters, format='board', file=None, max_returns=float('inf'), word_pack='word_pack/top_25000.txt'):
	for b in solve_qless(letters, max_returns=max_returns, word_pack=word_pack):
		if file is not None:
			with open(file, 'a') as f:
				if format == 'words':
					f.write(string_board_words(b))
				elif format == 'board':
					f.write(string_board(b))
		else:
			if format == 'words':
				print_board_words(b)
			elif format == 'board':
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
	if len(word) > 1:
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
	if len(word) > 1:
		words.append(word)
	return words


def is_valid_board(b):
	for coord, data in b.iterdata():
		for word in capture_words(b, coord):
			if len(word) > 1 and not is_word(word):
				return False
	return True


def capture_all_words(b):
	words = set()
	for coord, data in b.iterdata():
		for word in capture_words(b, coord):
			words.add(word)
	return words


def string_board_words(b):
	result = f'b: {[word for word in capture_all_words(b)]}'


def print_board_words(b):
	print(string_board_words(b))


def string_board(b):
	result = ''
	row = 0
	for coord in b:
		if coord[0] != row:
			result += '|\n'
			row = coord[0]
		if b[coord] is not board.Empty:
			result += f'|{b[coord]}'
		else:
			result += '|.'
	result += '|'
	return result


def print_board(b):
	print(string_board(b))


def boards_equal(b1, b2):
	for coord, data in b1.iterdata():
		if b2[coord] != data:
			return False
	return True


def main():
	parser = argparse.ArgumentParser(description='Solve a word search puzzle.')
	parser.add_argument('--word_pack', type=str, default='word_packs/top_25000.txt', help='The file containing the word pack.')
	parser.add_argument('--format', type=str,
						default='board',
						choices=['none', 'words', 'board'],
						help='The format to output the boards in. Choices are no output, the words that make up the solution, or the full board'
	)
	parser.add_argument('--file', type=str, help='The file to output the solution boards to.')
	parser.add_argument('--search',type=str, default='dfs', choices=['dfs', 'bfs'], help='The search algorithm to use.')
	parser.add_argument('--letters', default=None, type=str, help='The letters to use in the puzzle.')
	parser.add_argument('--max', type=float, default=float('inf'), help='The maximum number of boards to output.')

	args = parser.parse_args()

	if args.letters is None:
		#TODO make this a random letter generator
		args.letters = 'ndhgsklpkyee' #'ndhgsklpkyeera' #'aactm'

	print_qless_solutions(letters=args.letters, format=args.format, file=args.file, word_pack=args.word_pack, max_returns=args.max)


if __name__ == '__main__':
	main()
