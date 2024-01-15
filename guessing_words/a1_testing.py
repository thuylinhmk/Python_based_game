"""
Wordle
Assignment 1
Semester 1, 2022
CSSE1001/CSSE7030
"""
from __future__ import annotations
from random import choice, seed
from string import ascii_lowercase
from typing import Optional


from a1_support import (
    load_words,
    choose_word,
    VOCAB_FILE,
    ANSWERS_FILE,
    CORRECT,
    MISPLACED,
    INCORRECT,
    UNSEEN,
)


# Replace these <strings> with your name, student number and email address.
__author__ = "<Nguyen Thuy Linh>, <47277021>"
__email__ = "<s4727702@student.uq.edu.au>"


# Add your functions here


def has_won(guess: str, answer: str) -> bool:
    '''Winning condition.
        parameter: 
            guess (str): user prompt
            answer(str): chosen from vocab.txt
        return bool
    '''    
    if guess == answer:
        return True
    else:
        return False

def has_lost(guess_number: int) -> bool:
    '''Losing condition.
        parameter:
            guess_number (int): if guess_number over 6 then lose
        return bool
    '''
    if guess_number >= 6:
        return True
    else:
        return False

def find_word(answer: str, words: tuple[str, ...]):
    '''finding word position in a tuple:
        parameter: 
            cs (str): word want to find
            ys (tuple<str>): the tuple 
        return position number in tuple
    '''
    for i, c in enumerate(words):
        if c == answer:
            return i
    
def remove_word(words: tuple[str, ...], word: str) -> tuple():
    '''remove a word from tuple.
        parameter: 
            word (str): want to remove
            words (tuple<str>): tuple containing word
        return tuple<str> without word
    '''
    word_position = find_word(word, words) 
    new_words = words[0:word_position] + words[word_position+1:]
    return new_words

def load_words(filename: str) -> tuple():
    """ Loads all words from the file with the given name.

	Parameters:
		filename (str): The name of the file to load from. Each word must be on
						a separate line.

	Returns:
		tuple<str>: A tuple containing all the words in the file.
	"""
    with open(filename, 'r') as file:
        words = [line.strip() for line in file.readlines()]
    return tuple(words)

def choose_word(words: tuple[str,...]) -> str:
	""" Chooses a word at random from words.

	Parameters:
		words (tuple<str>): The words to choose from.

	Returns:
		str: A word chosen at random from words.
	"""
	return choice(words)

def prompt_user(guess_number: int, words: tuple[str, ...]) -> str:
    '''prompt the user next guess and reprompting until a valid input is enter.
        parameter: 
            guess_number(int)
            words (tuple<str>): tuple of valid guess
            guess (str): user input. must be in tuple(words) and has 6 letters
        return guess or help or keyboard or solver or quit
    '''
    
    while True:
        guess = str(input('Enter guess %d: ' %(guess_number)))
        guess = guess.lower()
        if guess == 'k':
            break
        if guess == 'a':
            break
        if guess == 'h':
            break
        if guess == 'q':
            break
        if len(guess) == 6 and guess not in words:
            print("Invalid! Unknown word")
            continue
        if len(guess) != 6:
            print("Invalid! Guess must be of length 6")
            continue
        if len(guess) == 6 and guess in words:
            break
    return guess
    
def process_user(guess: str, answer: str) -> str:
    '''Return representation of guess: green box if letter in corrected position; yellow box if letter appeal in answer but in uncorrected position; black box if letter not in answer
        parameter: 
            guess(str): guess in put of user, must contain 6 letters (letters can be duplicate) and exist in vocab.txt
            answer(str): choose from answer.txt contain 6 unique letters
        return str of square 
    '''
    guess_letter = tuple(guess)
    ans_letter = tuple(answer)
    match = []
    guess_enu = [[i, j] for i, j in enumerate(guess_letter)]
    ans_enu = [[i, j] for i, j in enumerate(ans_letter)]
    for index in range(6):
        if guess_enu[index] == ans_enu[index]:
            match.append(CORRECT)
        elif guess_enu[index] != ans_enu[index] and guess_enu[index][1] in ans_letter:
            if guess_enu[index][1] in guess:
                x = find_word(guess_enu[index][1], answer)
                if guess_enu[x] == ans_enu[x]:
                    match.append(INCORRECT)
                elif guess_enu[index][1] in guess[:index]: 
                    match.append(INCORRECT)
                else:
                    match.append(MISPLACED)
            else:
                match.append(MISPLACED)
        else:
            match.append(INCORRECT)
    processed_guess = ''.join(match)
    return processed_guess
        
def update_history(history: tuple[tuple[[str, str]], ...], guess: str, answer: str) -> tuple[tuple[str, str], ...]:   
    '''Return a copy of history update including lastes guess and its processe form.
        parameter:
            history(tuple<(str, str),>): contain guess and its processed form
            guess(str): guess prompted by user
            answer(str): chosen at the beginning of gameplay.
        return history(('guess', 'processed guess))
    '''
    history = history + (((guess, process_user(guess, answer))),)
    return history

def print_history(history: tuple[tuple[str, str], ...]) -> None:
    ''' Print the history of user's guess with its processed form.
        Parameters:
            history (tuple<(str, str), >): tuple resulted from update_history()
        return: 
            all the guessed and their processed forms up to the latest guesses
    '''
    for x in range(len(history)):
        print("---------------\nGuess %d: " %(x+1)," ".join(history[x][0]))
        print("        ", history[x][1])
        x += 1
    print("---------------\n")
    return None

def print_keyboard(history: tuple[tuple[str, str], ...]) -> None:
    '''Provide the known information about each letter.
        parameter:
            history (tuple<(str, str), >): result from update_history()
        return
            print list of all letters with the known information about which letters hav been guessed and their processed form
    '''
    dic_alphabet = dict.fromkeys(ascii_lowercase, '  ')

    for x in range(len(history)):
        key = list(history[x][0])
        value = list(history[x][1])
        dic_guess = dict(zip(key, value))
        for letter in dic_alphabet:
            if letter in dic_guess and dic_guess[letter]>dic_alphabet[letter]:
                dic_alphabet[letter] = dic_guess[letter]
    lp = list(dic_alphabet.items())
    print("\nKeyboard information")
    print("-"*15)
    for i in range(0,len(lp),2):
        print(lp[i][0], ':', lp[i][1], ' ',lp[i+1][0], ':', lp[i+1][1])
    return

def print_stats(stats: tuple[int,...]) -> None:
    '''print the stats of the game.
        parameter:
            stats (tuple<str>): tuple contains 7 elements representing which round won in 1-6 guess and the number of round lost.
        return: 
            stats
    '''
    print('\nGames won in:')
    for i in range(len(stats)-1):
        print('%d moves:' %(i+1), stats[i])
    print('Games lost:', stats[6])
    return None

#def replay(words: tuple[str, ...], word: str):

def guess_solver(words: tuple[str,...], history: tuple[[str, str], ...]) -> optional[str]:
    lpp_green = [] #list of elements containing green letter and its position
    lpp_yellow = [] #list of elements containing yellow letter and its position can be repeated
    lpp_yellow_letter = [] #list of elements containing yellow letter, can be repeated
    lpp_black = [] #list of elements containing black letter
    listwords = list(words)

    for x in range(len(history)):
        for i in range(len(history[x][0])):
            if history[x][1][i] == CORRECT:
                lpp_green.append((history[x][0][i], i),)
            if history[x][1][i] == MISPLACED:
                lpp_yellow.append((history[x][0][i], i),),
                lpp_yellow_letter.append((history[x][0][i]),)
            if history[x][1][i] == INCORRECT:
                lpp_black.append((history[x][0][i]))

    l_yel = [] #non repeated yellow letter
    lp_yel = [] #non repeated yellow letter and its position
    for ele in range(len(lpp_yellow)):
        if lpp_yellow[ele] not in l_yel:
            l_yel.append(lpp_yellow_letter[ele])

    for chr in range(len(lpp_yellow_letter)):
        if lpp_yellow_letter[chr] not in lp_yel:
            lp_yel.append((lpp_yellow[chr]), )

    #print(lpp_green)
    #print(l_yel)
    #print(lp_yel)
    #print(lpp_black)

    for index in range(len(listwords)):
        for char in lpp_black:
            if char in listwords[index]:
                listwords[index] = '' 
    listwords = list(filter(None, listwords))
    #print(listwords)

    guess_solver_raw = []
    #generate a list with words with green letter at correct position and contain yellow letter
    if len(lpp_green) > 0:
        for proc in range(len(lpp_green)):         #0
            for a_word in range(len(listwords)):       #word 0
                if lpp_green[proc][0] == listwords[a_word][lpp_green[proc][1]]: #00 word001
                    if all([c in listwords[a_word] for c in l_yel]) == True:
                        guess_solver_raw.append(listwords[a_word])
    else:
        for a_word in range(len(listwords)):
            if all([c in listwords[a_word] for c in l_yel]) == True:
                guess_solver_raw.append(listwords[a_word])
    #print(guess_solver_raw)
    '''
    guess_sol_refine = []
    #filter out all the words with yellow letter at known position
    if len(lp_yel) > 0:
        for each_word in range(len(guess_solver_raw)):
            for ylet in range(len(lp_yel)):
                numb = lp_yel[ylet][1]
                print(numb)
                if lp_yel[ylet][0] == guess_solver_raw[each_word][numb]:
                    guess_solver_raw[each_word] = ''
    else:
        pass
    '''
    #print(guess_solver_raw)
    guess_sol_refine = list(filter(None, guess_solver_raw))
    #print(guess_sol_refine)

    #choosing words
    guess_choice = choice(guess_sol_refine)
    return guess_choice
    

all_words = load_words('answers.txt')
available_vocab = load_words('vocab.txt')

def main():
    #select answer_word
    answer_word = choose_word(all_words)
    
    attempt = 0
    guess_storage = ()
    game_status = [0,0,0,0,0,0,0]
    while attempt < 6:
        
        #guess input from user
        guess_user = prompt_user(attempt, available_vocab)
        if guess_user  == 'h':
            print('Ah, you need help? Unfortunate.')
            guess_user = prompt_user(attempt, available_vocab)
    
        if guess_user == 'k':
            print_keyboard(guess_storage)
            continue
        elif guess_user == 'a':
            guess_user = guess_solver(available_vocab, guess_storage)
            guess_processed = process_user(guess_user, answer_word)
            #store guess and process form
            guess_storage = update_history(guess_storage, guess_user, answer_word)
            print_history(guess_storage)
        
        elif guess_user == 'q':
            break
        else:
            #process guess input to squares 
            guess_processed = process_user(guess_user, answer_word)
            #store guess and process form
            guess_storage = update_history(guess_storage, guess_user, answer_word)
            print_history(guess_storage)

        if has_won(guess_user, answer_word) == True:
            won_num = attempt - 1
            game_status[won_num] = 1
            print('Correct! You won in',attempt, 'guesses!')
            print_stats(game_status)
            break
        else:
                attempt += 1
        
        if has_lost(attempt) == True:
            print('You lose! The Answer was: ', answer_word) 
            game_status[attempt-1] = 1
            print_stats(game_status)
        else:
            continue
     #wanna replay? 
    play_again = str(input('Would you like to play again (y/n)?: '))
    if play_again == 'y':
        remove_word(all_words, answer_word)
        main()
    else:
        pass
           
   


if __name__ == "__main__":
    main()
