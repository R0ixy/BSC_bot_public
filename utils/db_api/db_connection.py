import pymongo
from data import config


class DBCommands:
    col = pymongo.MongoClient(
        f'mongodb+srv://{config.DB_USER}:{config.DB_PASSWORD}@walletsdb.cmac1.mongodb.net/walletsdb?retryWrites=true&w=majority') \
        .walletsdb.users

    async def get_wallet(self, user_id):
        try:
            return self.col.find_one({'_id': user_id})['wallet']
        except TypeError:
            return None

    async def get_id(self, wallet):
        return self.col.find_one({'wallet': wallet})['_id']

    async def insert_wallet(self, user_id, wallet):
        self.col.insert_one({"_id": user_id,
                             "wallet": wallet.lower()
                             })

    async def update_wallet(self, user_id, wallet):
        self.col.update_one({"_id": user_id},
                            {'$set': {"wallet": wallet.lower()}
                             })

    async def delete(self, user_id):
        self.col.delete_one({"_id": user_id})

    def get_all(self):
        data = []
        for i in self.col.find():
            data.append(i['wallet'])
        return data

    async def get_all_id(self):
        data = []
        for i in self.col.find():
            data.append(i['_id'])
        return data
