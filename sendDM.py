import requests
import json

class SendDM:
    token = ""
    default_url = "https://slack.com/api/"
    def __init__(self, token):
        self.token = token

    def getListOfUser(self):
        list = []
        r = requests.get(self.default_url + "users.list?token=" + self.token + "&pretty=1")

        dict = json.loads(r.text)
        for h in dict['members']:
            list.append((h['id'], h['name']))

        return list

    def makeUserListTxtFile(self, path):
        f = open(path, 'w')
        list = self.getListOfUser()
        for i in list:
            f.write(i[1])
            f.write("\t\n")

    def getChannelId(self, userID):
        r = requests.get(self.default_url + "im.open?token=" + self.token + "&user=" + userID + "&pretty=1")
        return json.loads(r.text)['channel']['id']

    def sendDMToAll(self, path):
        f = open(path, 'r')
        list = self.getListOfUser()
        while(1):
            line = f.readline()
            print(line)
            if not line: break
            line = line.split('\t')
            index = -1
            for i in list:
                if line[0] == i[1]:
                    index = list.index(i)
                    break

            if index > 0:
                message = line[1]
                id = list[index][0]

                channelid = self.getChannelId(id)
                r = requests.get(self.default_url + "chat.postMessage?token=" + self.token + "&channel=" + channelid + "&text=" + message + "&pretty=1")



file_path = "/Users/cho/Desktop/q.txt"

dm = SendDM("<token>")
# dm.makeUserListTxtFile(file_path)
dm.sendDMToAll(file_path)