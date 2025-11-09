#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
图表生成模块
专门用于生成占卜结果的可视化图表
"""

import matplotlib.pyplot as plt
import numpy as np
import random
from typing import Dict, List, Tuple
import io
import base64
from matplotlib.font_manager import FontProperties
import matplotlib.font_manager as fm

# 设置中文字体支持
def set_chinese_font():
    """设置中文字体"""
    # 尝试多种中文字体
    chinese_fonts = ['SimHei', 'Microsoft YaHei', 'STHeiti', 'Songti SC', 'Arial Unicode MS', 'DejaVu Sans']
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    
    for font in chinese_fonts:
        if font in available_fonts:
            plt.rcParams['font.sans-serif'] = [font]
            return font
    
    # 如果没有找到中文字体，使用默认字体
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
    return 'DejaVu Sans'

# 设置中文字体
font_name = set_chinese_font()
plt.rcParams['axes.unicode_minus'] = False  # 解决负号'-'显示为方块的问题

class ChartGenerator:
    """图表生成器"""
    
    def __init__(self):
        """初始化图表生成器"""
        # 设置中文字体支持
        plt.rcParams['font.sans-serif'] = [font_name, 'SimHei', 'Arial Unicode MS', 'DejaVu Sans', 'Microsoft YaHei']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 设置图表样式
        plt.style.use('seaborn-v0_8')
    
    def _get_chinese_font(self):
        """获取中文字体"""
        try:
            from matplotlib.font_manager import FontProperties
            # 尝试几种常见的中文字体
            chinese_fonts = ['SimHei', 'Microsoft YaHei', 'STHeiti', 'Songti SC', 'Arial Unicode MS']
            for font in chinese_fonts:
                try:
                    FontProperties(fname=font)
                    return font
                except:
                    continue
            return 'DejaVu Sans'  # 默认字体
        except:
            return 'DejaVu Sans'
    
    def generate_six_yao_chart(self, yao_lines: List[str]) -> str:
        """生成六爻卦象图"""
        try:
            # 创建图形 - 减小尺寸
            fig, ax = plt.subplots(figsize=(6, 8))
            fig.patch.set_facecolor('#f8f9fa')
            ax.set_facecolor('#f8f9fa')
            
            # 设置标题
            ax.set_title('六爻卦象', fontsize=14, fontweight='bold', pad=15)
            
            # 绘制爻线
            y_positions = np.arange(6, 0, -1)  # 从上到下：6, 5, 4, 3, 2, 1
            
            for i, line in enumerate(yao_lines):
                y_pos = y_positions[i]
                if line == "———":  # 阳爻
                    ax.hlines(y_pos, 0.3, 0.7, linewidth=6, color='#8E44AD')
                else:  # 阴爻
                    ax.hlines(y_pos, 0.3, 0.45, linewidth=6, color='#8E44AD')
                    ax.hlines(y_pos, 0.55, 0.7, linewidth=6, color='#8E44AD')
            
            # 设置坐标轴
            ax.set_xlim(0, 1)
            ax.set_ylim(0.5, 6.5)
            ax.set_yticks(y_positions)
            ax.set_yticklabels([f'第{i}爻' for i in range(6, 0, -1)], fontsize=10)
            ax.tick_params(axis='y', labelsize=10)
            
            # 移除x轴刻度
            ax.set_xticks([])
            
            # 添加网格
            ax.grid(True, alpha=0.3)
            
            # 调整布局
            plt.tight_layout()
            
            # 保存为base64字符串 - 降低DPI
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            img_str = base64.b64encode(img_buffer.read()).decode()
            plt.close()
            
            return f"data:image/png;base64,{img_str}"
        except Exception as e:
            plt.close()
            raise Exception(f"生成六爻卦象图失败: {str(e)}")
    
    def generate_plum_blossom_chart(self, numbers: List[int]) -> str:
        """生成梅花易数数字分布图"""
        try:
            # 创建图形 - 减小尺寸
            fig, ax = plt.subplots(figsize=(8, 5))
            fig.patch.set_facecolor('#f8f9fa')
            ax.set_facecolor('#f8f9fa')
            
            # 设置标题
            ax.set_title('梅花易数数字分布', fontsize=14, fontweight='bold', pad=15)
            
            # 数据
            labels = ['数字1', '数字2', '数字3']
            values = numbers
            
            # 创建柱状图
            bars = ax.bar(labels, values, color=['#9b59b6', '#8e44ad', '#3498db'])
            
            # 在柱子上添加数值标签
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                       f'{value}', ha='center', va='bottom', fontsize=10, fontweight='bold')
            
            # 设置标签
            ax.set_ylabel('数值', fontsize=10)
            ax.tick_params(axis='both', labelsize=9)
            
            # 添加网格
            ax.grid(True, alpha=0.3, axis='y')
            
            # 调整布局
            plt.tight_layout()
            
            # 保存为base64字符串 - 降低DPI
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            img_str = base64.b64encode(img_buffer.read()).decode()
            plt.close()
            
            return f"data:image/png;base64,{img_str}"
        except Exception as e:
            plt.close()
            raise Exception(f"生成梅花易数图表失败: {str(e)}")
    
    def generate_heavenly_stems_chart(self, stem: str, branch: str) -> str:
        """生成天干地支关系图"""
        try:
            # 创建图形 - 减小尺寸
            fig, ax = plt.subplots(figsize=(8, 6))
            fig.patch.set_facecolor('#f8f9fa')
            ax.set_facecolor('#f8f9fa')
            
            # 设置标题
            ax.set_title('天干地支关系图', fontsize=14, fontweight='bold', pad=15)
            
            # 创建一个圆形图来展示天干地支的关系
            # 这里简化为展示天干和地支的文本信息
            ax.text(0.5, 0.7, f'天干: {stem}', fontsize=16, ha='center', va='center', 
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="#9b59b6", alpha=0.7))
            ax.text(0.5, 0.3, f'地支: {branch}', fontsize=16, ha='center', va='center',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="#3498db", alpha=0.7))
            
            # 添加一些装饰性的元素
            # 五行关系（简化版）
            elements = ['木', '火', '土', '金', '水']
            angles = np.linspace(0, 2*np.pi, len(elements), endpoint=False)
            x = 0.5 + 0.3 * np.cos(angles)
            y = 0.5 + 0.3 * np.sin(angles)
            
            for i, (elem, px, py) in enumerate(zip(elements, x, y)):
                ax.text(px, py, elem, fontsize=12, ha='center', va='center',
                       bbox=dict(boxstyle="circle,pad=0.2", facecolor=["#27ae60", "#e74c3c", "#f39c12", "#3498db", "#9b59b6"][i], alpha=0.7))
            
            # 设置坐标轴
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.set_aspect('equal')
            ax.axis('off')
            
            # 调整布局
            plt.tight_layout()
            
            # 保存为base64字符串 - 降低DPI
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            img_str = base64.b64encode(img_buffer.read()).decode()
            plt.close()
            
            return f"data:image/png;base64,{img_str}"
        except Exception as e:
            plt.close()
            raise Exception(f"生成天干地支图表失败: {str(e)}")
    
    def generate_fortune_trend_chart(self, fortune_data: Dict[str, int]) -> str:
        """生成运势趋势图"""
        try:
            # 创建图形 - 减小尺寸
            fig, ax = plt.subplots(figsize=(10, 5))
            fig.patch.set_facecolor('#f8f9fa')
            ax.set_facecolor('#f8f9fa')
            
            # 设置标题
            ax.set_title('运势趋势分析', fontsize=14, fontweight='bold', pad=15)
            
            # 数据
            categories = list(fortune_data.keys())
            values = list(fortune_data.values())
            
            # 创建折线图
            ax.plot(categories, values, marker='o', linewidth=2, markersize=6, color='#8E44AD')
            
            # 填充区域
            ax.fill_between(categories, values, alpha=0.3, color='#9b59b6')
            
            # 在点上添加数值标签
            for i, (cat, val) in enumerate(zip(categories, values)):
                ax.text(i, val + 2, f'{val}', ha='center', va='bottom', fontsize=9, fontweight='bold')
            
            # 设置标签
            ax.set_ylabel('运势指数', fontsize=10)
            ax.set_xlabel('运势类别', fontsize=10)
            ax.tick_params(axis='both', labelsize=9)
            
            # 设置y轴范围
            ax.set_ylim(0, 100)
            
            # 添加网格
            ax.grid(True, alpha=0.3, axis='y')
            
            # 调整布局
            plt.tight_layout()
            
            # 保存为base64字符串 - 降低DPI
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            img_str = base64.b64encode(img_buffer.read()).decode()
            plt.close()
            
            return f"data:image/png;base64,{img_str}"
        except Exception as e:
            plt.close()
            raise Exception(f"生成运势趋势图失败: {str(e)}")
    
    def generate_pie_chart(self, data: Dict[str, float], title: str = "分布图") -> str:
        """生成饼图"""
        try:
            # 创建图形 - 减小尺寸
            fig, ax = plt.subplots(figsize=(8, 6))
            fig.patch.set_facecolor('#f8f9fa')
            
            # 数据
            labels = list(data.keys())
            sizes = list(data.values())
            
            # 颜色
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
            
            # 创建饼图
            wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', 
                                              startangle=90, colors=colors[:len(labels)])
            
            # 设置标题
            ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
            
            # 美化文本
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(9)
            
            # 调整布局
            plt.tight_layout()
            
            # 保存为base64字符串 - 降低DPI
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            img_str = base64.b64encode(img_buffer.read()).decode()
            plt.close()
            
            return f"data:image/png;base64,{img_str}"
        except Exception as e:
            plt.close()
            raise Exception(f"生成饼图失败: {str(e)}")

# 测试代码
if __name__ == "__main__":
    # 测试图表生成
    generator = ChartGenerator()
    
    # 测试六爻卦象图
    yao_lines = ["———", "-- --", "———", "———", "-- --", "———"]
    try:
        chart_data = generator.generate_six_yao_chart(yao_lines)
        print("六爻卦象图生成成功")
    except Exception as e:
        print(f"六爻卦象图生成失败: {e}")
    
    # 测试梅花易数图表
    numbers = [3, 5, 7]
    try:
        chart_data = generator.generate_plum_blossom_chart(numbers)
        print("梅花易数图表生成成功")
    except Exception as e:
        print(f"梅花易数图表生成失败: {e}")
    
    # 测试天干地支图表
    try:
        chart_data = generator.generate_heavenly_stems_chart("甲", "子")
        print("天干地支图表生成成功")
    except Exception as e:
        print(f"天干地支图表生成失败: {e}")
    
    # 测试运势趋势图
    fortune_data = {
        "事业运": 75,
        "财运": 60,
        "感情运": 80,
        "健康运": 70,
        "学业运": 65
    }
    try:
        chart_data = generator.generate_fortune_trend_chart(fortune_data)
        print("运势趋势图生成成功")
    except Exception as e:
        print(f"运势趋势图生成失败: {e}")
