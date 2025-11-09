#!/bin/bash

# 智能占卜师安装脚本

echo "🔮 开始安装智能占卜师项目依赖..."

# 检查是否安装了Python
if ! command -v python3 &> /dev/null
then
    echo "❌ 未找到Python3，请先安装Python3"
    exit 1
fi

echo "✅ 找到Python3"

# 检查是否安装了pip
if ! command -v pip3 &> /dev/null
then
    echo "❌ 未找到pip3，请先安装pip3"
    exit 1
fi

echo "✅ 找到pip3"

# 创建虚拟环境（可选）
echo "🔧 创建虚拟环境..."
python3 -m venv venv

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 升级pip
echo "🔧 升级pip..."
pip install --upgrade pip

# 安装依赖
echo "🔧 安装项目依赖..."
pip install -r requirements.txt

echo "✅ 依赖安装完成！"

echo "🚀 启动应用..."
echo "请运行以下命令启动应用："
echo "source venv/bin/activate"
echo "streamlit run app.py"

echo "💡 提示："
echo "1. 请确保已配置OPENAI_API_KEY环境变量以使用高级功能"
echo "2. 应用启动后将在浏览器中打开"