import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import matplotlib.animation as animation
from scipy.special import erfc
from pathlib import Path
from datetime import datetime

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# --- 1. 物理参数设置 ---
u0 = 0.5          # 表面流速 (m/s)
sec_per_day = 86400  # 每天的秒数
depth_max = 14.0
initial_days = 0.0
initial_log_nu = -6.0
initial_dz = 0.1


def calculate_velocity(depth, t_days, nu_value):
    if t_days <= 0:
        velocity = np.zeros_like(depth)
        # t=0 的边界条件：海表速度为 u0，内部速度为 0
        velocity[np.isclose(depth, 0.0)] = u0
        return velocity
    t_sec = t_days * sec_per_day
    return u0 * erfc(depth / (2 * np.sqrt(nu_value * t_sec)))


def build_depth_grid(dz):
    dz = float(max(0.02, dz))
    point_count = int(round(depth_max / dz)) + 1
    return np.linspace(0.0, depth_max, point_count)


def viscosity_label(nu_value):
    if nu_value < 1e-5:
        return '分子尺度'
    if nu_value < 1e-4:
        return '过渡尺度'
    return '湍流尺度'


fig, ax = plt.subplots(figsize=(8, 11.5))
plt.subplots_adjust(left=0.14, right=0.96, bottom=0.27, top=0.91)

ax.set_xlim(0, 0.55)
ax.set_ylim(depth_max, 0)
ax.xaxis.tick_top()
ax.xaxis.set_label_position('top')
ax.set_xlabel('速度 Speed (m/s)', fontsize=12, labelpad=2)
ax.set_ylabel('深度 Depth (m)', fontsize=12)
ax.set_title('分子粘性到湍流黏度的动量扩散演示', fontsize=14, pad=10)
ax.grid(True, linestyle='--', alpha=0.6)

smooth_depth = np.linspace(0.0, depth_max, 2000)

smooth_line, = ax.plot([], [], color='0.70', linewidth=2.0, label='平滑参考')
day_1_line, = ax.plot([], [], 'k--', alpha=0.45, label='1 Day')
day_10_line, = ax.plot([], [], 'b--', alpha=0.45, label='10 Days')
day_365_line, = ax.plot([], [], 'g--', alpha=0.45, label='365 Days')
current_line, = ax.plot([], [], 'r-o', linewidth=2.2, markersize=3.0, label='当前网格')

info_box = ax.text(
    0.02,
    0.04,
    '',
    transform=ax.transAxes,
    fontsize=11,
    va='bottom',
    ha='left',
    bbox=dict(boxstyle='round,pad=0.35', facecolor='white', edgecolor='0.8', alpha=0.88),
)

ax.legend(loc='lower right')

axcolor = 'lightgoldenrodyellow'
ax_time = plt.axes([0.24, 0.21, 0.64, 0.03], facecolor=axcolor)
ax_vis = plt.axes([0.24, 0.16, 0.64, 0.03], facecolor=axcolor)
ax_res = plt.axes([0.24, 0.11, 0.64, 0.03], facecolor=axcolor)
ax_play = plt.axes([0.18, 0.04, 0.16, 0.045])
ax_reset = plt.axes([0.40, 0.04, 0.16, 0.045])
ax_export = plt.axes([0.62, 0.04, 0.24, 0.045])

s_time = Slider(ax_time, '时间 (天)', 0.0, 365.0, valinit=initial_days, valstep=0.5)
s_vis = Slider(ax_vis, 'log10(ν)', -6.0, -2.0, valinit=initial_log_nu, valstep=0.01)
s_res = Slider(ax_res, '空间步长 Δz (m)', 0.02, 1.0, valinit=initial_dz, valstep=0.01)
btn_play = Button(ax_play, '自动播放')
btn_reset = Button(ax_reset, '重置')
btn_export = Button(ax_export, '导出 GIF')

is_autoplay = False
autoplay_phase = 0.0


def refresh_plot():
    current_days = float(s_time.val)
    nu_value = 10 ** float(s_vis.val)
    dz = float(s_res.val)

    current_depth = build_depth_grid(dz)
    point_count = current_depth.size

    smooth_line.set_data(calculate_velocity(smooth_depth, current_days, nu_value), smooth_depth)
    day_1_line.set_data(calculate_velocity(smooth_depth, 1.0, nu_value), smooth_depth)
    day_10_line.set_data(calculate_velocity(smooth_depth, 10.0, nu_value), smooth_depth)
    day_365_line.set_data(calculate_velocity(smooth_depth, 365.0, nu_value), smooth_depth)
    current_line.set_data(calculate_velocity(current_depth, current_days, nu_value), current_depth)

    ax.set_title(
        f'分子粘性到湍流黏度的动量扩散演示 | ν={nu_value:.1e} m²/s',
        fontsize=14,
        pad=8,
    )
    info_box.set_text(
        f'当前时间：{current_days:.1f} 天\n'
        f'空间步长：{dz:.2f} m（约 {point_count} 点）\n'
        f'黏度：{nu_value:.1e} m²/s（{viscosity_label(nu_value)}）\n'
        f'模式：{"自动播放" if is_autoplay else "手动"}'
    )

    fig.canvas.draw_idle()


def update(_):
    refresh_plot()


def set_autoplay_values(phase):
    # 课堂演示分三段：先扫时间，再扫黏度，最后粗化网格到 1m
    if phase < 0.45:
        local = phase / 0.45
        s_time.set_val(local * 365.0)
    elif phase < 0.80:
        local = (phase - 0.45) / 0.35
        s_vis.set_val(-6.0 + local * 4.0)
    else:
        local = (phase - 0.80) / 0.20
        s_res.set_val(0.02 + local * (1.0 - 0.02))


def on_play(_):
    global is_autoplay
    is_autoplay = not is_autoplay
    btn_play.label.set_text('暂停' if is_autoplay else '自动播放')
    refresh_plot()


def on_reset(_):
    global autoplay_phase
    autoplay_phase = 0.0
    s_time.set_val(initial_days)
    s_vis.set_val(initial_log_nu)
    s_res.set_val(initial_dz)
    refresh_plot()


def on_export(_):
    global is_autoplay, autoplay_phase
    saved_time = float(s_time.val)
    saved_vis = float(s_vis.val)
    saved_res = float(s_res.val)
    saved_phase = float(autoplay_phase)
    was_autoplay = is_autoplay

    is_autoplay = False
    btn_play.label.set_text('自动播放')
    anim.event_source.stop()

    export_dir = Path(__file__).resolve().parent
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    gif_path = export_dir / f'分子粘性课堂演示_{stamp}.gif'
    print('开始导出课堂演示，请稍候...')

    export_frames = np.linspace(0.0, 1.0, 240)

    def export_step(phase):
        set_autoplay_values(float(phase))
        return current_line, smooth_line, day_1_line, day_10_line, day_365_line

    export_anim = animation.FuncAnimation(
        fig,
        export_step,
        frames=export_frames,
        interval=80,
        blit=False,
        repeat=False,
    )

    try:
        export_anim.save(gif_path.as_posix(), writer=animation.PillowWriter(fps=12))
        print(f'GIF 导出完成：{gif_path.name}')
    except Exception as exc:
        print(f'GIF 导出失败：{exc}')

    autoplay_phase = saved_phase
    s_time.set_val(saved_time)
    s_vis.set_val(saved_vis)
    s_res.set_val(saved_res)
    is_autoplay = was_autoplay
    btn_play.label.set_text('暂停' if is_autoplay else '自动播放')
    anim.event_source.start()
    refresh_plot()


def autoplay_step(_):
    global autoplay_phase
    if not is_autoplay:
        return
    autoplay_phase += 0.0035
    if autoplay_phase > 1.0:
        autoplay_phase = 0.0
    set_autoplay_values(autoplay_phase)


s_time.on_changed(update)
s_vis.on_changed(update)
s_res.on_changed(update)
btn_play.on_clicked(on_play)
btn_reset.on_clicked(on_reset)
btn_export.on_clicked(on_export)

anim = animation.FuncAnimation(fig, autoplay_step, interval=80, cache_frame_data=False)

refresh_plot()
print('课堂演示模式已启用：点击“自动播放”开始，点击“暂停”停止。')
plt.show()