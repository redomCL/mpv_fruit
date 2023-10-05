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

* 3.集成了补帧用的引擎，并提供了四款补帧脚本。

* 4.集成了高配的Anime4K着色器。

* 5.配置了3款预设，供不同性能硬件使用。

* 6.关闭所有默认快捷键，重新定义常用快捷键，并绘制快捷键说明书。

* 注：随着mpv的更新，解码和渲染算法会出现变化，这可能导致当前预设出现预计之外的情况，请自行查询mpv最新说明书进行更改，本项目已列举mpv官方说明书地址。

# 使用方法🍉🍌🍓🍎：

* 可以直接使用本 [release](https://github.com/redomCL/mpv_fruit/releases) 下集成好的mpv播放器压缩包，也可以自行下载 [shichiro mpv windows build](https://github.com/shinchiro/mpv-winbuild-cmake/releases) 然后用本项目下的配置文件覆盖。

* mpv目录：为定制好的说明书、字体、默认预设（最高质量解码）、快捷键、脚本，不包含第三方滤镜，适合单纯使用mpv播放器的用户。
  
* 画质修补+补帧套件目录：包含集成好的所有第三方滤镜、对应按键开关等，需要时将该目录下的文件直接覆盖到mpv播放器根目录，覆盖后为本项目完整配置。

* 预设配置：内置3种预设，用户可根据不同习惯和硬件性能选择。

# 预设对比🆚:

|级别          |预设          |解码方式          |渲染方式                |色深抖动方式              |预览图质量        |
|------------- |--------------|-----------------|------------------------|-------------------------|-----------------|
|1|移动端|auto-safe|新渲染器<br>缩放算法：内置的profile＝fast|默认(fruit)|0(自动)|
|2|平  衡|d3d11va-copy|新渲染器<br>缩放算法：内置的 profile=gpu-hq|默认(fruit)|0(自动)|
|3|全精度|CPU|新渲染器<br>缩放算法：<br>deband=yes<br>cscale=ewa_lanczos<br>scale=ewa_lanczos<br>sigmoid-upscaling=yes<br>dscale=lanczos<br>correct-downscaling=yes|误差抖动(内核为floyd-steinberg)|2(高，支持HDR)|

# 使用了以下项目🔍：

* mpv player : https://mpv.io/

* mpv player User Scripts : https://github.com/mpv-player/mpv/wiki/User-Scripts

* mpv player Windows build : https://github.com/shinchiro/mpv-winbuild-cmake/releases

* dyphire/mpv-config : https://github.com/dyphire/mpv-config

* mpv_lazy : https://github.com/hooke007/MPV_lazy

* Anime4K : https://github.com/bloc97/Anime4K
