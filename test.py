import qless
import board
from is_word import WordLord


def test_annagrammed_to_words():
	word_lord = WordLord()
	assert word_lord.annagrammed_to_words('act') == ['act', 'cat']
	assert word_lord.annagrammed_to_words('ely') == ['eyl', 'ley', 'lye']



		




def test_is_word():
	word_lord = WordLord()
	assert word_lord.is_word('attack')
	assert word_lord.is_word('pumpkin')
	assert word_lord.is_word('ostrich')
	assert word_lord.is_word('tickle')
	assert word_lord.is_word('attic')
	assert not word_lord.is_word('csa')
	assert not word_lord.is_word('ajsdofiw')
	assert not word_lord.is_word('csa')
	assert not word_lord.is_word('yle')

def test_iter_valid_words():
	assert sorted(list(qless.iter_valid_words('tac'))) == ['act', 'at', 'cat', 'ta', 'tc']
	assert list(qless.iter_valid_words('attack')) == [
		'at', 'ta', 'aa', 'ak', 'ka', 'tt', 'tc', 'tk', 'att', 'tat', 'taa', 'act', 'cat', 
		'kat', 'tak', 'ack', 'tck', 'atta', 'tact', 'takt', 'acta', 'kata', 'taka', 'tack', 
		'katat', 'attack'] 
	
	word_lord = WordLord()
	for word in qless.iter_valid_words('ndhgsklpkyee'):
		assert word_lord.is_word(word)
	

def test_number_of_letters_on_board():
	b = board.Board((3,3))
	assert qless.number_of_letters_on_board(b) == 0
	b[(0,0)] = 'a'
	assert qless.number_of_letters_on_board(b) == 1
	b[(0,1)] = 'a'
	for coord in b:
		b[coord] = 'a'
	assert qless.number_of_letters_on_board(b) == 9


def test_place_word_vertical():
	board_size = (20,20)
	b = board.Board(board_size)
	coord = (10, 10)
	b[coord] = 'd'
	word = 'abcdefg'
	results = qless.place_word(b, coord, word, 'vertical')
	for result in results:
		qless.print_board(result)
	
	cb = board.Board(board_size)
	cb[(10, 7)] = 'a'
	cb[(10, 8)] = 'b'
	cb[(10, 9)] = 'c'
	cb[(10, 10)] = 'd'
	cb[(10, 11)] = 'e'
	cb[(10, 12)] = 'f'
	cb[(10, 13)] = 'g'

	assert qless.boards_equal(b, cb)

def test_place_word_horizontal():
	board_size = (20,20)
	b = board.Board(board_size)
	coord = (10, 10)
	b[coord] = 'd'
	word = 'abcdefg'
	results = qless.place_word(b, coord, word, 'horizontal')
	for result in results:
		qless.print_board(result)
	
	cb = board.Board(board_size)
	cb[(7, 10)] = 'a'
	cb[(8, 10)] = 'b'
	cb[(9, 10)] = 'c'
	cb[(10, 10)] = 'd'
	cb[(11, 10)] = 'e'
	cb[(12, 10)] = 'f'
	cb[(13, 10)] = 'g'

	assert qless.boards_equal(b, cb)

def test_capture_words():
	b = board.Board((20, 20))
	b[(8, 10)] = 'c'
	b[(9, 10)] = 'a'
	b[(10, 10)] = 't'
	b[(11, 10)] = 't'
	b[(12, 10)] = 'l'
	b[(13, 10)] = 'e'

	b[(10, 10)] = 't'
	b[(10, 11)] = 'i'
	b[(10, 12)] = 'c'
	b[(10, 13)] = 'k'
	b[(10, 14)] = 'l'
	b[(10, 15)] = 'e'
	assert sorted(qless.capture_words(b, (10, 10))) == ['cattle', 'tickle']

def test_is_valid_board():
	b = board.Board((20, 20))
	b[(8, 10)] = 'c'
	b[(9, 10)] = 'a'
	b[(10, 10)] = 't'
	b[(11, 10)] = 't'
	b[(12, 10)] = 'l'
	b[(13, 10)] = 'e'

	b[(13, 11)] = 'e'
	b[(13, 11)] = 'g'
	b[(13, 11)] = 'g'

	assert not qless.is_valid_board(b)

	b = board.Board((20, 20))
	b[(8, 10)] = 'c'
	b[(9, 10)] = 'a'
	b[(10, 10)] = 't'
	b[(11, 10)] = 't'
	b[(12, 10)] = 'l'
	b[(13, 10)] = 'e'

	b[(10, 10)] = 't'
	b[(10, 11)] = 'i'
	b[(10, 12)] = 'c'
	b[(10, 13)] = 'k'
	b[(10, 14)] = 'l'
	b[(10, 15)] = 'e'

	assert qless.is_valid_board(b)

	b = board.Board((20, 20))
	b[(8, 10)] = 'c'
	b[(9, 10)] = 'a'
	b[(10, 10)] = 't'
	b[(11, 10)] = 't'
	b[(12, 10)] = 'l'
	b[(13, 10)] = 'e'

	b[(13, 11)] = 'l'
	b[(13, 12)] = 'l'
	b[(13, 13)] = 'l'

	assert not qless.is_valid_board(b)


def test_subtract_letters():
	assert qless.subtract_letters('a', 'a') == ''
	assert qless.subtract_letters('aa', 'a') == 'a'
	assert qless.subtract_letters('abcde', 'bd') == 'ace'
	assert qless.subtract_letters('aabbcc', 'abc') == 'abc'
	assert qless.subtract_letters('abc', 'abd') == 'c'

	


def test_solve_qless():
	letters = 'ndhgsklpkyee'
	solution_generator = qless.solve_qless(letters)
	for _ in range(5):
		b = next(solution_generator)
		solution_letters = ''.join(x for _, x in b.iterdata())
		print(solution_letters, letters)
		qless.print_board(b)
		assert sorted(solution_letters) == sorted(letters)
		assert qless.is_valid_board(b)


def test_split_word_by_position():
	assert qless.split_word_by_position('abcdefg', 0) == ('', 'bcdefg')
	assert qless.split_word_by_position('abcdefg', 6) == ('abcdef', '')
	assert qless.split_word_by_position('abcdefg', 3) == ('abc', 'efg')


def test_add_first_word_boards_to_stack():
	#add_first_word_boards_to_stack(board_stack, letters, size)
	assert True


def test_find():
	assert qless.find('abcde', 'a') == [0]
	assert qless.find('abcde', 'e') == [4]
	assert qless.find('abcde', 'c') == [2]
	assert qless.find('abada', 'a') == [0, 2, 4]
	assert qless.find('aaaaa', 'a') == [0, 1, 2, 3, 4]
	assert qless.find('', 'a') == []