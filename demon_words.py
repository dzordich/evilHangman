file = open("words.txt")
word_list = file.readlines()
file.close()

from random import random


#prompts user to select difficulty and returns that difficulty
def user_choose_diff():
    diff_choice = input("Please choose a difficulty: 1. Easy (4 letter words), 2. Normal (6 letter words), 3. Hard(8 letter words) ")
    if diff_choice == "1" or diff_choice.lower() == "normal":
        diff = 1 
        print("You've selected easy difficulty.")
        return diff
    elif diff_choice == "2" or diff_choice.lower() == "normal":
        diff = 2
        print("You've selected normal difficulty. ")
        return diff
    elif diff_choice == "3" or diff_choice.lower() == "hard":
        diff = 3
        print("You've selected hard difficulty. Good luck. ")
        return diff
    else:
        return user_choose_diff()


def game(word_list):
    ez_words = []
    norm_words = []
    hard_words = []
    active_word_list = []
    word = ""
    round = 8
    diff = 2
    guesses = []
    incorrect_guesses = []
    valid_guess = "abcdefghijklmnopqrstuvwxyz"

    #sets list of words for each diff
    for word in word_list:
        if len(word.strip()) == 4:
            ez_words.append(word.lower().strip())
        elif len(word.strip()) == 6:
            norm_words.append(word.lower().strip())
        elif len(word.strip()) == 8:
            hard_words.append(word.lower().strip())

    #gets user's choice of diff
    diff = user_choose_diff()
    
    #sets the initial list of words that will be used for the game, based on diff
    if diff == 1:
        active_word_list = ez_words
        length_of_word = 4
    elif diff == 2:
        active_word_list = norm_words
        length_of_word = 6
    elif diff == 3:
        active_word_list = hard_words
        length_of_word = 8

    #sets word and lists for game
    #in this version of the game the actual value of word does not matter. However,
    #I left it in because length_of_word is still used.
    showListSize = input("Would you like to see the size of the word list while you are playing? y/n ")
    answer_reveal = ""
    outcome = ""
    hidden_word = []
    i = 0
    while i < length_of_word:
        hidden_word.append("_")
        i += 1
    print(" ")
    print("Get ready. The word is ", length_of_word, " letters long.")
    print(" ")

    #each iteration of this while loop is a round of the game
    #since a correct word is never defined in this version of the game,
    #the game is won by changing every _ in hidden_word to a letter.
    while round > 0:
        print(*hidden_word)
        print("ROUND " + str(round))
        if showListSize.lower() == "y":
            print("Size of list of words: ", len(active_word_list))
        print("Your guesses: ", *guesses)
        print(" ")
        round_guess = input("Please guess a letter: ").lower()
        #active_word_list is reset at the point in each round where the user makes a guess
        active_word_list = evilList(active_word_list, round_guess, length_of_word, incorrect_guesses)
        if round_guess not in valid_guess or len(round_guess) != 1:
            print("Not a valid guess. ")
        elif round_guess in guesses:
            print("You've already guessed that letter. Try a different one. ")
        elif guess_is_right(round_guess, active_word_list):
            index = list_of_indexes(round_guess, active_word_list[0])
            for i in index:
                hidden_word[i] = round_guess
            
            print(*hidden_word)
            print("Correct guess. ")
            if "_" not in hidden_word:
                print("You won! The word was " + (answer_reveal.join(hidden_word)).upper())
                outcome = "w"
                round = 0
            else:
                print("You have " + str(round - 1) + " rounds remaining. ")
        else:
            print(*hidden_word)
            print("Incorrect guess. ")
            incorrect_guesses.append(round_guess)
            print("You have " + str(round - 1) + " rounds remaining. ")
        round = round -1
        guesses.append(round_guess)
        
    if outcome != "w":
        #picks a random word from the active list to display
        word = wordPicker(active_word_list, hidden_word)
        print("You lost! You ran out of guesses. The word was " + word.upper())

    playAgain(input("Would you like to play again? y/n: "))
    print(" ")

#checks to see if the user wants to play again. Calls game() if yes. Exits program if no.
def playAgain (u):
    if u.lower() == "y":
        return game(word_list)
    elif u.lower() == "n":
        print("Thanks for playing!")
        exit()
    else:
        print("Please input y for yes or n to exit the program.")
        return playAgain(u)

#first sets the word family that does not contain the user's guess as the base case to be compared against.
#then checks if the word families containing the guess in each index is larger than the base case.
#resets the base case if the new family is larger.
#returns the longest list.
def evilList(words, guess, word_length, guesses):
    longest_list = []
    
    for w in words:
        if guess not in w and guessed_letter_in_word(w, guesses) == 0 :
            longest_list.append(w)
    # print(*longest_list, "***INITIAL***")
    for w in words:
        if len(words_w_same_index(words, w, guess)) > len(longest_list):
            longest_list = words_w_same_index(words, w, guess)
            # print(*longest_list, "***NEW***")
    return longest_list

def reveal(words, guess, word_length):
    longest_list = []
    
    for w in words:
        if w[0] == guess:
            longest_list.append(w)
    i = 1
    while i < word_length:
        list_to_compare = []
        for w in words:
            if w[i] == guess:
                list_to_compare.append(w)
        if len(list_to_compare) > len(longest_list):
            longest_list = list_to_compare
        i += 1
    return longest_list

def wordPicker(listWords, hidden_word):
    for word in listWords:
        boolean = True
        ind = 0
        for i in hidden_word:
            if i != word[ind] and i != "_":
                boolean = False
            ind += 1
        if boolean:
            return word
            

def guessed_letter_in_word(word, letters):
    count = 0
    for l in letters:
        for i in word:
            if l == i:
                count += 1
    return count

def guess_is_right(guess, active_list):
    for word in active_list:
        if guess in word:
            return True
    return False

#returns a list of indexes of guess in a word
def list_of_indexes(guess, word):
    index = []
    x = 0
    for i in word:
        if i == guess:
            index.append(x)
        x += 1
    return index

def words_w_same_index(words, word, guess):
    same_words = []
    same_words.append(word)
    for w in words:
        if list_of_indexes(guess, w) == list_of_indexes(guess, word):
            same_words.append(w)
    return same_words


game(word_list)