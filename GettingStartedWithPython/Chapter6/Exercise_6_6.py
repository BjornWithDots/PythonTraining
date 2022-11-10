def lettercounter(word,letter):
    count = 0
    for everyletter in word:
        if everyletter == letter: count = count + 1
    return count

word = input('Enter a word in which you want to count letters: ')
letter = input('Enter the letter you want to count: ')

count = lettercounter(word, letter)

print('The word', word, 'contains', count, letter+"'s")