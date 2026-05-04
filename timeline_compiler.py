import json
import os
import time

class TimelineManager:
    """时间轴管理器：负责卡点和 15 秒限制校验"""
    def __init__(self, max_duration_per_unit=15):
        self.max_duration = max_duration_per_unit
        self.current_timeline_sec = 0

    def calculate_timestamps(self, shots: list) -> list:
        processed_shots = []
        for shot in shots:
            duration = shot.get("duration", 5)
            # 严格约束：任何单镜不得超过设定的时间单元（例如 15 秒）
            if duration > self.max_duration:
                print(f"⚠️ [警告] 镜头 {shot['id']} 时长({duration}s)超限，已强制截断为 {self.max_duration}s")
                duration = self.max_duration

            start_time = self.current_timeline_sec
            end_time = start_time + duration
            self.current_timeline_sec = end_time

            shot["start_time"] = self._format_time(start_time)
            shot["end_time"] = self._format_time(end_time)
            shot["actual_duration"] = duration
            processed_shots.append(shot)
            
        return processed_shots

    def _format_time(self, seconds: int) -> str:
        """将秒数转化为 00:00 格式"""
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins:02d}:{secs:02d}"

class SyntaxFormatter:
    """语法格式化器：针对特定的底层 Agent 注入 @ 符号等专有语法"""
    def __init__(self, target_entities: list):
        self.targets = target_entities

    def format_prompt(self, raw_text: str) -> str:
        formatted_text = raw_text
        for entity in self.targets:
            # 将普通文本替换为高权重的 @ 标记语法
            if entity in formatted_text:
                formatted_text = formatted_text.replace(entity, f"@{entity}")
        return f"[Agent_Cmd] {formatted_text} --v 2.0"

class ProjectExporter:
    """工程导出器：将编译后的数据持久化到本地文件"""
    def export_to_json(self, data: list, filename: str = "export_timeline.json"):
        export_path = os.path.join(os.getcwd(), filename)
        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"📁 [工程导出] 成功！配置文件已生成至: {export_path}")

class AdvancedPipeline:
    def __init__(self):
        # 初始化各大核心模块
        self.timeline = TimelineManager(max_duration_per_unit=15)
        self.syntax = SyntaxFormatter(target_entities=["主角", "霓虹灯", "暗巷"])
        self.exporter = ProjectExporter()

    def run(self, raw_shots: list):
        print("⚙️ 开始编译多模态时间轴序列...\n" + "="*40)
        time.sleep(0.5) # 模拟处理延迟
        
        # 1. 计算时间轴与时长校验
        timed_shots = self.timeline.calculate_timestamps(raw_shots)
        
        # 2. 注入特定语法
        final_data = []
        for shot in timed_shots:
            shot["compiled_prompt"] = self.syntax.format_prompt(shot["action"])
            final_data.append(shot)
            print(f"🎬 [镜头 {shot['id']}] {shot['start_time']} -> {shot['end_time']} | 提示词: {shot['compiled_prompt']}")
            
        # 3. 导出为本地文件
        print("="*40)
        self.exporter.export_to_json(final_data)

# ==========================================
# 运行入口
# ==========================================
if __name__ == "__main__":
    # 模拟从上游接收到的带有预期时长的粗略分镜数据
    mock_input_data = [
        {"id": 1, "duration": 5, "action": "主角站在雨中的天桥上俯视街道"},
        {"id": 2, "duration": 18, "action": "主角点燃一根烟，霓虹灯火光照亮脸颊"}, # 这里故意设置 18 秒，测试 15 秒强制截断逻辑
        {"id": 3, "duration": 8, "action": "转身走向暗巷深处，画面逐渐变暗"}
    ]
    
    pipeline = AdvancedPipeline()
    pipeline.run(mock_input_data)