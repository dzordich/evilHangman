file = open("words.txt")
word_list = file.readlines()
file.close()

from random import random

#returns a random index, based on the difficulty the user chooses
def user_choose_diff(x):
    if x == "1":
        diff = 1 
        print("You've selected easy difficulty.")
        return diff
    elif x == "2" or x.lower() == "normal":
        diff = 2
        print("You've selected normal difficulty. ")
        return diff
    elif x == "3" or x.lower() == "hard":
        diff = 3
        print("You've selected hard difficulty. Good luck. ")
        return diff
    else:
        return user_choose_diff(x)

#contains the code for pretty much the whole game. is recursive too.
def game(word_list):
    ez_words = []
    norm_words = []
    hard_words = []
    word = ""
    round = 8
    diff = 2
    guesses = []
    valid_guess = "abcdefghijklmnopqrstuvwxyz"

    #sets list of words for each diff
    for word in word_list:
        if len(word) > 4 and len(word) < 6:
            ez_words.append(word)
        elif len(word) >= 6 and len(word) <= 7:
            norm_words.append(word)
        elif len(word) >= 8:
            hard_words.append(word)

    #gets user's choice of diff
    diff_choice = input("Please choose a difficulty: 1. Easy, 2. Normal, 3. Hard ")
    diff = user_choose_diff(diff_choice)
    #sets the list of words that will be used for the game, based on diff
    if diff == 1:
        word = ez_words[int(random() * len(ez_words))]
    elif diff == 2:
        word = norm_words[int(random() * len(norm_words))]
    else:
        word = hard_words[int(random() * len(hard_words))]

    #sets word and lists for game
    word = word.strip().lower()
    length_of_word = len(word)
    outcome = ""
    hidden_word = []
    correct_word = []
    for i in word:
        correct_word.append(i)
        hidden_word.append("_")
    print(" ")
    print("Get ready. The word is ", length_of_word, " letters long.")
    print(" ")
    print(" ")
    print(" ")

    #each iteration of this while loop is a round of the game
    while hidden_word != correct_word and round > 0:
        print(*hidden_word)
        print("ROUND " + str(round))
        print("Your guesses: ", *guesses)
        print(" ")
        round_guess = input("Please guess a letter: ").lower()
        guesses.append(round_guess)
        if round_guess not in valid_guess or len(round_guess) > 1:
            print("Not a valid guess. ")
        elif round_guess in guesses:
            print("You've already guessed that letter. Try a different one. ")
        else:
            if round_guess in word:
                n = 0
                for i in word:
                    if i == round_guess:
                        hidden_word[n] = round_guess
                    n = n + 1
                print(*hidden_word)
                print("Correct guess. ")
                if hidden_word == correct_word:
                    print("You won! The word was " + word.upper())
                    outcome = "w"
                    break
                print("You have " + str(round - 1) + " rounds remaining. ")
            else:
                print(*hidden_word)
                print("Incorrect guess. ")
                print("You have " + str(round - 1) + " rounds remaining. ")
            round = round -1

    if outcome != "w":
        print("You lost! You ran out of guesses. The word was " + word.upper())

    playAgain(input("Would you like to play again? y/n: "))
    print(" ")

#checks to see if the user wants to play again. Recursively calls game() if yes. Exits program if no.
def playAgain (u):
    if u.lower() == "y":
        return game(word_list)
    elif u.lower() == "n":
        print("Thanks for playing!")
        exit()
    else:
        print("Please input y for yes or n to exit the program.")
        return playAgain(u)





game(word_list)









