import random
from typing import List, Tuple, Optional
from openai import OpenAI
import os

class DivinationAgent:
    """占卜智能体，支持多种占卜方法"""
    
    def __init__(self, api_key: Optional[str] = None):
        """初始化占卜智能体"""
        # 如果没有提供API密钥，则从环境变量获取
        if api_key is None:
            api_key = os.getenv('MODELSCOPE_API_KEY')
        
        # 安全地初始化ModelScope客户端，避免传递不支持的参数
        client_kwargs = {
            'base_url': 'https://api-inference.modelscope.cn/v1',
            'api_key': api_key
        }
        
        # 只传递支持的参数
        self.client = OpenAI(**client_kwargs)
        
        # 使用的模型
        self.model = 'Qwen/Qwen3-235B-A22B-Instruct-2507'
    
    def _get_ai_interpretation(self, divination_type: str, question: str, result: str) -> str:
        """使用AI模型对占卜结果进行解释"""
        try:
            prompt = f"""
你是一个专业的占卜师，精通各种占卜方法。请根据以下占卜结果，为用户的问题提供专业解读。

占卜方式: {divination_type}
用户问题: {question}
占卜结果: {result}

请提供：
1. 详细的卦象/结果解析
2. 对用户问题的具体回答
3. 实用的建议和指导

请用中文回答，语言要通俗易懂，富有智慧。请确保回答完整，不要截断内容。
"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        'role': 'system',
                        'content': '你是一个专业的占卜师，精通各种占卜方法，能够为用户提供深入的占卜解读和实用建议。请确保回答完整，不要截断内容。'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                stream=False,
                temperature=0.7,
                max_tokens=1500  # 增加最大token数以确保完整响应
            )
            
            return response.choices[0].message.content
        except Exception as e:
            # 如果AI解释失败，返回默认解释
            return f"AI解读暂时不可用，使用默认解释：{result}"
    
    def _get_ai_interpretation_stream(self, divination_type: str, question: str, result: str):
        """使用AI模型对占卜结果进行解释（流式输出）"""
        try:
            prompt = f"""
你是一个专业的占卜师，精通各种占卜方法。请根据以下占卜结果，为用户的问题提供专业解读。

占卜方式: {divination_type}
用户问题: {question}
占卜结果: {result}

请提供：
1. 详细的卦象/结果解析
2. 对用户问题的具体回答
3. 实用的建议和指导

请用中文回答，语言要通俗易懂，富有智慧。请确保回答完整，不要截断内容。
"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        'role': 'system',
                        'content': '你是一个专业的占卜师，精通各种占卜方法，能够为用户提供深入的占卜解读和实用建议。请确保回答完整，不要截断内容。'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                stream=True,  # 启用流式输出
                temperature=0.7,
                max_tokens=1500
            )
            
            return response
        except Exception as e:
            # 如果AI解释失败，返回默认解释
            return f"AI解读暂时不可用，使用默认解释：{result}"
    
    def plum_blossom_divination(self, question: str) -> str:
        """梅花易数占卜"""
        # 模拟梅花易数计算过程
        numbers = [random.randint(1, 8) for _ in range(3)]
        hexagram = self._generate_hexagram(numbers)
        
        result = f"""
梅花易数占卜结果：

卦象：{hexagram}
数字：{numbers[0]}, {numbers[1]}, {numbers[2]}
"""

        # 使用AI进行解释
        ai_interpretation = self._get_ai_interpretation("梅花易数", question, result)
        return f"{result}\nAI解读：\n{ai_interpretation}"
    
    def plum_blossom_divination_stream(self, question: str):
        """梅花易数占卜（流式输出）"""
        # 模拟梅花易数计算过程
        numbers = [random.randint(1, 8) for _ in range(3)]
        hexagram = self._generate_hexagram(numbers)
        
        result = f"""
梅花易数占卜结果：

卦象：{hexagram}
数字：{numbers[0]}, {numbers[1]}, {numbers[2]}
"""

        # 使用AI进行解释（流式输出）
        yield f"占卜结果：{hexagram}\n数字：{numbers[0]}, {numbers[1]}, {numbers[2]}\n\n"
        yield "AI解读：\n"
        
        stream_response = self._get_ai_interpretation_stream("梅花易数", question, result)
        # 检查是否是字符串（错误情况）
        if isinstance(stream_response, str):
            yield stream_response
        else:
            # 处理流式响应
            try:
                for chunk in stream_response:
                    if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
            except Exception as e:
                yield f"\n流式输出过程中出现错误：{str(e)}"
    
    def heavenly_stems_earthly_branches(self, question: str) -> str:
        """天干地支占卜"""
        heavenly_stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        earthly_branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        
        stem = random.choice(heavenly_stems)
        branch = random.choice(earthly_branches)
        
        result = f"""
天干地支占卜结果：

天干：{stem}
地支：{branch}
干支组合：{stem}{branch}
"""

        # 使用AI进行解释
        ai_interpretation = self._get_ai_interpretation("天干地支", question, result)
        return f"{result}\nAI解读：\n{ai_interpretation}"
    
    def heavenly_stems_earthly_branches_stream(self, question: str):
        """天干地支占卜（流式输出）"""
        heavenly_stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        earthly_branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        
        stem = random.choice(heavenly_stems)
        branch = random.choice(earthly_branches)
        
        result = f"""
天干地支占卜结果：

天干：{stem}
地支：{branch}
干支组合：{stem}{branch}
"""

        # 使用AI进行解释（流式输出）
        yield f"天干：{stem}\n地支：{branch}\n干支组合：{stem}{branch}\n\n"
        yield "AI解读：\n"
        
        stream_response = self._get_ai_interpretation_stream("天干地支", question, result)
        # 检查是否是字符串（错误情况）
        if isinstance(stream_response, str):
            yield stream_response
        else:
            # 处理流式响应
            try:
                for chunk in stream_response:
                    if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
            except Exception as e:
                yield f"\n流式输出过程中出现错误：{str(e)}"
    
    def six_yao_divination(self, question: str) -> str:
        """六爻占卜"""
        yao_lines = []
        for i in range(6):
            # 生成爻线 (6为老阴，7为少阳，8为少阴，9为老阳)
            line_value = random.randint(6, 9)
            if line_value in [7, 9]:
                line = "———"  # 阳爻
            else:
                line = "-- --"  # 阴爻
            yao_lines.append(line)
        
        hexagram = "\n".join(yao_lines[::-1])  # 倒序显示（从下到上）
        
        result = f"""
六爻占卜结果：

卦象：
{hexagram}
"""

        # 使用AI进行解释
        ai_interpretation = self._get_ai_interpretation("六爻", question, result)
        return f"{result}\nAI解读：\n{ai_interpretation}"
    
    def six_yao_divination_stream(self, question: str):
        """六爻占卜（流式输出）"""
        yao_lines = []
        for i in range(6):
            # 生成爻线 (6为老阴，7为少阳，8为少阴，9为老阳)
            line_value = random.randint(6, 9)
            if line_value in [7, 9]:
                line = "———"  # 阳爻
            else:
                line = "-- --"  # 阴爻
            yao_lines.append(line)
        
        hexagram = "\n".join(yao_lines[::-1])  # 倒序显示（从下到上）
        
        result = f"""
六爻占卜结果：

卦象：
{hexagram}
"""

        # 使用AI进行解释（流式输出）
        yield f"六爻卦象：\n{hexagram}\n\n"
        yield "AI解读：\n"
        
        stream_response = self._get_ai_interpretation_stream("六爻", question, result)
        # 检查是否是字符串（错误情况）
        if isinstance(stream_response, str):
            yield stream_response
        else:
            # 处理流式响应
            try:
                for chunk in stream_response:
                    if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
            except Exception as e:
                yield f"\n流式输出过程中出现错误：{str(e)}"
    
    def purple_star_divination(self, question: str) -> str:
        """紫微斗数占卜"""
        stars = ["紫微星", "天机星", "太阳星", "武曲星", "天同星", "廉贞星"]
        positions = ["命宫", "兄弟宫", "夫妻宫", "子女宫", "财帛宫", "疾厄宫"]
        
        star = random.choice(stars)
        position = random.choice(positions)
        
        result = f"""
紫微斗数占卜结果：

主星：{star}
宫位：{position}
"""

        # 使用AI进行解释
        ai_interpretation = self._get_ai_interpretation("紫微斗数", question, result)
        return f"{result}\nAI解读：\n{ai_interpretation}"
    
    def purple_star_divination_stream(self, question: str):
        """紫微斗数占卜（流式输出）"""
        stars = ["紫微星", "天机星", "太阳星", "武曲星", "天同星", "廉贞星"]
        positions = ["命宫", "兄弟宫", "夫妻宫", "子女宫", "财帛宫", "疾厄宫"]
        
        star = random.choice(stars)
        position = random.choice(positions)
        
        result = f"""
紫微斗数占卜结果：

主星：{star}
宫位：{position}
"""

        # 使用AI进行解释（流式输出）
        yield f"主星：{star}\n宫位：{position}\n\n"
        yield "AI解读：\n"
        
        stream_response = self._get_ai_interpretation_stream("紫微斗数", question, result)
        # 检查是否是字符串（错误情况）
        if isinstance(stream_response, str):
            yield stream_response
        else:
            # 处理流式响应
            try:
                for chunk in stream_response:
                    if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
            except Exception as e:
                yield f"\n流式输出过程中出现错误：{str(e)}"
    
    def _generate_hexagram(self, numbers: List[int]) -> str:
        """根据数字生成卦象名称"""
        hexagrams = {
            (1, 1, 1): "乾卦",
            (1, 1, 2): "姤卦",
            (1, 2, 1): "同人卦",
            (1, 2, 2): "大有卦",
            (2, 1, 1): "履卦",
            (2, 1, 2): "小畜卦",
            (2, 2, 1): "需卦",
            (2, 2, 2): "大畜卦"
        }
        
        # 将数字转换为键
        key: Tuple[int, int, int] = tuple(min(n, 2) for n in numbers)  # type: ignore
        return hexagrams.get(key, "未知卦")
    
    def run_divination(self, divination_type: str, question: str) -> str:
        """执行占卜"""
        try:
            if divination_type == "梅花易数":
                return self.plum_blossom_divination(question)
            elif divination_type == "天干地支":
                return self.heavenly_stems_earthly_branches(question)
            elif divination_type == "六爻":
                return self.six_yao_divination(question)
            elif divination_type == "紫微斗数":
                return self.purple_star_divination(question)
            else:
                return f"暂不支持 {divination_type} 占卜方法"
        except Exception as e:
            return f"占卜过程中出现错误：{str(e)}"
    
    def run_divination_stream(self, divination_type: str, question: str):
        """执行占卜（流式输出）"""
        try:
            if divination_type == "梅花易数":
                yield from self.plum_blossom_divination_stream(question)
            elif divination_type == "天干地支":
                yield from self.heavenly_stems_earthly_branches_stream(question)
            elif divination_type == "六爻":
                yield from self.six_yao_divination_stream(question)
            elif divination_type == "紫微斗数":
                yield from self.purple_star_divination_stream(question)
            else:
                yield f"暂不支持 {divination_type} 占卜方法"
        except Exception as e:
            yield f"占卜过程中出现错误：{str(e)}"