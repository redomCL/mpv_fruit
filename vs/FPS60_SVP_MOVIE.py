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

super_params = "{pel:1,gpu:1,scale:{up:0},full:false}"
analyse_params = "{block:{overlap:0},main:{search:{coarse:{distance:-12,bad:{sad:2000}},type:2}},refine:[{thsad:250}]}"
smoothfps_params = "{gpuid:11,rate:{num:60,den:1,abs:true},algo:1,mask:{area:50}}"

if (fps < 59):
    super = core.svp1.Super(clip8, super_params)
    vectors = core.svp1.Analyse(super["clip"], super["data"], clip8, analyse_params)
    clip = core.svp2.SmoothFps(clip, super["clip"], super["data"], vectors["clip"], vectors["data"], smoothfps_params, src=clip, fps=fps)

clip.set_output()
