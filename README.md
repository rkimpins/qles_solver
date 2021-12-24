## Usage
Just run python3 qless.py

We have some options for arguments.

python3 qless.py --letters 'apoivhsfdaf' --word_pack 'my_words.txt' --format 'boards' --file 'output.txt' --search 'dfs' (not implemented yet) --max 100 

Explanation:
* letters: the letters we 'rolled' to start the game of qless
* format: how we want to output solutions. We can either output a full board or just the words in the solution
* file: the file we want to pipe output to instead
* max: the maximum number of results we want to return
* ...


## Word_packs
Words are considered valid if they appear in the word pack we denote in the command line arguments. I found that using the scrabble dictionary gave me solutions, just not very satisfying ones.

The word packs are:
* scrabble.txt -> all legal scrabble words
* top_25000.txt -> the 25000 most common english words
* top_100000.txt -> top 100,000 most common words
* top_100000_legal_scrabble.txt -> top 100,000 but filtering out words that aren't legal scrabble words
* no_two_letter_words.txt -> top 100,000 words but with all of the 2 letter words removed and only scrabble legal words


## TODO
Here are the things I still want to do
* Add a random letter generator to run this on a random input
* Explore what combinations of words are solvable and which aren't
* Different search methods, like bfs, A*, best first, most letters removed, least letters removed, etc
* Fix up the tests, I broke them with some refactoring and word packs
