import random

# ---------- Word bank: categories with lists of words ----------
WORD_BANK = {
    "animals": ["elephant", "giraffe", "penguin", "dolphin", "kangaroo",
                "tiger", "monkey", "rabbit", "zebra", "camel"],
    "fruits": ["banana", "mango", "orange", "papaya", "cherry",
               "grapes", "lemon", "guava", "apple", "peach"],
    "countries": ["india", "brazil", "canada", "france", "japan",
                  "egypt", "kenya", "mexico", "norway", "spain"],
    "tech": ["python", "keyboard", "program", "variable", "function",
             "monitor", "internet", "browser", "coding", "laptop"],
}

# ---------- Difficulty levels: how many wrong guesses are allowed ----------
DIFFICULTY = {"easy": 8, "medium": 6, "hard": 4}

# ---------- ASCII hangman: 7 stages (0 = empty gallows, 6 = fully drawn) ----------
HANGMAN_STAGES = [
    r"""
  +---+
  |   |
      |
      |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
      |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
  |   |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========""",
]


def choose_from_menu(title, options):
    """Show a numbered menu and keep asking until the player picks a valid number."""
    print("\n" + title)
    for i, name in enumerate(options, 1):
        print("  " + str(i) + ". " + name)

    while True:
        choice = input("Choose a number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        print("Please enter a number from 1 to " + str(len(options)) + ".")


def get_stage(wrong, max_wrong):
    """Map wrong guesses to a drawing stage (0-6), whatever the difficulty."""
    return (wrong * 6 + max_wrong - 1) // max_wrong  # rounds up


def play_round(category, max_wrong):
    """Play one round. Returns True if the player wins, False if they lose."""
    word = random.choice(WORD_BANK[category])
    guessed = []   # every letter the player has tried
    wrong = 0

    print("\n=== HANGMAN ===")
    print("Category:", category, "| Word length:", len(word))

    while True:
        print(HANGMAN_STAGES[get_stage(wrong, max_wrong)])

        # Build the word display, e.g. "p _ t h _ n"
        display = ""
        for letter in word:
            if letter in guessed:
                display += letter + " "
            else:
                display += "_ "

        print("\nWord:", display)
        print("Guessed:", " ".join(guessed) if guessed else "-")
        print("Wrong guesses left:", max_wrong - wrong)

        # Win / lose checks
        if "_" not in display:
            print("\nYou got it! The word was '" + word + "'.")
            return True
        if wrong >= max_wrong:
            print("\nGame over! The word was '" + word + "'.")
            return False

        guess = input("Enter a letter: ").strip().lower()

        # Validate the input
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single letter.")
        elif guess in guessed:
            print("You already guessed '" + guess + "'.")
        else:
            guessed.append(guess)
            if guess in word:
                print("Nice! '" + guess + "' is in the word.")
            else:
                wrong += 1
                print("Sorry, '" + guess + "' is not in the word.")


def main():
    wins = 0
    losses = 0
    print("Welcome to Hangman!")

    playing = True
    while playing:
        # Pick a category and a difficulty
        category = choose_from_menu("Pick a category:", list(WORD_BANK) + ["random"])
        if category == "random":
            category = random.choice(list(WORD_BANK))

        level = choose_from_menu("Pick a difficulty:", list(DIFFICULTY))
        max_wrong = DIFFICULTY[level]
        print("\n" + level.capitalize() + " mode: you get " + str(max_wrong) + " wrong guesses.")

        # Play and update the score
        if play_round(category, max_wrong):
            wins += 1
        else:
            losses += 1

        print("\nScore -> Wins: " + str(wins) + " | Losses: " + str(losses))

        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            playing = False

    print("\nFinal score -> Wins: " + str(wins) + " | Losses: " + str(losses))
    print("Thanks for playing!")


if __name__ == "__main__":
    main()
