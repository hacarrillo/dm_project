'''
Author: Hector Alexis Carrillo Cabada

Finds N nearest neighbors to a user and creates N trees from neighbors.
Trees are then used to "vote" on whether the user will like an anime or not. 

TODO:
	Check that ForestClassifier class works
		Do I need to convert features to floats?

	Similarity:
		Maybe also measure overlap in shows watched?
		Is there a way to account for user that watch more shows? (maybe square similarity, multiply by norm)
	More Anime Features?
		Maybe use some of the other features such as source, type, rating, studio
		Does the classifier work with floats and strings?
'''

import csv
import numpy as np
from sklearn import tree

# This class runs. Might need debugging though
class myDataReader:
	def __init__(self,train_percent):
		np.random.seed(0)
		self.currentVal = 0
		self.userListDict = {}
		self.animeListDict = {}
		self.userAnimeListDict = {}
		self.userAnimeID = {}
		# turn paths into input for object
		with open("./mediumUserListGenres.csv", "rt", encoding='ISO-8859-1') as userList,  open("./mediumUserAnimeList.csv", "rt", encoding='ISO-8859-1') as userAnimeList,  open("./ourExtendedAnimeList.csv", "rt", encoding='ISO-8859-1') as animeList: 
			userListReader = csv.reader(userList)
			animeListReader = csv.reader(animeList)
			userAnimeListReader = csv.reader(userAnimeList)

			userAnimeList.readline()
			userList.readline()
			animeList.readline()

			# might need to rethink these features (keep only total sum scores then normalize or keep both and normalize independently)
			for row in userListReader:
				f = np.array(row[17:]).astype(float)
				f_watched = f[0::2]
				f_rated = f[1::2]
				f_watched = np.array(f_watched)
				# to avoid division by zero,set zeros to 1
				idx = f_watched == 0
				f_watched[idx] = 1

				f_rated =  np.divide(f_rated,f_watched)

				# normalize so long as there are values (if max == 0 all values are 0 and we dont normalize these)
				# set 0s back to 1
				f_watched[idx] = 0
				if max(f_rated) != 0:
					f_rated = np.divide(f_rated - min(f_rated),max(f_rated)-min(f_rated))
				if max(f_watched) != 0:
					f_watched = np.divide(f_watched - min(f_watched),max(f_watched)-min(f_watched))
				self.userListDict[row[0]] = np.append(f_rated,f_watched)

			# duration,score,age,scored_by_log,members_log,favorites_log,genres
			for row in animeListReader:
				for i in range(len(row)):
					if row[i] == "Unknown":
						row[i] = -1
				self.animeListDict[row[0]] = np.array(row[26:]).astype(float)

			# first list is id, second is scores
			for row in userAnimeListReader:
				# change scores to 0 or 1
				# like = 0 if int(row[3]) <= 5 else 1
				# leave as is for now
				like = int(row[3])
				like = 0 if int(row[3]) <= 7 else 1
				if row[0] in self.userAnimeListDict:
					self.userAnimeListDict[row[0]][0] = self.userAnimeListDict[row[0]][0] + [row[1]]
					self.userAnimeListDict[row[0]][1] = self.userAnimeListDict[row[0]][1] + [like]
				else:
					self.userAnimeListDict[row[0]] = [[row[1]],[like]]

				if row[0] in self.userAnimeID:
					self.userAnimeID[row[0]] = self.userAnimeID[row[0]] + [int(row[1])]
				else:
					# print(row[0])
					self.userAnimeID[row[0]] = [int(row[1])]

			train_indices = np.random.choice(len(self.userListDict),int(len(self.userListDict)*train_percent))

			self.train_keys = []
			self.val_keys = []

			c = 0
			for key in self.userListDict:
				if c in train_indices:
					self.train_keys.append(key)
				else:
					self.val_keys.append(key)
				c = c + 1
			self.valSize = len(self.val_keys)

	def getNNNeighborsAnime(self, trialkey, N, animeID):
		target_features = self.userListDict[trialkey];

		keys = []
		similarity = []
		contains_show = []
		for key in self.train_keys:
			keys.append(key)
			features = self.userListDict[key]
			s = np.dot(target_features,features)/(np.linalg.norm(target_features)*np.linalg.norm(features))
			if s == np.inf or s == np.nan:
				s = -1;

			# Need some sort of way to account for magnitude. More shows is better
			# s = n*s
			contains = False
			if key in self.userAnimeListDict and animeID in self.userAnimeListDict[key][0]:
				contains = True
			contains_show.append(contains)
			similarity.append(s)

		similarity = np.array(similarity)
		keys = np.array(keys)
		# contains_show = np.array(contains_show)

		similarity = similarity[contains_show]
		keys = keys[contains_show]

		# print(N)
		# print(np.size(similarity))
		total_users = min(N,np.size(similarity))

		idx = np.argpartition(-1*similarity, total_users-1)
		idx = idx[:total_users]
		keys = keys[idx]
		similarity = similarity[idx]
		key_pairs = list(zip(keys,similarity))	

		return key_pairs

	def getNNNeighbors(self, trialkey, N):
		target_features = self.userListDict[trialkey]
		binary_target_features = self.userAnimeID[trialkey]

		keys = []
		similarity = []
		for key in self.train_keys:
			features = self.userListDict[key]
			if key in self.userAnimeID:
				keys.append(key)
				binary_features = self.userAnimeID[key]
			else:
				continue

			intersection = sum(np.isin(binary_features,binary_target_features))
			union = np.size(binary_features) + np.size(binary_target_features) - intersection

			if union == 0:
				su = 1
			else:
				su = 1 - intersection/union

			s = np.dot(target_features,features)/(np.linalg.norm(target_features)*np.linalg.norm(features))
			if s == np.inf or s == np.nan:
				s = -1;

			s = (s+1)/2

			similarity.append(su)

		print(min(similarity))
		print(max(similarity))
		similarity = np.array(similarity)
		keys = np.array(keys)
		# contains_show = np.array(contains_show)

		# idx = np.argpartition(-1*similarity, N)
		idx = np.argpartition(similarity, N)
		idx = idx[:N]
		keys = keys[idx]
		similarity = similarity[idx]
		key_pairs = list(zip(keys,similarity))	

		return key_pairs

	def getUserAnime(self, userkey):
		userAnime = self.userAnimeListDict[userkey]
		totalAnime = len(userAnime[0])
		animeInfo = []
		animeScore = []
		for idx in range(totalAnime):
			animeInfo.append(self.animeListDict[userAnime[0][idx]])
			animeScore.append(userAnime[1][idx])
		return animeInfo, animeScore

	def containsAnime(self, userkey, animeID):
		userAnime = self.userAnimeListDict[userkey]
		totalAnime = len(userAnime[0])
		for idx in range(totalAnime):
			if userAnime[0][idx] == animeID:
				return True
		return False

	def makeFilter(self, animeID):
		def myFilter(key):
			return self.containsAnime(key[0], animeID)
		return myFilter

	def getUserAnimeScore(self, userkey, animeID):
		userAnime = self.userAnimeListDict[userkey]
		totalAnime = len(userAnime[0])
		for idx in range(totalAnime):
			if userAnime[0][idx] == animeID:
				return userAnime[1][idx]

	def __iter__(self):
		return iter(self.val_keys)

	def next(self):
		if self.currentVal >= self.valSize:
			raise StopIteration
		else:
			self.currentVal += 1
			return self.val_keys[self.currentVal-1]

class ForestClassifier:
	def __init__(self,dataReader,valkey,N):
		self.dataReader = dataReader
		self.valkey = valkey
		self.valAnimeInfo, self.valAnimeScore = self.dataReader.getUserAnime(self.valkey)
		self.N = N
		self.valAnimeInfo = np.array(self.valAnimeInfo)
		self.valAnimeScore = np.array(self.valAnimeScore)

		self.NNNKeys = self.dataReader.getNNNeighbors(self.valkey,self.N)

		self.trees = []
		for neighbor_key, neighbor_similarity in self.NNNKeys:
			animeInfo, animeGT = self.dataReader.getUserAnime(neighbor_key)
			clf = tree.DecisionTreeClassifier()
			mytree = clf.fit(animeInfo,animeGT)
			self.trees.append(mytree)

	def classify(self):
		predictions = [tree.predict(self.valAnimeInfo) for tree in self.trees]
		predictions = np.array(predictions)

		# how do I merge the results
		# majority vote?
		s = np.shape(predictions)
		totalAnime = s[1]

		consensus = []
		for i in range(totalAnime):
			tmp = np.unique(predictions[:,i],return_counts=True)
			counts = tmp[1]
			scores = tmp[0]
			idx = np.argmax(counts)
			consensus.append(scores[idx])

		# prediction = [max(set(predictions[:,i]),key=count) for i in range(totalAnime)]
		# return both the prediction and the ground truth
		return consensus, self.valAnimeScore

class FilterClassifier:
	def __init__(self,dataReader,valkey,N):
		self.dataReader = dataReader
		self.valkey = valkey
		self.valAnimeInfo, self.valAnimeScore = self.dataReader.getUserAnime(self.valkey)
		self.N = N
		self.valAnimeInfo = np.array(self.valAnimeInfo)
		self.valAnimeScore = np.array(self.valAnimeScore)

		self.NNNKeys = self.dataReader.getNNNeighbors(self.valkey,self.N*20)
		self.NNNKeys = np.array(self.NNNKeys)
		# print(self.NNNKeys)

	def classify(self):
		self.animeids = self.dataReader.userAnimeListDict[self.valkey][0]
		consensus = []
		for anime_id in self.animeids:
			# self.NNNKeys = self.dataReader.getNNNeighborsAnime(self.valkey,self.N,anime_id)
			# idx = [key if self.dataReader.containsAnime(key,anime_id) for key in self.NNNKeys]
			myFilterFunc = self.dataReader.makeFilter(anime_id)
			filteredKeys = list(filter(myFilterFunc,self.NNNKeys))
			scores = []
			for neighbor_key, neighbor_similarity in filteredKeys:
				scores.append(self.dataReader.getUserAnimeScore(neighbor_key,anime_id))
			# print(scores)
			# print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=")
			tmp = np.unique(scores,return_counts=True)
			if np.size(tmp[0]) == 0:
				consensus.append(0)
			else:
				counts = tmp[1]
				scores = tmp[0]
				idx = np.argmax(counts)
				consensus.append(scores[idx])
		return consensus, self.valAnimeScore

print('initializing reader object')
dataReader = myDataReader(.2)
print('done with reader object')

# valkey = dataReader.next()
# classifier = ForestClassifier(dataReader,valkey,4)
# pred,actual = classifier.classify()
# totalAnime = len(pred)
# print(np.sum(np.equal(pred,actual))/totalAnime)

correct = []
total = 0
for idx, valkey in enumerate(dataReader):
	if idx == 100:
		break
	# try:
	print('-------------------------------------------------------------')
	classifier = FilterClassifier(dataReader,valkey,11)
	pred,actual = classifier.classify()
	# print(list(zip(actual,pred)))
	totalAnime = len(pred)
	print("1 prob actual {}".format(sum(actual)/totalAnime))
	print("1 prob pred {}".format(sum(pred)/totalAnime))
	total = total + totalAnime
	# print('Ground Truth/ Prediction = {}'.format(list(zip(actual,pred))))
	print('Total Anime = {}'.format(totalAnime))
	correct.append(np.sum(np.equal(pred,actual)))
	print('Accuracy = {}'.format(np.sum(np.equal(pred,actual))/totalAnime))
	# except:
	# 	print("++++++++++++++++++++VALKEY NOT FOUND: {}++++++++++++++++++++++++++++".format(valkey))

print("AVERAGE ACCURACY PER ANIME")
print(sum(correct)/total)