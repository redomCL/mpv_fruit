#### https://github.com/hooke007/MPV_lazy/wiki/3_K7sfunc
#### 基于mpv_lazy的SVP_PRO，补帧到142帧(144刷新显示器)

import vapoursynth as vs
from vapoursynth import core
import k7sfunc as k7f
clip = video_in

###用户选项
H_Pre = 1080
Fps_Num = 1420000
Fps_Den = 10001
Abs = True
Cpu = 1
Nvof = False
Gpu = 0
Lk_Fmt = False

## H_Pre	整数，预降低处理源高度（填你的显示器高度）
## Fps_Num	整数，Fps_Num/Fps_Den 的计算结果即最终帧率或倍率
## Fps_Den	整数
## Abs		<True|False> 输出帧率(True)还是倍率(False)
## Cpu		<0|1> 是否只使用CPU
## Nvof		<True|False> 是否启用Optical Flow（nvidia专用）
## Gpu		<0|11|12|21> 使用的显卡序号，0为排序一号
## Lk_Fmt	<True|False> 是否锁定像素格式为yuv420p8

ret = k7f.FPS_CTRL(clip, fps_in=container_fps, fps_ret=True)
clip = k7f.FMT_CTRL(clip, h_max=H_Pre, fmt_pix=1 if Lk_Fmt else 0)
clip = k7f.SVP_PRO(clip, fps_in=container_fps, fps_num=Fps_Num, fps_den=Fps_Den, abs=Abs, nvof=Nvof, cpu=Cpu, gpu=Gpu)
clip.set_output()
