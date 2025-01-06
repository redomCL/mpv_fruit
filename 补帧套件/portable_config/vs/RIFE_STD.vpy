#### https://github.com/hooke007/MPV_lazy/wiki/3_K7sfunc#rife_std
#### RIFE倍帧

import vapoursynth as vs
from vapoursynth import core
import k7sfunc as k7f
clip = video_in

###用户选项
H_Pre = 1080
Model = 23
T_Tta = False
Fps_Num = 2
Fps_Den = 1
Sc_Mode = 1
Skip = True
Stat_Th = 60.0
Gpu = 0
Gpu_T = 2
Lk_Fmt = False

## H_Pre	整数，预降低处理源高度（填你的显示器高度）
## Model	当前使用的模型23，当前可用的模型<23|70|72|73> 
## T_Tta 	<True|False> 是否使用ensemble版模型
## Fps_Num	整数，Fps_Num/Fps_Den 的值即帧率倍数
## Fps_Den	整数,Fps_Num/Fps_Den 的值即帧率倍数
## Sc_Mode	<0|1|2> 场景切换检测的模式，0为禁用
## Skip		<True|False> 是否跳过静止帧的补偿计算
## Stat_Th	浮点，静止帧的判定阈值
## Gpu		使用的显卡序号，0为排序一号
## Gpu_T	<1|2|3> 显卡线程数
## Lk_Fmt	<True|False> 是否锁定像素格式为yuv420p8

ret = k7f.FPS_CTRL(clip, fps_in=container_fps, fps_ret=True)
clip = k7f.FMT_CTRL(clip, h_max=H_Pre, fmt_pix=1 if Lk_Fmt else 0)
clip = k7f.RIFE_STD(clip, model=Model, t_tta=T_Tta, fps_num=Fps_Num, fps_den=Fps_Den, sc_mode=Sc_Mode, skip=Skip, stat_th=Stat_Th, gpu=Gpu, gpu_t=Gpu_T)
clip.set_output()
