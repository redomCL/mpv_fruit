# 信息公告栏（超出一定时间的会清除）：

#### 🔈❌❌❌webui和mpv_v0.38出现兼容性问题导致闪退，目前尚未修复，如果你使用0.38及以上的mpv，请不要配置webui ——1970.01.01
#### 🔈代码排版以本地notepad++为准。mpv播放器讨论QQ群：611768740 ——1970.01.01

---

# mpv_fruit🍉🍌🍓🍎

![](https://github.com/redomCL/mpv_fruit/blob/main/%E5%B1%95%E7%A4%BA/%E5%B1%95%E7%A4%BA1.png)
![](https://github.com/redomCL/mpv_fruit/blob/main/%E5%B1%95%E7%A4%BA/%E5%B1%95%E7%A4%BA2.png)
![](https://github.com/redomCL/mpv_fruit/blob/main/%E5%B1%95%E7%A4%BA/%E5%B1%95%E7%A4%BA3.png)
![](https://github.com/redomCL/mpv_fruit/blob/main/%E5%B1%95%E7%A4%BA/%E5%B1%95%E7%A4%BA4.png)
![](https://github.com/redomCL/mpv_fruit/blob/main/%E5%B1%95%E7%A4%BA/%E5%B1%95%E7%A4%BA5.png)
![](https://github.com/redomCL/mpv_fruit/blob/main/%E5%B1%95%E7%A4%BA/%E5%B1%95%E7%A4%BA6.png)
![](https://github.com/redomCL/mpv_fruit/blob/main/%E5%B1%95%E7%A4%BA/%E5%B1%95%E7%A4%BA7.png)
![](https://github.com/redomCL/mpv_fruit/blob/main/%E5%B1%95%E7%A4%BA/%E5%B1%95%E7%A4%BA8.png)


# 配置特性🍺：

* 0.基于mpv player、mpv_lazy、dyphire/mpv-config重新组装，仅专注本地PC/HTPC高质量播放（PC/HTPC是不同的高质量情景）。

* 1.使用mpv_lazy作者的osc_plus（本项目改为osc_fruit），osc实现的控制功能：暂停，文件和章节跳转，音频和字幕轨道切换，预览图；osc实现的显示功能：当前播放的文件名，章节，列表，窗口缩放，解码类型，音量，字幕延迟。

* 2.播放器实现的功能：章节列表、播放列表、音频设备列表、轨道列表。通过数字小键盘调节字幕的尺寸、位置。脚本尽可能显示简体中文，并统一了样式，字幕轨道默认选择简体中文。

* 3.通过tsl0922的菜单脚本实现mpv的菜单，并根据个人使用习惯做了简化，该脚本实现的菜单响应速度很快。 

* 4.集成KrigBilateral、NNEDI3、SSIM、Anime4K。

* 5.集成3款补帧方案（mpv_lazy的SVP PRO、RIFE STD）。

* 6.关闭所有默认快捷键，重新定义常用快捷键，并绘制快捷键说明书。

* 7.四种预设，适配不同性能的硬件和情境。详解查看 wiki：https://github.com/redomCL/mpv_fruit/wiki/%E5%85%B3%E4%BA%8E%E9%A2%84%E8%AE%BE 。

* 8.集成了simple-mpv-webui远程控制。

# 目录简介🥢（本项目不能覆盖更新）：

## 更多的目录及文件说明请查看各文件夹内的.md，并自行查阅mpv官方说明书

* 推荐只用本项目配置文件，mpv播放器自行下载 https://github.com/shinchiro/mpv-winbuild-cmake/releases 。

* 官方mpv更新非常频繁，所以本项目有滞后性，出现异常请自行查询mpv官方最新说明书进行修正 https://mpv.io/manual/master/ ，或等待本项目更新。

* /mpv：mpv播放器的配置文件，将该目录下的文件覆盖到mpv播放器根目录即可正常使用。内容为：A.定制好的说明书，B.解码配置，C.快捷键配置，D.脚本，E.着色器（KrigBilateral、NNEDI3、SSIM、Anime4K）。其中Anime4K为原作者的高预设，默认不启用，如果有需求，可在每次播放时按相应快捷键启用。

* /svpflow：收集到的svp补帧引擎，来源：https://github.com/hooke007/MPV_lazy/discussions/114 留作备份。

* /webui控制：simple-mpv-webui远程控制（ https://github.com/open-dynaMIX/simple-mpv-webui ），作为HTPC情境下除使用无线控制器（键鼠、手柄、遥控器等）外的另一个选择，删除了快捷键，并将文字全部替换为中文，能力有限，无法大幅度增强功能，不算完美，仅满足基本，所以默认没有集成到mpv内，如需要该功能，将该目录下的文件覆盖到mpv播放器根目录，默认访问地址为"你的设备IP:8086"。

* /展示：播放器效果展示，随着更新，展示效果可能是过时的，请以实际使用效果为准。
  
* /补帧套件：配置好的补帧套件和对应的快捷键配置，如需要该功能，将该目录下的文件覆盖到mpv播放器根目录，每次播放按相应快捷键启用。

* /解码预设：四种预设，需要时将该目录下的文件覆盖到mpv播放器根目录，详解查看wiki： https://github.com/redomCL/mpv_fruit/wiki/%E5%85%B3%E4%BA%8E%E9%A2%84%E8%AE%BE 。

# 预设对比🆚:

|级别          |预设          |解码             |渲染                    |色深抖动 
|------------- |--------------|-----------------|------------------------|-------------------------|
|1[低]|移动端：<br>适合低性能笔记本和台式，噪音很低|auto-safe|新渲染器<br>缩放算法：内置的profile＝fast|默认(fruit)|
|2[中]|平&emsp;衡：<br>适合普通笔记本和台式，硬件能耗比差可能有噪音，尤其是笔记本|d3d11va|新渲染器<br>缩放算法：内置的profile=gpu-hq|默认(fruit)|
|3[高]|高质量[默认预设]：<br>不考虑功耗的追求画质，仅适合性能好的台式，笔记本噪音可能很大。默认自适应原始的单声道 - 八声道，如果有预期外问题请在mpv.conf中设置"audio-channels=stereo"或其他目标声道数|CPU|新渲染器<br>缩放算法：<br>deband=yes<br>cscale=ewa_lanczos<br>scale=ewa_lanczos<br>sigmoid-upscaling=yes<br>dscale=lanczos<br>correct-downscaling=yes<br>抗震铃(部分失效参数不删除，或许上游作者会重新设计)，开启缩放优化<br>外置KrigBilateral+NNEDI3+SSIM着色器|误差抖动(内核为floyd-steinberg)|
|4[HTPC]|用于HTPC[配置同3，但设置了一些HTPC该有的默认习惯]：<br>√以全屏启动和播放<br>√音频设备独占<br>√杜比家族、DTS家族直通|配置同3|配置同3|配置同3|

# 使用了以下项目🔍：

* mpv player : https://mpv.io/

* mpv player User Scripts : https://github.com/mpv-player/mpv/wiki/User-Scripts

* mpv player Windows build : https://github.com/shinchiro/mpv-winbuild-cmake/releases

* dyphire/mpv-config : https://github.com/dyphire/mpv-config

* mpv_lazy : https://github.com/hooke007/MPV_lazy

* tsl0922/mpv-menu-plugin : https://github.com/tsl0922/mpv-menu-plugin

* Anime4K : https://github.com/bloc97/Anime4K

* KrigBilateral&SSIM : https://gist.github.com/igv

* NNEDI3 : https://github.com/bjin/mpv-prescalers

* simple-mpv-webui : https://github.com/open-dynaMIX/simple-mpv-webui
