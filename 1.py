import streamlit as st
import random
import time

# --- 页面基础配置 ---
st.set_page_config(
    page_title="COD Universe: Life Simulator",
    page_icon="🪖",
    layout="wide"
)

# --- 样式美化 ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    .stButton>button { background-color: #2E7D32; color: white; border-radius: 5px; border: none; width: 100%; }
    .log-text { font-family: 'Courier New', monospace; padding: 8px; border-left: 3px solid #4CAF50; background-color: #262730; margin-bottom: 5px; border-radius: 4px; }
    .highlight-141 { color: #64B5F6; font-weight: bold; } /* TF141 蓝色 */
    .highlight-kortac { color: #FF8A65; font-weight: bold; } /* KorTac 橙色 */
    .highlight-enemy { color: #E57373; font-weight: bold; } /* 敌人 红色 */
</style>
""", unsafe_allow_html=True)

# --- 游戏数据 (请注意：所有中文文本都被英文引号包裹) ---
COD_CHARACTERS = {
    "TF141": ["Captain Price", "Soap", "Ghost", "Gaz", "Alejandro"],
    "KorTac": ["König", "Horangi", "Stiletto"],
    "Chimera": ["Krueger", "Nikto", "Nikolai"],
    "Villains": ["General Shepherd", "Makarov", "Valeria", "Graves"]
}

# 基础事件库
EVENTS_CHILD = [
    "你在玩耍时捡到了一枚废弃的弹壳，对军事产生了兴趣。",
    "你在学校里因为保护同学打了一架，展现了惊人的格斗天赋。",
    "你在这个动荡的世界里学会了如何快速寻找掩体。",
    "你的家人教你如何使用无线电通讯。"
]

EVENTS_MILITARY_EARLY = [
    "你正式参军，并在新兵训练营打破了障碍赛的记录。",
    "你被选中参加特种空勤团 (SAS) 的选拔。",
    "你在一次边境冲突中第一次在实战中开火。",
    "你学会了如何在极端环境下生存。"
]

# --- 核心逻辑 ---
def get_relationship_desc(score):
    if score > 80: return "生死之交"
    if score > 50: return "亲密战友"
    if score > 20: return "熟人"
    if score < -50: return "死敌"
    if score < -20: return "关系紧张"
    return "点头之交"

def run_simulation(name, gender, start_age, looks):
    logs = []
    # 初始化所有角色的关系为0
    relationships = {}
    for faction in COD_CHARACTERS.values():
        for char in faction:
            relationships[char] = 0
            
    is_alive = True
    
    # 开头
    logs.append(f"📁 **档案建立**: {name} | 性别: {gender}")
    logs.append(f"👁️ **外貌特征**: {looks}")
    logs.append("