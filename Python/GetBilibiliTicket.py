import json
import os
import random
import requests
import time


def get_buyer_info(headers):
    url = "https://show.bilibili.com/api/ticket/buyer/list"
    response = requests.get(url, headers=headers)
    print(response.json())
    buyer_infos = response.json()["data"]["list"]
    buyer_info = [buyer_infos[0]]
    for i in range(len(buyer_infos)):
        print(
            "["
            + str(i)
            + "] "
            + buyer_infos[i]["name"]
            + " "
            + buyer_infos[i]["personal_id"]
            + " "
            + buyer_infos[i]["tel"]
        )
        if buyer_infos[i]["is_default"] == 1:
            buyer_info = [buyer_infos[i]]
    print("[INFO] 请选择购票人，默认" + buyer_info[0]["name"])
    buyer_id = "0"
    if buyer_id != "":
        buyer_info = [buyer_infos[int(buyer_id)]]
    return json.dumps(buyer_info)


def get_prepare(screen_id, sku_id, project_id):
    global headers
    url = "https://show.bilibili.com/api/ticket/order/prepare?project_id=" + project_id
    data = {
        "project_id": project_id,
        "screen_id": screen_id,
        "order_type": "1",
        "count": "1",
        "sku_id": sku_id,
        "token": "",
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json()["data"]


def create_order(screen_id, sku_id, token, deviceId, project_id, pay_money):
    global headers
    url = "https://show.bilibili.com/api/ticket/order/createV2?project_id=" + project_id
    x = str(1223 + random.randint(0, 10) - 5)
    y = str(653 + random.randint(0, 10) - 5)
    data = {
        "project_id": project_id,
        "screen_id": screen_id,
        "sku_id": sku_id,
        "count": "1",
        "pay_money": pay_money,
        "order_type": "1",
        "timestamp": str(int(time.time() * 1000)),
        "buyer_info": buyer_info,
        "token": token,
        "deviceId": deviceId,
        "clickPosition": '{"x":'
                         + x
                         + '"y":'
                         + y
                         + '"origin": '
                         + str(int(time.time() * 1000) - random.randint(1, 100))
                         + ',"now": '
                         + str(int(time.time() * 1000))
                         + "}",
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json()


def get_token(screen_id, sku_id, project_id):
    info = get_prepare(screen_id, sku_id, project_id)
    print(info)
    if info["shield"]["open"] == 0:
        print(
            "[SUCCESS] 成功准备订单"
            + "https://show.bilibili.com/platform/confirmOrder.html?token="
            + info["token"]
        )
        return info["token"]
    else:
        print("[INFO] 触发风控，打开：" + str(info["shield"]))
        os.system("start " + info["shield"]["naUrl"])
        print("[INFO] 请手动完成验证")
        pause = input("完成验证后，按回车继续")
        return get_token(screen_id, sku_id, project_id)


if __name__ == "__main__":
    project_id = "73710"
    pay_money = 12800
    deviceId = ""
    cookie = input("请输入cookie：")
    headers = {
        "Host": "show.bilibili.com",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "Accept": "*/*",
        "Origin": "https://show.bilibili.com",
        # "X-Risk-Header": "platform/pc uid/123456 deviceId/AAAAAAAA-BBBB-CCCC-DDDD-123456789aabbccddinfoc",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 ",
    }
    screen_id = "134761"
    sku_id = "398585"
    buyer_info = get_buyer_info(headers)

    token = get_token(screen_id, sku_id, project_id)
    print("[INFO] 开始下单")
    while 1:
        result = create_order(screen_id, sku_id, token, deviceId, project_id, pay_money)
        if result["errno"] == 100009:
            print(".", end="", flush=True)
        elif result["errno"] == 100001:
            print("[ERROR] 触发风控，等待0.2s")
            # time.sleep(2)
        elif result["errno"] == 0:
            print("[SUCCESS] 成功下单，锁票成功！请在5分钟内完成支付操作")
            pay_token = result["data"]["token"]
            print("[INFO] 请打开链接或在手机上完成支付")
            os.system("start https://show.bilibili.com/orderlist")
            exit()
        elif result["errno"] == 100051:
            token = get_token(screen_id, sku_id, project_id)
        else:
            print("[ERROR] " + str(result))
        time.sleep(1)
