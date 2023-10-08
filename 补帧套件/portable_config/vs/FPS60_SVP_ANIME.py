#core.std.LoadPlugin("svpflow1_vs64.dll")
#core.std.LoadPlugin("svpflow2_vs64.dll")

import vapoursynth as vs
core = vs.core
clip = video_in
fps = container_fps if container_fps > 0.1 else 23.976

if clip.format.id == vs.YUV420P8:
    clip8 = clip
elif clip.format.id == vs.YUV420P10:
    clip8 = clip.resize.Point(format=vs.YUV420P8)
else:
    clip = clip.resize.Point(format=vs.YUV420P10, dither_type="error_diffusion")
    clip8 = clip.resize.Point(format=vs.YUV420P8)

super_params = "{pel:1,gpu:1,scale:{up:2,down:4},full:false}"
analyse_params ="{block:{w:32,h:32,overlap:2},main:{levels:2,search:{type:4,distance:-16,coarse:{type:4,distance:-6,bad:{range:0}}}},penalty:{plevel:1.3,pzero:110,pnbour:75}},refine:[{thsad:200}]}"
smoothfps_params = "{gpuid:11,rate:{num:5,den:2,abs:false},algo:21,mask:{area:100},scene:{limits:{m1:1800,m2:3600,scene:5200,zero:100,blocks:45}}}"

if (fps < 60):
    super = core.svp1.Super(clip8, super_params)
    vectors = core.svp1.Analyse(super["clip"], super["data"], clip8, analyse_params)
    clip = core.svp2.SmoothFps(clip, super["clip"], super["data"], vectors["clip"], vectors["data"], smoothfps_params, src=clip, fps=fps)

clip.set_output()
