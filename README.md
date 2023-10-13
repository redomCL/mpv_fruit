# mpv_fruit🍉🍌🍓🍎

![](https://github.com/redomCL/mpv_fruit/blob/main/%E5%B1%95%E7%A4%BA/%E5%B1%95%E7%A4%BA1.png)
![](https://github.com/redomCL/mpv_fruit/blob/main/%E5%B1%95%E7%A4%BA/%E5%B1%95%E7%A4%BA2.png)
![](https://github.com/redomCL/mpv_fruit/blob/main/%E5%B1%95%E7%A4%BA/%E5%B1%95%E7%A4%BA3.png)
![](https://github.com/redomCL/mpv_fruit/blob/main/%E5%B1%95%E7%A4%BA/%E5%B1%95%E7%A4%BA4.png)
![](https://github.com/redomCL/mpv_fruit/blob/main/%E5%B1%95%E7%A4%BA/%E5%B1%95%E7%A4%BA5.png)

# 配置特性：

* 0.基于mpv player、mpv_lazy重新组装。（Repack based on mpv player/mpv_lazy.）

* 1."osc_plus.lua"改名为"osc_fruit.lua"🍉🍌🍓🍎，重新排版并修改样式。

* 2.修改已集成的lua内的字符串为中文，并统一样式。

* 3.集成了3款补帧脚本和所需要的组件(来自mpv_lazy项目的SVP LQ、SVP HQ、RIFE通用版)。

* 4.集成了广泛认可的NNEDI3和SSIM着色器（此项默认为始终在合适状态自动开启），集成了高配的Anime4K着色器（该着色器只适用于动画类视频，且对画面影响激烈！不同人群主观画质标准不同，因此默认不开启，用户可使用已经设置好的快捷键手动激活）。

* 5.配置了3款预设，供不同性能硬件使用。

* 6.关闭所有默认快捷键，重新定义常用快捷键，并绘制快捷键说明书。

# 使用方法🍉🍌🍓🍎：

* 推荐自行下载 [shichiro mpv windows build](https://github.com/shinchiro/mpv-winbuild-cmake/releases) 然后用本项目下的配置文件覆盖，也可以直接使用本 [release](https://github.com/redomCL/mpv_fruit/releases) 下集成好的mpv播放器压缩包，但不推荐，没有本项目配置文件更新的快，容易过时。

* mpv目录：定制好的说明书、字体、高质量解码配置、快捷键、脚本、NNEDI3和SSIM着色器（此项默认为始终在合适状态自动开启）、高配的Anime4K着色器（该着色器只适用于动画类视频，且对画面影响激烈！不同人群主观画质标准不同，因此默认不开启，用户可使用已经设置好的快捷键手动激活）。
  
* 补帧套件目录：集成好的补帧套件、对应按键开关，需要时将该目录下的文件直接覆盖到mpv播放器根目录。

* 预设配置：内置3种预设，用户可根据不同习惯和硬件性能选择。

* 随着官方mpv的更新，mpv内置的profile默认值可能会发生变化（如默认缩放算法的更换），本项目更新有一定滞后性，因此可能导致项目内3种预设出现预计之外的情况，若出现异常请自行查询官方mpv最新说明书进行修正或等待项目更新：https://mpv.io/manual/master/

# 预设对比🆚:

|级别          |预设          |解码方式          |渲染方式                |色深抖动方式              |预览图质量        |
|------------- |--------------|-----------------|------------------------|-------------------------|-----------------|
|1[低]|移动端|auto-safe|新渲染器<br>缩放算法：内置的profile＝fast|默认(fruit)|0(自动)|
|2[中]|平&emsp;衡|d3d11va|新渲染器<br>缩放算法：内置的profile=gpu-hq<br>外置SSIM着色器|默认(fruit)|0(自动)|
|3[高]|全精度|CPU|新渲染器<br>缩放算法：<br>deband=yes<br>cscale=ewa_lanczos<br>scale=ewa_lanczos<br>sigmoid-upscaling=yes<br>dscale=lanczos<br>correct-downscaling=yes<br>抗震铃(部分失效参数不删除，或许上游作者会重新设计)，开启缩放优化<br>外置NNEDI3+SSIM着色器|误差抖动(内核为floyd-steinberg)|2(高，支持HDR)|

# 使用了以下项目🔍：

* mpv player : https://mpv.io/

* mpv player User Scripts : https://github.com/mpv-player/mpv/wiki/User-Scripts

* mpv player Windows build : https://github.com/shinchiro/mpv-winbuild-cmake/releases

* dyphire/mpv-config : https://github.com/dyphire/mpv-config

* mpv_lazy : https://github.com/hooke007/MPV_lazy

* Anime4K : https://github.com/bloc97/Anime4K

* SSIM : https://gist.github.com/igv

* NNEDI3 : https://github.com/bjin/mpv-prescalers
