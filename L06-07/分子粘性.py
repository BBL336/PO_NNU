import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from scipy.special import erfc
import matplotlib.animation as animation

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# --- 1. 物理参数设置 ---
u0 = 0.5          # 表面流速 (m/s)
nu = 1e-6         # 运动粘度 (m^2/s)
sec_per_day = 86400  # 每天的秒数

# 深度数组，从 0 到 14 米，取 500 个点使曲线平滑
z = np.linspace(0, 14, 500)

# 计算给定天数下的流速分布 (利用解析解：互补误差函数)
def calculate_velocity(z, t_days):
    if t_days <= 0:
        return np.zeros_like(z)
    t_sec = t_days * sec_per_day
    # 公式：u(z,t) = u0 * erfc( z / (2 * sqrt(nu * t)) )
    return u0 * erfc(z / (2 * np.sqrt(nu * t_sec)))

# --- 2. 初始绘图设置 ---
fig, ax = plt.subplots(figsize=(7, 8))
plt.subplots_adjust(bottom=0.25) # 底部留出空间放滑块

# 设置坐标轴
ax.set_xlim(0, 0.55)
ax.set_ylim(14, 0) # 翻转Y轴，使 0 深度在最上方
ax.xaxis.tick_top() # 将X轴刻度移到顶部
ax.xaxis.set_label_position('top') # 将X轴标签移到顶部
ax.set_xlabel('速度 Speed (m/s)', fontsize=12)
ax.set_ylabel('深度 Depth (m)', fontsize=12)
ax.set_title('分子粘性导致的动量扩散 (交互演示)', fontsize=14, pad=20) # 增加pad防止标题和X轴重合
ax.grid(True, linestyle='--', alpha=0.6)

# 绘制三条静态参考线（虚线）
u_1_day = calculate_velocity(z, 1)
u_10_days = calculate_velocity(z, 10)
u_1_year = calculate_velocity(z, 365)

ax.plot(u_1_day, z, 'k--', alpha=0.5, label='1 Day')
ax.plot(u_10_days, z, 'b--', alpha=0.5, label='10 Days')
ax.plot(u_1_year, z, 'g--', alpha=0.5, label='One Year')
ax.legend(loc='lower right')

# 绘制动态实线，初始时间设为 1 天
initial_days = 1
line, = ax.plot(calculate_velocity(z, initial_days), z, 'r-', linewidth=2.5, label='当前时间')

# --- 3. 添加交互式滑块 ---
# 定义滑块的位置和大小 [左, 下, 宽, 高]
axcolor = 'lightgoldenrodyellow'
ax_time = plt.axes([0.15, 0.1, 0.65, 0.03], facecolor=axcolor)

# 创建滑块对象 (最小值 0.1天，最大值 365天，初始值 1天)
s_time = Slider(ax_time, '时间 (天)', 0.1, 365.0, valinit=initial_days, valstep=0.1)

# 定义滑块数值改变时的更新函数
def update(val):
    current_days = s_time.val
    # 重新计算当前天数的流速
    new_u = calculate_velocity(z, current_days)
    # 更新动态线的 x 坐标数据
    line.set_xdata(new_u)
    # 刷新画布
    fig.canvas.draw_idle()

# 绑定更新事件
s_time.on_changed(update)

# 生成动画
print("正在生成动画，请稍候...")
# 生成 1800 帧，使用 10 fps (1800 / 10 = 180 秒 = 3 分钟)
fps = 10
total_frames = 1800
frames = np.linspace(0.1, 365.0, total_frames)

def animate(frame):
    s_time.set_val(frame)  # 直接更新滑块，复用更新逻辑
    line.set_label(f'当前时间: {frame:.1f} 天')
    ax.legend(loc='lower right')
    return line,

anim = animation.FuncAnimation(fig, animate, frames=frames, interval=1000/fps)
# 保存为GIF
anim.save('分子粘性动画.gif', writer='pillow', fps=fps)
print("动画生成完毕！已保存为 '分子粘性动画.gif'")

# 显示图表
plt.show()