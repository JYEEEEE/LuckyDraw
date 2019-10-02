import pymongo

mongo_client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
db = mongo_client['LuckyDraw']    # use LuckyDraw  抽奖数据库
users_info = db.users_info        # use users_info 用户信息集合


def user_info_search(login_name,nick_name,login_pass):
    """
    用户检索
    """
    login_name_result = users_info.find_one({'login_name':login_name})
    nick_name_result = users_info.find_one({'nick_name': nick_name})
    login_pass_result = users_info.find_one({'login_pass': login_pass})

    return login_name_result,nick_name_result,login_pass_result



