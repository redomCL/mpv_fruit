# 测试用：存在随时不再支持、随时出现错误、随时删除的可能

## uosc dyn_menu lualite：主要用于Windows平台上未来可能向uosc过渡的测试
* 屏控用uosc，菜单用dyn_menu，尽量依靠uosc，减少其他lua数量。

## uosc lualite：主要用于Linux平台上未来可能向uosc过渡的测试
* 屏控和菜单完全使用uosc，考虑尽量依靠uosc，减少其他lua数量，该预设也完全弃用了dyn_menu（启用对于Windows上的菜单和文件浏览器）。由于是测试性质，短期不打算正式使用，所以并未归纳到Linux的分支
