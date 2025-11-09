# 智能占卜师 (AI增强版)

基于LangChain和Streamlit的智能占卜系统，支持多种传统占卜方法，现已集成ModelScope的Qwen大模型提供AI解读。

## 功能特点

- 支持多种占卜方法：梅花易数、天干地支、六爻、紫微斗数等
- 精美的Streamlit前端界面
- 对话式交互体验
- AI增强解读（基于Qwen3-235B大模型）
- 可扩展的智能体架构

## 安装步骤

### 方法一：使用安装脚本（推荐）

```bash
# 给脚本添加执行权限
chmod +x install.sh

# 运行安装脚本
./install.sh
```

### 方法二：手动安装

1. 克隆项目：
   ```bash
   git clone <repository-url>
   cd divination
   ```

2. 创建虚拟环境（推荐）：
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或者在Windows上: venv\Scripts\activate
   ```

3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

4. 配置环境变量：
   编辑 `.env` 文件，添加您的ModelScope API密钥：
   ```
   MODELSCOPE_API_KEY=your_modelscope_api_key_here
   ```

## 运行应用

```bash
streamlit run app.py
```

应用将在浏览器中打开，默认地址为 `http://localhost:8501`

## 使用说明

1. 在左侧选择占卜方式
2. 在输入框中输入您想占卜的问题
3. 点击回车或发送按钮
4. 等待系统生成占卜结果和AI解读

## 项目结构

```
divination/
├── app.py              # Streamlit应用主文件
├── divination_agent.py # 占卜智能体核心逻辑
├── requirements.txt    # 项目依赖
├── .env               # 环境变量配置文件
├── install.sh         # 自动安装脚本
├── test_agent.py      # 占卜智能体测试脚本
└── README.md          # 项目说明文档
```

## 占卜方法介绍

### 梅花易数
梅花易数是宋代易学家邵雍所创的一种占卜方法，以数字起卦，简便易学。

### 天干地支
天干地支是中国古代用来记录年、月、日、时的方法，共有十天干和十二地支。

### 六爻
六爻是《易经》占卜的主要方法，通过投掷硬币或蓍草得到六根爻线，组成卦象进行解读。

### 紫微斗数
紫微斗数是中国传统命理学中的一种重要方法，通过分析星曜在十二宫位的分布来预测命运。

## AI增强功能

本项目集成了ModelScope平台的Qwen3-235B大模型，为占卜结果提供专业的AI解读：
- 更深入的卦象解析
- 针对具体问题的个性化建议
- 通俗易懂的智慧指导

## 扩展开发

您可以根据需要添加更多占卜方法：

1. 在 [divination_agent.py](file:///Users/rayss/AI/divination/divination_agent.py) 中添加新的占卜函数
2. 在 [divination_agent.py](file:///Users/rayss/AI/divination/divination_agent.py) 的 [run_divination](file:///Users/rayss/AI/divination/divination_agent.py#L197-L208) 方法中添加对应的条件分支
3. 在 [app.py](file:///Users/rayss/AI/divination/app.py) 的下拉选择框中添加新的占卜方式选项

## 注意事项

- 本项目仅供娱乐和学习使用
- 占卜结果仅供参考，不应作为决策的唯一依据
- AI解读基于Qwen3-235B大模型，结果可能因模型理解而异