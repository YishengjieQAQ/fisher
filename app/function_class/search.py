def isbn_or_key(word):
    isbn_or_key = 'key'
    if len(word) == 13 and word.isdigit():
        return 'isbn'
    shor_word = word.replace('-', '')
    if len(word) == 10 and shor_word.isdigit():
        return 'isbn'
