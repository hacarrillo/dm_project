import csv

userListArray = {}
userAnimeListArray = {}
animeListArray = {}
with open("./ourUserListGenres.csv", "rt", encoding='ISO-8859-1') as userList,  open("./ourUserAnimeList.csv", "rt", encoding='ISO-8859-1') as userAnimeList,  open("./ourExtendedAnimeList.csv", "rt", encoding='ISO-8859-1') as animeList:  # noqa
    userListReader = csv.reader(userList)
    userAnimeListReader = csv.reader(userAnimeList)
    animeListReader = csv.reader(animeList)
    userAnimeList.readline();
    userList.readline();
    animeList.readline();
    c = 0
    for row in userListReader:
        if c == 10000:
            break
        userListArray[row[0]] = row
        c = c + 1
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
        if c == 1000000:
            break

with open("./smallUserList_genres.csv", "w", newline='', errors='replace') as result, open("./smallUserAnimeList.csv", "w", newline='', errors='replace') as result1 :  # noqa
    userList = open("./ourUserListGenres.csv","rt", encoding='ISO-8859-1')
    userAnimeList = open("./ourUserAnimeList.csv","rt", encoding='ISO-8859-1')
    userListReader = csv.reader(userList)
    userAnimeListReader = csv.reader(userAnimeList)

    userwriter = csv.writer(result)
    useranimewriter = csv.writer(result1)

    row1 = next(userListReader) 
    userwriter.writerow(row1)
    row1 = next(userAnimeListReader)
    useranimewriter.writerow(row1)
    for ul in userListArray:
        if ul in userAnimeListArray:
            useranime = userAnimeListArray[ul]
            for anime in useranime:
                useranimewriter.writerow(anime)
        rowToWrite = userListArray[ul]
        userwriter.writerow(rowToWrite)