def lettercounter(word, letter):

    count = word.count(letter)
    return count

word = 'banana'
letter = 'a'
counts = lettercounter(word, letter)

print("The word", word, "contains", counts, letter+"'s")