import panel as pn
import numpy as np
import asyncio
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for Panel server
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import io

# 配置中文字体显示
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

pn.extension('mathjax')

class TeaCupPhysics:
    def __init__(self):
        self.omega = 5.0  # 角速度 (rad/s)
        self.g = 9.8  # 重力加速度
        self.r_max = 0.05  # 茶杯半径 (m)
        self.time = 0
        self.is_stirring = True
        self.tea_leaves_positions = self._initialize_tea_leaves()
        
    def _initialize_tea_leaves(self):
        """初始化茶叶位置（随机分布）"""
        n_leaves = 30
        r = np.random.uniform(0, self.r_max, n_leaves)
        theta = np.random.uniform(0, 2*np.pi, n_leaves)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        return np.column_stack([x, y])
    
    def paraboloid_surface(self, omega):
        """计算旋转液体的抛物面"""
        r = np.linspace(0, self.r_max, 50)
        theta = np.linspace(0, 2*np.pi, 50)
        R, Theta = np.meshgrid(r, theta)
        
        # 抛物面方程: z = (omega^2 * r^2) / (2*g)
        Z = (omega**2 * R**2) / (2 * self.g)
        
        X = R * np.cos(Theta)
        Y = R * np.sin(Theta)
        
        return X, Y, Z
    
    def update_tea_leaves(self, dt, omega):
        """更新茶叶位置（次级流动）"""
        if self.is_stirring:
            # 搅拌时：茶叶向外移动
            for i in range(len(self.tea_leaves_positions)):
                x, y = self.tea_leaves_positions[i]
                r = np.sqrt(x**2 + y**2)
                if r < self.r_max * 0.9:
                    # 轻微向外移动
                    factor = 1.002
                    self.tea_leaves_positions[i] *= factor
        else:
            # 停止搅拌：茶叶向中心聚集（次级流动）
            for i in range(len(self.tea_leaves_positions)):
                x, y = self.tea_leaves_positions[i]
                r = np.sqrt(x**2 + y**2)
                if r > 0.002:  # 避免除以零
                    # 向中心移动
                    move_factor = 0.995
                    self.tea_leaves_positions[i] *= move_factor
    
    def create_3d_view(self):
        """创建3D视图显示抛物面"""
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')
        
        omega = self.omega if self.is_stirring else self.omega * 0.3
        X, Y, Z = self.paraboloid_surface(omega)
        
        # 绘制水面（抛物面）
        surf = ax.plot_surface(X*100, Y*100, Z*100, cmap=cm.Blues, 
                               alpha=0.7, linewidth=0, antialiased=True)
        
        # 绘制茶杯边缘
        theta = np.linspace(0, 2*np.pi, 50)
        cup_x = self.r_max * 100 * np.cos(theta)
        cup_y = self.r_max * 100 * np.sin(theta)
        cup_z = np.zeros_like(theta)
        ax.plot(cup_x, cup_y, cup_z, 'k-', linewidth=2, label='茶杯边缘')
        
        ax.set_xlabel('X (cm)')
        ax.set_ylabel('Y (cm)')
        ax.set_zlabel('高度 Z (cm)')
        ax.set_title(f'水面形状 - {"搅拌中" if self.is_stirring else "静止"}')
        ax.set_zlim(0, 3)
        
        plt.tight_layout()
        plt.close(fig)  # 释放 pyplot 持有的引用，避免累计过多图像
        return fig
    
    def create_top_view(self):
        """创建俯视图显示茶叶分布"""
        fig, ax = plt.subplots(figsize=(6, 6))
        
        # 绘制茶杯
        circle = plt.Circle((0, 0), self.r_max*100, fill=False, 
                           color='black', linewidth=2, label='茶杯')
        ax.add_patch(circle)
        
        # 绘制茶叶
        x_leaves = self.tea_leaves_positions[:, 0] * 100
        y_leaves = self.tea_leaves_positions[:, 1] * 100
        ax.scatter(x_leaves, y_leaves, c='#8B4513', s=50, 
                  alpha=0.8, label='茶叶', edgecolors='#654321')
        
        # 绘制水流方向（搅拌时）
        if self.is_stirring:
            # 绘制旋转箭头
            for r_arrow in [0.02, 0.03, 0.04]:
                n_arrows = 8
                for i in range(n_arrows):
                    angle = 2*np.pi*i/n_arrows
                    x = r_arrow*100 * np.cos(angle)
                    y = r_arrow*100 * np.sin(angle)
                    dx = -r_arrow*100*0.3 * np.sin(angle)
                    dy = r_arrow*100*0.3 * np.cos(angle)
                    ax.arrow(x, y, dx, dy, head_width=0.3, 
                            head_length=0.2, fc='blue', 
                            ec='blue', alpha=0.3, linewidth=0.5)
        
        ax.set_xlim(-6, 6)
        ax.set_ylim(-6, 6)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_xlabel('X (cm)')
        ax.set_ylabel('Y (cm)')
        ax.set_title(f'俯视图 - {"搅拌中" if self.is_stirring else "静止后茶叶聚集"}')
        ax.legend()
        
        plt.tight_layout()
        plt.close(fig)  # 释放 pyplot 持有的引用，避免累计过多图像
        return fig
    
    def get_physics_explanation(self):
        """返回物理原理解释"""
        explanation = """
        ## 物理原理分析
        
        ### 1. 搅拌时：水面形成抛物面
        
        当用筷子搅动茶水时，水体做圆周运动。液体需要**向心力**来维持圆周运动：
        
        $$F_{向心} = m\\omega^2 r$$
        
        其中 $\\omega$ 是角速度，$r$ 是到旋转轴的距离。
        
        在旋转参考系中，液体表面上任意一点受力平衡：
        - **重力** $mg$ （竖直向下）
        - **表面张力**（垂直于液面）
        
        液面形状满足方程：
        
        $$z = \\frac{\\omega^2 r^2}{2g}$$
        
        这是一个**抛物面**方程，离旋转轴越远，水位越高。
        
        ### 2. 停止搅拌后：茶叶汇聚中心
        
        停止搅拌后，茶叶向底部中心聚集，这是**次级流动（Secondary Flow）**现象：
        
        **形成机制：**
        1. **底部边界层效应**：杯底摩擦力使底层水流速减慢
        2. **压力梯度**：外侧水位较高，产生向内的压力梯度
        3. **次级环流**：
           - 底层水流：从外向内流动（向中心）
           - 表层水流：从内向外流动（补偿）
        
        $$\\frac{dp}{dr} = \\rho\\omega^2 r$$
        
        **茶叶运动：**
        - 茶叶密度大于水，沉在底部
        - 随底层水流向中心移动
        - 最终聚集在杯底中心
        
        ### 3. 实际应用
        
        - **咖啡杯效应**：搅拌咖啡后糖粒聚集中心
        - **河流弯道**：河水转弯时泥沙沉积规律
        - **茶叶悖论（Tea Leaf Paradox）**：爱因斯坦在1926年用此解释河流弯道沉积现象
        """
        return explanation

# 创建应用
physics = TeaCupPhysics()

# 创建控件
stirring_toggle = pn.widgets.Toggle(name='搅拌状态', value=True, button_type='success')
omega_slider = pn.widgets.FloatSlider(name='角速度 ω (rad/s)', 
                                      start=0, end=10, value=5, step=0.5)
auto_animate = pn.widgets.Toggle(name='自动动画 ▶', value=True, button_type='success')
frame_interval = pn.widgets.IntSlider(name='动画间隔 (ms)', start=100, end=1000, value=300, step=50)
reset_button = pn.widgets.Button(name='重置茶叶位置', button_type='primary')
update_button = pn.widgets.Button(name='更新视图', button_type='warning')

# 图表占位符
plot_3d = pn.pane.Matplotlib(physics.create_3d_view(), sizing_mode='stretch_width')
plot_top = pn.pane.Matplotlib(physics.create_top_view(), sizing_mode='stretch_width')
explanation_pane = pn.pane.Markdown(physics.get_physics_explanation(), 
                                    sizing_mode='stretch_width')

periodic_callback = None

def update_stirring(event):
    physics.is_stirring = event.new
    stirring_toggle.button_type = 'success' if event.new else 'danger'
    stirring_toggle.name = '搅拌中 🥢' if event.new else '已停止 ⏸️'
    if auto_animate.value:
        if physics.is_stirring:
            start_animation()
        else:
            stop_animation()

def update_omega(event):
    physics.omega = event.new

def reset_leaves(event):
    physics.tea_leaves_positions = physics._initialize_tea_leaves()
    update_views(None)

def update_views(event=None):
    # 更新茶叶位置
    for _ in range(10):
        physics.update_tea_leaves(0.1, physics.omega)
    
    # 重新生成图表
    plot_3d.object = physics.create_3d_view()
    plot_top.object = physics.create_top_view()

def update_auto_animate(event):
    auto_animate.button_type = 'success' if event.new else 'danger'
    auto_animate.name = '自动动画 ▶' if event.new else '自动动画 ⏸️'
    if event.new and physics.is_stirring:
        start_animation()
    else:
        stop_animation()

def update_interval(event):
    if periodic_callback is not None:
        periodic_callback.period = event.new

def start_animation():
    global periodic_callback
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return
    if periodic_callback is None:
        periodic_callback = pn.state.add_periodic_callback(update_views, period=frame_interval.value)
    else:
        periodic_callback.start()

def stop_animation():
    global periodic_callback
    if periodic_callback is not None:
        periodic_callback.stop()

# 连接回调
stirring_toggle.param.watch(update_stirring, 'value')
omega_slider.param.watch(update_omega, 'value')
auto_animate.param.watch(update_auto_animate, 'value')
frame_interval.param.watch(update_interval, 'value')
reset_button.on_click(reset_leaves)
update_button.on_click(update_views)

def _on_session_ready():
    if auto_animate.value and physics.is_stirring:
        start_animation()

pn.state.onload(_on_session_ready)

# 创建布局
header = pn.pane.Markdown("""
# 🍵 茶杯搅拌的物理学
## 水面抛物面与茶叶聚集现象演示
""", sizing_mode='stretch_width')

controls = pn.Card(
    pn.Column(
        stirring_toggle,
        omega_slider,
        auto_animate,
        frame_interval,
        pn.Row(update_button, reset_button),
        pn.pane.Markdown("""
        **操作说明：**
        1. 保持"搅拌中"并开启"自动动画"，观察连续变化
        2. 调整角速度查看抛物面曲率变化
        3. 关闭搅拌后，可关闭自动动画并多次点击"更新视图"
        4. 需要时点击"重置茶叶位置"重新开始
        """)
    ),
    title='⚙️ 控制面板',
    sizing_mode='stretch_width'
)

visualization = pn.Card(
    pn.Row(
        pn.Column(plot_3d, sizing_mode='stretch_width'),
        pn.Column(plot_top, sizing_mode='stretch_width')
    ),
    title='📊 可视化',
    sizing_mode='stretch_width'
)

explanation = pn.Card(
    explanation_pane,
    title='📚 物理原理',
    sizing_mode='stretch_width',
    collapsed=False
)

# 主应用
template = pn.template.FastListTemplate(
    title='茶杯搅拌物理演示',
    sidebar=[controls],
    main=[header, visualization, explanation],
    accent_base_color='#4CAF50',
    header_background='#2E7D32'
)

if __name__ == '__main__':
    pn.serve(template, show=True)
else:
    template.servable()
