import streamlit as st
import random
import time

# --- 1. 配置和 CSS 样式注入（战术 HUD 风格） ---

# 设置页面配置，使用宽模式和深色主题
st.set_page_config(
    page_title="COD 战术人生模拟器",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义 CSS 样式（玻璃半透明 + 战术 HUD 风格）
custom_css = """
<style>
/* Streamlit 基础重置 */
.stApp {
    background-color: #0b0f16; /* 深蓝灰色背景 */
    color: #e0e0e0; /* 灰白色字体 */
    font-family: 'Courier New', Courier, monospace; /* 终端/战术报告字体 */
}

/* 侧边栏样式 */
[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.05); /* 半透明侧边栏 */
    backdrop-filter: blur(10px);
    border-right: 1px solid rgba(135, 206, 235, 0.1); /* 轻微边框 */
    padding: 1.5rem;
}

/* 主容器样式 (Glassmorphism 卡片效果) */
.main > div {
    background: rgba(135, 206, 235, 0.03); /* 主内容区轻微半透明背景 */
    backdrop-filter: blur(5px);
    border-radius: 12px;
    padding: 20px;
    margin-top: 10px;
}

/* 按钮样式 */
.stButton>button {
    background-color: #334455; /* 深灰蓝按钮 */
    color: #b0c4de; /* 浅蓝字体 */
    border: 1px solid #4682b4;
    border-radius: 6px;
    padding: 10px 15px;
    transition: all 0.2s;
}
.stButton>button:hover {
    background-color: #4682b4; /* 鼠标悬停变亮 */
    color: #ffffff;
    box-shadow: 0 0 8px rgba(70, 130, 180, 0.8); /* 发光效果 */
    transform: scale(1.02);
}

/* 标题样式 */
h1, h2, h3 {
    color: #b0c4de;
    text-shadow: 0 0 5px rgba(135, 206, 235, 0.5); /* 轻微文字发光 */
    font-weight: bold;
}
h1 {
    text-align: center;
    padding-bottom: 20px;
    animation: fadeIn 1.5s ease-out forwards; /* 标题淡入动画 */
}

/* 日志卡片容器样式 (终端/报告风格) */
.event-log-container {
    background-color: #161b22; /* 比背景略深的颜色 */
    padding: 15px;
    border-radius: 8px;
    border: 1px solid #2e3b4a;
    max-height: 80vh; /* 限制高度并启用滚动 */
    overflow-y: auto;
}

/* 单条事件样式 */
.event-item {
    padding: 10px 15px;
    margin-bottom: 8px;
    border-left: 4px solid #4682b4; /* 左侧蓝色竖线 */
    background-color: rgba(70, 130, 180, 0.05);
    border-radius: 4px;
    line-height: 1.5;
    font-size: 0.95em;
    opacity: 0; /* 初始透明，用于动画 */
    animation: logFadeIn 0.5s ease-out forwards; /* Log 淡入动画 */
}

/* 死亡/重大事件样式 */
.major-event {
    border-left: 4px solid #dc143c !important; /* 红色高亮 */
    background-color: rgba(220, 20, 60, 0.15) !important;
    animation: logFadeIn 0.5s ease-out forwards, pulse 1.5s infinite alternate; /* 闪烁动画 */
    font-weight: bold;
}

/* 关系图表样式 */
.relation-item {
    margin-bottom: 10px;
    padding: 8px;
    border-bottom: 1px dashed #2e3b4a;
}

/* 动画定义 */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes logFadeIn {
    from { opacity: 0; transform: translateX(-10px); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes pulse {
    from { box-shadow: 0 0 4px rgba(220, 20, 60, 0.5); }
    to { box-shadow: 0 0 10px rgba(220, 20, 60, 1.0); }
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)
st.markdown('<div id="global_style"></div>', unsafe_allow_html=True) # 占位符，确保CSS在最前面

# --- 2. 数据定义（角色、事件、关系） ---

# COD 世界观角色及其阵营
COD_CHARACTERS = {
    "Price": {"faction": "TF 141", "gender": "Male"},
    "Soap MacTavish": {"faction": "TF 141", "gender": "Male"},
    "Ghost": {"faction": "TF 141", "gender": "Male"},
    "Gaz": {"faction": "TF 141", "gender": "Male"},
    "Shepherd": {"faction": "Shadow Company", "gender": "Male"},
    "König": {"faction": "KorTac", "gender": "Male"},
    "Horangi": {"faction": "KorTac", "gender": "Male"},
    "Nikolai": {"faction": "Chimera", "gender": "Male"},
    "Krueger": {"faction": "Chimera", "gender": "Male"},
    "Graves": {"faction": "Shadow Company", "gender": "Male"},
    "Alejandro": {"faction": "Los Vaqueros", "gender": "Male"},
    "Valeria Garza": {"faction": "Cartel", "gender": "Female"},
    "Farah Karim": {"faction": "Urzikstan Liberation Force", "gender": "Female"},
}

# 随机姓名列表 (COD 风格)
NAME_LIST = list(COD_CHARACTERS.keys()) + ["Alex Mason", "Frank Woods", "Seraph", "Makarov", "Richtofen", "Dempsey"]

# 随机外貌列表
APPEARANCE_LIST = [
    "左眼有深色战斗疤痕，眼神锐利。",
    "常年佩戴黑色骷髅面罩，沉默寡言。",
    "右臂被替换为碳纤维机械义肢。",
    "总穿着带有兜帽的战术外套，习惯性隐藏身形。",
    "剃着极短的板寸，下巴有一道陈旧的刀疤。",
    "拥有一头醒目的银色短发，气质冷峻。",
    "脸上画着油彩，但眼神中透着疲惫。",
    "体格健壮，身上有多处子弹和爆炸碎片留下的痕迹。",
    "Standard Issue: 穿着标准的作战服，外貌不起眼。"
]

# 关系评价等级
def get_relation_title(score):
    if score > 80:
        return "**💀🤝 灵魂伴侣 / 生死之交**"
    elif score > 50:
        return "**🌟 亲密战友 / 值得托付后背**"
    elif score > 20:
        return "**👍 熟悉的同袍**"
    elif score >= -20:
        return "普通同袍 / 点头之交"
    elif score >= -50:
        return "**⚠️ 关系紧张 / 战术分歧**"
    else:
        return "**💢 死敌 / 不共戴天**"

# --- 3. 核心游戏逻辑：生成人生经历 ---

def generate_lifeline(char_name, char_age, start_age, char_gender, char_appearance):
    """根据角色信息生成从 start_age 到 99 岁的人生时间线和关系网。"""
    
    # 初始化状态
    max_age = 99
    current_age = start_age
    is_alive = True
    military_status = "平民" # "平民", "军校", "现役", "退役"
    current_faction = "无" # "TF 141", "KorTac", "Shadow Company" 等
    
    # 关系字典: 角色名 -> 关系值
    relations = {name: 0 for name in COD_CHARACTERS}
    
    # 结果日志
    log = []
    
    # 首次日志记录（角色信息）
    log.append(f"""
        <div class="event-item major-event" style="animation-delay: 0.0s;">
            **[代号: {char_name}]**
            <br>
            **起始年龄**: {start_age} 岁
            <br>
            **性别**: {char_gender}
            <br>
            **外貌特征**: {char_appearance}
            <br>
            **人生信条**: 任务开始。
        </div>
    """)
    
    # 随机选择一个参军时的核心阵营（影响后期的主要队友）
    core_faction = random.choice(["TF 141", "KorTac", "Shadow Company", "Los Vaqueros"])
    
    # --- 循环生成每一年 ---
    while current_age <= max_age and is_alive:
        age_str = f"**{current_age} 岁**"
        
        # 1. 死亡判定
        death_chance = 0.0 # 基础死亡概率
        if current_age >= 50:
            death_chance += 0.01
        if current_age >= 60 and military_status == "现役": # 高龄现役风险高
             death_chance += 0.02
        if current_age >= 80:
            death_chance += 0.05
        
        # 任务/战斗阵亡（只在现役时发生，且几率较低）
        if military_status == "现役" and random.random() < 0.015: 
            death_event = random.choice([
                f"你在一次针对高价值目标的黑色行动中失踪，**被判定为 KIA** (Killed In Action)，遗体未找到。",
                f"在掩护队友撤退时，你为他们挡住了敌方火力，**壮烈牺牲**。",
                f"在一次激烈的巷战中，被敌方狙击手击中要害，**抢救无效阵亡**。",
                f"因情报泄露，你们遭遇伏击，你引爆了身上的C4与敌人同归于尽，**结束了你的使命**。"
            ])
            log.append(f"""
                <div class="event-item major-event" style="animation-delay: {current_age * 0.1}s;">
                    💀 {age_str}: **命运终结**。{death_event}
                </div>
            """)
            is_alive = False
            break # 结束人生
        
        # 自然/非战斗死亡（年龄概率）
        if random.random() < death_chance:
            death_event = random.choice([
                "在睡梦中平静地离开了，可能只是因为任务完成太久，终于可以放松了。",
                "被体内的旧伤和后遗症折磨，病逝于医院。",
                "在退休后的渔船上，因为一次心脏骤停而逝世。",
                "在一次例行检查中，被诊断出不治之症，数月后离世。"
            ])
            log.append(f"""
                <div class="event-item major-event" style="animation-delay: {current_age * 0.1}s;">
                    🕊️ {age_str}: **和平谢幕**。在 {military_status} 状态下，你 {death_event}
                </div>
            """)
            is_alive = False
            break # 结束人生

        # 2. 事件生成
        
        new_event = None
        
        # --- 0-17 岁：早期生活 ---
        if current_age < 18:
            icon = "👶" if current_age < 6 else "🏫"
            
            if random.random() < 0.2: # 早期性格事件
                new_event = random.choice([
                    f"{icon} 你在儿童游乐场和一群孩子打架，展现了不服输的性格。",
                    f"{icon} 家庭经历了一次搬迁，你适应了新的环境，并学会了观察陌生人。",
                    f"{icon} 你对军事玩具和模型表现出极大的兴趣，阅读了大量关于战争的资料。",
                    f"{icon} 遭遇了一次小型事故，留下了微小的疤痕，但心理变得更加坚韧。",
                    f"{icon} 成绩平平，但体育和射击天赋极高（如果适用）。",
                    f"{icon} 偶然间接触到了某种武器，好奇心被彻底激发。"
                ])
            
        # --- 18-60 岁：军事生涯核心期 ---
        elif 18 <= current_age <= 60:
            icon = "🪖"
            
            # --- 参军/入伍事件 ---
            if current_age == 18 and military_status == "平民":
                if random.random() < 0.7:
                    military_status = "军校"
                    new_event = f"{icon} **人生转折！** 你决定参军，进入一所优秀的军事院校深造，开始了严格的训练。"
                    
            elif current_age == 20 and military_status == "军校":
                military_status = "现役"
                current_faction = core_faction # 确定加入的阵营
                new_event = f"{icon} **毕业！** 你以优异的成绩从军校毕业，被选中加入 **[{current_faction}]** 成为一名现役作战人员。"
            
            # --- 现役任务/关系事件 ---
            elif military_status == "现役":
                
                # 随机选择一个同阵营队友，或一个非同阵营的特殊角色
                is_faction_event = random.random() < 0.7
                if is_faction_event:
                    # 优先选择核心阵营的队友
                    possible_targets = [name for name, data in COD_CHARACTERS.items() if data["faction"] == current_faction]
                else:
                    # 低概率和敌对阵营/特殊阵营角色互动
                    possible_targets = [name for name, data in COD_CHARACTERS.items() if data["faction"] != current_faction]
                
                # 确保有目标，否则随机从所有角色中选
                target_char = random.choice(possible_targets if possible_targets else list(COD_CHARACTERS.keys()))
                
                # 随机生成事件类型
                event_type_roll = random.random()
                
                # 好感度为正（友情/爱情）
                if relations[target_char] > -20 and event_type_roll < 0.7:
                    new_event, rel_change = random.choice([
                        (f"{icon} 在一次突袭行动中，**{target_char}** 及时为你清除了一个侧翼威胁，关系 +5。", 5),
                        (f"{icon} 任务结束后，你和 **{target_char}** 在酒吧分享了一瓶上好的威士忌，畅谈往事，关系 +3。", 3),
                        (f"{icon} 你们在寒冷的夜晚共同执行潜伏任务，**{target_char}** 分享了他的护身符给你，关系 +8。", 8),
                        (f"{icon} 你们的战术出现分歧，但最终 **{target_char}** 选择信任你的判断，任务成功，关系 +10。", 10),
                        (f"{icon} (高好感度触发) 在一次近距离接触战中，**{target_char}** 为你挡下了一枚致命的破片，自己受了重伤。**重大转折！** 关系 +20。", 20),
                        (f"{icon} (暧昧/爱情) 你们在直升机上执行长途运输，**{target_char}** 握住了你的手，没有说话，关系 +15。", 15),
                        (f"{icon} (稀有事件) 你们的友谊被一个阴谋考验。你选择相信 **{target_char}**，关系大幅提升，+15。", 15)
                    ])
                    
                # 好感度为负（冲突）
                elif relations[target_char] < 20 and event_type_roll >= 0.7:
                    new_event, rel_change = random.choice([
                        (f"{icon} 在战术会议上，你和 **{target_char}** 对任务方案产生激烈分歧，最终不欢而散，关系 -5。", -5),
                        (f"{icon} **{target_char}** 在一次任务中出现失误，你被牵连导致受伤，关系 -10。", -10),
                        (f"{icon} 你发现 **{target_char}** 隐瞒了部分关键情报，你们之间产生了严重的不信任，关系 -15。", -15),
                        (f"{icon} (稀有事件) 你被怀疑叛变，**Shepherd** 在幕后布局，**{target_char}** 相信了阴谋并向你开火，关系 -30。", -30),
                        (f"{icon} (和好事件) 尽管之前有冲突，但在关键时刻 **{target_char}** 救了你一命，关系回升 +10。", 10)
                    ])
                
                # 其他通用军事事件（不涉及关系）
                else: 
                    new_event = random.choice([
                        f"{icon} 你被晋升为小队队长/士官长，压力和责任更大了。",
                        f"{icon} 你在一次训练事故中受了轻伤，休假了一段时间。",
                        f"{icon} 你被调往 **{random.choice(['阿尔法部队', 'Delta Force', 'SAS', 'GIGN'])}** 进行联合训练。",
                        f"{icon} 完成了一项代号为 'Blackout' 的绝密任务，但无人知晓细节。",
                        f"{icon} 发现自己的部队可能被上级 **{Shepherd}** 背叛，但选择了隐忍。",
                        f"{icon} 你的一个普通战友在任务中阵亡，你开始反思战争的意义。",
                    ])
                    rel_change = 0
                    
                # 应用关系变化
                if rel_change != 0:
                    relations[target_char] += rel_change
                    
            # --- 退休事件 ---
            elif current_age == 60 and military_status == "现役":
                military_status = "退役"
                new_event = f"🧓 **退休！** 你决定在 60 岁光荣退役，离开了 **[{current_faction}]**，开始平民生活。但战争的阴影从未离开。"
            
        # --- 61-99 岁：退休生活 ---
        elif current_age > 60:
            icon = "🏡"
            if random.random() < 0.25:
                # 随机选一个高好感度的老战友
                close_friends = [name for name, score in relations.items() if score > 50]
                visit_char = random.choice(close_friends) if close_friends else random.choice(list(COD_CHARACTERS.keys()))
                
                new_event = random.choice([
                    f"{icon} 你被邀请回军事院校给年轻学员们讲授战术经验。",
                    f"{icon} **老战友 {visit_char}** 前来看望你，你们一起缅怀了逝去的岁月，关系 +5。",
                    f"{icon} 身体的旧伤开始复发，你不得不长期服用止痛药。",
                    f"{icon} 你写了一本关于你军事生涯的回忆录，引起了小范围的关注。",
                    f"{icon} 你的一个关系值低于-30的**死敌**找到了你，但你们只是沉默地对视，没有发生冲突，关系 +5。",
                    f"{icon} 你过着平静的退休生活，似乎已经摆脱了战争，但在深夜依然会被噩梦惊醒。"
                ])
                if "老战友" in new_event and visit_char in relations:
                     relations[visit_char] += 5
            
        # 如果本年没有事件，记一条平静的记录
        if new_event is None:
            new_event = f"{icon} 平静的一年。你继续 {military_status} 的生活。"

        # 将事件加入日志
        log.append(f"""
            <div class="event-item" style="animation-delay: {current_age * 0.1}s;">
                {new_event}
            </div>
        """)
        
        current_age += 1
        
    # --- 最终总结 ---
    final_status = "在 99 岁时自然老去。"
    if not is_alive and current_age < 100:
        final_status = f"在 {current_age - 1} 岁时阵亡。"
    elif is_alive:
        final_status = "活到了 99 岁，完成了完整的人生。"
        
    summary = f"""
        <div class="event-item major-event" style="animation-delay: {(current_age+1) * 0.1}s;">
            **[人生总结]** **{char_name}** 在 COD 世界观中 {final_status}。
        </div>
    """
    log.append(summary)
    
    return log, relations, is_alive

# --- 4. Streamlit UI 布局和交互 ---

st.title("COD 战术人生模拟器 V1.0")

# --- 侧边栏：角色创建与控制 ---
with st.sidebar:
    st.subheader("👤 角色配置 (Operator Creation)")
    
    # --- 角色信息输入 ---
    
    # 姓名
    char_name_input = st.text_input("代号 / 姓名 (Callsign)", value="", placeholder="如 Price, Soap, 或自定义")
    
    # 年龄
    col_age_1, col_age_2 = st.columns([2, 1])
    with col_age_1:
        char_age_input = st.number_input("起始年龄", min_value=1, max_value=99, value=random.randint(18, 30), key="age_input")
    with col_age_2:
        if st.button("🎲 随机年龄", key="random_age"):
            st.session_state.age_input = random.randint(1, 30)
            st.experimental_rerun()
            
    # 性别
    col_gender_1, col_gender_2 = st.columns([2, 1])
    with col_gender_1:
        char_gender_input = st.selectbox("生理性别", ["男", "女", "保密"], index=0, key="gender_select")
    with col_gender_2:
        if st.button("🎲 随机性别", key="random_gender"):
            st.session_state.gender_select = random.choice(["男", "女", "保密"])
            st.experimental_rerun()

    # 外貌
    char_appearance_input = st.text_input("外貌特征", value="", placeholder="如 戴黑色骷髅面罩, 左眼有疤")
    if st.button("🎲 随机外貌", key="random_appearance"):
        st.session_state.appearance_text = random.choice(APPEARANCE_LIST)
        st.experimental_rerun()
    
    # 统一处理输入值的 Fallback
    char_name = char_name_input.strip() or "Unknown Operator"
    char_age = st.session_state.age_input
    char_gender = st.session_state.gender_select
    char_appearance = char_appearance_input.strip() or random.choice(APPEARANCE_LIST)
    if 'appearance_text' in st.session_state and char_appearance_input.strip() == "":
        char_appearance = st.session_state.appearance_text

    st.markdown("---")
    
    # 核心启动按钮
    if st.button("🚀 开始模拟人生 (Run Simulation)", key="start_simulation", help="点击开始生成从现在到 99 岁的人生轨迹"):
        st.session_state.run_simulation = True
        st.session_state.log, st.session_state.relations, st.session_state.is_alive = generate_lifeline(
            char_name, char_age, char_age, char_gender, char_appearance
        )
    
    st.caption("每次点击'开始模拟'都将生成全新的时间线和随机事件，即使参数不变。")

# --- 主区域：日志和关系网 ---

# 默认状态或第一次运行前
if 'run_simulation' not in st.session_state or not st.session_state.run_simulation:
    st.markdown("""
        <div class="main-card" style="text-align: center; padding: 50px;">
            <h2>🚨 战术情报待命 (Tactical Intel Standby)</h2>
            <p>请在左侧侧边栏配置您的特种作战人员 (Operator)，然后点击 <strong>🚀 开始模拟人生</strong>。</p>
            <p>加载的日志将显示在这张战术报告卡上。</p>
        </div>
    """, unsafe_allow_html=True)
    st.stop()


# 获取模拟结果
life_log = st.session_state.log
final_relations = st.session_state.relations

# 分列布局
col_log, col_relation = st.columns([2.5, 1])

# --- 左侧：人生日志 (Log) ---
with col_log:
    st.subheader(f"📜 人生日志：{char_name} 的作战报告")
    st.caption(f"起始年龄: {char_age} 岁 | 最终状态: {'存活' if st.session_state.is_alive else '阵亡'}")
    
    # 将日志内容包装在一个可滚动的容器内
    st.markdown('<div class="event-log-container">', unsafe_allow_html=True)
    
    # 逐条输出日志（使用迭代器模拟时间流逝）
    for i, event in enumerate(life_log):
        # 使用 markdown 直接渲染带 CSS 样式的 HTML 字符串
        st.markdown(event, unsafe_allow_html=True)
        # 模拟动画延迟，但避免在实际运行中造成长时阻塞
        # time.sleep(0.01) # 在实际运行中，可以根据需求打开或关闭
        
    st.markdown('</div>', unsafe_allow_html=True)

# --- 右侧：关系结算 (Relation) ---
with col_relation:
    st.subheader("🤝 关系结算 (Aquired Assets)")
    st.caption("仅显示关系值不为零的 COD 角色。")
    
    # 过滤非零关系并排序
    active_relations = {k: v for k, v in final_relations.items() if v != 0}
    sorted_relations = sorted(active_relations.items(), key=lambda item: abs(item[1]), reverse=True)
    
    if not sorted_relations:
        st.info("你在本次模拟中没有和 COD 世界观中的主要人物产生显著的交集或影响。")
    else:
        for char_name, score in sorted_relations:
            # 关系值归一化到进度条 (0-100)。-100 到 100 映射到 0 到 100
            progress_value = (score + 100) / 200
            
            # 使用 CSS 风格的容器
            st.markdown(f'<div class="relation-item">', unsafe_allow_html=True)
            
            # 名字和阵营
            faction = COD_CHARACTERS.get(char_name, {}).get("faction", "Unknown")
            st.markdown(f"**{char_name}** _({faction})_")
            
            # 关系评价
            st.markdown(get_relation_title(score), unsafe_allow_html=True)
            
            # 进度条
            if score > 0:
                # 绿色进度条 (正面)
                st.progress(progress_value, text=f"好感: {score}")
            else:
                # 红色进度条 (负面)
                st.markdown(f"""
                    <div style="background-color: rgba(220, 20, 60, 0.2); border-radius: 4px; overflow: hidden; height: 10px;">
                        <div style="width: {progress_value * 100}%; height: 100%; background-color: #dc143c;"></div>
                    </div>
                    <p style="font-size: 0.8em; margin-top: 5px;">冲突: {score}</p>
                """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)


# 确保 Streamlit 在 session_state 中有默认值，防止第一次加载时报错
if 'age_input' not in st.session_state:
    st.session_state.age_input = random.randint(18, 30)
if 'gender_select' not in st.session_state:
    st.session_state.gender_select = random.choice(["男", "女", "保密"])
if 'appearance_text' not in st.session_state:
    st.session_state.appearance_text = random.choice(APPEARANCE_LIST)