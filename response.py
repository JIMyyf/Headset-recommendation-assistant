import re
import json

# 加载数据
with open('headphones.json', 'r', encoding='utf-8') as f:
    headphones_data = json.load(f)

with open('corpus.json', 'r', encoding='utf-8') as f:
    intents_data = json.load(f)

# 预加载所有耳机型号（用于快速匹配）
all_headphone_models = [
    hp['name'].lower() for hp in headphones_data['headphones']
]

# 初始化配置
comparison_keywords = ["不同", "区别", "比较", "差异", "对比"]
brand_aliases = {
    "苹果": "Apple",
    "索尼": "Sony",
    "airpods": "Apple",
    "wh-": "Sony",
    "wf-": "Sony"
}


def contains_headphone_model(user_input):
    """检查输入是否包含已知耳机型号"""
    input_lower = user_input.lower()
    return any(model in input_lower for model in all_headphone_models)


def recognize_intent(user_input):
    """增强版意图识别函数"""
    # 优先匹配包含已知型号的情况
    if contains_headphone_model(user_input):
        # 检查是否包含信息类关键词
        if re.search(r'(详细|信息|参数|介绍)', user_input):
            return 'ask_headphone_info'
        # 检查是否包含比较类关键词
        if any(keyword in user_input for keyword in comparison_keywords):
            return 'compare_headphones'

    # 比较意图检测
    if any(keyword in user_input for keyword in comparison_keywords):
        return 'compare_headphones'

    # 其他意图匹配
    for intent in intents_data['intents']:
        if intent['intent'] in ['ask_headphone_info', 'compare_headphones']:
            continue
        for example in intent['examples']:
            if re.search(example, user_input, re.IGNORECASE):
                return intent['intent']
    return 'unknown'


def handle_ask_headphone_info(user_input):
    """增强版耳机信息处理"""
    # 尝试直接匹配完整型号名称
    input_lower = user_input.lower()
    for hp in headphones_data['headphones']:
        if hp['name'].lower() in input_lower:
            return hp

    # 模糊匹配型号关键部分
    model_keywords = re.findall(r'[a-z0-9\-]+', input_lower)
    for hp in headphones_data['headphones']:
        hp_name = hp['name'].lower()
        if any(kw in hp_name for kw in model_keywords):
            return hp

    # 匹配品牌+型号片段
    brand_pattern = r'(苹果|Apple|索尼|Sony|AirPods|WH|WF)\s*[-\s]*([\w\s\-]+)'
    match = re.search(brand_pattern, input_lower, re.IGNORECASE)
    if match:
        brand_part = match.group(1)
        model_part = match.group(2).strip()
        # 标准化品牌
        brand = brand_aliases.get(brand_part.lower(), brand_part)
        if brand in ['airpods']:
            brand = 'Apple'
        # 构建查询名称
        search_name = f"{brand} {model_part}".strip()
        for hp in headphones_data['headphones']:
            if search_name.lower() in hp['name'].lower():
                return hp

    return None


def handle_compare_headphones(user_input):
    # 提取耳机名称
    potential_names = re.findall(r"[A-Za-z0-9\s-]+", user_input)
    valid_names = [
        name.strip() for name in potential_names if name.strip() in
        [hp['name'] for hp in headphones_data['headphones']]
    ]
    if len(valid_names) < 2:
        return None  # 未找到两个耳机名称

    # 查找耳机信息
    headphone1 = None
    headphone2 = None
    for hp in headphones_data['headphones']:
        if hp['name'] == valid_names[0]:
            headphone1 = hp
        elif hp['name'] == valid_names[1]:
            headphone2 = hp
        if headphone1 and headphone2:
            break

    if not headphone1 or not headphone2:
        return None  # 未找到匹配的耳机

    # 比较耳机属性
    differences = []
    for key in headphone1:
        if key in headphone2 and headphone1[key] != headphone2[
                key] and key != "name":
            differences.append(
                f"{key}: {valid_names[0]} 是 {headphone1[key]}, {valid_names[1]} 是 {headphone2[key]}"
            )

    # 生成回答模板
    response_template = f"以下是 {valid_names[0]} 和 {valid_names[1]} 的比较结果："
    if differences:
        response = response_template + "\n" + "\n".join(differences)
    else:
        response = f"{valid_names[0]} 和 {valid_names[1]} 在主要属性上没有明显区别。"
    return response


def handle_recommend_by_price(user_input):
    """价格推荐优化版"""
    budgets = [int(num) for num in re.findall(r'\d+', user_input)]
    if len(budgets) == 1:
        return [
            hp for hp in headphones_data['headphones']
            if hp['price'] <= budgets[0]
        ]
    elif len(budgets) >= 2:
        return [
            hp for hp in headphones_data['headphones']
            if budgets[0] <= hp['price'] <= budgets[1]
        ]
    return []


def handle_recommend_by_feature(user_input):
    """功能推荐优化版"""
    features = re.findall(r'(降噪|防水|无线|蓝牙|低音强|高解析|音质好|长续航|运动|游戏|通勤)',
                          user_input)
    if not features:
        return []

    return [
        hp for hp in headphones_data['headphones'] if any(
            f in ",".join(hp['features'] + hp['best_for']) for f in features)
    ]


def process_message(user_input):
    """
    新增函数：根据用户输入返回回复文本，用于后端接口调用。
    """
    intent = recognize_intent(user_input)
    try:
        if intent == 'ask_headphone_info':
            hp = handle_ask_headphone_info(user_input)
            if hp:
                response = (f"型号：{hp['name']}\n"
                            f"品牌：{hp['brand']}\n"
                            f"类型：{hp['type']}\n"
                            f"价格：{hp['price']} 元\n"
                            f"续航：{hp.get('battery_life', '未知')}\n"
                            f"功能：{', '.join(hp.get('features', []))}\n"
                            f"降噪：{hp.get('noise_cancelling', '未知')}\n"
                            f"防水：{hp.get('waterproof', '未知')}\n"
                            f"适用场景：{', '.join(hp.get('best_for', []))}")
            else:
                response = ("⚠️ 未找到指定耳机，请尝试以下查询方式：\n"
                            "1. 包含完整型号名称（如：AirPods Pro 2 USB-C）\n"
                            "2. 使用品牌+型号片段（如：索尼XM5）")
        elif intent == 'compare_headphones':
            response = handle_compare_headphones(user_input)
            if not response:
                response = "未找到匹配的耳机，请检查名称是否正确。"
        elif intent == 'recommend_by_price':
            recs = handle_recommend_by_price(user_input)
            if recs:
                response = "💰 推荐清单：\n"
                for hp in sorted(recs, key=lambda x: x['price']):
                    response += f"· {hp['name']} ({hp['price']}元) [特点：{', '.join(hp['features'][:2])}]\n"
            else:
                response = "⚠️ 请包含明确预算（示例：2000元左右的降噪耳机）"
        elif intent == 'recommend_by_feature':
            recs = handle_recommend_by_feature(user_input)
            if recs:
                response = "✨ 功能推荐：\n"
                for hp in recs:
                    response += f"· {hp['name']} [{hp['type']}] 功能：{', '.join(hp['features'])}\n"
            else:
                response = "⚠️ 请说明具体需求（示例：适合运动的防水耳机）"
        else:
            response = ("🤔 暂时无法回答这个问题，您可以尝试：\n"
                        "- 查询具体型号参数（示例：AirPods Pro的详细信息）\n"
                        "- 比较两个型号（示例：对比XM4和XM5）\n"
                        "- 按预算推荐（示例：1500元以下的耳机）")
    except Exception as e:
        response = f"❌ 系统错误：{str(e)}"
    return response


def chat():
    """原有交互式聊天函数，仅在命令行测试时使用"""
    print("🎧 欢迎使用智能耳机助手！")
    while True:
        user_input = input("\n请输入问题（输入 退出 结束）：").strip()
        if user_input.lower() in ['退出', 'exit']:
            break

        intent = recognize_intent(user_input)
        print(f"[系统诊断] 识别意图：{intent}")

        try:
            if intent == 'ask_headphone_info':
                hp = handle_ask_headphone_info(user_input)
                if hp:
                    print("\n📝 耳机详细信息：")
                    print(f"型号：{hp['name']}")
                    print(f"品牌：{hp['brand']}")
                    print(f"类型：{hp['type']}")
                    print(f"价格：{hp['price']} 元")
                    print(f"续航：{hp.get('battery_life', '未知')}")
                    print(f"功能：{', '.join(hp.get('features', []))}")
                    print(f"降噪：{hp.get('noise_cancelling', '未知')}")
                    print(f"防水：{hp.get('waterproof', '未知')}")
                    print(f"适用场景：{', '.join(hp.get('best_for', []))}")
                else:
                    print("⚠️ 未找到指定耳机，请尝试以下查询方式：")
                    print("1. 包含完整型号名称（如：AirPods Pro 2 USB-C）")
                    print("2. 使用品牌+型号片段（如：索尼XM5）")
            elif intent == 'compare_headphones':
                response = handle_compare_headphones(user_input)
                if response:
                    print(response)
                else:
                    print("未找到匹配的耳机，请检查名称是否正确。")
            elif intent == 'recommend_by_price':
                recs = handle_recommend_by_price(user_input)
                if recs:
                    print("\n💰 推荐清单：")
                    for hp in sorted(recs, key=lambda x: x['price']):
                        print(
                            f"· {hp['name']} ({hp['price']}元) [特点：{', '.join(hp['features'][:2])}]"
                        )
                else:
                    print("⚠️ 请包含明确预算（示例：2000元左右的降噪耳机）")
            elif intent == 'recommend_by_feature':
                recs = handle_recommend_by_feature(user_input)
                if recs:
                    print("\n✨ 功能推荐：")
                    for hp in recs:
                        print(
                            f"· {hp['name']} [{hp['type']}] 功能：{', '.join(hp['features'])}"
                        )
                else:
                    print("⚠️ 请说明具体需求（示例：适合运动的防水耳机）")
            else:
                print("🤔 暂时无法回答这个问题，您可以尝试：")
                print("- 查询具体型号参数（示例：AirPods Pro的详细信息）")
                print("- 比较两个型号（示例：对比XM4和XM5）")
                print("- 按预算推荐（示例：1500元以下的耳机）")
        except Exception as e:
            print(f"❌ 系统错误：{str(e)}")


if __name__ == "__main__":
    chat()
