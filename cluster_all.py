import json
from scipy.cluster.hierarchy import linkage, fcluster, dendrogram
from sklearn.cluster import AffinityPropagation
import matplotlib.pyplot as plt
from itertools import cycle

# text files for 5 people points
text_files = ['AGFollowerFriends.txt', 'EEFollowerFriends.txt', 'HCFollowerFriends.txt',
              'JFFollowerFriends.txt', 'JPFollowerFriends.txt']

# text_files = ['JPFollowerFriends.txt']


users = []
for f in text_files:
    # open text file for friends of followers of 5 people
    with open(f, "r") as file:
        friends_txt = file.read()

    # change to list of dicts, json format
    friends_txt = friends_txt.replace('{', '{"')
    friends_txt = friends_txt.replace('}', '},')
    friends_txt = friends_txt.replace(':', '":')
    friends_txt = '[' + friends_txt + ']'
    friends_txt = friends_txt.replace('},]', '}]')

    # get 200 followers from each of 5 users
    friends = json.loads(friends_txt)
    friends = friends[-100:]
    users = users + friends

# number users
num = len(users)
print(num)
# number of clusters expected
n = 5

# store correlations between users' friends
matrix = [[0 for i in range(num)] for j in range(num)]
for i in range(num):
    for j in range(num):
        # similarity: union(fr(1), fr(2))/(# fr(1) + # fr(2))/2
        union = 0
        for a in list(users[i].values())[0]:
            for b in list(users[j].values())[0]:
                if a == b:
                    union = union + 1
        matrix[i][j] = union/(len(list(users[i].values())[0]) + len(list(users[j].values())[0]))/2
        # i = j, similarity is 0
        if i == j:
            matrix[i][j] = 0

# Hierarchical Clustering algorithm
Z = linkage(matrix, 'single', 'correlation')
plt.figure()
f1 = fcluster(Z, t=0.1, criterion='maxclust')
print(f1)
# with open('clusters.txt', 'w') as f:
#     f.write(f1)
plot = dendrogram(Z, leaf_rotation=90, leaf_font_size=8, count_sort=False, color_threshold = 0.3)
axes = plt.gca()
axes.set_ylim([0, 1])
x = range(50)
# my_xtiks = ['AG']*10 + ['EE']*10 + ['HC']*10 + ['JF']*10 + ['JP']*10
# print(my_xtiks)
# plt.xticks(x, my_xtiks)
plt.title("Hierarchical Clustering of Followers")
plt.show()
