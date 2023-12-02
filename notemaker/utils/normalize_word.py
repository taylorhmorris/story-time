def normalize_word(word: str) -> str:
    if not isinstance(word, str):
        return ''
    result = ''
    for char in word:
        if char.isalpha() or char == ' ':
            result += char.lower()
    return result
