# mpv_fruit🍉🍌🍓🍎

![](https://github.com/redomCL/mpv_fruit/blob/main/%E5%B1%95%E7%A4%BA/%E5%B1%95%E7%A4%BA1.png)
![](https://github.com/redomCL/mpv_fruit/blob/main/%E5%B1%95%E7%A4%BA/%E5%B1%95%E7%A4%BA2.png)
![](https://github.com/redomCL/mpv_fruit/blob/main/%E5%B1%95%E7%A4%BA/%E5%B1%95%E7%A4%BA3.png)
![](https://github.com/redomCL/mpv_fruit/blob/main/%E5%B1%95%E7%A4%BA/%E5%B1%95%E7%A4%BA4.png)
![](https://github.com/redomCL/mpv_fruit/blob/main/%E5%B1%95%E7%A4%BA/%E5%B1%95%E7%A4%BA5.png)

# 配置特性🍺：

* 0.基于mpv player、mpv_lazy重新组装(Repack based on mpv player/mpv_lazy)，仅专注本地高质量播放。

* 1.使用mpv_lazy作者的osc_plus（本项目改为osc_fruit），osc实现的控制功能：暂停，文件和章节跳转，音频和字幕轨道切换，预览图；osc实现的显示功能：当前播放的文件名，章节，列表，窗口缩放，解码类型，音量，字幕延迟。

* 2.播放器实现的功能：章节列表、播放列表、音频设备列表、轨道列表。通过数字小键盘调节字幕的尺寸、位置。脚本尽可能显示简体中文，并统一了样式，字幕轨道默认选择简体中文。

* 3.集成KrigBilateral、NNEDI3、SSIM（默认启用），集成了高配的Anime4K着色器（默认不启用，可快捷键手动激活）。

* 4.集成了3款补帧工具(mpv_lazy的SVP PRO、RIFE STD)。

* 5.关闭所有默认快捷键，重新定义常用快捷键，并绘制快捷键说明书。

* 6.3款解码预设，供不同性能硬件使用。

# 目录简介🥢(本项目不能覆盖更新)：

* 推荐只用本项目下的配置文件，mpv自行下载 [shichiro mpv windows build](https://github.com/shinchiro/mpv-winbuild-cmake/releases) ，不推荐本项目下的release，没有本项目配置文件更新及时，容易过时。

* 官方mpv更新非常频繁，因此本项目有滞后性，若出现异常请自行查询官方mpv最新说明书进行修正或等待项目更新：https://mpv.io/manual/master/

* /mpv：定制好的说明书、字体、高质量解码配置、快捷键、脚本、KrigBilateral、NNEDI3、SSIM着色器（默认启用）、高配的Anime4K着色器（默认不启用，按相应快捷键激活）。

* /svpflow：收集到的svp补帧引擎文件，来源：https://github.com/hooke007/MPV_lazy/discussions/114 留作备份。

* /展示：图片展示，随着更新，展示效果可能是过时的，请以实际使用效果为准。
  
* /补帧套件：集成好的补帧套件、对应按键开关，需要时将该目录下的文件直接覆盖到mpv播放器根目录。

# 预设对比🆚:

|级别          |预设          |解码方式          |渲染方式                |色深抖动方式              |预览图质量        |
|------------- |--------------|-----------------|------------------------|-------------------------|-----------------|
|1[低]|移动端|auto-safe|新渲染器<br>缩放算法：内置的profile＝fast|默认(fruit)|0(自动)|
|2[中]|平&emsp;衡|d3d11va|新渲染器<br>缩放算法：内置的profile=gpu-hq<br>外置SSIM着色器|默认(fruit)|0(自动)|
|3[高]|全精度|CPU|新渲染器<br>缩放算法：<br>deband=yes<br>cscale=ewa_lanczos<br>scale=ewa_lanczos<br>sigmoid-upscaling=yes<br>dscale=lanczos<br>correct-downscaling=yes<br>抗震铃(部分失效参数不删除，或许上游作者会重新设计)，开启缩放优化<br>外置KrigBilateral+NNEDI3+SSIM着色器|误差抖动(内核为floyd-steinberg)|2(高，支持HDR)|

# 使用了以下项目🔍：

* mpv player : https://mpv.io/

* mpv player User Scripts : https://github.com/mpv-player/mpv/wiki/User-Scripts

* mpv player Windows build : https://github.com/shinchiro/mpv-winbuild-cmake/releases

* dyphire/mpv-config : https://github.com/dyphire/mpv-config

* mpv_lazy : https://github.com/hooke007/MPV_lazy

* Anime4K : https://github.com/bloc97/Anime4K

* KrigBilateral&SSIM : https://gist.github.com/igv

* NNEDI3 : https://github.com/bjin/mpv-prescalers
