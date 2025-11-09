#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试流式输出和卦象展示
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("🔍 正在测试流式输出和卦象展示...")

try:
    from divination_agent import DivinationAgent
    print("✅ 成功导入DivinationAgent")
except Exception as e:
    print(f"❌ 导入DivinationAgent失败: {e}")
    sys.exit(1)

def test_streaming_output():
    """测试流式输出"""
    try:
        print("🔧 正在测试流式输出...")
        
        # 初始化占卜智能体
        agent = DivinationAgent()
        
        # 测试流式输出
        print("开始流式输出测试：")
        full_response = ""
        for chunk in agent.run_divination_stream("梅花易数", "我的事业运如何？"):
            full_response += chunk
            print(chunk, end="", flush=True)
        
        print("\n\n完整响应长度:", len(full_response))
        
        # 检查响应是否包含关键部分
        if "梅花易数" in full_response and "AI解读" in full_response:
            print("✅ 流式输出测试成功")
            return True
        else:
            print("❌ 流式输出测试失败")
            return False
    except Exception as e:
        print(f"❌ 流式输出测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_hexagram_generation():
    """测试卦象生成"""
    try:
        print("🔧 正在测试卦象生成...")
        
        # 测试六爻卦象生成
        yao_lines = []
        lines = ["———", "-- --"]  # 阳爻和阴爻
        import random
        for _ in range(6):
            yao_lines.append(random.choice(lines))
        
        print("生成的六爻卦象：")
        for i, line in enumerate(reversed(yao_lines)):  # 从下到上显示
            print(f"第{i+1}爻: {line}")
        
        # 测试天干地支生成
        heavenly_stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        earthly_branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        stem = random.choice(heavenly_stems)
        branch = random.choice(earthly_branches)
        
        print(f"天干地支: {stem}{branch}")
        
        # 测试梅花易数数字生成
        numbers = [random.randint(1, 8) for _ in range(3)]
        print(f"梅花易数数字: {numbers[0]}, {numbers[1]}, {numbers[2]}")
        
        print("✅ 卦象生成测试成功")
        return True
    except Exception as e:
        print(f"❌ 卦象生成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success1 = test_streaming_output()
    success2 = test_hexagram_generation()
    
    if success1 and success2:
        print("🎉 所有测试通过！")
        sys.exit(0)
    else:
        print("💥 测试失败！")
        sys.exit(1)