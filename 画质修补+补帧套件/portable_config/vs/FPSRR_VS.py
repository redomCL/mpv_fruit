import vapoursynth as vs
core = vs.core
clip = video_in.resize.Bicubic(format=vs.YUV420P8)
vden = 1000
vfps = container_fps*vden
dfps = display_fps*vden
clip = core.std.AssumeFPS(clip, fpsnum=vfps, fpsden=vden)
super = core.mv.Super(clip, pel=2, sharp=0, rfilter=2)
mvfw = core.mv.Analyse(super, blksize=32, isb=False, search=3, dct=5)
mvbw = core.mv.Analyse(super, blksize=32, isb=True,  search=3, dct=5)
clip = core.mv.FlowFPS(clip, super, mvbw, mvfw, num=dfps, den=vden, mask=1)
clip.set_output()
