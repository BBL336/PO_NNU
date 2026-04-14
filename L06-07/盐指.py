import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 设置中文字体，防止中文显示为方块 (根据您的操作系统可能需要调整字体名称，如 'SimHei' 或 'Microsoft YaHei')
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
fig.suptitle('双扩散驱动的盐指形成过程 (四层模型)', fontsize=16, fontweight='bold')

# --- 1. 绘制初始状态 (左图) ---
ax1.set_title('初始状态 (几分钟前)', fontsize=14)
ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)
ax1.axis('off') # 隐藏坐标轴

# 上层: 暖咸水
rect_top_init = patches.Rectangle((0.1, 0.5), 0.8, 0.4, linewidth=2, edgecolor='black', facecolor='#ffcccc')
ax1.add_patch(rect_top_init)
ax1.text(0.5, 0.7, "第一层: 暖咸水\nT = 20°C, S = 35\n密度 = ρ1", 
         ha='center', va='center', fontsize=12)

# 下层: 冷淡水
rect_bot_init = patches.Rectangle((0.1, 0.1), 0.8, 0.4, linewidth=2, edgecolor='black', facecolor='#cceeff')
ax1.add_patch(rect_bot_init)
ax1.text(0.5, 0.3, "第二层: 冷淡水\nT = 10°C, S = 25\n密度 = ρ1", 
         ha='center', va='center', fontsize=12)

# --- 2. 绘制演变状态 (右图) ---
ax2.set_title('界面演变 (产生不稳定性)', fontsize=14)
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
ax2.axis('off')

# L1: 暖咸水 (剩余部分)
rect_l1 = patches.Rectangle((0.1, 0.65), 0.8, 0.25, linewidth=2, edgecolor='black', facecolor='#ffcccc')
ax2.add_patch(rect_l1)
ax2.text(0.5, 0.775, "第一层: 暖咸水\nT = 20°C, S = 35, 密度 = ρ1", ha='center', va='center', fontsize=11)

# L2: 冷咸水 (热量流失，盐分保留 -> 变重)
rect_l2 = patches.Rectangle((0.1, 0.5), 0.8, 0.15, linewidth=2, edgecolor='black', facecolor='#b3b3ff')
ax2.add_patch(rect_l2)
ax2.text(0.5, 0.575, "第二层: 冷咸水\nT = 15°C, S = 35, 密度 = ρ2", ha='center', va='center', fontsize=11, fontweight='bold', color='darkblue')

# L3: 暖淡水 (吸收热量，盐分未到 -> 变轻)
rect_l3 = patches.Rectangle((0.1, 0.35), 0.8, 0.15, linewidth=2, edgecolor='black', facecolor='#ffffcc')
ax2.add_patch(rect_l3)
ax2.text(0.5, 0.425, "第三层: 暖淡水\nT = 15°C, S = 25, 密度 = ρ3", ha='center', va='center', fontsize=11, fontweight='bold', color='olive')

# L4: 冷淡水 (剩余部分)
rect_l4 = patches.Rectangle((0.1, 0.1), 0.8, 0.25, linewidth=2, edgecolor='black', facecolor='#cceeff')
ax2.add_patch(rect_l4)
ax2.text(0.5, 0.225, "第四层: 冷淡水\nT = 10°C, S = 25, 密度 = ρ1", ha='center', va='center', fontsize=11)

# --- 3. 添加箭头和说明 ---
# 第二层向下沉降的箭头 (盐指)
ax2.annotate('向下沉降\n(形成盐指)', xy=(0.75, 0.35), xytext=(0.75, 0.5),
            arrowprops=dict(facecolor='darkblue', shrink=0.05, width=3, headwidth=8),
            ha='center', va='bottom', color='darkblue', fontsize=10, fontweight='bold')

# 第三层向上浮升的箭头
ax2.annotate('向上浮升', xy=(0.25, 0.65), xytext=(0.25, 0.5),
            arrowprops=dict(facecolor='olive', shrink=0.05, width=3, headwidth=8),
            ha='center', va='top', color='olive', fontsize=10, fontweight='bold')

# 底部添加核心逻辑说明
plt.figtext(0.5, 0.05, "核心动力学逻辑: 由于热扩散远快于盐扩散，导致界面处发生局部密度逆转：ρ2 > ρ1 > ρ3", 
            ha='center', fontsize=13, fontweight='bold', color='red', bbox=dict(facecolor='white', alpha=0.8, edgecolor='red'))

plt.tight_layout(rect=[0, 0.1, 1, 0.95]) # 调整布局给底部文字留出空间
plt.show()