import streamlit as st
from divination_agent import DivinationAgent
from chart_generator import ChartGenerator
import time
import os
import random
import base64
from io import BytesIO

# 设置页面配置
st.set_page_config(
    page_title="🔮 智能占卜师",
    page_icon="🔮",
    layout="wide"
)

# 添加自定义CSS样式
st.markdown("""
<style>
    /* 页面背景和整体样式 */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4edf5 100%);
        animation: gradientShift 8s ease-in-out infinite;
    }
    
    /* 渐变背景动画 */
    @keyframes gradientShift {
        0%, 100% { background: linear-gradient(135deg, #f5f7fa 0%, #e4edf5 100%); }
        50% { background: linear-gradient(135deg, #e4edf5 0%, #f5f7fa 100%); }
    }
    
    /* 主标题动画效果 */
    .main-header {
        text-align: center;
        color: #8E44AD;
        font-family: 'Arial', sans-serif;
        animation: fadeInDown 1s ease-out, titleGlow 3s ease-in-out infinite alternate;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        position: relative;
    }
    
    /* 标题发光效果 */
    @keyframes titleGlow {
        0% { text-shadow: 2px 2px 4px rgba(0,0,0,0.1), 0 0 10px rgba(142, 68, 173, 0.3); }
        100% { text-shadow: 2px 2px 4px rgba(0,0,0,0.1), 0 0 20px rgba(142, 68, 173, 0.6); }
    }
    
    /* 卡片样式优化 */
    .divination-card {
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        transition: all 0.3s ease;
        animation: fadeIn 0.8s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .divination-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .divination-card:hover::before {
        left: 100%;
    }
    
    .divination-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 12px 24px rgba(0,0,0,0.15);
    }
    
    /* 结果容器优化 - 改善文字显示 */
    .result-container {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 15px;
        padding: 25px 30px;
        margin-top: 25px;
        border-left: 6px solid #8E44AD;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        line-height: 1.8;
        font-size: 16px;
        color: #2c3e50;
        transition: all 0.3s ease;
        animation: slideInUp 0.6s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .result-container::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #8E44AD 0%, #9b59b6 100%);
        border-radius: 0 15px 0 60px;
        opacity: 0.1;
    }
    
    /* 改善文本样式 */
    .result-container p {
        margin-bottom: 1.2em;
        line-height: 1.8;
        position: relative;
        z-index: 1;
    }
    
    .result-container ul, .result-container ol {
        margin-bottom: 1.2em;
        padding-left: 1.5em;
    }
    
    .result-container li {
        margin-bottom: 0.5em;
        line-height: 1.7;
    }
    
    .result-container strong {
        color: #8E44AD;
        font-weight: 600;
        position: relative;
    }
    
    .result-container strong::after {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, #8E44AD, #9b59b6);
        animation: underlineGlow 2s ease-in-out infinite alternate;
    }
    
    @keyframes underlineGlow {
        0% { opacity: 0.3; }
        100% { opacity: 0.8; }
    }
    
    .result-container em {
        color: #9b59b6;
        font-style: italic;
        background: linear-gradient(90deg, transparent, rgba(155, 89, 182, 0.1), transparent);
        padding: 2px 4px;
        border-radius: 3px;
    }
    
    .result-container:hover {
        box-shadow: 0 6px 16px rgba(0,0,0,0.12);
        transform: translateX(2px);
    }
    
    /* 侧边栏样式 */
    .sidebar-content {
        font-family: 'Arial', sans-serif;
        animation: fadeIn 1s ease-out;
    }
    
    /* 按钮样式优化 */
    .stButton>button {
        background: linear-gradient(135deg, #8E44AD 0%, #9b59b6 100%);
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton>button:hover::before {
        left: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        background: linear-gradient(135deg, #9b59b6 0%, #8E44AD 100%);
    }
    
    /* 下拉框样式 */
    .stSelectbox>div>div {
        background-color: #f0f2f6;
        border-radius: 8px;
        border: 1px solid #d1d5db;
        transition: all 0.3s ease;
    }
    
    .stSelectbox>div>div:hover {
        border-color: #8E44AD;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* AI徽章样式 */
    .ai-badge {
        background: linear-gradient(135deg, #9b59b6 0%, #8E44AD 100%);
        color: white;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.85em;
        margin-left: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        animation: pulse 2s infinite, bounce 3s infinite;
    }
    
    /* 模型信息样式 */
    .model-info {
        background: linear-gradient(135deg, #e8f4f8 0%, #d1ecf1 100%);
        border-radius: 10px;
        padding: 15px;
        margin-top: 15px;
        font-size: 0.95em;
        border: 1px solid #bee5eb;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .model-info:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* 过程步骤样式 */
    .process-step {
        background: linear-gradient(135deg, #e8f4f8 0%, #d1ecf1 100%);
        border-radius: 10px;
        padding: 15px;
        margin: 8px 0;
        font-size: 0.95em;
        border-left: 4px solid #8E44AD;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        animation: fadeInUp 0.5s ease-out;
        position: relative;
    }
    
    .process-step::after {
        content: '✨';
        position: absolute;
        right: 15px;
        top: 50%;
        transform: translateY(-50%);
        opacity: 0.7;
        animation: sparkle 1.5s infinite;
    }
    
    @keyframes sparkle {
        0%, 100% { opacity: 0.7; transform: translateY(-50%) scale(1); }
        50% { opacity: 1; transform: translateY(-50%) scale(1.2); }
    }
    
    .process-step:hover {
        transform: translateX(5px) scale(1.02);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border-left-color: #9b59b6;
    }
    
    /* 卦象显示样式 */
    .hexagram-display {
        text-align: center;
        font-size: 2.2em;
        font-weight: bold;
        margin: 25px 0;
        color: #8E44AD;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        animation: bounceIn 1s ease-out, float 3s ease-in-out infinite;
    }
    
    /* 浮动效果 */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    /* 可视化容器样式 */
    .visualization-container {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 15px;
        padding: 25px;
        margin: 25px 0;
        box-shadow: 0 6px 12px rgba(0,0,0,0.08);
        border: 1px solid #e9ecef;
        transition: all 0.3s ease;
        animation: zoomIn 0.6s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .visualization-container::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #8E44AD, #9b59b6, #3498db, #e74c3c);
        border-radius: 15px;
        z-index: -1;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .visualization-container:hover::before {
        opacity: 0.3;
    }
    
    .visualization-container:hover {
        box-shadow: 0 8px 16px rgba(0,0,0,0.12);
        transform: scale(1.01);
    }
    
    /* 爻线样式 */
    .yao-line {
        text-align: center;
        font-size: 2.2em;
        margin: 8px 0;
        padding: 15px;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        animation: slideIn 0.5s ease-out;
    }
    
    .yao-line:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        background: linear-gradient(135deg, #e9ecef 0%, #f8f9fa 100%);
    }
    
    /* 流式文本样式优化 */
    .stream-text {
        white-space: pre-wrap;
        font-family: 'Microsoft YaHei', 'SimHei', Arial, sans-serif;
        line-height: 1.8;
        color: #2c3e50;
        font-size: 16px;
        position: relative;
    }
    
    .stream-text::after {
        content: '✨';
        animation: sparkle 1.5s infinite;
        margin-left: 5px;
    }
    
    @keyframes sparkle {
        0%, 100% { opacity: 0; transform: scale(0.8); }
        50% { opacity: 1; transform: scale(1.2); }
    }
    
    /* 图表容器样式 */
    .chart-container {
        text-align: center;
        margin: 15px 0;
        padding: 15px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        animation: fadeIn 0.8s ease-out;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .chart-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #8E44AD, #9b59b6, #3498db);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .chart-container:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.12);
    }
    
    /* 图表图片样式 */
    .chart-container img {
        max-width: 100%;
        height: auto;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .chart-container:hover img {
        transform: scale(1.02);
        filter: brightness(1.05);
    }
    
    /* 动画关键帧 */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes zoomIn {
        from {
            opacity: 0;
            transform: scale(0.95);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    @keyframes bounceIn {
        0% {
            opacity: 0;
            transform: scale(0.3);
        }
        50% {
            transform: scale(1.05);
        }
        70% {
            transform: scale(0.9);
        }
        100% {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(155, 89, 182, 0.4);
        }
        70% {
            box-shadow: 0 0 0 10px rgba(155, 89, 182, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(155, 89, 182, 0);
        }
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% {
            transform: translateY(0);
        }
        40% {
            transform: translateY(-10px);
        }
        60% {
            transform: translateY(-5px);
        }
    }
    
    /* 打字机效果 */
    .typing-effect {
        overflow: hidden;
        border-right: .15em solid #8E44AD;
        white-space: pre-wrap;
        animation: typing 3.5s steps(40, end), blink-caret .75s step-end infinite;
    }
    
    @keyframes typing {
        from { width: 0 }
        to { width: 100% }
    }
    
    @keyframes blink-caret {
        from, to { border-color: transparent }
        50% { border-color: #8E44AD; }
    }
    
    /* 滚动条美化 */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #8E44AD 0%, #9b59b6 100%);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #8E44AD;
    }
    
    /* 输入框样式 */
    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 12px 15px;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #8E44AD;
        box-shadow: 0 0 0 3px rgba(142, 68, 173, 0.1);
        outline: none;
    }
    
    /* 聊天消息样式 */
    .stChatMessage {
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        animation: messageSlide 0.5s ease-out;
    }
    
    @keyframes messageSlide {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* 加载动画 */
    .loading-dots {
        display: inline-block;
    }
    
    .loading-dots::after {
        content: '';
        animation: dots 1.5s infinite;
    }
    
    @keyframes dots {
        0%, 20% { content: ''; }
        40% { content: '.'; }
        60% { content: '..'; }
        80%, 100% { content: '...'; }
    }
</style>
""", unsafe_allow_html=True)

# 页面标题
st.markdown("<h1 class='main-header'>🔮 智能占卜师 <span class='ai-badge'>AI增强版</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2em;'>探索传统智慧，指引人生方向</p>", unsafe_allow_html=True)

# 初始化session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# 初始化API密钥
if "api_key" not in st.session_state:
    st.session_state.api_key = os.getenv("MODELSCOPE_API_KEY", "ms-df56303c-e814-48da-a195-3dc2487c3b33")

# 初始化占卜智能体
divination_agent = DivinationAgent(api_key=st.session_state.api_key)
chart_generator = ChartGenerator()

# 侧边栏设置
with st.sidebar:
    st.markdown("<div class='sidebar-content'>", unsafe_allow_html=True)
    st.header("⚙️ 占卜设置")
    
    # API密钥输入
    api_key_input = st.text_input(
        "ModelScope API密钥",
        value=st.session_state.api_key,
        type="password",
        help="请输入您的ModelScope API密钥以使用AI占卜功能"
    )
    
    # 保存API密钥按钮
    if st.button("💾 保存API密钥", use_container_width=True):
        if api_key_input and api_key_input != st.session_state.api_key:
            st.session_state.api_key = api_key_input
            # 重新初始化占卜智能体
            divination_agent = DivinationAgent(api_key=st.session_state.api_key)
            st.success("API密钥已保存并更新！")
        elif api_key_input == st.session_state.api_key:
            st.info("API密钥没有变化")
        else:
            st.warning("请输入API密钥")
    
    st.divider()
    
    divination_type = st.selectbox(
        "选择占卜方式",
        ["梅花易数", "天干地支", "六爻", "紫微斗数"]
    )
    
    st.divider()
    st.subheader("🔮 占卜介绍")
    
    divination_descriptions = {
        "梅花易数": "宋代邵雍所创，以数字起卦，简便易学。",
        "天干地支": "中国古代纪年法，包含十天干十二地支。",
        "六爻": "《易经》占卜法，通过六根爻线组成卦象。",
        "紫微斗数": "传统命理学，分析星曜分布预测命运。"
    }
    
    st.info(f"**{divination_type}**\n\n{divination_descriptions[divination_type]}")
    
    st.divider()
    st.subheader("🤖 AI模型信息")
    st.markdown("""
    <div class="model-info">
        <strong>模型</strong>: Qwen3-235B<br>
        <strong>平台</strong>: ModelScope<br>
        <strong>功能</strong>: 专业占卜解读
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    if st.button("🗑️ 清除对话历史"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.subheader("⚠️ 免责声明")
    st.caption("本系统仅供娱乐和学习使用，占卜结果仅供参考，不应作为决策的唯一依据。")
    
    st.markdown("</div>", unsafe_allow_html=True)

# 艺术字显示 - 当对话历史为空时
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div style="
        text-align: center;
        margin: 100px 0;
        animation: fadeIn 2s ease-out, float 3s ease-in-out infinite;
        position: relative;
        padding: 40px 20px;
    ">
        <div style="
            font-size: 3.5em;
            font-weight: 900;
            background: linear-gradient(135deg, #8E44AD 0%, #9b59b6 50%, #3498db 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-size: 200% 200%;
            animation: gradientShift 3s ease-in-out infinite;
            -webkit-text-stroke: 2px rgba(255,255,255,0.8);
            text-shadow: 
                0 0 20px rgba(142, 68, 173, 0.5);
            font-family: 'Microsoft YaHei', 'SimHei', 'Arial', sans-serif;
            position: relative;
            z-index: 1;
        ">
            献给我亲爱的树树
        </div>
        <div style="
            font-size: 1.2em;
            color: #7f8c8d;
            margin-top: 20px;
        </div>
        <div style="
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle at center, rgba(255,255,255,0.3) 0%, transparent 70%);
            animation: sparkle 2s infinite;
            opacity: 0.7;
        "></div>
    </div>
    """, unsafe_allow_html=True)

# 显示对话历史
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            st.markdown(f"<div class='result-container'>{message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(message["content"])

# 用户输入
if prompt := st.chat_input("请输入您想占卜的问题..."):
    # 添加用户消息到历史记录
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 添加助手响应到历史记录
    with st.chat_message("assistant"):
        # 显示占卜过程
        process_placeholder = st.empty()
        
        # 占卜过程动画
        if divination_type == "梅花易数":
            process_steps = [
                "🔮 启动梅花易数占卜程序...",
                "🌀 生成随机数字...",
                "🔢 计算卦象...",
                "📊 分析卦象含义...",
                "🧠 调用AI模型进行深度解读...",
                "📈 等待AI模型返回结果...",
                "✅ 占卜完成！"
            ]
        elif divination_type == "天干地支":
            process_steps = [
                "🔮 启动天干地支占卜程序...",
                "🌀 推算天干...",
                "🔢 推算地支...",
                "📊 组合干支...",
                "🧠 调用AI模型进行深度解读...",
                "📈 等待AI模型返回结果...",
                "✅ 占卜完成！"
            ]
        elif divination_type == "六爻":
            process_steps = [
                "🔮 启动六爻占卜程序...",
                "🌀 抛掷第一爻...",
                "🔢 抛掷第二爻...",
                "📊 抛掷第三爻...",
                "🧠 抛掷第四爻...",
                "🔮 抛掷第五爻...",
                "✨ 抛掷第六爻...",
                "📊 绘制卦象...",
                "🧠 调用AI模型进行深度解读...",
                "📈 等待AI模型返回结果...",
                "✅ 占卜完成！"
            ]
        else:  # 紫微斗数
            process_steps = [
                "🔮 启动紫微斗数占卜程序...",
                "🌀 推算命宫...",
                "🔢 分析主星...",
                "📊 定位宫位...",
                "🧠 调用AI模型进行深度解读...",
                "📈 等待AI模型返回结果...",
                "✅ 占卜完成！"
            ]
        
        # 显示过程步骤（除了最后一步）
        process_text = ""
        for i, step in enumerate(process_steps[:-1]):  # 不显示最后一步"占卜完成"
            process_text += f"<div class='process-step'>步骤 {i+1}: {step}</div>"
            process_placeholder.markdown(process_text, unsafe_allow_html=True)
            time.sleep(0.5)
        
        # 执行占卜（这会等待AI返回结果）
        try:
            # 显示卦象图表
            hexagram_placeholder = st.empty()
            chart_placeholder = st.empty()
            
            if divination_type == "六爻":
                # 提取爻线信息
                lines = ["———", "-- --"]  # 阳爻和阴爻
                yao_lines = []
                for _ in range(6):
                    yao_lines.append(random.choice(lines))
                
                # 显示卦象
                hexagram_html = "<div class='hexagram-display'>六爻卦象</div>"
                hexagram_html += "<div class='visualization-container'>"
                hexagram_html += "<h3>📊 卦象展示</h3>"
                for i, line in enumerate(reversed(yao_lines)):  # 从下到上显示
                    hexagram_html += f"<div class='yao-line'>{line}</div>"
                hexagram_html += "</div>"
                hexagram_placeholder.markdown(hexagram_html, unsafe_allow_html=True)
                
                # 生成六爻卦象图表
                try:
                    chart_data = chart_generator.generate_six_yao_chart(yao_lines)
                    chart_html = f"""
                    <div class='chart-container'>
                        <h3>📈 六爻卦象可视化</h3>
                        <img src='{chart_data}' style='max-width: 100%; height: auto; border-radius: 10px;' />
                    </div>
                    """
                    chart_placeholder.markdown(chart_html, unsafe_allow_html=True)
                except Exception as e:
                    st.warning(f"图表生成失败: {str(e)}")
            
            elif divination_type == "天干地支":
                # 模拟天干地支
                heavenly_stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
                earthly_branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
                stem = random.choice(heavenly_stems)
                branch = random.choice(earthly_branches)
                
                # 显示天干地支
                hexagram_html = f"<div class='hexagram-display'>天干地支：{stem}{branch}</div>"
                hexagram_html += "<div class='visualization-container'>"
                hexagram_html += "<h3>📊 干支详情</h3>"
                hexagram_html += f"<p><strong>天干</strong>：{stem}</p>"
                hexagram_html += f"<p><strong>地支</strong>：{branch}</p>"
                hexagram_html += f"<p><strong>组合</strong>：{stem}{branch}</p>"
                hexagram_html += "</div>"
                hexagram_placeholder.markdown(hexagram_html, unsafe_allow_html=True)
                
                # 生成天干地支图表
                try:
                    chart_data = chart_generator.generate_heavenly_stems_chart(stem, branch)
                    chart_html = f"""
                    <div class='chart-container'>
                        <h3>📈 天干地支关系图</h3>
                        <img src='{chart_data}' style='max-width: 100%; height: auto; border-radius: 10px;' />
                    </div>
                    """
                    chart_placeholder.markdown(chart_html, unsafe_allow_html=True)
                except Exception as e:
                    st.warning(f"图表生成失败: {str(e)}")
            
            elif divination_type == "梅花易数":
                # 模拟数字
                numbers = [random.randint(1, 8) for _ in range(3)]
                
                # 显示数字
                hexagram_html = f"<div class='hexagram-display'>梅花易数：{numbers[0]}, {numbers[1]}, {numbers[2]}</div>"
                hexagram_html += "<div class='visualization-container'>"
                hexagram_html += "<h3>📊 数字详情</h3>"
                hexagram_html += f"<p><strong>数字1</strong>：{numbers[0]}</p>"
                hexagram_html += f"<p><strong>数字2</strong>：{numbers[1]}</p>"
                hexagram_html += f"<p><strong>数字3</strong>：{numbers[2]}</p>"
                hexagram_html += "</div>"
                hexagram_placeholder.markdown(hexagram_html, unsafe_allow_html=True)
                
                # 生成梅花易数图表
                try:
                    chart_data = chart_generator.generate_plum_blossom_chart(numbers)
                    chart_html = f"""
                    <div class='chart-container'>
                        <h3>📈 梅花易数数字分布</h3>
                        <img src='{chart_data}' style='max-width: 100%; height: auto; border-radius: 10px;' />
                    </div>
                    """
                    chart_placeholder.markdown(chart_html, unsafe_allow_html=True)
                except Exception as e:
                    st.warning(f"图表生成失败: {str(e)}")
            
            # 检查API密钥是否设置
            if not st.session_state.api_key:
                # 显示API密钥未设置的提示
                process_text += f"<div class='process-step'>步骤 {len(process_steps)}: {process_steps[-1]}</div>"
                process_placeholder.markdown(process_text, unsafe_allow_html=True)
                time.sleep(0.5)
                process_placeholder.empty()
                
                warning_msg = "⚠️ API密钥未设置或使用默认密钥，无法调用AI模型进行深度解读。请在侧边栏输入您的ModelScope API密钥以启用AI功能。"
                st.warning(warning_msg)
                st.session_state.messages.append({"role": "assistant", "content": warning_msg})
            else:
                # 现在显示最后一步"占卜完成"
                process_text += f"<div class='process-step'>步骤 {len(process_steps)}: {process_steps[-1]}</div>"
                process_placeholder.markdown(process_text, unsafe_allow_html=True)
                
                # 等待一小段时间让用户看到"占卜完成"
                time.sleep(0.5)
                
                # 清除过程显示
                process_placeholder.empty()
                
                # 流式输出结果
                result_placeholder = st.empty()
                result_text = ""
                
                # 使用流式输出
                try:
                    for chunk in divination_agent.run_divination_stream(divination_type, prompt):
                        result_text += chunk
                        result_placeholder.markdown(f"<div class='result-container'><div class='stream-text'>{result_text}</div></div>", unsafe_allow_html=True)
                    
                    # 确保最终完整结果显示
                    result_placeholder.markdown(f"<div class='result-container'><div class='stream-text'>{result_text}</div></div>", unsafe_allow_html=True)
                    st.session_state.messages.append({"role": "assistant", "content": result_text})
                except Exception as ai_error:
                    # 清除过程显示
                    process_placeholder.empty()
                    
                    # 处理AI错误
                    error_msg = f"❌ AI解读失败：{str(ai_error)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
        except Exception as e:
            # 清除过程显示
            process_placeholder.empty()
            
            # 显示错误信息
            error_msg = f"❌ 占卜过程中出现错误：{str(e)}"
            st.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
