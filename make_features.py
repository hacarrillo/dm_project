import csv
# delete columns
# with open("./userList.csv", "rt", encoding='utf-8') as src:
#     rdr = csv.reader(src)
#     with open("./ourUserList.csv", "w", newline='', errors='replace') as result:  # noqa
#         wtr = csv.writer(result)
#         for r in rdr:
#             wtr.writerow((r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[10], r[13], r[14], r[15], r[16]))  # noqa

# remove empty rows
# with open("./ourUserAnimeList2.csv", "rt", encoding="ISO-8859-1") as src:
#     rdr = csv.reader(src)
#     with open("./ourUserAnimeList.csv", "w", newline='', errors='replace') as result:  # noqa
#         writer = csv.writer(result)
#         for row in rdr:
#             if row:
#                 writer.writerow(row)

# add column to front of csv
# with open("./ourUserList2.csv", "rt", encoding='ISO-8859-1') as ourUserList,  open("./UserList.csv", "rt", encoding='ISO-8859-1') as userList:  # noqa
#     userListReader2 = csv.reader(ourUserList)
#     userListReader = csv.reader(userList)
#     with open("./ourUserList.csv", "w", newline='', errors='replace') as result:  # noqa
#         writer = csv.writer(result)
#         for row1, row2 in zip(userListReader, userListReader2):
#             row2.insert(0, row1[0])
#             writer.writerow(row2)

# todo
# 1. open files ourUserList, ourAnimeList, ourUserAnimeList
# 2. from ourUserAnimeList get the anime id watched by a user
# 3. match the id with the anime from ourAnimeList
# 4. get the genres of the anime
# 5. update the watched genres in ourUserList_genres
# 6. once the name cganges write to the row
genres = (["Action", "Adventure", "Cars", "Comedy", "Dementia",
           "Demons", "Drama", "Ecchi", "Fantasy", "Game",
           "Harem", "Hentai", "Historical", "Horror", "Josei",
           "Kids", "Magic", "Martial Arts", "Mecha", "Military",
           "Music", "Mystery", "Parody", "Police", "Psychological",
           "Romance", "Samurai", "School", "Sci-Fi", "Seinen",
           "Shoujo", "Shoujo Ai", "Shounen", "Shounen Ai", "Slice of Life",
           "Space", "Sports", "Super Power", "Supernatural", "Thriller",
           "Vampire", "Yaoi", "Yuri"])
watched = [0]*len(genres)
score = [0]*len(genres)
userListArray = {}
userAnimeListArray = {}
animeListArray = {}
with open("./ourUserList.csv", "rt", encoding='ISO-8859-1') as userList,  open("./ourUserAnimeList.csv", "rt", encoding='ISO-8859-1') as userAnimeList,  open("./ourAnimeList.csv", "rt", encoding='ISO-8859-1') as animeList:  # noqa
    userListReader = csv.reader(userList)
    userAnimeListReader = csv.reader(userAnimeList)
    animeListReader = csv.reader(animeList)
    userAnimeList.readline();
    userList.readline();
    animeList.readline();
    for row in userListReader:
        userListArray[row[0]] = row
    for row in animeListReader:
        animeListArray[row[0]] = row
    c = 0
    for row in userAnimeListReader:
        c = c + 1
        if row[0] in userAnimeListArray:
            userAnimeListArray[row[0]] = userAnimeListArray[row[0]] + [row]
        else:
            userAnimeListArray[row[0]] = [row] 
        if c % 1000000 == 0:
            print(c)

with open("./ourUserList_genres.csv", "w", newline='', errors='replace') as result:  # noqa
    userList = open("./ourUserList.csv", "rt", encoding='ISO-8859-1')
    userListReader = csv.reader(userList)
    writer = csv.writer(result)
    row1 = next(userListReader)  # get the first row
    # create new array that holds all the string values for the new columns
    genreWatchedScored = [""]*(2*len(genres))
    for i in range(len(genres)):
        genreWatchedScored[2*i] = genres[i] + "_Watched"
        genreWatchedScored[(2*i)+1] = genres[i] + "_Scored"
    # append all the new columns to the row
    for newCol in genreWatchedScored:
        row1.append(newCol)
    writer.writerow(row1)
    name = ""
    for ul in userListArray:
        watched = [0]*len(genres)
        score = [0]*len(genres)
        if ul in userAnimeListArray:
            useranime = userAnimeListArray[ul]
            for anime in useranime:
                animeid = anime[1]
                animeScore = anime[3]
                status = int(anime[4])
                anime_info = animeListArray[animeid]
                genreList = anime_info[14]
                for i in range(len(genres)):
                    # keep only completed, dropped, or non zero reviews 
                    if status == 2 or status == 4 or int(animeScore) != 0:
                        if genres[i] in genreList:
                            watched[i] += 1
                            score[i] += int(animeScore)
        rowToWrite = userListArray[ul]
        for i in range(len(genres)):
            rowToWrite.append(watched[i])
            rowToWrite.append(score[i])
        writer.writerow(rowToWrite)
