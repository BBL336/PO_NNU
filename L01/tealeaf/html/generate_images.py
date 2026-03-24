import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import matplotlib

matplotlib.use('Agg')


class TeaCupPhysics:
    def __init__(self):
        self.omega = 5.0
        self.g = 9.8
        self.r_max = 0.05
        self.is_stirring = True
        self.tea_leaves_positions = self._initialize_tea_leaves()

    def _initialize_tea_leaves(self):
        n_leaves = 30
        r = np.random.uniform(0, self.r_max, n_leaves)
        theta = np.random.uniform(0, 2 * np.pi, n_leaves)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        return np.column_stack([x, y])

    def paraboloid_surface(self, omega):
        r = np.linspace(0, self.r_max, 50)
        theta = np.linspace(0, 2 * np.pi, 50)
        R, Theta = np.meshgrid(r, theta)
        Z = (omega ** 2 * R ** 2) / (2 * self.g)
        X = R * np.cos(Theta)
        Y = R * np.sin(Theta)
        return X, Y, Z

    def update_tea_leaves(self, dt):
        if self.is_stirring:
            for i in range(len(self.tea_leaves_positions)):
                x, y = self.tea_leaves_positions[i]
                r = np.sqrt(x ** 2 + y ** 2)
                if r < self.r_max * 0.9:
                    self.tea_leaves_positions[i] *= 1.003
        else:
            for i in range(len(self.tea_leaves_positions)):
                x, y = self.tea_leaves_positions[i]
                r = np.sqrt(x ** 2 + y ** 2)
                if r > 0.002:
                    self.tea_leaves_positions[i] *= 0.995

    def create_3d_view(self):
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')

        omega = self.omega if self.is_stirring else self.omega * 0.3
        X, Y, Z = self.paraboloid_surface(omega)

        ax.plot_surface(X * 100, Y * 100, Z * 100, cmap=cm.Blues,
                        alpha=0.7, linewidth=0, antialiased=True)

        theta = np.linspace(0, 2 * np.pi, 50)
        cup_x = self.r_max * 100 * np.cos(theta)
        cup_y = self.r_max * 100 * np.sin(theta)
        cup_z = np.zeros_like(theta)
        ax.plot(cup_x, cup_y, cup_z, 'k-', linewidth=2, label='茶杯边缘')

        ax.set_xlabel('X (cm)')
        ax.set_ylabel('Y (cm)')
        ax.set_zlabel('高度 Z (cm)')
        title = '水面形状 - 搅拌中' if self.is_stirring else '水面形状 - 静止'
        ax.set_title(title)
        ax.set_zlim(0, 3)

        plt.tight_layout()
        return fig

    def create_top_view(self):
        fig, ax = plt.subplots(figsize=(6, 6))

        circle = plt.Circle((0, 0), self.r_max * 100, fill=False,
                            color='black', linewidth=2, label='茶杯')
        ax.add_patch(circle)

        x_leaves = self.tea_leaves_positions[:, 0] * 100
        y_leaves = self.tea_leaves_positions[:, 1] * 100
        ax.scatter(x_leaves, y_leaves, c='#8B4513', s=50,
                   alpha=0.8, label='茶叶', edgecolors='#654321')

        if self.is_stirring:
            for r_arrow in [0.02, 0.03, 0.04]:
                n_arrows = 8
                for i in range(n_arrows):
                    angle = 2 * np.pi * i / n_arrows
                    x = r_arrow * 100 * np.cos(angle)
                    y = r_arrow * 100 * np.sin(angle)
                    dx = -r_arrow * 100 * 0.3 * np.sin(angle)
                    dy = r_arrow * 100 * 0.3 * np.cos(angle)
                    ax.arrow(x, y, dx, dy, head_width=0.3,
                             head_length=0.2, fc='blue',
                             ec='blue', alpha=0.3, linewidth=0.5)

        ax.set_xlim(-6, 6)
        ax.set_ylim(-6, 6)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_xlabel('X (cm)')
        ax.set_ylabel('Y (cm)')
        title = '俯视图 - 搅拌中' if self.is_stirring else '俯视图 - 静止后茶叶聚集'
        ax.set_title(title)
        ax.legend()

        plt.tight_layout()
        return fig


plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


def save_frame(prefix_3d, prefix_top, frame_index, physics):
    fig1 = physics.create_3d_view()
    fig2 = physics.create_top_view()
    fig1.savefig(f'{prefix_3d}_{frame_index}.png', dpi=80, bbox_inches='tight')
    fig2.savefig(f'{prefix_top}_{frame_index}.png', dpi=80, bbox_inches='tight')
    plt.close('all')


print('生成搅拌中的动画帧...')
physics = TeaCupPhysics()
physics.is_stirring = True
for frame in range(6):
    physics.omega = 2 + frame * 1.5
    save_frame('stirring_3d', 'stirring_top', frame, physics)
    print(f'  ✓ 帧 {frame + 1}/6 - omega={physics.omega:.1f} rad/s')

print('\n生成茶叶聚集的动画帧...')
physics.is_stirring = False
physics.tea_leaves_positions = physics._initialize_tea_leaves()
for frame in range(8):
    for _ in range(5):
        physics.update_tea_leaves(0.1)
    save_frame('settling_3d', 'settling_top', frame, physics)
    print(f'  ✓ 帧 {frame + 1}/8')

print('\n✅ 所有动画帧已生成！')