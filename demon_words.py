file = open("words.txt")
word_list = file.readlines()
file.close()

from random import random


#prompts user to select difficulty and returns that difficulty
def user_choose_diff():
    diff_choice = input("Please choose a difficulty: 1. Easy, 2. Normal, 3. Hard ")
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
    valid_guess = "abcdefghijklmnopqrstuvwxyz"

    #sets list of words for each diff
    for word in word_list:
        if len(word) > 4 and len(word) < 6:
            ez_words.append(word)
        elif len(word) >= 6 and len(word) <= 8:
            norm_words.append(word)
        elif len(word) >= 9:
            hard_words.append(word)

    #gets user's choice of diff
    diff = user_choose_diff()
    
    #sets the initial list of words that will be used for the game, based on diff
    if diff == 1:
        active_word_list = ez_words
    elif diff == 2:
        active_word_list = norm_words
    elif diff == 3:
        active_word_list = hard_words

    #sets word and lists for game
    #in this version of the game the actual value of word does not matter. However,
    #I left it in because length_of_word is still used.
    showListSize = input("Would you like to see the size of the word list while you are playing? y/n ")
    word = wordPicker(active_word_list)
    word = word.strip().lower()
    length_of_word = len(word)
    answer_reveal = ""
    outcome = ""
    hidden_word = []
    for i in word:
        hidden_word.append("_")
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
        active_word_list = evilList(active_word_list, round_guess, length_of_word)
        if round_guess not in valid_guess or len(round_guess) > 1:
            print("Not a valid guess. ")
        elif round_guess in guesses:
            print("You've already guessed that letter. Try a different one. ")
        else:
            for i in active_word_list:
                if round_guess in i:
                    index_to_reveal = i.find(round_guess)
                    hidden_word[index_to_reveal] = round_guess
                    print(*hidden_word)
                    print("Correct guess. ")
                    if "_" not in hidden_word:
                        print("You won! The word was " + (answer_reveal.join(hidden_word)).upper())
                        outcome = "w"
                        round = 0
                        break
                    else:
                        print("You have " + str(round - 1) + " rounds remaining. ")
                        break
                else:
                    print(*hidden_word)
                    print("Incorrect guess. ")
                    print("You have " + str(round - 1) + " rounds remaining. ")
                    break
            round = round -1
            guesses.append(round_guess)
        
    if outcome != "w":
        #picks a random word from the active list to display
        word = wordPicker(active_word_list)
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
def evilList(words, guess, word_length):
    longest_list = []
    for w in words:
        if guess not in w:
            longest_list.append(w)
    i = 0
    while i <= word_length:
        list_to_compare = []
        for w in words:
            if w[i] == guess:
                list_to_compare.append(w)
        if len(list_to_compare) > len(longest_list):
            longest_list = list_to_compare
        i += 1
    return longest_list

def wordPicker(listWords):
    word = listWords[int(random() * len(listWords))]
    return word



game(word_list)