### https://github.com/hooke007/MPV_lazy/wiki/3_K7sfunc
### svpflow倍帧，中等消耗

import vapoursynth as vs
from vapoursynth import core
import k7sfunc as k7f

clip = video_in

############
# 用户选项 #
############

H_Pre = 1440
Cpu = 0
Gpu = 0
Lk_Fmt = False
## 整数，预降低处理源高度（填你的显示器高度）
## <0|1> 是否只使用CPU
## <0|11|12|21> 使用的显卡序号，0为排序一号
## <True|False> 是否锁定像素格式为yuv420p8

ret = k7f.FPS_CTRL(clip, fps_in=container_fps, fps_ret=True)
clip = k7f.FMT_CTRL(clip, h_max=H_Pre, fmt_pix=1 if Lk_Fmt else 0)
clip = k7f.SVP_LQ(clip, fps_in=container_fps, cpu=Cpu, gpu=Gpu)

clip.set_output()
