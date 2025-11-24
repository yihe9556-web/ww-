import streamlit as st
import random
import time

# --- 游戏数据配置 ---

COD_CHARACTERS = {
    "TF141": ["Captain Price", "Soap MacTavish", "Ghost (Simon Riley)", "Gaz", "General Shepherd"],
    "KorTac": ["König", "Horangi", "Roze"],
    "Chimera": ["Krueger", "Nikto", "Nikolai"],
    "Shadow": ["Philip Graves"]
}

# 角色特定的互动事件库
CHARACTER_EVENTS = {
    "Captain Price": [
        "Price 递给你一支雪茄，虽然你不抽烟，但这是某种认可。",
        "在简报室里，Price 对你的战术提出了表扬。",
        "Price 拍了拍你的肩膀：'起来，士兵，我们还要去拯救世界。'",
        "你和 Price 在酒吧里喝着威士忌，听他讲以前在切尔诺贝利的故事。"
    ],
    "Soap MacTavish": [
        "Soap 在你的战术背心上画了一个笑脸，你无奈地笑了。",
        "在拆弹任务中，Soap 开了个不合时宜的玩笑，缓解了你的紧张。",
        "Soap 邀请你去苏格兰看望他的家人。",
        "你和 Soap 比赛飞刀，结果你输了 50 美元。"
    ],
    "Ghost (Simon Riley)": [
        "Ghost 只是在这个角落里默默地擦拭他的面具，但他递给了你一瓶水。",
        "在潜行任务中，Ghost 救了你一命，但他什么也没说，只是点了点头。",
        "你试图和 Ghost 聊天，他沉默了五分钟后回了一句：'保持专注'。",
        "Ghost 极其罕见地向你展示了一张家人的旧照片，随即迅速收回。"
    ],
    "Gaz": [
        "Gaz 嘲笑你的驾驶技术，然后亲自教你如何在大雨中漂移。",
        "你和 Gaz 讨论哪种手枪最好用，争论了一整晚。",
    ],
    "General Shepherd": [
        "Shepherd 将军在视察时盯着你看了很久，那是猎人审视猎物的眼神。",
        "Shepherd 给了你一项绝密任务，你总觉得这任务有点不对劲。",
        "Shepherd 问你：'如果为了大局，你愿意牺牲什么？'"
    ],
    "König": [
        "König 因为身高太高撞到了门框，你没忍住笑了一声，他害羞地低下了头。",
        "战场上，König 像一头野兽一样为你挡住了侧翼的火力。",
        "König 显得很焦虑，你拍了拍他的后背安抚他的情绪。"
    ],
    "Nikto": [
        "Nikto 用俄语骂了一句你听不懂的话，但随后扔给你一个急救包。",
        "你看见 Nikto 独自一人坐在黑暗中，似乎在忍受某种痛苦。"
    ]
}

# --- 辅助函数 ---

def random_name_generator():
    names = ["Alex", "Roach", "Viper", "Echo", "Spectre", "Rook", "Nomad", "Zero", "Frost", "Sandman"]
    return random.choice(names)

def random_looks_generator():
    features = ["伤疤横贯左眼", "眼神冰冷", "总是戴着战术面罩", "手臂上有骷髅纹身", "短发，干练", "身材魁梧如熊", "总是戴着墨镜", "有一只义眼"]
    gear = ["穿着吉利服", "重型防弹衣", "经典的SAS黑色作战服", "沙色迷彩", "便衣特工装扮"]
    return f"{random.choice(features)}，{random.choice(gear)}。"

# --- 核心模拟逻辑 ---

def run_life(name, gender, looks, log_placeholder):
    age = 1
    alive = True
    in_military = False
    rank = "平民"
    friends = {} 
    relationships = {} 
    log_lines = []

    # 定义全角色列表
    all_chars = []
    for faction in COD_CHARACTERS.values():
        all_chars.extend(faction)

    # 初始信息写入日志
    initial_log = f"/// FILE ACCESSED: {name.upper()} ///\n"
    initial_log += f"/// GENDER: {gender.upper()} ///\n"
    initial_log += f"/// VISUALS: {looks} ///\n"
    initial_log += "-"*60 + "\n\n"
    log_lines.append(initial_log)

    # 主循环 (1 到 99 岁)
    while age <= 99 and alive:
        event_text = f"【{age}岁】 "
        
        # --- 阶段 1: 童年与少年 (1-17) ---
        if age < 18:
            if age == 1:
                event_text += f"你出生在一个动荡的地区，或是军事世家。"
            elif age == 6:
                event_text += "你第一次接触到了玩具枪，展现出了惊人的天赋。"
            elif age == 14:
                event_text += "你在学校里是个刺头，或者是个体育健将。你听说这世界正在爆发冲突。"
            elif age == 17:
                event_text += "你看着征兵海报，内心渴望着战斗与荣耀。"
            else:
                events = ["平淡的一年。", "你打了一架。", "你在体能训练中打破了纪录。", "你学习了外语。"]
                event_text += random.choice(events)

        # --- 阶段 2: 参军与特战生涯 (18-55) ---
        elif 18 <= age <= 55:
            if age == 18:
                in_military = True
                rank = "列兵"
                event_text += "你正式入伍。新兵训练营简直是地狱，但你挺过来了。"
            
            elif age == 22 and in_military:
                event_text += "由于表现优异，你被选拔进入特种部队。你的代号是 '" + name + "'。"
                first_meet = random.choice(all_chars)
                friends[first_meet] = 10
                event_text += f"\n   > 你在训练基地第一次见到了 {first_meet}。"

            else:
                dice = random.randint(1, 100)
                
                if dice < 40: # 任务
                    missions = ["乌兹克斯坦", "阿马兹拉", "福尔丹斯克", "一艘货轮", "雪山基地"]
                    event_text += f"你被部署到 {random.choice(missions)} 执行任务。"
                    if random.random() < 0.2: event_text += " 任务出了差错，你受了伤，留下了伤疤。"
                    elif random.random() < 0.2: event_text += " 你成功完成了关键掩护。"

                elif dice < 80: # 角色互动
                    char = random.choice(all_chars)
                    if char not in friends: friends[char] = 0
                    
                    interaction_type = random.choice(["positive", "conflict", "romance"])
                    
                    if interaction_type == "positive":
                        friends[char] = min(100, friends[char] + 10)
                        if char in CHARACTER_EVENTS:
                            event_text += random.choice(CHARACTER_EVENTS[char])
                        else:
                            event_text += f"你和 {char} 配合默契，完成了任务。"
                            
                    elif interaction_type == "conflict":
                        friends[char] = max(-50, friends[char] - 15)
                        reason = random.choice(["战术分歧", "抢了最后一块比萨", "误伤友军(演习)", "性格不合"])
                        event_text += f"你和 {char} 因为 {reason} 大吵了一架。"
                        if friends[char] < -30:
                            event_text += f" **警告：{char} 现在非常讨厌你。**"

                    elif interaction_type == "romance":
                        if friends[char] > 50 and random.random() < 0.3 and 'Lover' not in relationships:
                            event_text += f"在漫长的潜伏任务中，你和 {char} 之间产生了一种超越战友的情愫。"
                            relationships["Lover"] = char
                        elif 'Lover' in relationships and relationships['Lover'] == char:
                             event_text += f"你和你的爱人 {char} 度过了一个安静的休假。"
                        else:
                            event_text += f"你发现自己在这个残酷的世界里，居然有些在意 {char}。"
                
                elif dice < 90: # 重大转折
                    if "General Shepherd" in friends and friends["General Shepherd"] > 0 and random.random() < 0.4:
                        event_text += "Shepherd 将军私下找你谈话，让你去销毁一些证据。你照做了，但内心感到不安。"
                    else:
                        event_text += "情报出了问题，你的小队遭到了伏击。你失去了几位好兄弟。"

                else: # 死亡判定
                     if random.random() < 0.05:
                         event_text += "你在执行一项自杀式任务时，为了掩护队友撤退，引爆了手雷。"
                         event_text += "\n\n--- K.I.A (阵亡) ---"
                         log_lines.append(event_text)
                         alive = False
                         break
                     else:
                         event_text += "你在一次近距离交火中死里逃生，防弹插板救了你一命。"

        # --- 阶段 3: 晚年与退役 (56-99) ---
        else:
            if age == 56:
                 event_text += "你正式从一线作战部队退役。你的膝盖和背部在阴雨天总是隐隐作痛。"
                 in_military = False
            
            dice = random.randint(1, 100)
            if dice < 30:
                old_friend = random.choice(list(friends.keys())) if friends else "Price"
                event_text += f"{old_friend} 来看望你了，你们坐在门廊上回忆往昔。"
            elif dice < 60:
                event_text += "你在军事学院担任教官，看着新一代的特种兵，你想起了年轻时的 Soap 和 Ghost。"
            else:
                event_text += "平静的一年。你偶尔会在新闻上看到那场似乎永远打不完的战争。"
            
            if age == 99:
                event_text += "\n\n--- 寿命终结 ---"
                event_text += "\n你安详地离世了。你的葬礼上，甚至有曾经的敌人前来致敬。"

        # 更新日志并刷新界面
        log_lines.append(event_text)
        log_placeholder.code("\n".join(log_lines), language='text')
        time.sleep(0.01) # 增加微小延迟，模拟实时打印效果

        age += 1

    # 游戏结束总结
    if alive:
        summary = "\n\n/// 模拟结束 ///\n"
        summary += f"最高军衔: 特战队员/教官\n"
        # 格式化关系输出
        friendly_relations = [f"{k}: {v}" for k, v in friends.items() if v >= 30]
        if friendly_relations:
            summary += "亲密战友: " + ", ".join(friendly_relations) + "\n"
        if "Lover" in relationships:
            summary += f"灵魂伴侣: {relationships['Lover']}\n"
        
        log_lines.append(summary)
        log_placeholder.code("\n".join(log_lines), language='text')

# --- Streamlit UI 配置 ---

# 设置页面配置和终端风格
st.set_page_config(layout="wide", page_title="COD: Operator Life Simulator")

# 通过 Markdown/HTML 注入 CSS 实现终端风格
st.markdown(
    """
    <style>
    /* 全局背景和文字 */
    .main {
        background-color: #0d1117; /* GitHub Dark Theme */
        color: #00ff41; /* 亮绿色 */
    }
    /* 标题样式 */
    h1 {
        color: #00ff41;
        font-family: 'Consolas', monospace;
    }
    /* 按钮样式 */
    .stButton>button {
        background-color: #003300;
        color: #00ff41;
        border: 1px solid #00ff41;
        font-family: 'Consolas', monospace;
    }
    /* 输入框样式 */
    .stTextInput>div>div>input {
        background-color: #1a1a1a;
        color: #00ff41;
        font-family: 'Consolas', monospace;
    }
    /* 代码块（日志区域）样式 */
    .stCodeBlock {
        background-color: #1a1a1a;
        color: #00ff41;
        border: 2px solid #00ff41;
        padding: 10px;
        white-space: pre-wrap; /* 允许文本换行 */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("/// OPERATOR DOSSIER GENERATOR ///")

# 1. 角色信息输入
with st.container():
    st.subheader("角色配置")
    
    col_name, col_gender, col_sep = st.columns([2, 1, 0.5])
    
    # 姓名输入 (使用 session_state 保持随机值)
    if 'name_input' not in st.session_state:
        st.session_state['name_input'] = ""
        
    with col_name:
        name_input = st.text_input("CODENAME/NAME", value=st.session_state['name_input'], key="name_key")
        
    with col_gender:
        gender_input = st.selectbox("GENDER", ["Male", "Female"])
        
    if col_sep.button("随机姓名", key="btn_name"):
        st.session_state['name_input'] = random_name_generator()
        st.rerun() # 重新运行脚本以更新输入框的值

    # 外貌输入
    if 'looks_input' not in st.session_state:
        st.session_state['looks_input'] = ""
        
    looks_input = st.text_input("VISUALS (外貌描述)", value=st.session_state['looks_input'], key="looks_key")
    if st.button("生成随机外貌", key="btn_looks"):
        st.session_state['looks_input'] = random_looks_generator()
        st.rerun() # 重新运行脚本以更新输入框的值

st.markdown("---")

# 2. 启动模拟按钮
if st.button(">> INITIATE SIMULATION (启动模拟) <<", type="primary"):
    
    final_name = st.session_state['name_input'] if st.session_state['name_input'] else "Echo"
    final_looks = st.session_state['looks_input'] if st.session_state['looks_input'] else "标准战术装备"
    
    # 日志区域占位符
    log_placeholder = st.empty()
    
    # 运行模拟
    run_life(final_name, gender_input, final_looks, log_placeholder)

    st.success("--- SIMULATION COMPLETE ---")

else:
    st.info("请配置角色信息并点击上方按钮开始你的 COD 人生模拟。")