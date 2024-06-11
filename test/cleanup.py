file = open("output.txt", "r")
unfilteredText = file.read()

unwantedCharacters = ["←", "25l", "25h", "2K1G", "[?", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏", "⠋"]

filteredText = unfilteredText.removesuffix("←").removesuffix("25l").removesuffix("25h").removesuffix("2K1G").removesuffix("[?").removesuffix("⠙").removesuffix("⠹").removesuffix("⠸").removesuffix("⠼").removesuffix("⠴").removesuffix("⠦").removesuffix("⠧").removesuffix("⠇").removesuffix("⠏").removesuffix("⠋")
print(filteredText)

file.close()