import json
from scipy.cluster.hierarchy import linkage
from scipy.cluster.hierarchy import dendrogram
from sklearn import cluster
import matplotlib.pyplot as plt


# open text file with friends of followers of Hillary Clinton
# open text file with followers of Jimmy Fallon
# can do with all users
with open("HCFollowerFriends.txt", "r") as f:
    friends_txt = f.read()

# change to list of dicts, json format
friends_txt = friends_txt.replace('{', '{"')
friends_txt = friends_txt.replace('}', '},')
friends_txt = friends_txt.replace(':', '":')
friends_txt = '[' + friends_txt + ']'
friends_txt = friends_txt.replace('},]', '}]')

friends = json.loads(friends_txt)
friends = friends[:1000]

# list of followers
keys = []
for i in friends:
    keys.append(list(i.keys())[0])

# number of followers - want 1000 followers
num = 1000

# store correlations between followers' friends
matrix = [[0 for i in range(num)] for j in range(num)]
for i in range(num):
    for j in range(num):
        # similarity: union(fr(1), fr(2))/(# fr(1) + # fr(2))/2
        union = 0
        for a in list(friends[i].values())[0]:
            for b in list(friends[j].values())[0]:
                if a == b:
                    union = union + 1
        matrix[i][j] = union/(len(friends[i].values()) + len(friends[j].values()))/2

        # i = j, similarity is 0
        if i == j:
            matrix[i][j] = 0
print(matrix)
# # Hierarchical Clustering algorithm
Z = linkage(matrix, 'single', 'correlation')
plt.figure()
plot = dendrogram(Z, labels=range(num))
plt.title("Hierarchical Clustering of Followers of Hillary Clinton")
plt.show()