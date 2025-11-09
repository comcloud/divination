#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试优化后的功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("🔍 正在测试优化后的功能...")

# 测试图表生成器
try:
    from chart_generator import ChartGenerator
    print("✅ 成功导入ChartGenerator")
    
    # 测试图表生成
    generator = ChartGenerator()
    
    # 测试六爻卦象图
    yao_lines = ["———", "-- --", "———", "———", "-- --", "———"]
    chart_data = generator.generate_six_yao_chart(yao_lines)
    if chart_data and chart_data.startswith("data:image/png;base64,"):
        print("✅ 六爻卦象图生成成功")
    else:
        print("❌ 六爻卦象图生成失败")
    
    # 测试梅花易数图表
    numbers = [3, 5, 7]
    chart_data = generator.generate_plum_blossom_chart(numbers)
    if chart_data and chart_data.startswith("data:image/png;base64,"):
        print("✅ 梅花易数图表生成成功")
    else:
        print("❌ 梅花易数图表生成失败")
    
    # 测试天干地支图表
    stem = "甲"
    branch = "子"
    chart_data = generator.generate_heavenly_stems_chart(stem, branch)
    if chart_data and chart_data.startswith("data:image/png;base64,"):
        print("✅ 天干地支图表生成成功")
    else:
        print("❌ 天干地支图表生成失败")
        
except Exception as e:
    print(f"❌ 图表生成器测试失败: {e}")
    import traceback
    traceback.print_exc()

print("🎉 测试完成！")
