import vapoursynth as vs
core = vs.core
clip = video_in
vfps = int(container_fps*1e8)
vden = 1e8

if not (container_fps > 59):
    clip = core.std.AssumeFPS(clip, fpsnum=vfps, fpsden=vden)
    sup  = core.mv.Super(clip, pel=2, sharp=2, rfilter=4,hpad=16,vpad=8,levels=0)
    bvec = core.mv.Analyse(sup,blksize=32,blksizev=16,overlap=16,overlapv=8,
                           levels=0,isb=True,
                           search=3,searchparam=0,pelsearch=3,
                           badrange=-1,badsad=10000,
                          )
#blksize=32,blksizev=16,overlap=16,overlapv=2,
#blksize=32,blksizev=16,overlap=16,overlapv=8,
#4x4, 8x4, 8x8, 16x2, 16x8, 16x16, 32x16, 32x32, 64x32, 64x64, 128x64, or 128x128
    fvec = core.mv.Analyse(sup,blksize=32,blksizev=16,overlap=16,overlapv=8,
                           levels=0,isb=False,
                           search=3,searchparam=0,pelsearch=3,
                           badrange=-1,badsad=10000,
                          )
    clip = core.mv.BlockFPS(clip,sup,bvec,fvec,num=int(vfps*round(60/container_fps,2)),den=vden,mode=2,ml=1020.0,thscd1=16320,thscd2=255)
clip.set_output()