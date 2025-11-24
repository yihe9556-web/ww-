import tkinter as tk
from tkinter import ttk, scrolledtext
import random

# --- 配置与数据 ---

COD_CHARACTERS = {
    TF141 [Captain Price, Soap MacTavish, Simon 'Ghost' Riley, Kyle 'Gaz' Garrick],
    KorTac [König, Horangi],
    Chimera [Krueger, Nikto, Nikolai],
    Villains [General Shepherd, Makarov]
}

# 基础事件池 (根据年龄段)
EVENTS_CHILD = [
    "你在玩耍时捡到了一枚废弃的弹壳，对军事产生了兴趣。",
    "你在学校里因为保护同学打了一架，展现了惊人的格斗天赋。",
    "你在这个动荡的世界里学会了如何快速寻找掩体。",
    "你的家人教你如何使用无线电通讯。"
]

EVENTS_MILITARY_EARLY = [
    你正式参军，并在新兵训练营打破了障碍赛的记录。,
    你被选中参加特种空勤团 (SAS) 的选拔。,
    你在一次边境冲突中第一次在实战中开火。,
    你学会了如何在极端环境下生存。
]

# --- 核心逻辑类 ---

class CoDLifeSim
    def __init__(self, root)
        self.root = root
        self.root.title(COD Universe Life Simulator  Created by Yulia Riley)
        self.root.geometry(900x700)
        self.root.configure(bg=#1e1e1e) # 深色战术风格背景

        # 样式设置
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(TLabel, foreground=white, background=#1e1e1e, font=(Arial, 10))
        style.configure(TButton, foreground=white, background=#4a5a4a, font=(Arial, 10, bold))
        style.configure(TEntry, fieldbackground=#333333, foreground=white)

        self.relationships = {} # 存储与角色的关系值
        self.is_alive = True
        self.setup_ui()

    def setup_ui(self)
        # 顶部：输入区
        input_frame = tk.Frame(self.root, bg=#2b2b2b, bd=2, relief=groove)
        input_frame.pack(fill=x, padx=10, pady=10)

        # 姓名
        tk.Label(input_frame, text=姓名 (留空随机), bg=#2b2b2b, fg=white).grid(row=0, column=0, padx=5, pady=5)
        self.entry_name = ttk.Entry(input_frame)
        self.entry_name.grid(row=0, column=1, padx=5)

        # 性别
        tk.Label(input_frame, text=性别 (留空随机), bg=#2b2b2b, fg=white).grid(row=0, column=2, padx=5)
        self.entry_gender = ttk.Entry(input_frame)
        self.entry_gender.grid(row=0, column=3, padx=5)

        # 初始年龄
        tk.Label(input_frame, text=初始年龄 (1-99), bg=#2b2b2b, fg=white).grid(row=1, column=0, padx=5)
        self.entry_age = ttk.Entry(input_frame)
        self.entry_age.insert(0, 1)
        self.entry_age.grid(row=1, column=1, padx=5)

        # 外貌
        tk.Label(input_frame, text=外貌特征 (留空生成), bg=#2b2b2b, fg=white).grid(row=1, column=2, padx=5)
        self.entry_looks = ttk.Entry(input_frame)
        self.entry_looks.grid(row=1, column=3, padx=5)

        # 按钮区
        btn_frame = tk.Frame(self.root, bg=#1e1e1e)
        btn_frame.pack(pady=5)
        
        ttk.Button(btn_frame, text=🎲 随机生成身份, command=self.randomize_inputs).pack(side=left, padx=10)
        ttk.Button(btn_frame, text=🚀 开始模拟人生, command=self.start_simulation).pack(side=left, padx=10)

        # 中部：主要文本显示区
        self.output_text = scrolledtext.ScrolledText(self.root, bg=#000000, fg=#00FF00, font=(Consolas, 10), wrap=tk.WORD)
        self.output_text.pack(expand=True, fill=both, padx=10, pady=5)

    def randomize_inputs(self)
        names = [Alex, Roach, Frost, Yuri, Echo, Viper, Raptor]
        last_names = [Mason, Woods, Sanderson, Allen, Riley (No Relation), Chang]
        genders = [男, 女]
        looks = [左眼有刀疤, 戴着黑色面罩, 身材高大魁梧, 眼神锐利, 总戴着战术墨镜, 有一条机械义肢]

        self.entry_name.delete(0, tk.END)
        self.entry_name.insert(0, f{random.choice(names)} {random.choice(last_names)})
        
        self.entry_gender.delete(0, tk.END)
        self.entry_gender.insert(0, random.choice(genders))
        
        self.entry_looks.delete(0, tk.END)
        self.entry_looks.insert(0, random.choice(looks))

    def log(self, text)
        self.output_text.insert(tk.END, text + n)
        self.output_text.see(tk.END)

    def init_relationships(self)
        self.relationships = {}
        for faction, chars in COD_CHARACTERS.items()
            for char in chars
                self.relationships[char] = 0 # 0 = 陌生, 50 = 友善爱慕,  -20 = 敌对

    def get_relationship_desc(self, score)
        if score  80 return 【灵魂伴侣生死之交】
        if score  50 return 【亲密战友】
        if score  20 return 【熟人】
        if score  -50 return 【死敌】
        if score  -20 return 【关系紧张】
        return 【点头之交】

    def interaction_event(self, age)
        # 随机选择一个角色进行互动
        faction = random.choice(list(COD_CHARACTERS.keys()))
        char = random.choice(COD_CHARACTERS[faction])
        
        event_type = random.choice([friendly, conflict, romance, mission])
        
        if char == General Shepherd and age  25
            # 谢菲尔德特殊事件
            if random.random()  0.1
                self.log(f⚠️ [重大危机] {age}岁：谢菲尔德将军在任务简报中对你隐瞒了关键情报。你察觉到了背叛的气息。)
                self.relationships[char] -= 50
                return

        if event_type == friendly
            self.relationships[char] += random.randint(5, 15)
            events = [
                f你和 {char} 在食堂分享了一瓶威士忌，聊起了家乡。,
                f在训练中，{char} 拉了你一把，把你从泥潭里拽了出来。,
                f{char} 称赞了你的枪法。
            ]
            self.log(f🤝 [社交] {age}岁：{random.choice(events)} (关系 {self.relationships[char]}))

        elif event_type == conflict
            self.relationships[char] -= random.randint(5, 15)
            events = [
                f你和 {char} 在战术执行上发生了激烈的争吵。,
                f{char} 嘲笑了你的装备选择，你们差点打起来。,
                f一次误会导致你和 {char} 互相冷战了几个月。
            ]
            self.log(f💢 [冲突] {age}岁：{random.choice(events)} (关系 {self.relationships[char]}))

        elif event_type == romance and age  18
            if self.relationships[char]  40 # 只有好感度足够才触发
                self.relationships[char] += 20
                events = [
                    f在撤离的直升机上，{char} 紧紧握住了你的手，眼神中流露出一丝温柔。,
                    f{char} 在深夜悄悄为你包扎伤口，气氛变得有些暧昧。,
                    f你们在安全屋度过了一个难得的宁静夜晚，{char} 对你吐露了心声。
                ]
                self.log(f❤️ [情感] {age}岁：{random.choice(events)} {self.get_relationship_desc(self.relationships[char])})

        elif event_type == mission
             self.relationships[char] += 5
             scenarios = [
                 f你与 {char} 被派往乌兹别克斯坦执行潜入任务。,
                 f在福尔丹斯克，你和 {char} 共同抵御了一波又一波的攻击。,
                 f你负责为 {char} 提供狙击掩护，配合完美。
             ]
             self.log(f🔫 [任务] {age}岁：{random.choice(scenarios)})

    def start_simulation(self)
        # 获取输入
        name = self.entry_name.get() or Unknown Soldier
        gender = self.entry_gender.get() or Unknown
        looks = self.entry_looks.get() or Standard military issue
        try
            start_age = int(self.entry_age.get())
        except
            start_age = 1

        # 重置
        self.output_text.delete(1.0, tk.END)
        self.init_relationships()
        self.is_alive = True

        # 头部信息
        self.log(=60)
        self.log(f档案建立 {name}  性别 {gender}  外貌 {looks})
        self.log(正在连接 COD 世界服务器... 模拟开始...)
        self.log(=60)

        # 循环年份
        for age in range(start_age, 100)
            if not self.is_alive
                break
            
            # 死亡判定 (年龄越大，或者任务中运气极差)
            death_chance = 0.005 if age  50 else (age - 50)  0.002
            if age  80 death_chance += 0.1
            
            if random.random()  death_chance
                causes = [在一次秘密行动中光荣牺牲, 因旧伤复发在医院去世, 在睡梦中安详离世, 为了掩护队友撤离引爆了手雷]
                self.log(fn💀 [死亡] {age}岁：你{random.choice(causes)}。)
                self.is_alive = False
                break

            # 年龄段逻辑
            if age  18
                if random.random()  0.3
                    self.log(f👶 [成长] {age}岁：{random.choice(EVENTS_CHILD)})
            
            elif age == 18
                self.log(f🪖 [转折] {age}岁：你成年了。你决定加入军队，开始你的军事生涯。)
            
            elif 18  age  60
                # 每年发生1-2个事件
                if random.random()  0.7
                    self.interaction_event(age)
                
                # 随机特殊剧情
                if random.random()  0.05
                     self.log(f🎖️ [晋升] {age}岁：由于表现优异，你的军衔得到了提升。)
            
            else # 60岁以上
                if random.random()  0.4
                    retirement_events = [
                        Price 上尉（虽然很老了）来看望你，你们一起抽了雪茄。,
                        你收到了以前救过的新兵寄来的感谢信。,
                        你因为旧伤在雨天感到疼痛。,
                        你在军事学院担任客座讲师，讲述当年的传奇故事。
                    ]
                    self.log(f☕ [退休] {age}岁：{random.choice(retirement_events)})

            # 更新UI防止卡顿
            self.root.update()
            # time.sleep(0.05) # 如果想慢慢看可以取消注释

        # 结束总结
        if not self.is_alive or age == 99
            self.log(n + =60)
            self.log(【生涯总结 - 人际关系网】)
            sorted_rels = sorted(self.relationships.items(), key=lambda x x[1], reverse=True)
            for char, score in sorted_rels
                if score != 0
                    self.log(f{char} {score} {self.get_relationship_desc(score)})
            self.log(=60)
            self.log(SIMULATION COMPLETE.)

# --- 运行程序 ---
if __name__ == __main__
    root = tk.Tk()
    app = CoDLifeSim(root)
    root.mainloop()