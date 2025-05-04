#### https://github.com/hooke007/MPV_lazy/wiki/3_K7sfunc
#### RIFE (v4+) 倍帧，性能要求较高，N卡专用

import vapoursynth as vs
from vapoursynth import core
import k7sfunc as k7f
clip = video_in

###用户选项
H_Pre = 1440
Lt_D2k = False
Model = 46
Ext_Proc = False
T_Tta = False
Fps_Num = 5
Fps_Den = 1
Sc_Mode = 1
Gpu = 0
Gpu_T = 2
St_Eng = False
Ws_Size = 0
Lk_Fmt = False

## H_Pre	整数，预降低处理源高度（填你的显示器高度）
## Lt_D2k	<True|False> 是否对超过DCI2K分辨率的源进行补帧
## Model	<46|4251|426|4262> 使用的模型
## Ext_Proc	<True|False> 是否使用外部的填充裁切处理
## T_Tta	<True|False> 是否使用ensemble版模型
## Fps_Num	整数，Fps_Num/Fps_Den 的值即帧率倍数
## Fps_Den	整数，Fps_Num/Fps_Den 的值即帧率倍数
## Sc_Mode	<0|1|2> 场景切换检测的模式，0为禁用
## Gpu		使用的显卡序号，0为排序一号
## Gpu_T	<1|2|3> 显卡线程数
## St_Eng	<True|False> 是否使用静态引擎（需要对不同分辨率的源各进行预处理）；动态引擎自适应不同分辨率（QVGA→DCI4K）
## Ws_Size	整数，约束显存（MiB），静态引擎的最小值为128（动态引擎自动双倍），设为低于此数的值即最大化利用
## Lk_Fmt	<True|False> 锁定像素格式为yuv420p8

ret = k7f.FPS_CTRL(clip, fps_in=container_fps, fps_ret=True)
clip = k7f.FMT_CTRL(clip, h_max=H_Pre, fmt_pix=1 if Lk_Fmt else 0)
clip = k7f.RIFE_NV(clip, lt_d2k=Lt_D2k, model=Model, ext_proc=Ext_Proc, t_tta=T_Tta, fps_in=container_fps, fps_num=Fps_Num, fps_den=Fps_Den, sc_mode=Sc_Mode, gpu=Gpu, gpu_t=Gpu_T, st_eng=St_Eng, ws_size=Ws_Size)
clip.set_output()
