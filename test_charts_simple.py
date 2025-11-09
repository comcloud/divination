#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简化版图表生成器测试脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("🔍 正在测试图表生成器功能...")

try:
    from chart_generator import ChartGenerator
    print("✅ 成功导入ChartGenerator")
except Exception as e:
    print(f"❌ 导入ChartGenerator失败: {e}")
    sys.exit(1)

def test_chart_generator():
    """测试图表生成器基本功能"""
    try:
        print("🔧 正在测试图表生成器基本功能...")
        
        # 初始化图表生成器
        generator = ChartGenerator()
        
        # 测试六爻卦象图生成
        print("  正在测试六爻卦象图生成...")
        yao_lines = ["———", "-- --", "———", "———", "-- --", "———"]
        chart_data = generator.generate_six_yao_chart(yao_lines)
        if chart_data and chart_data.startswith("data:image/png;base64,"):
            print("  ✅ 六爻卦象图生成成功")
        else:
            print("  ❌ 六爻卦象图生成失败")
            return False
        
        # 测试梅花易数图表生成
        print("  正在测试梅花易数图表生成...")
        numbers = [3, 5, 7]
        chart_data = generator.generate_plum_blossom_chart(numbers)
        if chart_data and chart_data.startswith("data:image/png;base64,"):
            print("  ✅ 梅花易数图表生成成功")
        else:
            print("  ❌ 梅花易数图表生成失败")
            return False
        
        # 测试天干地支图表生成
        print("  正在测试天干地支图表生成...")
        stem = "甲"
        branch = "子"
        chart_data = generator.generate_heavenly_stems_chart(stem, branch)
        if chart_data and chart_data.startswith("data:image/png;base64,"):
            print("  ✅ 天干地支图表生成成功")
        else:
            print("  ❌ 天干地支图表生成失败")
            return False
        
        print("✅ 图表生成器基本功能测试通过")
        return True
    except Exception as e:
        print(f"❌ 图表生成器基本功能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_chart_generator()
    
    if success:
        print("🎉 图表生成器测试通过！")
        sys.exit(0)
    else:
        print("💥 图表生成器测试失败！")
        sys.exit(1)
