# -*- coding: utf-8 -*-
# @Time: 2023/2/18 22:07
# @FileName: biliintl.py
# @Software: PyCharm
# @GitHub: KimmyXYC
import asyncio
import aiohttp
from aiohttp import ClientConnectorError
from loguru import logger
from pyrogram.types import InlineKeyboardButton


def get_requests(json_data):
    return json_data["code"] == 0 and not json_data["result"]["limit"]


# collector section
async def fetch_biliintl(collector, session: aiohttp.ClientSession, proxy=None, reconnection=2):
    """
    biliintl解锁测试
    :param collector:
    :param reconnection:
    :param session:
    :param proxy:
    :return:
    """
    link = "https://api.bilibili.tv/intl/gateway/v2/ogv/view/app/season?season_id={}&s_locale=zh_SG&mobi_app=bstar_a&build=1080003"
    try:
        res = await session.get(link.format(1006275), proxy=proxy, timeout=5)
        link_click = get_requests(await res.json())
        if link_click:
            res = await session.get(link.format(1048837), proxy=proxy, timeout=5)
            spy_family = get_requests(await res.json())
            if spy_family:
                res = await session.get(link.format(1057120), proxy=proxy, timeout=5)
                spy_family_th = get_requests(await res.json())

                res = await session.get(link.format(1057175), proxy=proxy, timeout=5)
                spy_family_vn = get_requests(await res.json())

                res = await session.get(link.format(1057318), proxy=proxy, timeout=5)
                spy_family_id = get_requests(await res.json())

                if spy_family_th:
                    collector.info['biliintl'] = "解锁(泰国)"
                elif spy_family_vn:
                    collector.info['biliintl'] = "解锁(越南)"
                elif spy_family_id:
                    collector.info['biliintl'] = "解锁(印尼)"
                else:
                    collector.info['biliintl'] = "解锁(东南亚)"
            else:
                collector.info['biliintl'] = "仅限国创"
        else:
            collector.info['biliintl'] = "失败"
    except ClientConnectorError as c:
        logger.warning("biliintl请求发生错误:" + str(c))
        if reconnection != 0:
            await fetch_biliintl(collector, session=session, proxy=proxy, reconnection=reconnection - 1)
    except asyncio.exceptions.TimeoutError:
        logger.warning("biliintl请求超时，正在重新发送请求......")
        if reconnection != 0:
            await fetch_biliintl(collector, session=session, proxy=proxy, reconnection=reconnection - 1)


def task(Collector, session, proxy):
    return asyncio.create_task(fetch_biliintl(Collector, session, proxy=proxy))


# cleaner section
def get_biliintl_info(self):
    """

        :return: str: 解锁信息: [解锁(东南亚)、解锁(泰国)、解锁(越南)、解锁(印尼)、仅限国创、失败、N/A]
        """
    try:
        if 'biliintl' not in self.data:
            logger.warning("采集器内无数据: biliintl")
            return "N/A"
        else:
            try:
                info = self.data['biliintl']
                if info is None:
                    logger.warning("无法读取biliintl解锁信息")
                    return "N/A"
                else:
                    logger.info("biliintl情况: " + info)
                    return info
            except KeyError:
                logger.warning("无法读取biliintl解锁信息")
                return "N/A"
    except Exception as e:
        logger.error(e)
        return "N/A"


SCRIPT = {
    "MYNAME": "Biliintl",
    "TASK": task,
    "GET": get_biliintl_info
}

# bot_setting_board

button = InlineKeyboardButton("✅Biliintl", callback_data='✅Biliintl')

if __name__ == "__main__":
    "this is a test demo"
    import sys
    import os

    os.chdir(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
    sys.path.append(os.path.abspath(os.path.join(os.getcwd(), os.pardir, os.pardir)))
    from libs.collector import Collector as CL, media_items

    media_items.clear()
    media_items.append("Biliintl")
    cl = CL()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(cl.start(proxy="http://127.0.0.1:1111"))
    print(cl.info)
