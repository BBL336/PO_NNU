"""将 Panel 应用导出为独立 HTML 文件"""
import panel as pn
import sys

pn.extension('mathjax')

# 导入应用
from tea_cup_physics import (
    physics, stirring_toggle, omega_slider, auto_animate, 
    frame_interval, reset_button, update_button, plot_3d, 
    plot_top, explanation_pane, header, controls, visualization, explanation
)

# 创建模板
template = pn.template.FastListTemplate(
    title='茶杯搅拌物理演示',
    sidebar=[controls],
    main=[header, visualization, explanation],
    accent_base_color='#4CAF50',
    header_background='#2E7D32'
)

# 导出为 HTML
output_file = "tea_cup_physics.html"
template.save(output_file)
print(f"✅ HTML 文件已生成：{output_file}")
print(f"📍 在浏览器中打开：file:///{__file__.replace(chr(92), '/').rsplit('/', 1)[0]}/{output_file}")
