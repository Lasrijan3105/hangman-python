import random
import string

# List of candidate secret words for the game.
words = ["python", "java", "swift", "javascript"]

# Session counters for wins and losses (kept in memory while the program runs).
success_nb, lost_nb = 0, 0


def get_user_input(guessed_letters):
    """
    Prompt the user for a single lowercase ASCII letter.
    guessed_letters: list used for display (e.g. ['p', '-', '-', 'h', ...]).
    Returns a validated single character string.
    """
    while True:
        # Print the current guessed pattern (e.g. "p-y--")
        print("\n" + "".join(guessed_letters))
        entry = input("Input a letter: ").strip()

        # Validation: must be exactly one character
        if len(entry) != 1:
            print("Please, input a single letter.")
        # Validation: must be a lowercase ASCII letter
        elif entry not in string.ascii_lowercase:
            print("Please, enter a lowercase letter from the English alphabet.")
        else:
            # Valid input, exit loop and return it
            break
    return entry


def play():
    """
    Run a single round of Hangman:
    - Select a secret word at random.
    - Allow up to `remaining_attempts` incorrect guesses.
    - Reveal all occurrences of a correctly guessed letter.
    Returns the secret word on success, or an empty string on failure.
    """
    remaining_attempts = 8  # number of incorrect guesses allowed
    secret_word = random.choice(words)  # randomly chosen secret word
    guessed_letters = ['-'] * len(secret_word)  # display list, '-' for unknown letters
    fake_guessed_letters = set()  # set of incorrect letters already guessed
    # remaining_letters holds unrevealed letters; each occurrence is kept as an element
    remaining_letters = list(secret_word)

    # Main guessing loop: continue until attempts run out or word is guessed
    while remaining_attempts != 0:
        user_input = get_user_input(guessed_letters)

        # If the user's letter is still in remaining_letters (i.e., an unrevealed occurrence)
        if user_input in remaining_letters:
            # Find all indexes in the secret word where the letter appears
            indexes = [idx for idx, value in enumerate(secret_word) if value == user_input]

            # For each index found, reveal the letter in guessed_letters and remove one occurrence
            # from remaining_letters (so duplicates are handled by removing one occurrence per index).
            for _, idx in enumerate(indexes):
                remaining_letters.remove(user_input)
                guessed_letters[idx] = user_input

            # If all letters have been revealed, the player wins
            if secret_word == "".join(guessed_letters):
                print(f"You guessed the word {secret_word}!")
                return secret_word

        # Detect repeated guesses:
        # - user_input not in remaining_letters but in secret_word:
        #   means the letter exists in the word but all its occurrences were already revealed
        # - or user_input in fake_guessed_letters: previously guessed incorrect letter
        elif user_input not in remaining_letters and user_input in secret_word or user_input in fake_guessed_letters:
            print("You've already guessed this letter.")
        else:
            # New incorrect guess: decrement attempts, notify player, and save the guess
            remaining_attempts -= 1
            print(f"That letter doesn't appear in the word, {remaining_attempts} attempts remaining.")
            fake_guessed_letters.add(user_input)

    # If the loop ends because attempts reached 0, return empty string to signal loss
    return ''


# Game title printed at startup
print("H A N G M A N")

# Main menu loop: allow player to start a game, view results, or exit
while True:
    menu = (input('Type "play" to play the game, "results" to show the scoreboard, and "exit" to quit: ')
            .strip()
            .lower())

    if menu == "play":
        result = play()
        if result:
            # Non-empty result indicates a win
            success_nb += 1
            print("You survived!")
        else:
            # Empty result indicates a loss
            lost_nb += 1
            print("\nYou lost!")
    elif menu == "results":
        # Show current session scoreboard
        print(f"You won: {success_nb} times.")
        print(f"You lost: {lost_nb} times.")
    elif menu == "exit":
        # Quit the program
        break
