import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity

# 加载语料库和耳机数据
with open('corpus.json', 'r', encoding='utf-8') as f:
    intents_data = json.load(f)

with open('headphones.json', 'r', encoding='utf-8') as f:
    headphones_data = json.load(f)

# 准备训练数据
intent_examples = []
intent_labels = []
intent_responses = {}
for intent in intents_data['intents']:
    for example in intent['examples']:
        intent_examples.append(example)
        intent_labels.append(intent['intent'])
    intent_responses[intent['intent']] = intent['responses']

# 初始化 TF-IDF 向量化器
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(intent_examples)

# 应用 LSA 进行降维
lsa = TruncatedSVD(n_components=50)  # 选择合适的组件数量
X_lsa = lsa.fit_transform(X)


def recognize_intent(user_input):
    """基于 LSA 的意图识别函数"""
    # 如果用户输入包含“预算”关键词，直接返回 recommend_by_price 意图
    if "预算" in user_input or "价格" in user_input or "元" in user_input or any(
            keyword in user_input for keyword in ["以内", "以下", '左右']):
        return "recommend_by_price"

    # 如果用户输入包含“比较”关键词，直接返回 compare_headphones 意图
    if "比较" in user_input or "对比" in user_input or "区别" in user_input:
        return "compare_headphones"

    # 如果用户输入包含“信息”关键词，直接返回 ask_headphone_info 意图
    if "详细" in user_input or "信息" in user_input or "参数" in user_input or "介绍" in user_input:
        return "ask_headphone_info"
    # 将用户输入转换为 TF-IDF 向量并应用 LSA
    user_input_vec = vectorizer.transform([user_input])
    user_input_vec_lsa = lsa.transform(user_input_vec)

    # 计算与所有示例的余弦相似度
    similarities = cosine_similarity(user_input_vec_lsa, X_lsa)

    # 找到最相似的示例
    most_similar_index = similarities.argmax()
    most_similar_intent = intent_labels[most_similar_index]

    # 返回识别到的意图
    return most_similar_intent


def get_headphone_info(headphone_name):
    """获取耳机详细信息"""
    for hp in headphones_data['headphones']:
        if hp['name'].lower() == headphone_name.lower():
            return hp
    return None


def extract_headphone_names(user_input):
    """从用户输入中提取耳机名称"""
    # 获取所有耳机名称
    all_headphone_names = [hp['name'] for hp in headphones_data['headphones']]

    # 检查用户输入中是否包含耳机名称
    found_names = []
    for name in all_headphone_names:
        if name.lower() in user_input.lower():
            found_names.append(name)

    return found_names


def extract_numbers(user_input):
    """从用户输入中提取数字（不使用正则表达式）"""
    numbers = []
    current_number = ""
    for char in user_input:
        if char.isdigit():
            current_number += char
        elif current_number:
            numbers.append(int(current_number))
            current_number = ""
    if current_number:
        numbers.append(int(current_number))
    return numbers


def generate_comparison_response(headphone1, headphone2):
    """生成耳机比较的回答"""
    response = intent_responses['compare_headphones'][0].format(
        headphone1=headphone1['name'], headphone2=headphone2['name'])
    differences = []
    for key in headphone1:
        if key in headphone2 and headphone1[key] != headphone2[
                key] and key != "name":
            differences.append(
                f"{key}: {headphone1['name']} 是 {headphone1.get(key)}, {headphone2['name']} 是 {headphone2.get(key)}"
            )
    if differences:
        response += "\n" + "\n".join(differences)
    else:
        response += "\n这两款耳机在主要属性上没有明显区别。"
    return response


def generate_recommendation_by_price(budgets):
    """根据预算生成推荐回答"""
    if len(budgets) == 1:
        recs = [
            hp for hp in headphones_data['headphones']
            if hp['price'] <= budgets[0]
        ]
    elif len(budgets) >= 2:
        recs = [
            hp for hp in headphones_data['headphones']
            if budgets[0] <= hp['price'] <= budgets[1]
        ]
    else:
        return "请提供明确的预算范围。"

    if recs:
        response = intent_responses['recommend_by_price'][0] + "\n"
        for hp in sorted(recs, key=lambda x: x['price']):
            response += f"· {hp['name']} ({hp['price']}元) [特点：{', '.join(hp['features'][:2])}]\n"
        return response
    else:
        return "没有找到符合预算的耳机。"


def generate_headphone_info_response(headphone_names):
    """生成耳机信息查询的回答（优化换行版本）"""
    if not headphone_names:
        return "请告诉我您想查询哪款耳机的详细信息？"

    headphone = get_headphone_info(headphone_names[0])
    if not headphone:
        return f"找不到关于 {headphone_names[0]} 的详细信息，请确认名称是否正确"

    # 带换行符的响应模板
    template = """\
🎧 {headphone} 详细信息：

品牌：{brand}
类型：{type}
价格：{price}元
续航时间：{battery_life}
降噪功能：{noise_cancelling}
防水等级：{waterproof}
主要特点：
{features}
适用场景：{best_for}"""

    return template.format(
        headphone=headphone['name'],
        brand=headphone['brand'],
        type=headphone['type'],
        price=headphone['price'],
        battery_life=headphone['battery_life'],
        noise_cancelling=headphone['noise_cancelling'],
        waterproof=headphone['waterproof'],
        features="\n".join([f"· {feat}" for feat in headphone['features']]),
        best_for=" | ".join(headphone['best_for']))


def generate_response(intent, user_input):
    """根据意图生成回答"""
    if intent == 'compare_headphones':
        headphone_names = extract_headphone_names(user_input)
        if len(headphone_names) >= 2:
            headphone1 = get_headphone_info(headphone_names[0])
            headphone2 = get_headphone_info(headphone_names[1])
            if headphone1 and headphone2:
                return generate_comparison_response(headphone1, headphone2)
        return "需要对比至少两款耳机，请确认名称是否正确"

    elif intent == 'recommend_by_price':
        budgets = extract_numbers(user_input)
        return generate_recommendation_by_price(budgets)

    elif intent == 'ask_headphone_info':
        headphone_names = extract_headphone_names(user_input)
        return generate_headphone_info_response(headphone_names)

    return "暂时无法回答这个问题，您可以尝试换种方式提问"


def process_message(user_input):
    '''
    供服务端调用的函数，隐藏了不必要输出的细节
    '''
    intent = recognize_intent(user_input)
    response = '\n🤖 回答：' + generate_response(intent, user_input)
    return response


# 主聊天函数
def chat():
    print("🎧 欢迎使用智能耳机助手！")
    while True:
        user_input = input("\n请输入问题（输入 退出 结束）：").strip()
        if user_input.lower() in ['退出', 'exit']:
            break

        # 识别意图
        intent = recognize_intent(user_input)
        print(f"[系统诊断] 识别意图：{intent}")

        # 生成回答
        response = generate_response(intent, user_input)
        print("\n🤖 回答：")
        print(response)


if __name__ == "__main__":
    chat()
