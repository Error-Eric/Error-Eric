import matplotlib.pyplot as plt
import networkx as nx

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # Windows
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 创建图结构
G = nx.Graph()
center = "波德莱尔《巴黎的忧郁》"
titles = ['异乡人', '老妇人的绝望', '光环丢了', '狗和香水瓶', '英勇的死', '穷人的眼睛', '头发中的半个地球', '钟表', '穷人的玩具', '浓汤和云']

# 添加节点和边
G.add_node(center)
G.add_nodes_from(titles)
for title in titles:
    G.add_edge(center, title)

# 定义边标签
edge_labels = {
    ('异乡人', '老妇人的绝望'): '共同点：被社会抛弃的边缘人物\n不同点：接受异化 vs 绝望抗拒',
    ('异乡人', '光环丢了'): '共同点：全对话展开形式',
    ('狗和香水瓶', '英勇的死'): '共同点：借喻讽刺社会打压艺术\n不同点：群众本性 vs 统治者煽动',
    ('穷人的眼睛', '狗和香水瓶'): '共同点：对比表现艺术追求\n不同点：语言描写 vs 动作描写',
    ('穷人的眼睛', '头发中的半个地球'): '共同点：第二人称叙事\n不同点：对立 vs 向往的象征',
    ('钟表', '异乡人'): '共同点：批判实用主义\n不同点：具体意象 vs 抽象象征',
    ('穷人的眼睛', '穷人的玩具'): '共同点：贫富差距对比\n不同点：态度对比 vs 外貌对比',
    ('浓汤和云', '穷人的眼睛'): '共同点：女性角色\n不同点：现实象征 vs 富人冷漠'
}

# 添加边
G.add_edges_from(edge_labels.keys())

# 生成布局
pos = nx.spring_layout(G, seed=42)

# 绘图
plt.figure(figsize=(15, 12))
nx.draw_networkx_nodes(G, pos, nodelist=[center], node_size=5000, node_color='gold', alpha=0.8)
nx.draw_networkx_nodes(G, pos, nodelist=titles, node_size=3000, node_color='lightblue', alpha=0.8)
nx.draw_networkx_edges(G, pos, edge_color='gray', width=1.5, alpha=0.6)
nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

# 添加边标签
for (src, dst), label in edge_labels.items():
    x = (pos[src][0] + pos[dst][0]) / 2
    y = (pos[src][1] + pos[dst][1]) / 2
    plt.text(x, y, label, fontsize=8, ha='center', va='center', color='darkred', wrap=True)

plt.title("波德莱尔《巴黎的忧郁》关联分析", fontsize=14)
plt.axis('off')
plt.tight_layout()
plt.show()