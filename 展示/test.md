# 预设对比

|级别          |预设          |解码方式          |渲染方式                |色深抖动方式              |预览图质量        |
|------------- |--------------|-----------------|------------------------|-------------------------|-----------------|
|1|移动端|auto-safe|新渲染器，缩放算法：默认|默认(fruit)|0(自动)|
|2|平  衡|d3d11va-copy|新渲染器，缩放算法：内置的 profile=gpu-hq|默认(fruit)|0(自动)|
|3|全精度|CPU|新渲染器，deband=yes,cscale=ewa_lanczos,scale=ewa_lanczos,sigmoid-upscaling=yes,dscale=lanczos,correct-downscaling=yes|误差抖动(内核为floyd-steinberg)|2(高，支持HDR)|
