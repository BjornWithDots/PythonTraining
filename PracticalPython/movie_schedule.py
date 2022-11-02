current_movies = {'The Grinch': '23:00',
                  'Rudolph': '13:00',
                  'Frosty the Snowman': '15:00',
                  'Christmas Vacation': '17:00'}

print("We're showing th following movies:")
for key in current_movies:
    print(key)

movie = input('What movie would like the showtime for?\n')

showtime = current_movies.get(movie)
if showtime is None:
    print("Requested movie isn't playing")
else:
    print(movie, 'is playing at', showtime)
