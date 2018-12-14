import csv
# delete columns
with open("./filteredUserListGenres.csv", "rt", encoding='utf-8') as src:
    rdr = csv.reader(src)
    with open("./filteredUserListGenres_Clustering.csv", "w", newline='', errors='replace') as result:  # noqa
        wtr = csv.writer(result)
        for r in rdr:
            for c in range(len(r)):
                if r[c] == '':
                    r[c] = 0
            # last col number is 102
            wtr.writerow((r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[11], r[12], r[13], r[17], r[18], r[19], r[20], r[21], r[22], r[23], r[24], r[25], r[26], r[27], r[28], r[29], r[30], r[31], r[32], r[33], r[34], r[35], r[36], r[37], r[38], r[39], r[40], r[41], r[42], r[43], r[44], r[45], r[46], r[47], r[48], r[49], r[50], r[51], r[52], r[53], r[54], r[55], r[56], r[57], r[58], r[59], r[60], r[61], r[62], r[63], r[64], r[65], r[66], r[67], r[68], r[69], r[70], r[71], r[72], r[73], r[74], r[75], r[76], r[77], r[78], r[79], r[80], r[81], r[82], r[83], r[84], r[85], r[86], r[87], r[88], r[89], r[90], r[91], r[92], r[93], r[94], r[95], r[96], r[97], r[98], r[99], r[100], r[101], r[102]))  # noqa
# for i in range(17, 103):
#     print("r[%d], "  % i, end='', flush=True)
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
# genres = (["Action", "Adventure", "Cars", "Comedy", "Dementia",
#            "Demons", "Drama", "Ecchi", "Fantasy", "Game",
#            "Harem", "Hentai", "Historical", "Horror", "Josei",
#            "Kids", "Magic", "Martial Arts", "Mecha", "Military",
#            "Music", "Mystery", "Parody", "Police", "Psychological",
#            "Romance", "Samurai", "School", "Sci-Fi", "Seinen",
#            "Shoujo", "Shoujo Ai", "Shounen", "Shounen Ai", "Slice of Life",
#            "Space", "Sports", "Super Power", "Supernatural", "Thriller",
#            "Vampire", "Yaoi", "Yuri"])
# watched = [0]*len(genres)
# score = [0]*len(genres)
# with open("./ourUserList.csv", "rt", encoding='ISO-8859-1') as userList,  open("./ourUserAnimeList.csv", "rt", encoding='ISO-8859-1') as userAnimeList,  open("./ourAnimeList.csv", "rt", encoding='ISO-8859-1') as animeList:  # noqa
#     userListReader = csv.reader(userList)
#     userAnimeListReader = csv.reader(userAnimeList)
#     animeListReader = csv.reader(animeList)
#     with open("./smallUserList_genres.csv", "w", newline='', errors='replace') as result:  # noqa
#         writer = csv.writer(result)
#         row1 = next(userListReader)  # get the first row
#         # create new array that holds all the string values for the new columns
#         genreWatchedScored = [""]*(2*len(genres))
#         for i in range(len(genres)):
#             genreWatchedScored[2*i] = genres[i] + "_Watched"
#             genreWatchedScored[(2*i)+1] = genres[i] + "_Scored"
#         # append all the new columns to the row
#         for newCol in genreWatchedScored:
#             row1.append(newCol)
#         writer.writerow(row1)
#         name = ""
#         userAnimeList.readline()  # skip the first line
#         for row in userAnimeListReader:
#             if row:
#                 if name != "" and name != row[0]:
#                     userList.seek(0)
#                     for rowToWrite in userListReader:
#                         if name == rowToWrite[0]:
#                             for i in range(len(genres)):
#                                 rowToWrite.append(watched[i])
#                                 rowToWrite.append(score[i])
#                             writer.writerow(rowToWrite)
#                     watched = [0]*len(genres)
#                     score = [0]*len(genres)
#                 name = row[0]
#                 animeID = row[1]
#                 animeScore = row[3]
#                 animeList.seek(0)
#                 for animeRow in animeListReader:
#                     if animeID == animeRow[0]:
#                         genreList = animeRow[14]
#                         for i in range(len(genres)):
#                             if genres[i] in genreList:
#                                 watched[i] += 1
#                                 score[i] += int(animeScore)
#         userList.seek(0)
#         for rowToWrite in userListReader:
#             if name == rowToWrite[0]:
#                 for i in range(len(genres)):
#                     rowToWrite.append(watched[i])
#                     rowToWrite.append(score[i])
#                 writer.writerow(rowToWrite)
