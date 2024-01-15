from __future__ import annotations
from random import choice, seed
from string import ascii_lowercase
from typing import Optional


from support import (
    load_words,
    choose_word,
    VOCAB_FILE,
    ANSWERS_FILE,
    CORRECT,
    MISPLACED,
    INCORRECT,
    UNSEEN,
)


def has_won(guess: str, answer: str) -> bool:
    """ Winning condition.
            Parameter: 
                guess (str): user prompt
                answer(str): chosen from vocab.txt
            Return bool
    """   
    if guess == answer:
        return True

    else:
        return False

def has_lost(guess_number: int) -> bool:
    """ Losing condition.
            Parameter:
                guess_number (int): if guess_number over 6 then lose
            Return bool
    """
    if guess_number >= 6:
        return True
    else:
        return False

def find_word(answer: str, words: tuple[str, ...]):
    """ Finding word position in a tuple.
            Parameter: 
                cs (str): word want to find
                ys (tuple<str>): the tuple 
            Return position number in tuple
    """
    for i, c in enumerate(words):
        if c == answer: 
            return i
    
def remove_word(words: tuple[str, ...], word: str) -> tuple():
    """ Remove a word from tuple.
            Parameter: 
                word (str): want to remove
                words (tuple<str>): tuple containing word
            Return tuple<str> without word
    """
    word_position = find_word(word, words) 
    new_words = words[0:word_position] + words[word_position+1:] #create a new tuple without word
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
    """ Prompt the user next guess and reprompting until a valid input is enter.
            Parameter: 
                guess_number(int)
                words (tuple<str>): tuple of valid guess
                guess (str): user input. must be in tuple(words) and has 6 letters
            Return guess or help('h') or keyboard ('k') or solver ('a') or quit ('q')
    """
    while True:
        guess = str(input('Enter guess %d: ' %(guess_number))) #take user input as guess
        guess = guess.lower() #turn user guess into lowercase
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
    """ Representation of guess: green box if letter in corrected position; yellow box if letter appeal in answer but in uncorrected position; black box if letter not in answer
            Parameter: 
                guess(str): guess in put of user, must contain 6 letters (letters can be duplicate) and exist in vocab.txt
                answer(str): choose from answer.txt contain 6 unique letters
            Return str of square 
    """
    guess_letter = tuple(guess)
    ans_letter = tuple(answer)
    match = []
    guess_enu = [[i, j] for i, j in enumerate(guess_letter)]
    ans_enu = [[i, j] for i, j in enumerate(ans_letter)]
    for index in range(6): #loop for comparing each letter of guess with each letter of answer at the same position
        if guess_enu[index] == ans_enu[index]: #green square if letter of guess in correct position 
            match.append(CORRECT)
        elif guess_enu[index] != ans_enu[index] and guess_enu[index][1] in ans_letter: #letter of guess at index position is not the same for answer at that position but letter in answer
            if guess_enu[index][1] in guess[index:]: #if duplicate letter in guess
                x = find_word(guess_enu[index][1], answer) #find misplace letter position answer
                if guess_enu[x] == ans_enu[x]: #if the other position is match, then return black at this position
                    match.append(INCORRECT)
                elif guess_enu[index][1] in guess[:index]: #if letter has been processed before -> black
                    match.append(INCORRECT)
                else:
                    match.append(MISPLACED) #misplaced if this letter never been processed and other position is not correct 
            else:
                match.append(MISPLACED) #not duplicate then misplaced
        else:
            match.append(INCORRECT)
    processed_guess = ''.join(match)
    return processed_guess
        
def update_history(history: tuple[tuple[[str, str]], ...], guess: str, answer: str) -> tuple[tuple[str, str], ...]:   
    """ A history update including all guesses and its processe form.
            Parameter:
                history(tuple<(str, str),>): contain guess and its processed form
                guess(str): guess prompted by user
                answer(str): chosen at the beginning of gameplay.
            Return history(('guess', 'processed guess))
    """
    history = history + (((guess, process_user(guess, answer))),) #update the history with new guess and its processed form
    return history

def print_history(history: tuple[tuple[str, str], ...]) -> None:
    """ Print the history of user's guess with its processed form.
            Parameters:
                history (tuple<(str, str), >): tuple resulted from update_history()
            return: 
                all the guessed and their processed forms up to the latest guesses
    """
    for x in range(len(history)):
        print("---------------\nGuess %d: " %(x+1)," ".join(history[x][0])) #print user's guess
        print("        ", history[x][1]) #print processed form
        x += 1
    print("---------------\n")
    return None

def print_keyboard(history: tuple[tuple[str, str], ...]) -> None:
    """ Provide the known information about each letter.
        Parameter:
            history (tuple<(str, str), >): result from update_history()
        Return
            print list of all letters with the known information about which letters have been guessed and their processed form
    """
    dic_alphabet = dict.fromkeys(ascii_lowercase, UNSEEN) #create dictionary with key: alphabet anf value: UNSEEN

    for x in range(len(history)):
        key = list(history[x][0])
        value = list(history[x][1])
        dic_guess = dict(zip(key, value)) #create dictionary with key: letter in guesses and value is its processed form
        for letter in dic_alphabet:
            if letter in dic_guess and dic_guess[letter]>dic_alphabet[letter]: #update processed letter in the alphabet dictionary
                dic_alphabet[letter] = dic_guess[letter]
    lp = list(dic_alphabet.items())
    print("\nKeyboard information\n------------")
    for i in range(0,len(lp),2):
        print('{}: {}\t{}: {}'.format(lp[i][0], lp[i][1], lp[i+1][0], lp[i+1][1])) #print the alphabet dictionary
    print('')
    return

def print_stats(stats: tuple[int,...]) -> None:
    """ Print the stats of the game.
            Parameter:
                stats (tuple<str>): tuple contains 7 elements representing which round won in 1-6 guesses and the number of rounds lost.
            Return: 
                print status of game play
    """
    print('\nGames won in:') 
    for i in range(len(stats)-1):
        print('%d moves:' %(i+1), stats[i]) #print each move and its status
    print('Games lost:', stats[6])
    return None

def guess_next(words: tuple[str,...], history: tuple[[str, str], ...]) -> optional[str]:
    """ Generate a guess word for the user.
            Parameters:
                words(tuple<str>): tuple contains all the available vocabs
                history (tuple<(str, str>, ...): result of uqdate_history
            Return
                generate a valid guess without violating the previous processed guess
            
    """
    possible_list = list(words) #list store available vocab
    for w in range(len(words)): #slice word in available vocab
        for attempt in range(len(history)):   #slice element in history
            for i in range(6): #slicing letter position in user's guess
                    if history[attempt][1][i] == CORRECT and history[attempt][0][i] != words[w][i]: #if letter is green and isn't in word then change word to none
                        possible_list[w] = None 
                        break
                    elif history[attempt][1][i] == INCORRECT and history[attempt][0][i] in words[w]: #letter is black and is in word 
                        if history[attempt][0][i] not in history[attempt][0][:i]: 
                            if history[attempt][0][i] not in history[attempt][0][i+1:]: #letter is not duplicated in guess then change word to none
                                possible_list[w] = None
                                break
                            elif history[attempt][0][i] in history[attempt][0][i:]: #letter is duplicated and equal to the letter at the same position of word then change word to none
                                if history[attempt][0][i] == words[w][i]:
                                    possible_list[w] = None
                                    break
                    elif history[attempt][1][i] == MISPLACED and history[attempt][0][i] not in words[w]: #letter is yellow and not in word then word -> none
                        possible_list[w] = None
                        break
                    elif history[attempt][1][i] == MISPLACED and history[attempt][0][i] == words[w][i]: #letter is yellow and equal to the letter in the same position of word then word -> none
                        possible_list[w] = None
                        break
    possible_list = list(filter(None, possible_list)) #delete all the none
    pos_guess = possible_list[0] #non-random choose word by choosing 1st word of the list
    return pos_guess


all_words = load_words('answers.txt')
available_vocab = load_words('vocab.txt')

def main():
    #select answer_word
    answer_word = choose_word(all_words)
    
    attempt = 1
    guess_storage = ()
    game_status = [0,0,0,0,0,0,0]
    
    while attempt <= 6:
        #get user guess
        while True: 
            guess_user = prompt_user(attempt, available_vocab)
            if guess_user == 'q': 
                break
            if guess_user  == 'h':
                print('Ah, you need help? Unfortunate.')
                guess_user = prompt_user(attempt, available_vocab) #ask for guess again
                break
            elif guess_user == 'k':
                print_keyboard(guess_storage)
                continue
            elif guess_user == 'a':
                guess_user = guess_next(available_vocab, guess_storage)
                break
            else:
                break
            
        if guess_user == 'q': #end game if user press q
            break
        else:
            guess_storage = update_history(guess_storage, guess_user, answer_word) #process and update guess
            print_history(guess_storage) #print history 
        
        if has_won(guess_user, answer_word) == True: #compare guess with answer and check if we win
            won_num = attempt - 1
            game_status[won_num] = 1
            print('Correct! You won in',attempt, 'guesses!')
            print_stats(game_status)
            play_again = str(input('Would you like to play again (y/n)? ')) #replay? 
            if play_again == 'y':
                remove_word(all_words, answer_word) #delete previous answer from all_words and call main() to play
                main()
            elif play_again == 'n': #exit while loop and stop the game
                break
        else:
            attempt += 1
            
        if has_lost(attempt - 1) == True: #if lost condition with over 6 guessing times
            print('You lose! The answer was:', answer_word) 
            game_status[attempt-1] = 1
            print_stats(game_status)
            play_again = str(input('Would you like to play again (y/n)? ')) #replay? 
            if play_again == 'y':
                remove_word(all_words, answer_word) 
                main()
            elif play_again == 'n': 
                break
        else:
            continue
        


if __name__ == "__main__":
    main()
