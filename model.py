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
		self.currentVal = 0
		self.userListDict = {}
		self.animeListDict = {}
		self.userAnimeListDict = {}
		with open("./ourUserListGenres.csv", "rt", encoding='ISO-8859-1') as userList,  open("./ourUserAnimeList.csv", "rt", encoding='ISO-8859-1') as userAnimeList,  open("./ourExtendedAnimeList.csv", "rt", encoding='ISO-8859-1') as animeList: 
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
				self.animeListDict[row[0]] = np.array(row[20:]).astype(float)

			# this is just to not read in all the data so I can debug/code
			c = 0
			# first list is id, second is scores
			for row in userAnimeListReader:
				if c == 10000:
					break
				c = c + 1
				# change scores to 0 or 1
				# like = 0 if int(row[3]) <= 5 else 1
				# leave as is for now
				like = int(row[3])
				if row[0] in self.userAnimeListDict:
					self.userAnimeListDict[row[0]][0] = self.userAnimeListDict[row[0]][0] + [row[1]]
					self.userAnimeListDict[row[0]][1] = self.userAnimeListDict[row[0]][1] + [like]
				else:
					self.userAnimeListDict[row[0]] = [[row[1]],[like]]

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

	def getNNNeighbors(self, trialkey, N):
		target_features = self.userListDict[trialkey];

		keys = []
		similarity = []
		for key in self.train_keys:
			keys.append(key)
			features = self.userListDict[key]
			s = np.dot(target_features,features)/(np.linalg.norm(target_features)*np.linalg.norm(features))
			if s == np.inf or s == np.nan:
				s = -1;
			# Need some sort of way to account for magnitude. More shows is better
			# s = n*s
			similarity.append(s)

		similarity = np.array(similarity)
		keys = np.array(keys)

		idx = np.argpartition(-1*similarity, N)
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
			animeScore.append([userAnime[1][idx]])
		return animeInfo, animeScore

	def __iter__(self):
		return iter(self.val_keys)

	def next(self):
		if self.currentVal >= self.valSize:
			raise StopIteration
		else:
			self.currentVal += 1
			return self.val_keys[self.currentVal-1]

# NOT SURE IF THIS WORKS YET
class ForestClassifier:
	def __init__(self,dataReader,valkey):
		self.dataReader = dataReader
		self.valkey = valkey
		self.valAnimeInfo, self.valAnimeScore = self.dataReader.getUserAnime(self.valkey)
		
		NNNKeys = self.dataReader.getNNNeighbors(self.valkey,10)
		self.trees = []
		for neighbor_key, neighbor_similarity in NNNKeys:
			animeInfo, animeGT = self.dataReader.getUserAnime(neighbor_key)
			clf = tree.DecisionTreeClassifier()
			clf = clf.fit(animeInfo,animeGT)
			self.trees = self.trees.append(clf)

	def classify(self):
		predictions = [tree.predict([self.valAnimeInfo]) for tree in trees]
		# how do I merge the results
		# majority vote?
		prediction = max(set(predictions),key=predictions.count)
		# return both the prediction and the ground truth
		return prediction, self.valAnimeScore

print('initializing reader object')
dataReader = myDataReader(.2)
print('done with reader object')

# NOTE: not sure if forestclassifier even runs right now
# accuracies = []
# for valkey in dataReader:
# 	classifier = ForestClassifier(dataReader,valkey)
# 	pred,actual = classifier.classify()
# 	accuracies.append(np.sum(np.equal(pred,actual)))