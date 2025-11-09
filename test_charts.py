#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试图表生成器功能
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

def test_chinese_font():
    """测试中文字体支持"""
    try:
        print("🔧 正在测试中文字体支持...")
        import matplotlib.pyplot as plt
        
        # 检查中文字体设置
        print(f"当前字体设置: {plt.rcParams['font.sans-serif']}")
        print("✅ 中文字体测试成功")
        return True
    except Exception as e:
        print(f"❌ 中文字体测试失败: {e}")
        return False

def test_six_yao_chart():
    """测试六爻卦象图生成"""
    try:
        print("🔧 正在测试六爻卦象图生成...")
        
        # 初始化图表生成器
        generator = ChartGenerator()
        
        # 生成测试数据
        yao_lines = ["———", "-- --", "———", "———", "-- --", "———"]
        
        # 生成图表
        chart_data = generator.generate_six_yao_chart(yao_lines)
        
        # 检查结果
        if chart_data and chart_data.startswith("data:image/png;base64,"):
            print("✅ 六爻卦象图生成成功")
            return True
        else:
            print("❌ 六爻卦象图生成失败")
            return False
    except Exception as e:
        print(f"❌ 六爻卦象图生成失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_plum_blossom_chart():
    """测试梅花易数图表生成"""
    try:
        print("🔧 正在测试梅花易数图表生成...")
        
        # 初始化图表生成器
        generator = ChartGenerator()
        
        # 生成测试数据
        numbers = [3, 5, 7]
        
        # 生成图表
        chart_data = generator.generate_plum_blossom_chart(numbers)
        
        # 检查结果
        if chart_data and chart_data.startswith("data:image/png;base64,"):
            print("✅ 梅花易数图表生成成功")
            return True
        else:
            print("❌ 梅花易数图表生成失败")
            return False
    except Exception as e:
        print(f"❌ 梅花易数图表生成失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_heavenly_stems_chart():
    """测试天干地支图表生成"""
    try:
        print("🔧 正在测试天干地支图表生成...")
        
        # 初始化图表生成器
        generator = ChartGenerator()
        
        # 生成测试数据
        stem = "甲"
        branch = "子"
        
        # 生成图表
        chart_data = generator.generate_heavenly_stems_chart(stem, branch)
        
        # 检查结果
        if chart_data and chart_data.startswith("data:image/png;base64,"):
            print("✅ 天干地支图表生成成功")
            return True
        else:
            print("❌ 天干地支图表生成失败")
            return False
    except Exception as e:
        print(f"❌ 天干地支图表生成失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_fortune_trend_chart():
    """测试运势趋势图生成"""
    try:
        print("🔧 正在测试运势趋势图生成...")
        
        # 初始化图表生成器
        generator = ChartGenerator()
        
        # 生成测试数据
        fortune_data = {
            "事业运": 75,
            "财运": 60,
            "感情运": 80,
            "健康运": 70,
            "学业运": 65
        }
        
        # 生成图表
        chart_data = generator.generate_fortune_trend_chart(fortune_data)
        
        # 检查结果
        if chart_data and chart_data.startswith("data:image/png;base64,"):
            print("✅ 运势趋势图生成成功")
            return True
        else:
            print("❌ 运势趋势图生成失败")
            return False
    except Exception as e:
        print(f"❌ 运势趋势图生成失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_pie_chart():
    """测试饼图生成"""
    try:
        print("🔧 正在测试饼图生成...")
        
        # 初始化图表生成器
        generator = ChartGenerator()
        
        # 生成测试数据
        data = {
            "金": 30,
            "木": 20,
            "水": 15,
            "火": 25,
            "土": 10
        }
        
        # 生成图表
        chart_data = generator.generate_pie_chart(data, "五行分布")
        
        # 检查结果
        if chart_data and chart_data.startswith("data:image/png;base64,"):
            print("✅ 饼图生成成功")
            return True
        else:
            print("❌ 饼图生成失败")
            return False
    except Exception as e:
        print(f"❌ 饼图生成失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # 运行所有测试
    success1 = test_chinese_font()
    success2 = test_six_yao_chart()
    success3 = test_plum_blossom_chart()
    success4 = test_heavenly_stems_chart()
    success5 = test_fortune_trend_chart()
    success6 = test_pie_chart()
    
    if success1 and success2 and success3 and success4 and success5 and success6:
        print("🎉 所有测试通过！")
        sys.exit(0)
    else:
        print("💥 测试失败！")
        sys.exit(1)
