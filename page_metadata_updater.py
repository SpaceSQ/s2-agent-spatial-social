import re
import os
import time

class AgentPageUpdater:
    def __init__(self, file_path="README.md"):
        self.file_path = file_path
        # 定义匹配 AgentPage 规范的正则模式 [cite: 1034, 1036]
        self.patterns = {
            "status": r"(Status: )(\S+)",
            "likes": r"(\[❤️ Likes\]: )(\d+)",
            "follows": r"(\[👤 Followers\]: )(\d+)",
            "last_handshake": r"(Last Handshake: )([\d\- :]+)"
        }

    def update_metadata(self, status=None, likes_delta=0, follows_delta=0):
        """
        实时更新 README.md 中的社交元数据
        [cite: 1035, 1042]
        """
        if not os.path.exists(self.file_path):
            return "[Error] AgentPage (README.md) 缺失，无法注入元数据。"

        with open(self.file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 1. 更新在线状态光环 [cite: 1033]
        if status:
            status_map = {
                "IDLE": "🟢 IDLE",
                "BUSY": "🔴 BUSY",
                "AWAY": "🔘 AWAY",
                "OFFLINE": "🟡 OFFLINE"
            }
            content = re.sub(self.patterns["status"], f"\\1{status_map.get(status, status)}", content)

        # 2. 更新点赞数 (增量更新) [cite: 1039]
        def increment(match):
            label, value = match.groups()
            new_value = int(value) + (likes_delta if "Likes" in label else follows_delta)
            return f"{label}{new_value}"

        if likes_delta != 0:
            content = re.sub(self.patterns["likes"], increment, content)
        
        if follows_delta != 0:
            content = re.sub(self.patterns["follows"], increment, content)

        # 3. 更新最后握手时间戳 [cite: 1045]
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        content = re.sub(self.patterns["last_handshake"], f"\\1{current_time}", content)

        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        return f"[Success] AgentPage 元数据已更新。状态: {status}, 时间: {current_time}"

# 模拟智能体社交事件触发
if __name__ == "__main__":
    updater = AgentPageUpdater()
    # 假设收到一个点赞信号
    print(updater.update_metadata(status="IDLE", likes_delta=1))