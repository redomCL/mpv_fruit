# 测试用：存在随时不再支持、随时出现错误、随时删除的可能

## uosc dyn_menu lualite：主要用于Windows平台上未来可能向uosc过渡的测试
* 屏控用uosc，菜单用dyn_menu，尽量依靠uosc，减少其他lua数量。

## uosc lualite：主要用于Linux平台上未来可能向uosc过渡的测试，因为dyn_menu是为Windows设计的，Linux无法使用
* 屏控和菜单用uosc，尽量依靠uosc，减少其他lua数量，用于打开文件的外部浏览器依然需要dyn_menu的dialog部分（Linux下使用uosc内置文件浏览器）。
