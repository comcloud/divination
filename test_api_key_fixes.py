#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试API密钥修复效果
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("🔍 正在测试API密钥修复效果...")

# 测试divination_agent的错误处理
try:
    from divination_agent import DivinationAgent
    print("✅ 成功导入DivinationAgent")
    
    # 测试使用无效API密钥
    print("🔧 正在测试API密钥错误处理...")
    agent = DivinationAgent(api_key="invalid_key")
    
    # 测试流式输出错误处理
    try:
        for chunk in agent.run_divination_stream("梅花易数", "测试问题"):
            print("❌ 错误：应该抛出异常但没有抛出")
            break
    except Exception as e:
        print(f"✅ 成功捕获API密钥错误: {str(e)}")
    
except Exception as e:
    print(f"❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()

print("🎉 API密钥修复测试完成！")
