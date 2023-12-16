# -*- coding: utf-8 -*-
# @Time: 2023/12/16 19:14 
# @FileName: faq.py
# @Software: PyCharm
# @GitHub: KimmyXYC
import base64
from asyncio import sleep

from pagermaid.listener import listener
from pagermaid.enums import Client, Message

pip_install("aiohttp")

import aiohttp


@listener(command="faq", description="伪造语录")
async def fake_quote(bot: Client, message: Message):
    QUOTLY_API: str = 'https://bot.lyo.su/quote/generate'
    json_data = {
        "type": "quote",
        "format": "png",
        "backgroundColor": "#1b1429",
        "width": 768,
        "height": 768,
        "scale": 2.5,
        "messages": []
    }
    text = message.text.split(' ', 1)
    if len(text) > 1:
        cmd = text[0]
        text = ''.join(text[1:]).strip()
    else:
        cmd = text[0]
        text = ''
    opt = [x.strip() for x in text.split(' ') if x]
    if not message.reply_to_message:
        return await message.edit("你需要回复一条消息或者输入一串字符。")
    if not opt:
        return await message.edit("未指定内容, 无法生成")
    else:
        reply = message.reply_to_message

        sid, title, name = await forward_info(reply)
        messages_json = {
            "entities": [],
            "avatar": True,
            "from": {
                "id": sid,
                "language_code": "zh",
                "title": title,
                "name": name
            },
            "text": opt[0]
        }
        # Add the new message to the 'messages' array
        json_data["messages"].append(messages_json)

        # Convert the updated data back to JSON
        # updated_json = json.dumps(json_data, indent=4)

        await message.edit('等待Lyosu语录生成返回结果...')
        async with aiohttp.ClientSession() as session:
            async with session.post(QUOTLY_API, json=json_data) as resp:
                req = await resp.json()
                if req['ok']:
                    try:
                        buffer = base64.b64decode(req['result']['image'].encode('utf-8'))
                        with open('Quotly.webp', 'wb') as out_file:
                            out_file.write(buffer)
                        await message.edit("已在Lyosu生成并保存语录, 正在上传中...")
                        await message.reply_document('Quotly.webp', force_document=False, reply_to_message_id=reply.id)
                        await message.safe_delete()
                    except:
                        await message.edit("请求成功但出现错误")
                        await sleep(3)
                        await message.safe_delete()
                    return
                else:
                    return await message.edit("请求出现错误")


async def forward_info(reply):
    # 判断转发来源
    # 转发自频道
    if reply.forward_from_chat:
        sid = reply.forward_from_chat.id
        title = reply.forward_from_chat.title
        name = title
    # 转发自用户或机器人
    elif reply.forward_from:
        sid = reply.forward_from.id
        try:
            try:
                name = first_name = reply.forward_from.first_name
            except TypeError:
                name = '死号'
            if reply.forward_from.last_name:
                last_name = reply.forward_from.last_name
                name = f'{first_name} {last_name}'
        except AttributeError:
            pass
        title = name
    # 拒绝查看转发消息来源时
    elif reply.forward_sender_name:
        title = name = sender_name = reply.forward_sender_name
        sid = 0
    # 不是转发的消息
    elif reply.from_user:
        try:
            sid = reply.from_user.id
            try:
                name = first_name = reply.from_user.first_name
            except TypeError:
                name = '死号'
            if reply.from_user.last_name:
                last_name = reply.from_user.last_name
                name = f'{first_name} {last_name}'
        except AttributeError:
            pass
        title = name
    return sid, title, name
