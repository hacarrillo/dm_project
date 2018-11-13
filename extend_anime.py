'''
This program writes genres as vectors in the anime list csv file. 
That is, if the anime is of genre action, the action column is set to 1
'''

import csv
import numpy as np

genres = (["Action", "Adventure", "Cars", "Comedy", "Dementia",
           "Demons", "Drama", "Ecchi", "Fantasy", "Game",
           "Harem", "Hentai", "Historical", "Horror", "Josei",
           "Kids", "Magic", "Martial Arts", "Mecha", "Military",
           "Music", "Mystery", "Parody", "Police", "Psychological",
           "Romance", "Samurai", "School", "Sci-Fi", "Seinen",
           "Shoujo", "Shoujo Ai", "Shounen", "Shounen Ai", "Slice of Life",
           "Space", "Sports", "Super Power", "Supernatural", "Thriller",
           "Vampire", "Yaoi", "Yuri"])

with open("./ourAnimeList.csv", "rt", encoding='ISO-8859-1') as animeList,  open("./ourExtendedAnimeList.csv", "w", newline='', errors='replace') as result: 
	animeListReader = csv.reader(animeList)
	writer = csv.writer(result)

	header = next(animeListReader)
	print(header)
	for genre in genres:
			header.append(genre)
	writer.writerow(header)

	for row in animeListReader:
		genresList = row[14]
		for i in range(len(genres)):
			if genres[i] in genresList:
				row.append(1)
			else:
				row.append(0)
		writer.writerow(row)
