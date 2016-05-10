import oauth2 as oauth
import json
import time

# get keys for twitter access
with open('keys.json', 'r') as f:
    keys = json.load(f)

# number of keys
num_keys = len(keys['owner'])

# repeat for all followers

# open text file with followers of Jodi Picoult
with open('JodiPicoultFollowers.txt', 'r') as f:
    followers = json.load(f)

# file to store friend IDs of Jodi Picoult's followers
file = open('JPFollowerFriends.txt', 'w')

# current index in followers list
index = 0
# go through keys, make requests, wait 15 min in between
while True:
    # iterate through the keys
    for i in range(0, num_keys):
        conskey = keys['conskey'][i]
        consecret = keys['consecret'][i]
        token = keys['token'][i]
        tokensecret = keys['tokensecret'][i]
        owner = keys['owner'][i]
        ownerID = keys['ownerID'][i]

        consumer = oauth.Consumer(key=conskey, secret=consecret)
        access_token = oauth.Token(key=token, secret=tokensecret)
        client = oauth.Client(consumer, access_token)

        # can make 15 requests every 15 minutes per key
        for i in range(15):
            # break if at end of followers list
            if index == 2000:
                break

            id = followers[index]
            # get friends list
            friends = "https://api.twitter.com/1.1/friends/ids.json?user_id=" + str(id) + "&count=5000"
            response, data = client.request(friends)
            friend_list = json.loads(data.decode('utf-8'))
            f_list = {}

            # format = {userID : friends list}
            if 'ids' in friend_list:
                f_list[id] = friend_list['ids']
                file.write(str(f_list))

            index += 1

        # break if at end of followers list
        if index == 2000:
            break

    # break if at end of followers list
    if index == 2000:
        break

    # rests for 15 minutes
    time.sleep(900)