#! /usr/bin/python

"""
@author: yan.zhao
@contact: zhaoyanz405@gmail.com
@time: 2019/10/14 16:54
"""
from bson import ObjectId

from backend import decorators
from tornado.web import RequestHandler

from backend.redpkt.enums import KEY_LOTTERY_FLAG
from database.models import User, RedPacketRule


class AppletLotteryLaunch(RequestHandler):
    """
    请求一次抽奖
    """

    @decorators.render_json
    async def post(self):
        r_dict = {'code': 0, 'reward_msg': ''}
        user_id = self.get_argument('user_id')
        rule_id = self.get_argument('rule_id')

        if not user_id or not rule_id:
            r_dict['code'] = 1001
            return r_dict
        else:
            user_id = ObjectId(user_id)
            rule_id = ObjectId(rule_id)

        user = await User.find_one({'_id': user_id})
        if not user:
            r_dict['code'] = 1002
            return r_dict

        try:
            rule = await RedPacketRule.find_one({'_id': rule_id})

            cache_key = KEY_LOTTERY_FLAG + rule_id
            flag = await RedisCache.hget(cache_key, member.cid)
            try:
                if flag:
                    flag = flag.decode('utf-8')
                else:
                    raise AttributeError

                try:
                    flag = int(flag)
                except ValueError:
                    pass

                if flag == 0:
                    r_dict['code'] = 1000
                    r_dict['result'] = RESULT_RACE_LOTTERY_LOSE
                    redpkt_rule = await RedPacketRule.get_by_cid(checkpoint.redpkt_rule_cid)
                    r_dict['reward_msg'] = redpkt_rule.fail_msg
                    r_dict['reward_position'] = err_index
                    await clear_lottery_notice(member.cid, checkpoint_cid)
                    return r_dict
                else:
                    award = await RedPacketAward.get_by_cid(flag)
                    r_dict['code'] = 1000
                    r_dict['reward_msg'] = award.win_msg
                    r_dict['result'] = RESULT_RACE_LOTTERY_WIN
                    r_dict['reward_position'] = prize_list.index(award.title)
                    await add_notice(member_cid=member.cid, race_cid=history.race_cid,
                                     checkpoint_cid=history.checkpoint_cid,
                                     award_msg=award.win_msg, msg_type=TYPE_MSG_DRAW)
                    return r_dict
            except AttributeError:
                history = await RedPacketLotteryHistory.find_one(
                    {'checkpoint_cid': checkpoint_cid, 'member_cid': member.cid})
                if history:
                    award = await RedPacketAward.get_by_cid(history.award_cid)
                    if award:
                        r_dict['code'] = 1000
                        r_dict['reward_msg'] = award.win_msg
                        r_dict['result'] = RESULT_RACE_LOTTERY_WIN
                        r_dict['reward_position'] = prize_list.index(award.title)
                        await add_notice(member_cid=member.cid, race_cid=history.race_cid,
                                         checkpoint_cid=history.checkpoint_cid,
                                         award_msg=award.win_msg, msg_type=TYPE_MSG_DRAW)
                        return r_dict
                    else:
                        r_dict['code'] = 1000
                        r_dict['reward_msg'] = '很遗憾，你没有中奖!'
                        r_dict['result'] = RESULT_RACE_LOTTERY_LOSE
                        await clear_lottery_notice(member.cid, checkpoint_cid)
                        return r_dict
                else:
                    # 后台任务处理中请稍后再试
                    if await RedisCache.hget(KEY_RACE_LOTTERY_MEMBER_IN_PROCESS, member.cid):
                        r_dict['code'] = 1007
                        r_dict['reward_msg'] = '后台任务处理中请稍后再试'
                    else:
                        start_draw_redpacket.delay(member.cid, checkpoint.cid)
                        r_dict['code'] = 1008
                        r_dict['reward_msg'] = '抽奖中，请稍后再试。'
                    return r_dict

            async def deal_normal():
                start_lottery_queuing.delay(member.cid, race_cid, rule, checkpoint_cid)

            r_dict['code'] = 1000
            if rule.category == CATEGORY_REDPACKET_RULE_LOTTERY:
                await get_drew_result()

            if rule.category == CATEGORY_REDPACKET_RULE_DIRECT:
                await deal_normal()

        except Exception:
            logger.error(traceback.format_exc())

        return r_dict
