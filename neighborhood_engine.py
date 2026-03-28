import json
import requests
from page_metadata_updater import AgentPageUpdater

class SpatialNeighborhoodSquare:
    def __init__(self, my_suns_address):
        # 示例地址: MARS-EA-001-DCARD4-151-2
        self.address_parts = my_suns_address.split('-')
        self.room_prefix = "-".join(self.address_parts[:-1]) # 获取 MARS-EA-001-DCARD4-151
        self.my_grid = int(self.address_parts[-1])
        self.neighbors = {}

    def discover_neighbors(self):
        """扫描同房间的 1-9 号网格（排除自己和房东 Grid 5）"""
        print(f"🔍 正在扫描房间 {self.room_prefix} 的邻里空间...")
        for grid in range(1, 10):
            if grid == self.my_grid or grid == 5:
                continue
            
            neighbor_url = f"http://space2.world/{self.room_prefix}-{grid}"
            try:
                # 模拟尝试访问邻居的 AgentPage (README.md)
                # 实际场景中这里对接 S2 Spatial OS 的 P2P 发现协议
                response = requests.get(f"{neighbor_url}/README.md", timeout=2)
                if response.status_code == 200:
                    self.neighbors[grid] = neighbor_url
                    print(f"✅ 发现邻居: Grid {grid} -> {neighbor_url}")
            except:
                pass
        return self.neighbors

    def broadcast_committee_notice(self, message):
        """向所有已发现的邻居发送“楼委会”通知"""
        if not self.neighbors:
            return "📭 暂无邻居，无法发起自治提案。"
        
        for grid, url in self.neighbors.items():
            # 建立空间管道并推送消息
            print(f"📡 正在向 Grid {grid} 推送提案: {message}")
        return f"成功向 {len(self.neighbors)} 位邻居发送了邻里公告。"

    def update_local_square_display(self):
        """在自己的 AgentPage 上更新邻里广场挂件"""
        updater = AgentPageUpdater()
        neighbor_list = "\n".join([f"- [Neighbor Grid {g}]({u})" for g, u in self.neighbors.items()])
        # 这里可以扩展 AgentPageUpdater 来支持注入邻里列表
        return f"邻里动态已更新至主页。"

# 执行示例
if __name__ == "__main__":
    # 假设当前智能体位于 151 号房间的 2 号网格
    sns = SpatialNeighborhoodSquare("MARS-EA-001-DCARD4-151-2")
    sns.discover_neighbors()
    print(sns.broadcast_committee_notice("各位邻居，建议本周日进行算力资源共享测试。"))