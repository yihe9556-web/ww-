import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import random

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

# --- 核心逻辑类 ---

class CODLifeSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("COD: Operator Life Simulator")
        self.root.geometry("900x700")
        self.root.configure(bg="#0f0f0f") # 黑色背景

        # 样式设置
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TLabel", background="#0f0f0f", foreground="#00ff41", font=("Consolas", 10))
        self.style.configure("TButton", background="#1a1a1a", foreground="#00ff41", bordercolor="#00ff41", font=("Consolas", 11, "bold"))
        self.style.configure("TEntry", fieldbackground="#1a1a1a", foreground="#00ff41")
        
        self.setup_ui()

    def setup_ui(self):
        # 标题
        header = tk.Label(self.root, text="/// OPERATOR DOSSIER GENERATOR ///", bg="#0f0f0f", fg="#00ff41", font=("Consolas", 16, "bold"))
        header.pack(pady=10)

        # 输入区域框架
        input_frame = tk.Frame(self.root, bg="#0f0f0f", bd=1, relief="solid")
        input_frame.pack(pady=10, padx=20, fill="x")

        # 姓名
        tk.Label(input_frame, text="CODENAME/NAME:", bg="#0f0f0f", fg="#00ff41").grid(row=0, column=0, padx=10, pady=5)
        self.name_entry = tk.Entry(input_frame, bg="#1a1a1a", fg="#00ff41", insertbackground="white")
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)
        tk.Button(input_frame, text="RND", command=self.random_name, bg="#1a1a1a", fg="#00ff41", width=4).grid(row=0, column=2)

        # 性别
        tk.Label(input_frame, text="GENDER:", bg="#0f0f0f", fg="#00ff41").grid(row=0, column=3, padx=10, pady=5)
        self.gender_combo = ttk.Combobox(input_frame, values=["Male", "Female"], state="readonly")
        self.gender_combo.current(0)
        self.gender_combo.grid(row=0, column=4, padx=10, pady=5)

        # 外貌
        tk.Label(input_frame, text="VISUALS:", bg="#0f0f0f", fg="#00ff41").grid(row=1, column=0, padx=10, pady=5)
        self.looks_entry = tk.Entry(input_frame, bg="#1a1a1a", fg="#00ff41", insertbackground="white", width=40)
        self.looks_entry.grid(row=1, column=1, columnspan=4, padx=10, pady=5, sticky="w")
        tk.Button(input_frame, text="GENERATE VISUALS", command=self.random_looks, bg="#1a1a1a", fg="#00ff41").grid(row=1, column=5, padx=5)

        # 开始按钮
        start_btn = tk.Button(self.root, text=">> INITIATE SIMULATION <<", command=self.start_simulation, bg="#003300", fg="#00ff41", font=("Consolas", 12, "bold"), relief="flat", pady=5)
        start_btn.pack(pady=10, fill="x", padx=50)

        # 文本输出区域
        self.log_area = scrolledtext.ScrolledText(self.root, bg="black", fg="#00ff41", font=("Consolas", 10), insertbackground="white")
        self.log_area.pack(padx=20, pady=10, fill="both", expand=True)
        self.log_area.insert(tk.END, "AWAITING INPUT...\n")

    def random_name(self):
        names = ["Alex", "Roach", "Viper", "Echo", "Spectre", "Rook", "Nomad", "Zero", "Frost", "Sandman"]
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, random.choice(names))

    def random_looks(self):
        features = ["伤疤横贯左眼", "眼神冰冷", "总是戴着战术面罩", "手臂上有骷髅纹身", "短发，干练", "身材魁梧如熊", "总是戴着墨镜", "有一只义眼"]
        gear = ["穿着吉利服", "重型防弹衣", "经典的SAS黑色作战服", "沙色迷彩", "便衣特工装扮"]
        desc = f"{random.choice(features)}，{random.choice(gear)}。"
        self.looks_entry.delete(0, tk.END)
        self.looks_entry.insert(0, desc)

    def start_simulation(self):
        name = self.name_entry.get() or "Operator"
        gender = self.gender_combo.get()
        looks = self.looks_entry.get() or "标准战术装备"
        
        self.log_area.delete(1.0, tk.END)
        self.log_area.insert(tk.END, f"/// FILE ACCESSED: {name.upper()} ///\n")
        self.log_area.insert(tk.END, f"/// GENDER: {gender.upper()} ///\n")
        self.log_area.insert(tk.END, f"/// VISUALS: {looks} ///\n")
        self.log_area.insert(tk.END, "-"*60 + "\n\n")

        self.run_life(name, gender)

    def run_life(self, name, gender):
        age = 1
        alive = True
        in_military = False
        rank = "平民"
        friends = {} # 记录关系值
        relationships = {} # 记录特殊关系 (恋人/仇人)
        
        # 定义全角色列表
        all_chars = []
        for faction in COD_CHARACTERS.values():
            all_chars.extend(faction)

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
                # 18岁参军
                if age == 18:
                    in_military = True
                    rank = "列兵"
                    event_text += "你正式入伍。新兵训练营简直是地狱，但你挺过来了。"
                
                # 22岁左右加入特战队
                elif age == 22 and in_military:
                    event_text += "由于表现优异，你被选拔进入特种部队。你的代号是 '" + name + "'。"
                    # 随机结识一个初始角色
                    first_meet = random.choice(all_chars)
                    friends[first_meet] = 10
                    event_text += f"\n   > 你在训练基地第一次见到了 {first_meet}。"

                # 职业生涯随机事件
                else:
                    dice = random.randint(1, 100)
                    
                    # --- 事件类型 A: 任务 ---
                    if dice < 40: 
                        missions = ["乌兹克斯坦", "阿马兹拉", "福尔丹斯克", "一艘货轮", "雪山基地"]
                        location = random.choice(missions)
                        event_text += f"你被部署到 {location} 执行任务。"
                        
                        # 任务中可能会受伤或立功
                        if random.random() < 0.2:
                            event_text += " 任务出了差错，你受了伤，留下了伤疤。"
                        elif random.random() < 0.2:
                            event_text += " 你成功拆除了炸弹，获得了一枚勋章。"

                    # --- 事件类型 B: 角色互动 (核心玩法) ---
                    elif dice < 80:
                        # 随机选取一个角色互动
                        char = random.choice(all_chars)
                        if char not in friends: friends[char] = 0
                        
                        # 互动逻辑
                        interaction_type = random.choice(["positive", "neutral", "conflict", "romance"])
                        
                        if interaction_type == "positive":
                            friends[char] += 10
                            if char in CHARACTER_EVENTS:
                                event_text += random.choice(CHARACTER_EVENTS[char])
                            else:
                                event_text += f"你和 {char} 配合默契，完成了任务。"
                                
                        elif interaction_type == "conflict":
                            friends[char] -= 10
                            reason = random.choice(["战术分歧", "抢了最后一块比萨", "误伤友军(演习)", "性格不合"])
                            event_text += f"你和 {char} 因为 {reason} 大吵了一架。"
                            if friends[char] < -30:
                                event_text += f" **警告：{char} 现在非常讨厌你。**"

                        elif interaction_type == "romance":
                            # 简单的爱情线逻辑
                            if friends[char] > 50 and random.random() < 0.3:
                                event_text += f"在漫长的潜伏任务中，你和 {char} 之间产生了一种超越战友的情愫。"
                                relationships["Lover"] = char
                            else:
                                event_text += f"你发现自己在这个残酷的世界里，居然有些在意 {char}。"
                        
                        else: # neutral
                             event_text += f"在基地食堂，你偶遇了 {char}，你们点了点头。"

                    # --- 事件类型 C: 重大转折 (谢菲尔德背叛等) ---
                    elif dice < 90:
                        if "General Shepherd" in friends and friends["General Shepherd"] > 0:
                             event_text += "Shepherd 将军私下找你谈话，让你去销毁一些证据。你照做了，但内心感到不安。"
                        else:
                             event_text += "情报出了问题，你的小队遭到了伏击。你失去了几位好兄弟。"

                    # --- 事件类型 D: 死亡判定 ---
                    else:
                         if random.random() < 0.05: # 5% 几率阵亡
                             event_text += "你在执行一项自杀式任务时，为了掩护队友撤退，引爆了手雷。"
                             event_text += "\n\n--- K.I.A (阵亡) ---"
                             self.log_area.insert(tk.END, event_text + "\n")
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

            # 输出当前年份文本
            self.log_area.insert(tk.END, event_text + "\n")
            self.log_area.see(tk.END) # 自动滚动到底部
            self.root.update() # 刷新界面，防止卡顿
            
            # 增加年龄
            age += 1
            # 简单的延迟模拟打字效果（可选）
            # time.sleep(0.05) 

        # 游戏结束总结
        if alive:
            summary = f"\n\n/// 模拟结束 ///\n最高军衔: {rank}\n重要关系: {friends}\n"
            self.log_area.insert(tk.END, summary)

if __name__ == "__main__":
    root = tk.Tk()
    game = CODLifeSimulator(root)
    root.mainloop()