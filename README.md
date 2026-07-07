* 本分支用于Linux mpv，该分支下只存放Linux mpv必要文件（解码配置、按键配置、脚本、着色器、备用osc），“体验类”等非必要部分通用，为减少项目同步更新压力，请在[主分支](https://github.com/redomCL/mpv_fruit/tree/main)获取、使用和查阅。

* apt默认配置路径：~/.config/mpv

* flatpak的默认配置路径：~/.var/app/io.mpv.Mpv/config/mpv

* 命令行下使用mpv --player-operation-mode=pseudo-gui -v可以打开mpv空窗口，后面添加的-v参数则可以在终端持续输出工作日志，这在调试时可能更有用处。

* 在flatpak版本中，则使用flatpak run io.mpv.Mpv --player-operation-mode=pseudo-gui -v

