##################################################
### K7sfunc 的可选附属脚本
##################################################

__version__ = "0.1.1"

__all__ = ["QTGMC", "QTGMC_obs", "QTGMCv2"]


from distutils.version import LooseVersion
import functools
import math
import typing
import vapoursynth as vs

core = vs.core
vstools = None
QTGMC_globals = {}
dfttest2 = None

### MOD HAvsFunc (f11d79c98589c9dcb5b10beec35b631db68b495c)

def QTGMC(
	Input: vs.VideoNode,
	Preset: str = 'Slower',
	TR0: typing.Optional[int] = None,
	TR1: typing.Optional[int] = None,
	TR2: typing.Optional[int] = None,
	Rep0: typing.Optional[int] = None,
	Rep1: int = 0,
	Rep2: typing.Optional[int] = None,
	EdiMode: typing.Optional[str] = None,
	RepChroma: bool = True,
	NNSize: typing.Optional[int] = None,
	NNeurons: typing.Optional[int] = None,
	EdiQual: int = 1,
	EdiMaxD: typing.Optional[int] = None,
	ChromaEdi: str = '',
	EdiExt: typing.Optional[vs.VideoNode] = None,
	Sharpness: typing.Optional[float] = None,
	SMode: typing.Optional[int] = None,
	SLMode: typing.Optional[int] = None,
	SLRad: typing.Optional[int] = None,
	SOvs: int = 0,
	SVThin: float = 0.0,
	Sbb: typing.Optional[int] = None,
	SrchClipPP: typing.Optional[int] = None,
	SubPel: typing.Optional[int] = None,
	SubPelInterp: int = 2,
	BlockSize: typing.Optional[int] = None,
	Overlap: typing.Optional[int] = None,
	Search: typing.Optional[int] = None,
	SearchParam: typing.Optional[int] = None,
	PelSearch: typing.Optional[int] = None,
	ChromaMotion: typing.Optional[bool] = None,
	TrueMotion: bool = False,
	Lambda: typing.Optional[int] = None,
	LSAD: typing.Optional[int] = None,
	PNew: typing.Optional[int] = None,
	PLevel: typing.Optional[int] = None,
	GlobalMotion: bool = True,
	DCT: int = 0,
	ThSAD1: int = 640,
	ThSAD2: int = 256,
	ThSCD1: int = 180,
	ThSCD2: int = 98,
	SourceMatch: int = 0,
	MatchPreset: typing.Optional[str] = None,
	MatchEdi: typing.Optional[str] = None,
	MatchPreset2: typing.Optional[str] = None,
	MatchEdi2: typing.Optional[str] = None,
	MatchTR2: int = 1,
	MatchEnhance: float = 0.5,
	Lossless: int = 0,
	NoiseProcess: typing.Optional[int] = None,
	EZDenoise: typing.Optional[float] = None,
	EZKeepGrain: typing.Optional[float] = None,
	NoisePreset: str = 'Fast',
	Denoiser: typing.Optional[str] = None,
	FftThreads: int = 1,
	DenoiseMC: typing.Optional[bool] = None,
	NoiseTR: typing.Optional[int] = None,
	Sigma: typing.Optional[float] = None,
	ChromaNoise: bool = False,
	ShowNoise: typing.Union[bool, float] = 0.0,
	GrainRestore: typing.Optional[float] = None,
	NoiseRestore: typing.Optional[float] = None,
	NoiseDeint: typing.Optional[str] = None,
	StabilizeNoise: typing.Optional[bool] = None,
	InputType: int = 0,
	ProgSADMask: typing.Optional[float] = None,
	FPSDivisor: int = 1,
	ShutterBlur: int = 0,
	ShutterAngleSrc: float = 180.0,
	ShutterAngleOut: float = 180.0,
	SBlurLimit: int = 4,
	Border: bool = False,
	Precise: typing.Optional[bool] = None,
	Tuning: str = 'None',
	ShowSettings: bool = False,
	GlobalNames: str = 'QTGMC',
	PrevGlobals: str = 'Replace',
	ForceTR: int = 0,
	Str: float = 2.0,
	Amp: float = 0.0625,
	FastMA: bool = False,
	ESearchP: bool = False,
	RefineMotion: bool = False,
	TFF: typing.Optional[bool] = None,
	nnedi3_args: typing.Mapping[str, typing.Any] = {},
	eedi3_args: typing.Mapping[str, typing.Any] = {},
	opencl: bool = False,
	device: typing.Optional[int] = None,
) -> vs.VideoNode:
	'''
	QTGMC 3.33

	A very high quality deinterlacer with a range of features for both quality and convenience. These include a simple presets system, extensive noise
	processing capabilities, support for repair of progressive material, precision source matching, shutter speed simulation, etc. Originally based on
	TempGaussMC_beta2 by Didée.

	Parameters:
		Input: Clip to process.

		Preset: Sets a range of defaults for different encoding speeds.
			Select from "Placebo", "Very Slow", "Slower", "Slow", "Medium", "Fast", "Faster", "Very Fast", "Super Fast", "Ultra Fast" & "Draft".

		TR0: Temporal binomial smoothing radius used to create motion search clip. In general 2=quality, 1=speed, 0=don't use.

		TR1: Temporal binomial smoothing radius used on interpolated clip for initial output. In general 2=quality, 1=speed, 0=don't use.

		TR2: Temporal linear smoothing radius used for final stablization / denoising. Increase for smoother output.

		Rep0: Repair motion search clip (0=off): repair unwanted blur after temporal smooth TR0 (see QTGMC_KeepOnlyBobShimmerFixes function for details).

		Rep1: Repair initial output clip (0=off): repair unwanted blur after temporal smooth TR1.

		Rep2: Repair final output clip (0=off): unwanted blur after temporal smooth TR2 (will also repair TR1 blur if Rep1 not used).

		EdiMode: Interpolation method, from "NNEDI3", "EEDI3+NNEDI3" (EEDI3 with sclip from NNEDI3), "EEDI3" or "Bwdif", anything else uses "Bob".

		RepChroma: Whether the repair modes affect chroma.

		NNSize: Area around each pixel used as predictor for NNEDI3. A larger area is slower with better quality, read the NNEDI3 docs to see the area choices.
			Note: area sizes are not in increasing order (i.e. increased value doesn't always mean increased quality).

		NNeurons: Controls number of neurons in NNEDI3, larger = slower and better quality but improvements are small.

		EdiQual: Quality setting for NNEDI3. Higher values for better quality - but improvements are marginal.

		EdiMaxD: Spatial search distance for finding connecting edges in EEDI3.

		ChromaEdi: Interpolation method used for chroma. Set to "" to use EdiMode above (default). Otherwise choose from "NNEDI3", "Bwdif" or "Bob" - all high
			speed variants. This can give a minor speed-up if using a very slow EdiMode (i.e. one of the EEDIx modes).

		EdiExt: Provide externally created interpolated clip rather than use one of the above modes.

		Sharpness: How much to resharpen the temporally blurred clip (default is always 1.0 unlike original TGMC).

		SMode: Resharpening mode.
			0 = none
			1 = difference from 3x3 blur kernel
			2 = vertical max/min average + 3x3 kernel

		SLMode: Sharpness limiting.
			0 = off
			[1 = spatial, 2 = temporal]: before final temporal smooth
			[3 = spatial, 4 = temporal]: after final temporal smooth

		SLRad: Temporal or spatial radius used with sharpness limiting (depends on SLMode). Temporal radius can only be 0, 1 or 3.

		SOvs: Amount of overshoot allowed with temporal sharpness limiting (SLMode=2,4), i.e. allow some oversharpening.

		SVThin: How much to thin down 1-pixel wide lines that have been widened due to interpolation into neighboring field lines.

		Sbb: Back blend (blurred) difference between pre & post sharpened clip (minor fidelity improvement).
			0 = off
			1 = before (1st) sharpness limiting
			2 = after (1st) sharpness limiting
			3 = both

		SrchClipPP: Pre-filtering for motion search clip.
			0 = none
			1 = simple blur
			2 = Gauss blur
			3 = Gauss blur + edge soften

		SubPel: Sub-pixel accuracy for motion analysis.
			1 = 1 pixel
			2 = 1/2 pixel
			4 = 1/4 pixel

		SubPelInterp: Interpolation used for sub-pixel motion analysis.
			0 = bilinear (soft)
			1 = bicubic (sharper)
			2 = Weiner (sharpest)

		BlockSize: Size of blocks that are matched during motion analysis.

		Overlap: How much to overlap motion analysis blocks (requires more blocks, but essential to smooth block edges in motion compenstion).

		Search: Search method used for matching motion blocks - see MVTools2 documentation for available algorithms.

		SearchParam: Parameter for search method chosen. For default search method (hexagon search) it is the search range.

		PelSearch: Search parameter (as above) for the finest sub-pixel level (see SubPel).

		ChromaMotion: Whether to consider chroma when analyzing motion. Setting to false gives good speed-up,
			but may very occasionally make incorrect motion decision.

		TrueMotion: Whether to use the 'truemotion' defaults from MAnalyse (see MVTools2 documentation).

		Lambda: Motion vector field coherence - how much the motion analysis favors similar motion vectors for neighboring blocks.
			Should be scaled by BlockSize*BlockSize/64.

		LSAD: How much to reduce need for vector coherence (i.e. Lambda above) if prediction of motion vector from neighbors is poor,
			typically in areas of complex motion. This value is scaled in MVTools (unlike Lambda).

		PNew: Penalty for choosing a new motion vector for a block over an existing one - avoids choosing new vectors for minor gain.

		PLevel: Mode for scaling lambda across different sub-pixel levels - see MVTools2 documentation for choices.

		GlobalMotion: Whether to estimate camera motion to assist in selecting block motion vectors.

		DCT: Modes to use DCT (frequency analysis) or SATD as part of the block matching process - see MVTools2 documentation for choices.

		ThSAD1: SAD threshold for block match on shimmer-removing temporal smooth (TR1). Increase to reduce bob-shimmer more (may smear/blur).

		ThSAD2: SAD threshold for block match on final denoising temporal smooth (TR2). Increase to strengthen final smooth (may smear/blur).

		ThSCD1: Scene change detection parameter 1 - see MVTools documentation.

		ThSCD2: Scene change detection parameter 2 - see MVTools documentation.

		SourceMatch:
			0 = source-matching off (standard algorithm)
			1 = basic source-match
			2 = refined match
			3 = twice refined match

		MatchPreset: Speed/quality for basic source-match processing, select from "Placebo", "Very Slow", "Slower", "Slow", "Medium", "Fast", "Faster",
			"Very Fast", "Super Fast", "Ultra Fast" ("Draft" is not supported). Ideal choice is the same as main preset,
			but can choose a faster setting (but not a slower setting). Default is 3 steps faster than main Preset.

		MatchEdi: Override default interpolation method for basic source-match. Default method is same as main EdiMode setting (usually NNEDI3).
			Only need to override if using slow method for main interpolation (e.g. EEDI3) and want a faster method for source-match.

		MatchPreset2: Speed/quality for refined source-match processing, select from "Placebo", "Very Slow", "Slower", "Slow", "Medium", "Fast", "Faster",
			"Very Fast", "Super Fast", "Ultra Fast" ("Draft" is not supported). Default is 2 steps faster than MatchPreset.
			Faster settings are usually sufficient but can use slower settings if you get extra aliasing in this mode.

		MatchEdi2: Override interpolation method for refined source-match. Can be a good idea to pick MatchEdi2="Bob" for speed.

		MatchTR2: Temporal radius for refined source-matching. 2=smoothness, 1=speed/sharper, 0=not recommended. Differences are very marginal.
			Basic source-match doesn't need this setting as its temporal radius must match TR1 core setting (i.e. there is no MatchTR1).

		MatchEnhance: Enhance the detail found by source-match modes 2 & 3. A slight cheat - will enhance noise if set too strong. Best set < 1.0.

		Lossless: Puts exact source fields into result & cleans any artefacts. 0=off, 1=after final temporal smooth, 2=before resharpening.
			Adds some extra detail but: mode 1 gets shimmer / minor combing, mode 2 is more stable/tweakable but not exactly lossless.

		NoiseProcess: Bypass mode.
			0 = disable
			1 = denoise source & optionally restore some noise back at end of script [use for stronger denoising]
			2 = identify noise only & optionally restore some after QTGMC smoothing [for grain retention / light denoising]

		EZDenoise: Automatic setting to denoise source. Set > 0.0 to enable. Higher values denoise more. Can use ShowNoise to help choose value.

		EZKeepGrain: Automatic setting to retain source grain/detail. Set > 0.0 to enable. Higher values retain more grain. A good starting point = 1.0.

		NoisePreset: Automatic setting for quality of noise processing. Choices: "Slower", "Slow", "Medium", "Fast", and "Faster".

		Denoiser: Select denoiser to use for noise bypass / denoising. Select from "bm3d", "dfttest", "fft3dfilter" or "knlmeanscl".
			Unknown value selects "fft3dfilter".

		FftThreads: Number of threads to use if using "fft3dfilter" for Denoiser.

		DenoiseMC: Whether to provide a motion-compensated clip to the denoiser for better noise vs detail detection (will be a little slower).

		NoiseTR: Temporal radius used when analyzing clip for noise extraction. Higher values better identify noise vs detail but are slower.

		Sigma: Amount of noise known to be in the source, sensible values vary by source and denoiser, so experiment. Use ShowNoise to help.

		ChromaNoise: When processing noise (NoiseProcess > 0), whether to process chroma noise or not (luma noise is always processed).

		ShowNoise: Display extracted and "deinterlaced" noise rather than normal output. Set to true or false, or set a value (around 4 to 16) to specify
			contrast for displayed noise. Visualising noise helps to determine suitable value for Sigma or EZDenoise - want to see noise and noisy detail,
			but not too much clean structure or edges - fairly subjective.

		GrainRestore: How much removed noise/grain to restore before final temporal smooth. Retain "stable" grain and some detail (effect depends on TR2).

		NoiseRestore: How much removed noise/grain to restore after final temporal smooth. Retains any kind of noise.

		NoiseDeint: When noise is taken from interlaced source, how to 'deinterlace' it before restoring.
			"Bob" & "DoubleWeave" are fast but with minor issues: "Bob" is coarse and "Doubleweave" lags by one frame.
			"Generate" is a high quality mode that generates fresh noise lines, but it is slower. Unknown value selects "DoubleWeave".

		StabilizeNoise: Use motion compensation to limit shimmering and strengthen detail within the restored noise. Recommended for "Generate" mode.

		InputType: Default = 0 for interlaced input. Settings 1, 2 & 3 accept progressive input for deshimmer or repair. Frame rate of progressive source is not
			doubled. Mode 1 is for general progressive material. Modes 2 & 3 are designed for badly deinterlaced material.

		ProgSADMask: Only applies to InputType=2,3. If ProgSADMask > 0.0 then blend InputType modes 1 and 2/3 based on block motion SAD.
			Higher values help recover more detail, but repair less artefacts. Reasonable range about 2.0 to 20.0, or 0.0 for no blending.

		FPSDivisor: 1=Double-rate output, 2=Single-rate output. Higher values can be used too (e.g. 60fps & FPSDivisor=3 gives 20fps output).

		ShutterBlur: 0=Off, 1=Enable, 2,3=Higher precisions (slower). Higher precisions reduce blur "bleeding" into static areas a little.

		ShutterAngleSrc: Shutter angle used in source. If necessary, estimate from motion blur seen in a single frame.
			0=pin-sharp, 360=fully blurred from frame to frame.

		ShutterAngleOut: Shutter angle to simulate in output. Extreme values may be rejected (depends on other settings).
			Cannot reduce motion blur already in the source.

		SBlurLimit: Limit motion blur where motion lower than given value. Increase to reduce blur "bleeding". 0=Off. Sensible range around 2-12.

		Border: Pad a little vertically while processing (doesn't affect output size) - set true you see flickering on the very top or bottom line of the
			output. If you have wider edge effects than that, you should crop afterwards instead.

		Precise: Set to false to use faster algorithms with *very* slight imprecision in places.

		Tuning: Tweaks the defaults for different source types. Choose from "None", "DV-SD", "DV-HD".

		ShowSettings: Display all the current parameter values - useful to find preset defaults.

		GlobalNames: The name used to expose intermediate clips to calling script. QTGMC now exposes its motion vectors and other intermediate clips to the
			calling script through global variables. These globals are uniquely named. By default they begin with the prefix "QTGMC_". The available clips are:
				Backward motion vectors                 bVec1, bVec2, bVec3 (temporal radius 1 to 3)
				Forward motion vectors                  fVec1, fVec2, fVec3
				Filtered clip used for motion analysis  srchClip
				MVTools "super" clip for filtered clip  srchSuper
			Not all these clips are necessarily created - it depends on your QTGMC settings. To ensure motion vector creation to radius X, set ForceTR=X
			Clips can be accessed from other scripts with havsfunc.QTGMC_globals['Prefix_Name']

		PrevGlobals: What to do with global variables from earlier QTGMC call that match above name. Either "Replace", or "Reuse" (for a speed-up).
			Set PrevGlobals="Reuse" to reuse existing similar named globals for this run & not recalculate motion vectors etc. This will improve performance.
			Set PrevGlobals="Replace" to overwrite similar named globals from a previous run. This is the default and easiest option for most use cases.

		ForceTR: Ensure globally exposed motion vectors are calculated to this radius even if not needed by QTGMC.

		Str: With this parameter you control the strength of the brightening of the prefilter clip for motion analysis.
			This is good when problems with dark areas arise.

		Amp: Use this together with Str (active when Str is different from 1.0). This defines the amplitude of the brightening in the luma range,
			for example by using 1.0 all the luma range will be used and the brightening will find its peak at luma value 128 in the original.

		FastMA: Use 8-bit for faster motion analysis when using high bit depth input.

		ESearchP: Use wider search range for hex and umh search method.

		RefineMotion: Refines and recalculates motion data of previously estimated motion vectors with new parameters set (e.g. lesser block size).
			The two-stage method may be also useful for more stable (robust) motion estimation.

		TFF: Since VapourSynth only has a weak notion of field order internally, TFF may have to be set. Setting TFF to true means top field first and false
			means bottom field first. Note that the _FieldBased frame property, if present, takes precedence over TFF.

		nnedi3_args: Additional arguments to pass to NNEDI3.

		eedi3_args: Additional arguments to pass to EEDI3.

		opencl: Whether to use the OpenCL version of NNEDI3 and EEDI3.

		device: Sets target OpenCL device.
	'''

	global vstools
	if vstools is None :
		import vstools

	import vsdenoise
	import vsexprtools
	import vsrgtools

	global dfttest2
	if dfttest2 is None :
		import dfttest2
	if LooseVersion(dfttest2.__version__) < LooseVersion("0.3.3") :
		raise EnvironmentError("依赖 dfttest2 的版本号过低，至少 0.3.3")

	def _average_frames(
		clip: vs.VideoNode, weights: float | typing.Sequence[float], scenechange: float | None = None, planes: vstools.PlanesT = None
	) -> vs.VideoNode:
		assert vstools.check_variable(clip, _average_frames)
		planes = vstools.normalize_planes(clip, planes)
		def _scdetect(clip: vs.VideoNode, threshold: float = 0.1) -> vs.VideoNode:
			def _copy_property(n: int, f: list[vs.VideoFrame]) -> vs.VideoFrame:
				fout = f[0].copy()
				fout.props["_SceneChangePrev"] = f[1].props["_SceneChangePrev"]
				fout.props["_SceneChangeNext"] = f[1].props["_SceneChangeNext"]
				return fout
			assert vstools.check_variable(clip, _scdetect)
			sc = clip
			if clip.format.color_family == vs.RGB:
				sc = clip.resize.Point(format=vs.GRAY8, matrix_s="709")
			sc = sc.misc.SCDetect(threshold)
			if clip.format.color_family == vs.RGB:
				sc = clip.std.ModifyFrame([clip, sc], _copy_property)
			return sc
		if scenechange:
			clip = _scdetect(clip, scenechange)
		return clip.std.AverageFrames(weights=weights, scenechange=scenechange, planes=planes)

	def _mt_clamp(
		clip: vs.VideoNode,
		bright: vs.VideoNode,
		dark: vs.VideoNode,
		overshoot: int = 0,
		undershoot: int = 0,
		planes: vstools.PlanesT = None,
	) -> vs.VideoNode:
		## clamp the value of the clip between bright + overshoot and dark - undershoot
		vstools.check_ref_clip(clip, bright, _mt_clamp)
		vstools.check_ref_clip(clip, dark, _mt_clamp)
		planes = vstools.normalize_planes(clip, planes)
		if vsexprtools.complexpr_available:
			expr = f"x z {undershoot} - y {overshoot} + clamp"
		else:
			expr = f"x z {undershoot} - max y {overshoot} + min"
		return vsexprtools.norm_expr([clip, bright, dark], expr, planes)

	if not isinstance(Input, vs.VideoNode):
		raise vs.Error('QTGMC: this is not a clip')

	if EdiExt is not None:
		if not isinstance(EdiExt, vs.VideoNode):
			raise vs.Error('QTGMC: EdiExt is not a clip')

		if EdiExt.format.id != Input.format.id:
			raise vs.Error('QTGMC: EdiExt must have the same format as input')

	if InputType != 1 and TFF is None:
		with Input.get_frame(0) as f:
			if (field_based := f.props.get('_FieldBased')) not in [1, 2]:
				raise vs.Error('QTGMC: TFF was not specified and field order could not be determined from frame properties')

		TFF = field_based == 2

	is_gray = Input.format.color_family == vs.GRAY

	bits = vstools.get_depth(Input)
	neutral = 1 << (bits - 1)

	SOvs = vstools.scale_value(SOvs, 8, bits)

	# ---------------------------------------
	# Presets

	# Select presets / tuning
	Preset = Preset.lower()
	presets = ['placebo', 'very slow', 'slower', 'slow', 'medium', 'fast', 'faster', 'very fast', 'super fast', 'ultra fast', 'draft']
	try:
		pNum = presets.index(Preset)
	except ValueError:
		raise vs.Error("QTGMC: 'Preset' choice is invalid")

	if MatchPreset is None:
		mpNum1 = min(pNum + 3, 9)
		MatchPreset = presets[mpNum1]
	else:
		try:
			mpNum1 = presets[:10].index(MatchPreset.lower())
		except ValueError:
			raise vs.Error("QTGMC: 'MatchPreset' choice is invalid/unsupported")

	if MatchPreset2 is None:
		mpNum2 = min(mpNum1 + 2, 9)
		MatchPreset2 = presets[mpNum2]
	else:
		try:
			mpNum2 = presets[:10].index(MatchPreset2.lower())
		except ValueError:
			raise vs.Error("QTGMC: 'MatchPreset2' choice is invalid/unsupported")

	try:
		npNum = presets[2:7].index(NoisePreset.lower())
	except ValueError:
		raise vs.Error("QTGMC: 'NoisePreset' choice is invalid")

	try:
		tNum = ['none', 'dv-sd', 'dv-hd'].index(Tuning.lower())
	except ValueError:
		raise vs.Error("QTGMC: 'Tuning' choice is invalid")

	# Tunings only affect blocksize in this version
	bs = [16, 16, 32][tNum]
	bs2 = 32

	# fmt: off
	#                                                         Very                                                        Very      Super     Ultra
	# Preset groups:                                Placebo   Slow      Slower    Slow      Medium    Fast      Faster    Fast      Fast      Fast      Draft
	TR0 = vstools.fallback(TR0,                   [ 2,        2,        2,        2,        2,        2,        1,        1,        1,        1,        0      ][pNum])
	TR1 = vstools.fallback(TR1,                   [ 2,        2,        2,        1,        1,        1,        1,        1,        1,        1,        1      ][pNum])
	TR2X = vstools.fallback(TR2,                  [ 3,        2,        1,        1,        1,        0,        0,        0,        0,        0,        0      ][pNum])
	Rep0 = vstools.fallback(Rep0,                 [ 4,        4,        4,        4,        3,        3,        0,        0,        0,        0,        0      ][pNum])
	Rep2 = vstools.fallback(Rep2,                 [ 4,        4,        4,        4,        4,        4,        4,        4,        3,        3,        0      ][pNum])
	EdiMode = vstools.fallback(EdiMode,           ['NNEDI3', 'NNEDI3', 'NNEDI3', 'NNEDI3', 'NNEDI3', 'NNEDI3', 'NNEDI3', 'NNEDI3', 'NNEDI3', 'Bwdif',  'Bob'   ][pNum]).lower()
	NNSize = vstools.fallback(NNSize,             [ 1,        1,        1,        1,        5,        5,        4,        4,        4,        4,        4      ][pNum])
	NNeurons = vstools.fallback(NNeurons,         [ 2,        2,        1,        1,        1,        0,        0,        0,        0,        0,        0      ][pNum])
	EdiMaxD = vstools.fallback(EdiMaxD,           [ 12,       10,       8,        7,        7,        6,        6,        5,        4,        4,        4      ][pNum])
	SMode = vstools.fallback(SMode,               [ 2,        2,        2,        2,        2,        2,        2,        2,        2,        2,        0      ][pNum])
	SLModeX = vstools.fallback(SLMode,            [ 2,        2,        2,        2,        2,        2,        2,        2,        0,        0,        0      ][pNum])
	SLRad = vstools.fallback(SLRad,               [ 3,        1,        1,        1,        1,        1,        1,        1,        1,        1,        1      ][pNum])
	Sbb = vstools.fallback(Sbb,                   [ 3,        1,        1,        0,        0,        0,        0,        0,        0,        0,        0      ][pNum])
	SrchClipPP = vstools.fallback(SrchClipPP,     [ 3,        3,        3,        3,        3,        2,        2,        2,        1,        1,        0      ][pNum])
	SubPel = vstools.fallback(SubPel,             [ 2,        2,        2,        2,        1,        1,        1,        1,        1,        1,        1      ][pNum])
	BlockSize = vstools.fallback(BlockSize,       [ bs,       bs,       bs,       bs,       bs,       bs,       bs2,      bs2,      bs2,      bs2,      bs2    ][pNum])
	bs = BlockSize
	Overlap = vstools.fallback(Overlap,           [ bs // 2,  bs // 2,  bs // 2,  bs // 2,  bs // 2,  bs // 2,  bs // 2,  bs // 4,  bs // 4,  bs // 4,  bs // 4][pNum])
	Search = vstools.fallback(Search,             [ 5,        4,        4,        4,        4,        4,        4,        4,        0,        0,        0      ][pNum])
	SearchParam = vstools.fallback(SearchParam,   [ 2,        2,        2,        2,        2,        2,        2,        1,        1,        1,        1      ][pNum])
	PelSearch = vstools.fallback(PelSearch,       [ 2,        2,        2,        2,        1,        1,        1,        1,        1,        1,        1      ][pNum])
	ChromaMotion = vstools.fallback(ChromaMotion, [ True,     True,     True,     False,    False,    False,    False,    False,    False,    False,    False  ][pNum])
	Precise = vstools.fallback(Precise,           [ True,     True,     False,    False,    False,    False,    False,    False,    False,    False,    False  ][pNum])
	ProgSADMask = vstools.fallback(ProgSADMask,   [ 10.0,     10.0,     10.0,     10.0,     10.0,     0.0,      0.0,      0.0,      0.0,      0.0,      0.0    ][pNum])

	if ESearchP and Search in [4, 5]:
		if pNum < 4:
			SearchParam = 24
		elif pNum < 8:
			SearchParam = 16

	# Noise presets                                     Slower      Slow       Medium     Fast      Faster
	Denoiser = vstools.fallback(Denoiser,             ['dfttest',  'dfttest', 'dfttest', 'fft3df', 'fft3df'][npNum]).lower()
	DenoiseMC = vstools.fallback(DenoiseMC,           [ True,       True,      False,     False,    False  ][npNum])
	NoiseTR = vstools.fallback(NoiseTR,               [ 2,          1,         1,         1,        0      ][npNum])
	NoiseDeint = vstools.fallback(NoiseDeint,         ['Generate', 'Bob',      '',        '',       ''     ][npNum]).lower()
	StabilizeNoise = vstools.fallback(StabilizeNoise, [ True,       True,      True,      False,    False  ][npNum])
	# fmt: on

	# The basic source-match step corrects and re-runs the interpolation of the input clip. So it initially uses same interpolation settings as the main preset
	MatchNNSize = NNSize
	MatchNNeurons = NNeurons
	MatchEdiMaxD = EdiMaxD
	MatchEdiQual = EdiQual

	# However, can use a faster initial interpolation when using source-match allowing the basic source-match step to "correct" it with higher quality settings
	if SourceMatch > 0 and mpNum1 < pNum:
		raise vs.Error("QTGMC: 'MatchPreset' cannot use a slower setting than 'Preset'")
	# Basic source-match presets
	if SourceMatch > 0:
		# fmt: off
		#                    Very                                      Very  Super  Ultra
		#           Placebo  Slow  Slower  Slow  Medium  Fast  Faster  Fast  Fast   Fast
		NNSize =   [1,       1,    1,      1,    5,      5,    4,      4,    4,     4    ][mpNum1]
		NNeurons = [2,       2,    1,      1,    1,      0,    0,      0,    0,     0    ][mpNum1]
		EdiMaxD =  [12,      10,   8,      7,    7,      6,    6,      5,    4,     4    ][mpNum1]
		EdiQual =  [1,       1,    1,      1,    1,      1,    1,      1,    1,     1    ][mpNum1]
		# fmt: on
	TempEdi = EdiMode  # Main interpolation is actually done by basic-source match step when enabled, so a little swap and wriggle is needed
	if SourceMatch > 0:
		EdiMode = vstools.fallback(MatchEdi, EdiMode if mpNum1 < 9 else 'Bwdif').lower()  # Force Bwdif for "Ultra Fast" basic source match
	MatchEdi = TempEdi

	# fmt: off
	#                                           Very                                                        Very      Super    Ultra
	# Refined source-match presets    Placebo   Slow      Slower    Slow      Medium    Fast      Faster    Fast      Fast     Fast
	MatchEdi2 = vstools.fallback(MatchEdi2, ['NNEDI3', 'NNEDI3', 'NNEDI3', 'NNEDI3', 'NNEDI3', 'NNEDI3', 'NNEDI3', 'NNEDI3', 'NNEDI3', ''   ][mpNum2]).lower()
	MatchNNSize2 =                  [ 1,        1,        1,        1,        5,        5,        4,        4,        4,       4    ][mpNum2]
	MatchNNeurons2 =                [ 2,        2,        1,        1,        1,        0,        0,        0,        0,       0    ][mpNum2]
	MatchEdiMaxD2 =                 [ 12,       10,       8,        7,        7,        6,        6,        5,        4,       4    ][mpNum2]
	MatchEdiQual2 =                 [ 1,        1,        1,        1,        1,        1,        1,        1,        1,       1    ][mpNum2]
	# fmt: on

	# ---------------------------------------
	# Settings

	# Core defaults
	TR2 = vstools.fallback(TR2, max(TR2X, 1)) if SourceMatch > 0 else TR2X  # ***TR2 defaults always at least 1 when using source-match***

	# Source-match defaults
	MatchTR1 = TR1

	# Sharpness defaults. Sharpness default is always 1.0 (0.2 with source-match), but adjusted to give roughly same sharpness for all settings
	if Sharpness is not None and Sharpness <= 0:
		SMode = 0
	SLMode = vstools.fallback(SLMode, 0) if SourceMatch > 0 else SLModeX  # ***Sharpness limiting disabled by default for source-match***
	if SLRad <= 0:
		SLMode = 0
	spatialSL = SLMode in [1, 3]
	temporalSL = SLMode in [2, 4]
	Sharpness = vstools.fallback(Sharpness, 0.0 if SMode <= 0 else 0.2 if SourceMatch > 0 else 1.0)  # Default sharpness is 1.0, or 0.2 if using source-match
	sharpMul = 2 if temporalSL else 1.5 if spatialSL else 1  # Adjust sharpness based on other settings
	sharpAdj = Sharpness * (sharpMul * (0.2 + TR1 * 0.15 + TR2 * 0.25) + (0.1 if SMode == 1 else 0))  # [This needs a bit more refinement]
	if SMode <= 0:
		Sbb = 0

	# Noise processing settings
	if EZDenoise is not None and EZDenoise > 0 and EZKeepGrain is not None and EZKeepGrain > 0:
		raise vs.Error("QTGMC: EZDenoise and EZKeepGrain cannot be used together")
	if NoiseProcess is None:
		if EZDenoise is not None and EZDenoise > 0:
			NoiseProcess = 1
		elif (EZKeepGrain is not None and EZKeepGrain > 0) or Preset in ['placebo', 'very slow']:
			NoiseProcess = 2
		else:
			NoiseProcess = 0
	if GrainRestore is None:
		if EZDenoise is not None and EZDenoise > 0:
			GrainRestore = 0.0
		elif EZKeepGrain is not None and EZKeepGrain > 0:
			GrainRestore = 0.3 * math.sqrt(EZKeepGrain)
		else:
			GrainRestore = [0.0, 0.7, 0.3][NoiseProcess]
	if NoiseRestore is None:
		if EZDenoise is not None and EZDenoise > 0:
			NoiseRestore = 0.0
		elif EZKeepGrain is not None and EZKeepGrain > 0:
			NoiseRestore = 0.1 * math.sqrt(EZKeepGrain)
		else:
			NoiseRestore = [0.0, 0.3, 0.1][NoiseProcess]
	if Sigma is None:
		if EZDenoise is not None and EZDenoise > 0:
			Sigma = EZDenoise
		elif EZKeepGrain is not None and EZKeepGrain > 0:
			Sigma = 4.0 * EZKeepGrain
		else:
			Sigma = 2.0
	if isinstance(ShowNoise, bool):
		ShowNoise = 10.0 if ShowNoise else 0.0
	if ShowNoise > 0:
		NoiseProcess = 2
		NoiseRestore = 1.0
	if NoiseProcess <= 0:
		NoiseTR = 0
		GrainRestore = 0.0
		NoiseRestore = 0.0
	totalRestore = GrainRestore + NoiseRestore
	if totalRestore <= 0:
		StabilizeNoise = False
	noiseTD = [1, 3, 5][NoiseTR]
	noiseCentre = vstools.scale_value(128.5, 8, bits) if Denoiser in ['fft3df', 'fft3dfilter'] else neutral

	# MVTools settings
	Lambda = vstools.fallback(Lambda, (1000 if TrueMotion else 100) * BlockSize * BlockSize // 64)
	LSAD = vstools.fallback(LSAD, 1200 if TrueMotion else 400)
	PNew = vstools.fallback(PNew, 50 if TrueMotion else 25)
	PLevel = vstools.fallback(PLevel, 1 if TrueMotion else 0)

	# Motion blur settings
	if ShutterAngleOut * FPSDivisor == ShutterAngleSrc:  # If motion blur output is same as input
		ShutterBlur = 0

	# Miscellaneous
	PrevGlobals = PrevGlobals.lower()
	ReplaceGlobals = PrevGlobals in ['replace', 'reuse']  # If reusing existing globals put them back afterwards - simplifies logic later
	ReuseGlobals = PrevGlobals == 'reuse'
	if InputType < 2:
		ProgSADMask = 0.0

	# Get maximum temporal radius needed
	maxTR = max(SLRad if temporalSL else 0, MatchTR2, TR1, TR2, NoiseTR)
	if (ProgSADMask > 0 or StabilizeNoise or ShutterBlur > 0) and maxTR < 1:
		maxTR = 1
	maxTR = max(ForceTR, maxTR)

	# ---------------------------------------
	# Pre-Processing

	w = Input.width
	h = Input.height

	# Reverse "field" dominance for progressive repair mode 3 (only difference from mode 2)
	if InputType >= 3:
		TFF = not TFF

	# Pad vertically during processing (to prevent artefacts at top & bottom edges)
	if Border:
		h += 8
		clip = Input.resize.Point(w, h, src_top=-4, src_height=h)
	else:
		clip = Input

	hpad = vpad = BlockSize

	# ---------------------------------------
	# Motion Analysis

	# Bob the input as a starting point for motion search clip
	if InputType <= 0:
		bobbed = clip.resize.Bob(tff=TFF, filter_param_a=0, filter_param_b=0.5)
	elif InputType == 1:
		bobbed = clip
	else:
		bobbed = clip.std.Convolution(matrix=[1, 2, 1], mode='v')

	# If required, get any existing global clips with a matching "GlobalNames" setting. Unmatched values get None
	if ReuseGlobals:
		srchClip = QTGMC_GetUserGlobal(GlobalNames, 'srchClip')
		srchSuper = QTGMC_GetUserGlobal(GlobalNames, 'srchSuper')
		bVec1 = QTGMC_GetUserGlobal(GlobalNames, 'bVec1')
		fVec1 = QTGMC_GetUserGlobal(GlobalNames, 'fVec1')
		bVec2 = QTGMC_GetUserGlobal(GlobalNames, 'bVec2')
		fVec2 = QTGMC_GetUserGlobal(GlobalNames, 'fVec2')
		bVec3 = QTGMC_GetUserGlobal(GlobalNames, 'bVec3')
		fVec3 = QTGMC_GetUserGlobal(GlobalNames, 'fVec3')
	else:
		srchClip = srchSuper = bVec1 = fVec1 = bVec2 = fVec2 = bVec3 = fVec3 = None

	CMplanes = [0, 1, 2] if ChromaMotion and not is_gray else [0]

	# The bobbed clip will shimmer due to being derived from alternating fields. Temporally smooth over the neighboring frames using a binomial kernel. Binomial
	# kernels give equal weight to even and odd frames and hence average away the shimmer. The two kernels used are [1 2 1] and [1 4 6 4 1] for radius 1 and 2.
	# These kernels are approximately Gaussian kernels, which work well as a prefilter before motion analysis (hence the original name for this script)
	# Create linear weightings of neighbors first                                                  -2    -1    0     1     2
	if not isinstance(srchClip, vs.VideoNode):
		if TR0 > 0:
			ts1 = _average_frames(bobbed, weights=[1] * 3, scenechange=28 / 255, planes=CMplanes)  # 0.00  0.33  0.33  0.33  0.00
		if TR0 > 1:
			ts2 = _average_frames(bobbed, weights=[1] * 5, scenechange=28 / 255, planes=CMplanes)  # 0.20  0.20  0.20  0.20  0.20

	# Combine linear weightings to give binomial weightings - TR0=0: (1), TR0=1: (1:2:1), TR0=2: (1:4:6:4:1)
	if isinstance(srchClip, vs.VideoNode):
		binomial0 = None
	elif TR0 <= 0:
		binomial0 = bobbed
	elif TR0 == 1:
		binomial0 = core.std.Merge(ts1, bobbed, weight=0.25 if ChromaMotion or is_gray else [0.25, 0])
	else:
		binomial0 = core.std.Merge(
			core.std.Merge(ts1, ts2, weight=0.357 if ChromaMotion or is_gray else [0.357, 0]), bobbed, weight=0.125 if ChromaMotion or is_gray else [0.125, 0]
		)

	# Remove areas of difference between temporal blurred motion search clip and bob that are not due to bob-shimmer - removes general motion blur
	if isinstance(srchClip, vs.VideoNode) or Rep0 <= 0:
		repair0 = binomial0
	else:
		repair0 = QTGMC_KeepOnlyBobShimmerFixes(binomial0, bobbed, Rep0, RepChroma and ChromaMotion)

	matrix = [1, 2, 1, 2, 4, 2, 1, 2, 1]

	# Blur image and soften edges to assist in motion matching of edge blocks. Blocks are matched by SAD (sum of absolute differences between blocks), but even
	# a slight change in an edge from frame to frame will give a high SAD due to the higher contrast of edges
	if not isinstance(srchClip, vs.VideoNode):
		if SrchClipPP == 1:
			spatialBlur = repair0.resize.Bilinear(w // 2, h // 2).std.Convolution(matrix=matrix, planes=CMplanes).resize.Bilinear(w, h)
		elif SrchClipPP >= 2:
			spatialBlur = vsrgtools.gauss_blur(repair0.std.Convolution(matrix=matrix, planes=CMplanes), 1.75)
			spatialBlur = core.std.Merge(spatialBlur, repair0, weight=0.1 if ChromaMotion or is_gray else [0.1, 0])
		if SrchClipPP <= 0:
			srchClip = repair0
		elif SrchClipPP < 3:
			srchClip = spatialBlur
		else:
			expr = 'x {i3} + y < x {i3} + x {i3} - y > x {i3} - y ? ?'.format(i3=vstools.scale_value(3, 8, bits))
			tweaked = core.std.Expr([repair0, bobbed], expr=expr if ChromaMotion or is_gray else [expr, ''])
			expr = 'x {i7} + y < x {i2} + x {i7} - y > x {i2} - x 51 * y 49 * + 100 / ? ?'.format(i7=vstools.scale_value(7, 8, bits), i2=vstools.scale_value(2, 8, bits))
			srchClip = core.std.Expr([spatialBlur, tweaked], expr=expr if ChromaMotion or is_gray else [expr, ''])
		srchClip = vsdenoise.prefilter_to_full_range(srchClip, Str, CMplanes)
		if bits > 8 and FastMA:
			srchClip = vstools.depth(srchClip, 8, dither_type=vstools.DitherType.NONE)

	super_args = dict(pel=SubPel, hpad=hpad, vpad=vpad)
	analyse_args = dict(
		blksize=BlockSize,
		overlap=Overlap,
		search=Search,
		searchparam=SearchParam,
		pelsearch=PelSearch,
		truemotion=TrueMotion,
		lambda_=Lambda,
		lsad=LSAD,
		pnew=PNew,
		plevel=PLevel,
		global_=GlobalMotion,
		dct=DCT,
		chroma=ChromaMotion,
	)
	recalculate_args = dict(
		thsad=ThSAD1 // 2,
		blksize=max(BlockSize // 2, 4),
		search=Search,
		searchparam=SearchParam,
		chroma=ChromaMotion,
		truemotion=TrueMotion,
		pnew=PNew,
		overlap=max(Overlap // 2, 2),
		dct=DCT,
	)

	# Calculate forward and backward motion vectors from motion search clip
	if maxTR > 0:
		if not isinstance(srchSuper, vs.VideoNode):
			srchSuper = srchClip.mv.Super(sharp=SubPelInterp, chroma=ChromaMotion, **super_args)
		if not isinstance(bVec1, vs.VideoNode):
			bVec1 = srchSuper.mv.Analyse(isb=True, delta=1, **analyse_args)
			if RefineMotion:
				bVec1 = core.mv.Recalculate(srchSuper, bVec1, **recalculate_args)
		if not isinstance(fVec1, vs.VideoNode):
			fVec1 = srchSuper.mv.Analyse(isb=False, delta=1, **analyse_args)
			if RefineMotion:
				fVec1 = core.mv.Recalculate(srchSuper, fVec1, **recalculate_args)
	if maxTR > 1:
		if not isinstance(bVec2, vs.VideoNode):
			bVec2 = srchSuper.mv.Analyse(isb=True, delta=2, **analyse_args)
			if RefineMotion:
				bVec2 = core.mv.Recalculate(srchSuper, bVec2, **recalculate_args)
		if not isinstance(fVec2, vs.VideoNode):
			fVec2 = srchSuper.mv.Analyse(isb=False, delta=2, **analyse_args)
			if RefineMotion:
				fVec2 = core.mv.Recalculate(srchSuper, fVec2, **recalculate_args)
	if maxTR > 2:
		if not isinstance(bVec3, vs.VideoNode):
			bVec3 = srchSuper.mv.Analyse(isb=True, delta=3, **analyse_args)
			if RefineMotion:
				bVec3 = core.mv.Recalculate(srchSuper, bVec3, **recalculate_args)
		if not isinstance(fVec3, vs.VideoNode):
			fVec3 = srchSuper.mv.Analyse(isb=False, delta=3, **analyse_args)
			if RefineMotion:
				fVec3 = core.mv.Recalculate(srchSuper, fVec3, **recalculate_args)

	# Expose search clip, motion search super clip and motion vectors to calling script through globals
	if ReplaceGlobals:
		QTGMC_SetUserGlobal(GlobalNames, 'srchClip', srchClip)
		QTGMC_SetUserGlobal(GlobalNames, 'srchSuper', srchSuper)
		QTGMC_SetUserGlobal(GlobalNames, 'bVec1', bVec1)
		QTGMC_SetUserGlobal(GlobalNames, 'fVec1', fVec1)
		QTGMC_SetUserGlobal(GlobalNames, 'bVec2', bVec2)
		QTGMC_SetUserGlobal(GlobalNames, 'fVec2', fVec2)
		QTGMC_SetUserGlobal(GlobalNames, 'bVec3', bVec3)
		QTGMC_SetUserGlobal(GlobalNames, 'fVec3', fVec3)

	# ---------------------------------------
	# Noise Processing

	# Expand fields to full frame size before extracting noise (allows use of motion vectors which are frame-sized)
	if NoiseProcess > 0:
		if InputType > 0:
			fullClip = clip
		else:
			fullClip = clip.resize.Bob(tff=TFF, filter_param_a=0, filter_param_b=1)
	if NoiseTR > 0:
		fullSuper = fullClip.mv.Super(levels=1, chroma=ChromaNoise, **super_args)  # TEST chroma OK?

	CNplanes = [0, 1, 2] if ChromaNoise and not is_gray else [0]

	if NoiseProcess > 0:
		# Create a motion compensated temporal window around current frame and use to guide denoisers
		if not DenoiseMC or NoiseTR <= 0:
			noiseWindow = fullClip
		elif NoiseTR == 1:
			noiseWindow = core.std.Interleave(
				[
					core.mv.Compensate(fullClip, fullSuper, fVec1, thscd1=ThSCD1, thscd2=ThSCD2),
					fullClip,
					core.mv.Compensate(fullClip, fullSuper, bVec1, thscd1=ThSCD1, thscd2=ThSCD2),
				]
			)
		else:
			noiseWindow = core.std.Interleave(
				[
					core.mv.Compensate(fullClip, fullSuper, fVec2, thscd1=ThSCD1, thscd2=ThSCD2),
					core.mv.Compensate(fullClip, fullSuper, fVec1, thscd1=ThSCD1, thscd2=ThSCD2),
					fullClip,
					core.mv.Compensate(fullClip, fullSuper, bVec1, thscd1=ThSCD1, thscd2=ThSCD2),
					core.mv.Compensate(fullClip, fullSuper, bVec2, thscd1=ThSCD1, thscd2=ThSCD2),
				]
			)
		if Denoiser == 'bm3d':
			dnWindow = vsdenoise.BM3D.denoise(noiseWindow, Sigma, NoiseTR, planes=CNplanes)
		elif Denoiser == 'dfttest':
			dnWindow = dfttest2.DFTTest(clip=noiseWindow, sigma=Sigma * 4, tbsize=noiseTD, planes=CNplanes) #TODO:GPU
		elif Denoiser in ['knlm', 'knlmeanscl']:
			dnWindow = vsdenoise.nl_means(noiseWindow, strength=Sigma, tr=NoiseTR, planes=CNplanes)
		else:
			dnWindow = noiseWindow.fft3dfilter.FFT3DFilter(sigma=Sigma, planes=CNplanes, bt=noiseTD, ncpu=FftThreads)

		# Rework denoised clip to match source format - various code paths here: discard the motion compensation window, discard doubled lines (from point resize)
		# Also reweave to get interlaced noise if source was interlaced (could keep the full frame of noise, but it will be poor quality from the point resize)
		if not DenoiseMC:
			if InputType > 0:
				denoised = dnWindow
			else:
				denoised = dnWindow.std.SeparateFields(tff=TFF).std.SelectEvery(cycle=4, offsets=[0, 3]).std.DoubleWeave(TFF)[::2]
		elif InputType > 0:
			if NoiseTR <= 0:
				denoised = dnWindow
			else:
				denoised = dnWindow.std.SelectEvery(cycle=noiseTD, offsets=NoiseTR)
		else:
			denoised = dnWindow.std.SeparateFields(tff=TFF).std.SelectEvery(cycle=noiseTD * 4, offsets=[NoiseTR * 2, NoiseTR * 6 + 3]).std.DoubleWeave(TFF)[::2]

		if totalRestore > 0:
			# Get actual noise from difference. Then 'deinterlace' where we have weaved noise - create the missing lines of noise in various ways
			noise = core.std.MakeDiff(clip, denoised, planes=CNplanes)
			if InputType > 0:
				deintNoise = noise
			elif NoiseDeint == 'bob':
				deintNoise = noise.resize.Bob(tff=TFF, filter_param_a=0, filter_param_b=0.5)
			elif NoiseDeint == 'generate':
				deintNoise = QTGMC_Generate2ndFieldNoise(noise, denoised, ChromaNoise, TFF)
			else:
				deintNoise = noise.std.SeparateFields(tff=TFF).std.DoubleWeave(tff=TFF)

			# Motion-compensated stabilization of generated noise
			if StabilizeNoise:
				noiseSuper = deintNoise.mv.Super(sharp=SubPelInterp, levels=1, chroma=ChromaNoise, **super_args)
				mcNoise = core.mv.Compensate(deintNoise, noiseSuper, bVec1, thscd1=ThSCD1, thscd2=ThSCD2)
				expr = f'x {neutral} - abs y {neutral} - abs > x y ? 0.6 * x y + 0.2 * +'
				finalNoise = core.std.Expr([deintNoise, mcNoise], expr=expr if ChromaNoise or is_gray else [expr, ''])
			else:
				finalNoise = deintNoise

	# If NoiseProcess=1 denoise input clip. If NoiseProcess=2 leave noise in the clip and let the temporal blurs "denoise" it for a stronger effect
	innerClip = denoised if NoiseProcess == 1 else clip

	# ---------------------------------------
	# Interpolation

	# Support badly deinterlaced progressive content - drop half the fields and reweave to get 1/2fps interlaced stream appropriate for QTGMC processing
	if InputType > 1:
		ediInput = innerClip.std.SeparateFields(tff=TFF).std.SelectEvery(cycle=4, offsets=[0, 3]).std.DoubleWeave(TFF)[::2]
	else:
		ediInput = innerClip

	# Create interpolated image as starting point for output
	if EdiExt is not None:
		edi1 = EdiExt.resize.Point(w, h, src_top=(EdiExt.height - h) // 2, src_height=h)
	else:
		edi1 = QTGMC_Interpolate(
			ediInput, InputType, EdiMode, NNSize, NNeurons, EdiQual, EdiMaxD, bobbed, ChromaEdi.lower(), TFF, nnedi3_args, eedi3_args, opencl, device
		)

	# InputType=2,3: use motion mask to blend luma between original clip & reweaved clip based on ProgSADMask setting. Use chroma from original clip in any case
	if InputType < 2:
		edi = edi1
	elif ProgSADMask <= 0:
		if not is_gray:
			edi = core.std.ShufflePlanes([edi1, innerClip], planes=[0, 1, 2], colorfamily=Input.format.color_family)
		else:
			edi = edi1
	else:
		inputTypeBlend = core.mv.Mask(srchClip, bVec1, kind=1, ml=ProgSADMask)
		edi = core.std.MaskedMerge(innerClip, edi1, inputTypeBlend, planes=0)

	# Get the max/min value for each pixel over neighboring motion-compensated frames - used for temporal sharpness limiting
	if TR1 > 0 or temporalSL:
		ediSuper = edi.mv.Super(sharp=SubPelInterp, levels=1, **super_args)
	if temporalSL:
		bComp1 = core.mv.Compensate(edi, ediSuper, bVec1, thscd1=ThSCD1, thscd2=ThSCD2)
		fComp1 = core.mv.Compensate(edi, ediSuper, fVec1, thscd1=ThSCD1, thscd2=ThSCD2)
		tMax = core.std.Expr([core.std.Expr([edi, fComp1], expr='x y max'), bComp1], expr='x y max')
		tMin = core.std.Expr([core.std.Expr([edi, fComp1], expr='x y min'), bComp1], expr='x y min')
		if SLRad > 1:
			bComp3 = core.mv.Compensate(edi, ediSuper, bVec3, thscd1=ThSCD1, thscd2=ThSCD2)
			fComp3 = core.mv.Compensate(edi, ediSuper, fVec3, thscd1=ThSCD1, thscd2=ThSCD2)
			tMax = core.std.Expr([core.std.Expr([tMax, fComp3], expr='x y max'), bComp3], expr='x y max')
			tMin = core.std.Expr([core.std.Expr([tMin, fComp3], expr='x y min'), bComp3], expr='x y min')

	# ---------------------------------------
	# Create basic output

	# Use motion vectors to blur interpolated image (edi) with motion-compensated previous and next frames. As above, this is done to remove shimmer from
	# alternate frames so the same binomial kernels are used. However, by using motion-compensated smoothing this time we avoid motion blur. The use of
	# MDegrain1 (motion compensated) rather than TemporalSmooth makes the weightings *look* different, but they evaluate to the same values
	# Create linear weightings of neighbors first                                                               -2    -1    0     1     2
	if TR1 > 0:
		degrain1 = core.mv.Degrain1(edi, ediSuper, bVec1, fVec1, thsad=ThSAD1, thscd1=ThSCD1, thscd2=ThSCD2)  # 0.00  0.33  0.33  0.33  0.00
	if TR1 > 1:
		degrain2 = core.mv.Degrain1(edi, ediSuper, bVec2, fVec2, thsad=ThSAD1, thscd1=ThSCD1, thscd2=ThSCD2)  # 0.33  0.00  0.33  0.00  0.33

	# Combine linear weightings to give binomial weightings - TR1=0: (1), TR1=1: (1:2:1), TR1=2: (1:4:6:4:1)
	if TR1 <= 0:
		binomial1 = edi
	elif TR1 == 1:
		binomial1 = core.std.Merge(degrain1, edi, weight=0.25)
	else:
		binomial1 = core.std.Merge(core.std.Merge(degrain1, degrain2, weight=0.2), edi, weight=0.0625)

	# Remove areas of difference between smoothed image and interpolated image that are not bob-shimmer fixes: repairs residual motion blur from temporal smooth
	if Rep1 <= 0:
		repair1 = binomial1
	else:
		repair1 = QTGMC_KeepOnlyBobShimmerFixes(binomial1, edi, Rep1, RepChroma)

	# Apply source match - use difference between output and source to succesively refine output [extracted to function to clarify main code path]
	if SourceMatch <= 0:
		match = repair1
	else:
		match = QTGMC_ApplySourceMatch(
			repair1,
			InputType,
			ediInput,
			bVec1 if maxTR > 0 else None,
			fVec1 if maxTR > 0 else None,
			bVec2 if maxTR > 1 else None,
			fVec2 if maxTR > 1 else None,
			SubPel,
			SubPelInterp,
			hpad,
			vpad,
			ThSAD1,
			ThSCD1,
			ThSCD2,
			SourceMatch,
			MatchTR1,
			MatchEdi,
			MatchNNSize,
			MatchNNeurons,
			MatchEdiQual,
			MatchEdiMaxD,
			MatchTR2,
			MatchEdi2,
			MatchNNSize2,
			MatchNNeurons2,
			MatchEdiQual2,
			MatchEdiMaxD2,
			MatchEnhance,
			TFF,
			nnedi3_args,
			eedi3_args,
			opencl,
			device,
		)

	# Lossless=2 - after preparing an interpolated, de-shimmered clip, restore the original source fields into it and clean up any artefacts
	# This mode will not give a true lossless result because the resharpening and final temporal smooth are still to come, but it will add further detail
	# However, it can introduce minor combing. This setting is best used together with source-match (it's effectively the final source-match stage)
	if Lossless >= 2:
		lossed1 = QTGMC_MakeLossless(match, innerClip, InputType, TFF)
	else:
		lossed1 = match

	# ---------------------------------------
	# Resharpen / retouch output

	# Resharpen to counteract temporal blurs. Little sharpening needed for source-match mode since it has already recovered sharpness from source
	if SMode <= 0:
		resharp = lossed1
	elif SMode == 1:
		resharp = core.std.Expr([lossed1, lossed1.std.Convolution(matrix=matrix)], expr=f'x x y - {sharpAdj} * +')
	else:
		vresharp1 = core.std.Merge(lossed1.std.Maximum(coordinates=[0, 1, 0, 0, 0, 0, 1, 0]), lossed1.std.Minimum(coordinates=[0, 1, 0, 0, 0, 0, 1, 0]))
		if Precise:  # Precise mode: reduce tiny overshoot
			vresharp = core.std.Expr([vresharp1, lossed1], expr='x y < x {i1} + x y > x {i1} - x ? ?'.format(i1=vstools.scale_value(1, 8, bits)))
		else:
			vresharp = vresharp1
		resharp = core.std.Expr([lossed1, vresharp.std.Convolution(matrix=matrix)], expr=f'x x y - {sharpAdj} * +')

	# Slightly thin down 1-pixel high horizontal edges that have been widened into neighboring field lines by the interpolator
	SVThinSc = SVThin * 6.0
	if SVThin > 0:
		expr = f'y x - {SVThinSc} * {neutral} +'
		vertMedD = core.std.Expr([lossed1, lossed1.rgvs.VerticalCleaner(mode=1 if is_gray else [1, 0])], expr=expr if is_gray else [expr, ''])
		vertMedD = vertMedD.std.Convolution(matrix=[1, 2, 1], planes=0, mode='h')
		expr = f'y {neutral} - abs x {neutral} - abs > y {neutral} ?'
		neighborD = core.std.Expr([vertMedD, vertMedD.std.Convolution(matrix=matrix, planes=0)], expr=expr if is_gray else [expr, ''])
		thin = core.std.MergeDiff(resharp, neighborD, planes=0)
	else:
		thin = resharp

	# Back blend the blurred difference between sharpened & unsharpened clip, before (1st) sharpness limiting (Sbb == 1,3). A small fidelity improvement
	if Sbb not in [1, 3]:
		backBlend1 = thin
	else:
		backBlend1 = core.std.MakeDiff(thin, vsrgtools.gauss_blur(core.std.MakeDiff(thin, lossed1, planes=0).std.Convolution(matrix=matrix, planes=0), 1.2), planes=0)

	# Limit over-sharpening by clamping to neighboring (spatial or temporal) min/max values in original
	# Occurs here (before final temporal smooth) if SLMode == 1,2. This location will restrict sharpness more, but any artefacts introduced will be smoothed
	if SLMode == 1:
		if SLRad <= 1:
			sharpLimit1 = core.rgvs.Repair(backBlend1, edi, mode=1)
		else:
			sharpLimit1 = core.rgvs.Repair(backBlend1, core.rgvs.Repair(backBlend1, edi, mode=12), mode=1)
	elif SLMode == 2:
		sharpLimit1 = _mt_clamp(backBlend1, tMax, tMin, SOvs, SOvs)
	else:
		sharpLimit1 = backBlend1

	# Back blend the blurred difference between sharpened & unsharpened clip, after (1st) sharpness limiting (Sbb == 2,3). A small fidelity improvement
	if Sbb < 2:
		backBlend2 = sharpLimit1
	else:
		backBlend2 = core.std.MakeDiff(
			sharpLimit1, vsrgtools.gauss_blur(core.std.MakeDiff(sharpLimit1, lossed1, planes=0).std.Convolution(matrix=matrix, planes=0), 1.2), planes=0
		)

	# Add back any extracted noise, prior to final temporal smooth - this will restore detail that was removed as "noise" without restoring the noise itself
	# Average luma of FFT3DFilter extracted noise is 128.5, so deal with that too
	if GrainRestore <= 0:
		addNoise1 = backBlend2
	else:
		expr = f'x {noiseCentre} - {GrainRestore} * {neutral} +'
		addNoise1 = core.std.MergeDiff(backBlend2, finalNoise.std.Expr(expr=expr if ChromaNoise or is_gray else [expr, '']), planes=CNplanes)

	# Final light linear temporal smooth for denoising
	if TR2 > 0:
		stableSuper = addNoise1.mv.Super(sharp=SubPelInterp, levels=1, **super_args)
	if TR2 <= 0:
		stable = addNoise1
	elif TR2 == 1:
		stable = core.mv.Degrain1(addNoise1, stableSuper, bVec1, fVec1, thsad=ThSAD2, thscd1=ThSCD1, thscd2=ThSCD2)
	elif TR2 == 2:
		stable = core.mv.Degrain2(addNoise1, stableSuper, bVec1, fVec1, bVec2, fVec2, thsad=ThSAD2, thscd1=ThSCD1, thscd2=ThSCD2)
	else:
		stable = core.mv.Degrain3(addNoise1, stableSuper, bVec1, fVec1, bVec2, fVec2, bVec3, fVec3, thsad=ThSAD2, thscd1=ThSCD1, thscd2=ThSCD2)

	# Remove areas of difference between final output & basic interpolated image that are not bob-shimmer fixes: repairs motion blur caused by temporal smooth
	if Rep2 <= 0:
		repair2 = stable
	else:
		repair2 = QTGMC_KeepOnlyBobShimmerFixes(stable, edi, Rep2, RepChroma)

	# Limit over-sharpening by clamping to neighboring (spatial or temporal) min/max values in original
	# Occurs here (after final temporal smooth) if SLMode == 3,4. Allows more sharpening here, but more prone to introducing minor artefacts
	if SLMode == 3:
		if SLRad <= 1:
			sharpLimit2 = core.rgvs.Repair(repair2, edi, mode=1)
		else:
			sharpLimit2 = core.rgvs.Repair(repair2, core.rgvs.Repair(repair2, edi, mode=12), mode=1)
	elif SLMode >= 4:
		sharpLimit2 = _mt_clamp(repair2, tMax, tMin, SOvs, SOvs)
	else:
		sharpLimit2 = repair2

	# Lossless=1 - inject source fields into result and clean up inevitable artefacts. Provided NoiseRestore=0.0 or 1.0, this mode will make the script result
	# properly lossless, but this will retain source artefacts and cause some combing (where the smoothed deinterlace doesn't quite match the source)
	if Lossless == 1:
		lossed2 = QTGMC_MakeLossless(sharpLimit2, innerClip, InputType, TFF)
	else:
		lossed2 = sharpLimit2

	# Add back any extracted noise, after final temporal smooth. This will appear as noise/grain in the output
	# Average luma of FFT3DFilter extracted noise is 128.5, so deal with that too
	if NoiseRestore <= 0:
		addNoise2 = lossed2
	else:
		expr = f'x {noiseCentre} - {NoiseRestore} * {neutral} +'
		addNoise2 = core.std.MergeDiff(lossed2, finalNoise.std.Expr(expr=expr if ChromaNoise or is_gray else [expr, '']), planes=CNplanes)

	# ---------------------------------------
	# Post-Processing

	# Shutter motion blur - get level of blur depending on output framerate and blur already in source
	blurLevel = (ShutterAngleOut * FPSDivisor - ShutterAngleSrc) * 100 / 360
	if blurLevel < 0:
		raise vs.Error('QTGMC: cannot reduce motion blur already in source: increase ShutterAngleOut or FPSDivisor')
	if blurLevel > 200:
		raise vs.Error('QTGMC: exceeded maximum motion blur level: decrease ShutterAngleOut or FPSDivisor')

	# ShutterBlur mode 2,3 - get finer resolution motion vectors to reduce blur "bleeding" into static areas
	rBlockDivide = [1, 1, 2, 4][ShutterBlur]
	rBlockSize = max(BlockSize // rBlockDivide, 4)
	rOverlap = max(Overlap // rBlockDivide, 2)
	rBlockDivide = BlockSize // rBlockSize
	rLambda = Lambda // (rBlockDivide * rBlockDivide)
	if ShutterBlur > 1:
		recalculate_args = dict(
			thsad=ThSAD1,
			blksize=rBlockSize,
			overlap=rOverlap,
			search=Search,
			searchparam=SearchParam,
			truemotion=TrueMotion,
			lambda_=rLambda,
			pnew=PNew,
			dct=DCT,
			chroma=ChromaMotion,
		)
		sbBVec1 = core.mv.Recalculate(srchSuper, bVec1, **recalculate_args)
		sbFVec1 = core.mv.Recalculate(srchSuper, fVec1, **recalculate_args)
	elif ShutterBlur > 0:
		sbBVec1 = bVec1
		sbFVec1 = fVec1

	# Shutter motion blur - use MFlowBlur to blur along motion vectors
	if ShutterBlur > 0:
		sblurSuper = addNoise2.mv.Super(sharp=SubPelInterp, levels=1, **super_args)
		sblur = core.mv.FlowBlur(addNoise2, sblurSuper, sbBVec1, sbFVec1, blur=blurLevel, thscd1=ThSCD1, thscd2=ThSCD2)

	# Shutter motion blur - use motion mask to reduce blurring in areas of low motion - also helps reduce blur "bleeding" into static areas, then select blur type
	if ShutterBlur <= 0:
		sblurred = addNoise2
	elif SBlurLimit <= 0:
		sblurred = sblur
	else:
		sbMotionMask = core.mv.Mask(srchClip, bVec1, kind=0, ml=SBlurLimit)
		sblurred = core.std.MaskedMerge(addNoise2, sblur, sbMotionMask)

	# Reduce frame rate
	if FPSDivisor > 1:
		decimated = sblurred.std.SelectEvery(cycle=FPSDivisor, offsets=0)
	else:
		decimated = sblurred

	# Crop off temporary vertical padding
	if Border:
		cropped = decimated.std.Crop(top=4, bottom=4)
	else:
		cropped = decimated

	# Show output of choice + settings
	if ShowNoise <= 0:
		output = cropped
	else:
		expr = f'x {neutral} - {ShowNoise} * {neutral} +'
		output = finalNoise.std.Expr(expr=expr if ChromaNoise or is_gray else [expr, repr(neutral)])
	output = output.std.SetFieldBased(value=0)
	if not ShowSettings:
		return output
	else:
		text = (
			f'{TR0=} | {TR1=} | {TR2=} | {Rep0=} | {Rep1=} | {Rep2=} | {RepChroma=} | {EdiMode=} | {NNSize=} | {NNeurons=} | {EdiQual=} | {EdiMaxD=} | '
			+ f'{ChromaEdi=} | {Sharpness=} | {SMode=} | {SLMode=} | {SLRad=} | {SOvs=} | {SVThin=} | {Sbb=} | {SrchClipPP=} | {SubPel=} | {SubPelInterp=} | '
			+ f'{BlockSize=} | {Overlap=} | {Search=} | {SearchParam=} | {PelSearch=} | {ChromaMotion=} | {TrueMotion=} | {Lambda=} | {LSAD=} | {PNew=} | '
			+ f'{PLevel=} | {GlobalMotion=} | {DCT=} | {ThSAD1=} | {ThSAD2=} | {ThSCD1=} | {ThSCD2=} | {SourceMatch=} | {MatchPreset=} | {MatchEdi=} | '
			+ f'{MatchPreset2=} | {MatchEdi2=} | {MatchTR2=} | {MatchEnhance=} | {Lossless=} | {NoiseProcess=} | {Denoiser=} | {FftThreads=} | {DenoiseMC=} | '
			+ f'{NoiseTR=} | {Sigma=} | {ChromaNoise=} | {ShowNoise=} | {GrainRestore=} | {NoiseRestore=} | {NoiseDeint=} | {StabilizeNoise=} | {InputType=} | '
			+ f'{ProgSADMask=} | {FPSDivisor=} | {ShutterBlur=} | {ShutterAngleSrc=} | {ShutterAngleOut=} | {SBlurLimit=} | {Border=} | {Precise=} | '
			+ f'{Preset=} | {Tuning=} | {GlobalNames=} | {PrevGlobals=} | {ForceTR=} | {Str=} | {Amp=} | {FastMA=} | {ESearchP=} | {RefineMotion=}'
		)
		return output.text.Text(text=text)

def QTGMC_Interpolate(
	Input: vs.VideoNode,
	InputType: int,
	EdiMode: str,
	NNSize: int,
	NNeurons: int,
	EdiQual: int,
	EdiMaxD: int,
	Fallback: typing.Optional[vs.VideoNode] = None,
	ChromaEdi: str = '',
	TFF: typing.Optional[bool] = None,
	nnedi3_args: typing.Mapping[str, typing.Any] = {},
	eedi3_args: typing.Mapping[str, typing.Any] = {},
	opencl: bool = False,
	device: typing.Optional[int] = None,
) -> vs.VideoNode:
	'''
	Interpolate input clip using method given in EdiMode. Use Fallback or Bob as result if mode not in list. If ChromaEdi string if set then interpolate chroma
	separately with that method (only really useful for EEDIx). The function is used as main algorithm starting point and for first two source-match stages
	'''

	global vstools
	if vstools is None :
		import vstools

	is_gray = Input.format.color_family == vs.GRAY
	if is_gray:
		ChromaEdi = ''
	planes = [0, 1, 2] if ChromaEdi == '' and not is_gray else [0]

	field = 3 if TFF else 2

	if opencl:
		nnedi3 = functools.partial(core.nnedi3cl.NNEDI3CL, field=field, device=device, **nnedi3_args)
		eedi3 = functools.partial(core.eedi3m.EEDI3CL, field=field, planes=planes, mdis=EdiMaxD, device=device, **eedi3_args)
	else:
		nnedi3 = functools.partial(core.znedi3.nnedi3, field=field, **nnedi3_args)
		eedi3 = functools.partial(core.eedi3m.EEDI3, field=field, planes=planes, mdis=EdiMaxD, **eedi3_args)

	if InputType == 1:
		return Input
	elif EdiMode == 'nnedi3':
		interp = nnedi3(Input, planes=planes, nsize=NNSize, nns=NNeurons, qual=EdiQual)
	elif EdiMode == 'eedi3+nnedi3':
		interp = eedi3(Input, sclip=nnedi3(Input, planes=planes, nsize=NNSize, nns=NNeurons, qual=EdiQual))
	elif EdiMode == 'eedi3':
		interp = eedi3(Input)
	elif EdiMode == 'bwdif':
		interp = Input.bwdif.Bwdif(field=field)
	else:
		interp = vstools.fallback(Fallback, Input.resize.Bob(tff=TFF, filter_param_a=0, filter_param_b=0.5))

	if ChromaEdi == 'nnedi3':
		interpuv = nnedi3(Input, planes=[1, 2], nsize=4, nns=0, qual=1)
	elif ChromaEdi == 'bwdif':
		interpuv = Input.bwdif.Bwdif(field=field)
	elif ChromaEdi == 'bob':
		interpuv = Input.resize.Bob(tff=TFF, filter_param_a=0, filter_param_b=0.5)
	else:
		return interp

	return core.std.ShufflePlanes([interp, interpuv], planes=[0, 1, 2], colorfamily=Input.format.color_family)

def QTGMC_KeepOnlyBobShimmerFixes(Input: vs.VideoNode, Ref: vs.VideoNode, Rep: int = 1, Chroma: bool = True) -> vs.VideoNode:
	'''
	Helper function: Compare processed clip with reference clip: only allow thin, horizontal areas of difference, i.e. bob shimmer fixes
	Rough algorithm: Get difference, deflate vertically by a couple of pixels or so, then inflate again. Thin regions will be removed
					by this process. Restore remaining areas of difference back to as they were in reference clip
	'''

	global vstools
	if vstools is None :
		import vstools

	is_gray = Input.format.color_family == vs.GRAY
	planes = [0, 1, 2] if Chroma and not is_gray else [0]

	bits = vstools.get_depth(Input)
	neutral = 1 << (bits - 1)

	# ed is the erosion distance - how much to deflate then reflate to remove thin areas of interest: 0 = minimum to 6 = maximum
	# od is over-dilation level  - extra inflation to ensure areas to restore back are fully caught:  0 = none to 3 = one full pixel
	# If Rep < 10, then ed = Rep and od = 0, otherwise ed = 10s digit and od = 1s digit (nasty method, but kept for compatibility with original TGMC)
	ed = Rep if Rep < 10 else Rep // 10
	od = 0 if Rep < 10 else Rep % 10

	diff = core.std.MakeDiff(Ref, Input)

	coordinates = [0, 1, 0, 0, 0, 0, 1, 0]

	# Areas of positive difference
	choke1 = diff.std.Minimum(planes=planes, coordinates=coordinates)
	if ed > 2:
		choke1 = choke1.std.Minimum(planes=planes, coordinates=coordinates)
	if ed > 5:
		choke1 = choke1.std.Minimum(planes=planes, coordinates=coordinates)
	if ed % 3 != 0:
		choke1 = choke1.std.Deflate(planes=planes)
	if ed in [2, 5]:
		choke1 = choke1.std.Median(planes=planes)
	choke1 = choke1.std.Maximum(planes=planes, coordinates=coordinates)
	if ed > 1:
		choke1 = choke1.std.Maximum(planes=planes, coordinates=coordinates)
	if ed > 4:
		choke1 = choke1.std.Maximum(planes=planes, coordinates=coordinates)

	# Over-dilation - extra reflation up to about 1 pixel
	if od == 1:
		choke1 = choke1.std.Inflate(planes=planes)
	elif od == 2:
		choke1 = choke1.std.Inflate(planes=planes).std.Inflate(planes=planes)
	elif od >= 3:
		choke1 = choke1.std.Maximum(planes=planes)

	# Areas of negative difference (similar to above)
	choke2 = diff.std.Maximum(planes=planes, coordinates=coordinates)
	if ed > 2:
		choke2 = choke2.std.Maximum(planes=planes, coordinates=coordinates)
	if ed > 5:
		choke2 = choke2.std.Maximum(planes=planes, coordinates=coordinates)
	if ed % 3 != 0:
		choke2 = choke2.std.Inflate(planes=planes)
	if ed in [2, 5]:
		choke2 = choke2.std.Median(planes=planes)
	choke2 = choke2.std.Minimum(planes=planes, coordinates=coordinates)
	if ed > 1:
		choke2 = choke2.std.Minimum(planes=planes, coordinates=coordinates)
	if ed > 4:
		choke2 = choke2.std.Minimum(planes=planes, coordinates=coordinates)

	if od == 1:
		choke2 = choke2.std.Deflate(planes=planes)
	elif od == 2:
		choke2 = choke2.std.Deflate(planes=planes).std.Deflate(planes=planes)
	elif od >= 3:
		choke2 = choke2.std.Minimum(planes=planes)

	# Combine above areas to find those areas of difference to restore
	expr1 = f'x {vstools.scale_value(129, 8, bits)} < x y {neutral} < {neutral} y ? ?'
	expr2 = f'x {vstools.scale_value(127, 8, bits)} > x y {neutral} > {neutral} y ? ?'
	restore = core.std.Expr(
		[core.std.Expr([diff, choke1], expr=expr1 if Chroma or is_gray else [expr1, '']), choke2], expr=expr2 if Chroma or is_gray else [expr2, '']
	)
	return core.std.MergeDiff(Input, restore, planes=planes)

def QTGMC_Generate2ndFieldNoise(Input: vs.VideoNode, InterleavedClip: vs.VideoNode, ChromaNoise: bool = False, TFF: typing.Optional[bool] = None) -> vs.VideoNode:
	'''
	Given noise extracted from an interlaced source (i.e. the noise is interlaced), generate "progressive" noise with a new "field" of noise injected. The new
	noise is centered on a weighted local average and uses the difference between local min & max as an estimate of local variance
	'''

	global vstools
	if vstools is None :
		import vstools

	is_gray = Input.format.color_family == vs.GRAY
	planes = [0, 1, 2] if ChromaNoise and not is_gray else [0]

	bits = vstools.get_depth(Input)
	neutral = 1 << (bits - 1)

	origNoise = Input.std.SeparateFields(tff=TFF)
	noiseMax = origNoise.std.Maximum(planes=planes).std.Maximum(planes=planes, coordinates=[0, 0, 0, 1, 1, 0, 0, 0])
	noiseMin = origNoise.std.Minimum(planes=planes).std.Minimum(planes=planes, coordinates=[0, 0, 0, 1, 1, 0, 0, 0])
	random = (
		InterleavedClip.std.SeparateFields(tff=TFF)
		.std.BlankClip(color=[neutral] * Input.format.num_planes)
		.grain.Add(var=1800, uvar=1800 if ChromaNoise else 0)
	)
	expr = f'x {neutral} - y * {vstools.scale_value(256, 8, bits)} / {neutral} +'
	varRandom = core.std.Expr([core.std.MakeDiff(noiseMax, noiseMin, planes=planes), random], expr=expr if ChromaNoise or is_gray else [expr, ''])
	newNoise = core.std.MergeDiff(noiseMin, varRandom, planes=planes)
	return core.std.Interleave([origNoise, newNoise]).std.DoubleWeave(TFF)[::2]

def QTGMC_MakeLossless(Input: vs.VideoNode, Source: vs.VideoNode, InputType: int, TFF: typing.Optional[bool] = None) -> vs.VideoNode:
	'''
	Insert the source lines into the result to create a true lossless output. However, the other lines in the result have had considerable processing and won't
	exactly match source lines. There will be some slight residual combing. Use vertical medians to clean a little of this away
	'''

	global vstools
	if vstools is None :
		import vstools

	if InputType == 1:
		raise vs.Error('QTGMC: lossless modes are incompatible with InputType=1')

	neutral = 1 << (vstools.get_depth(Input) - 1)

	# Weave the source fields and the "new" fields that have generated in the input
	if InputType <= 0:
		srcFields = Source.std.SeparateFields(tff=TFF)
	else:
		srcFields = Source.std.SeparateFields(tff=TFF).std.SelectEvery(cycle=4, offsets=[0, 3])
	newFields = Input.std.SeparateFields(tff=TFF).std.SelectEvery(cycle=4, offsets=[1, 2])
	processed = core.std.Interleave([srcFields, newFields]).std.SelectEvery(cycle=4, offsets=[0, 1, 3, 2]).std.DoubleWeave(TFF)[::2]

	# Clean some of the artefacts caused by the above - creating a second version of the "new" fields
	vertMedian = processed.rgvs.VerticalCleaner(mode=1)
	vertMedDiff = core.std.MakeDiff(processed, vertMedian)
	vmNewDiff1 = vertMedDiff.std.SeparateFields(tff=TFF).std.SelectEvery(cycle=4, offsets=[1, 2])
	vmNewDiff2 = core.std.Expr(
		[vmNewDiff1.rgvs.VerticalCleaner(mode=1), vmNewDiff1], expr=f'x {neutral} - y {neutral} - * 0 < {neutral} x {neutral} - abs y {neutral} - abs < x y ? ?'
	)
	vmNewDiff3 = core.rgvs.Repair(vmNewDiff2, vmNewDiff2.rgvs.RemoveGrain(mode=2), mode=1)

	# Reweave final result
	return core.std.Interleave([srcFields, core.std.MakeDiff(newFields, vmNewDiff3)]).std.SelectEvery(cycle=4, offsets=[0, 1, 3, 2]).std.DoubleWeave(TFF)[::2]

def QTGMC_ApplySourceMatch(
	Deinterlace: vs.VideoNode,
	InputType: int,
	Source: vs.VideoNode,
	bVec1: typing.Union[vs.VideoNode, None],
	fVec1: typing.Union[vs.VideoNode, None],
	bVec2: typing.Union[vs.VideoNode, None],
	fVec2: typing.Union[vs.VideoNode, None],
	SubPel: int,
	SubPelInterp: int,
	hpad: int,
	vpad: int,
	ThSAD1: int,
	ThSCD1: int,
	ThSCD2: int,
	SourceMatch: int,
	MatchTR1: int,
	MatchEdi: str,
	MatchNNSize: int,
	MatchNNeurons: int,
	MatchEdiQual: int,
	MatchEdiMaxD: int,
	MatchTR2: int,
	MatchEdi2: str,
	MatchNNSize2: int,
	MatchNNeurons2: int,
	MatchEdiQual2: int,
	MatchEdiMaxD2: int,
	MatchEnhance: float,
	TFF: typing.Optional[bool] = None,
	nnedi3_args: typing.Mapping[str, typing.Any] = {},
	eedi3_args: typing.Mapping[str, typing.Any] = {},
	opencl: bool = False,
	device: typing.Optional[int] = None,
) -> vs.VideoNode:
	'''
	Source-match, a three stage process that takes the difference between deinterlaced input and the original interlaced source, to shift the input more towards
	the source without introducing shimmer. All other arguments defined in main script
	'''

	# Basic source-match. Find difference between source clip & equivalent fields in interpolated/smoothed clip (called the "error" in formula below). Ideally
	# there should be no difference, we want the fields in the output to be as close as possible to the source whilst remaining shimmer-free. So adjust the
	# *source* in such a way that smoothing it will give a result closer to the unadjusted source. Then rerun the interpolation (edi) and binomial smooth with
	# this new source. Result will still be shimmer-free and closer to the original source.
	# Formula used for correction is P0' = P0 + (P0-P1)/(k+S(1-k)), where P0 is original image, P1 is the 1st attempt at interpolation/smoothing , P0' is the
	# revised image to use as new source for interpolation/smoothing, k is the weighting given to the current frame in the smooth, and S is a factor indicating
	# "temporal similarity" of the error from frame to frame, i.e. S = average over all pixels of [neighbor frame error / current frame error] . Decreasing
	# S will make the result sharper, sensible range is about -0.25 to 1.0. Empirically, S=0.5 is effective [will do deeper analysis later]
	errorTemporalSimilarity = 0.5  # S in formula described above
	errorAdjust1 = [1.0, 2.0 / (1.0 + errorTemporalSimilarity), 8.0 / (3.0 + 5.0 * errorTemporalSimilarity)][MatchTR1]
	if SourceMatch < 1 or InputType == 1:
		match1Clip = Deinterlace
	else:
		match1Clip = Deinterlace.std.SeparateFields(tff=TFF).std.SelectEvery(cycle=4, offsets=[0, 3]).std.DoubleWeave(TFF)[::2]
	if SourceMatch < 1 or MatchTR1 <= 0:
		match1Update = Source
	else:
		match1Update = core.std.Expr([Source, match1Clip], expr=f'x {errorAdjust1 + 1} * y {errorAdjust1} * -')
	if SourceMatch > 0:
		match1Edi = QTGMC_Interpolate(
			match1Update,
			InputType,
			MatchEdi,
			MatchNNSize,
			MatchNNeurons,
			MatchEdiQual,
			MatchEdiMaxD,
			TFF=TFF,
			nnedi3_args=nnedi3_args,
			eedi3_args=eedi3_args,
			opencl=opencl,
			device=device,
		)
		if MatchTR1 > 0:
			match1Super = match1Edi.mv.Super(pel=SubPel, sharp=SubPelInterp, levels=1, hpad=hpad, vpad=vpad)
			match1Degrain1 = core.mv.Degrain1(match1Edi, match1Super, bVec1, fVec1, thsad=ThSAD1, thscd1=ThSCD1, thscd2=ThSCD2)
		if MatchTR1 > 1:
			match1Degrain2 = core.mv.Degrain1(match1Edi, match1Super, bVec2, fVec2, thsad=ThSAD1, thscd1=ThSCD1, thscd2=ThSCD2)
	if SourceMatch < 1:
		match1 = Deinterlace
	elif MatchTR1 <= 0:
		match1 = match1Edi
	elif MatchTR1 == 1:
		match1 = core.std.Merge(match1Degrain1, match1Edi, weight=0.25)
	else:
		match1 = core.std.Merge(core.std.Merge(match1Degrain1, match1Degrain2, weight=0.2), match1Edi, weight=0.0625)

	if SourceMatch < 2:
		return match1

	# Enhance effect of source-match stages 2 & 3 by sharpening clip prior to refinement (source-match tends to underestimate so this will leave result sharper)
	if SourceMatch > 1 and MatchEnhance > 0:
		match1Shp = core.std.Expr([match1, match1.std.Convolution(matrix=[1, 2, 1, 2, 4, 2, 1, 2, 1])], expr=f'x x y - {MatchEnhance} * +')
	else:
		match1Shp = match1

	# Source-match refinement. Find difference between source clip & equivalent fields in (updated) interpolated/smoothed clip. Interpolate & binomially smooth
	# this difference then add it back to output. Helps restore differences that the basic match missed. However, as this pass works on a difference rather than
	# the source image it can be prone to occasional artefacts (difference images are not ideal for interpolation). In fact a lower quality interpolation such
	# as a simple bob often performs nearly as well as advanced, slower methods (e.g. NNEDI3)
	if SourceMatch < 2 or InputType == 1:
		match2Clip = match1Shp
	else:
		match2Clip = match1Shp.std.SeparateFields(tff=TFF).std.SelectEvery(cycle=4, offsets=[0, 3]).std.DoubleWeave(TFF)[::2]
	if SourceMatch > 1:
		match2Diff = core.std.MakeDiff(Source, match2Clip)
		match2Edi = QTGMC_Interpolate(
			match2Diff,
			InputType,
			MatchEdi2,
			MatchNNSize2,
			MatchNNeurons2,
			MatchEdiQual2,
			MatchEdiMaxD2,
			TFF=TFF,
			nnedi3_args=nnedi3_args,
			eedi3_args=eedi3_args,
			opencl=opencl,
			device=device,
		)
		if MatchTR2 > 0:
			match2Super = match2Edi.mv.Super(pel=SubPel, sharp=SubPelInterp, levels=1, hpad=hpad, vpad=vpad)
			match2Degrain1 = core.mv.Degrain1(match2Edi, match2Super, bVec1, fVec1, thsad=ThSAD1, thscd1=ThSCD1, thscd2=ThSCD2)
		if MatchTR2 > 1:
			match2Degrain2 = core.mv.Degrain1(match2Edi, match2Super, bVec2, fVec2, thsad=ThSAD1, thscd1=ThSCD1, thscd2=ThSCD2)
	if SourceMatch < 2:
		match2 = match1
	elif MatchTR2 <= 0:
		match2 = match2Edi
	elif MatchTR2 == 1:
		match2 = core.std.Merge(match2Degrain1, match2Edi, weight=0.25)
	else:
		match2 = core.std.Merge(core.std.Merge(match2Degrain1, match2Degrain2, weight=0.2), match2Edi, weight=0.0625)

	# Source-match second refinement - correct error introduced in the refined difference by temporal smoothing. Similar to error correction from basic step
	errorAdjust2 = [1.0, 2.0 / (1.0 + errorTemporalSimilarity), 8.0 / (3.0 + 5.0 * errorTemporalSimilarity)][MatchTR2]
	if SourceMatch < 3 or MatchTR2 <= 0:
		match3Update = match2Edi
	else:
		match3Update = core.std.Expr([match2Edi, match2], expr=f'x {errorAdjust2 + 1} * y {errorAdjust2} * -')
	if SourceMatch > 2:
		if MatchTR2 > 0:
			match3Super = match3Update.mv.Super(pel=SubPel, sharp=SubPelInterp, levels=1, hpad=hpad, vpad=vpad)
			match3Degrain1 = core.mv.Degrain1(match3Update, match3Super, bVec1, fVec1, thsad=ThSAD1, thscd1=ThSCD1, thscd2=ThSCD2)
		if MatchTR2 > 1:
			match3Degrain2 = core.mv.Degrain1(match3Update, match3Super, bVec2, fVec2, thsad=ThSAD1, thscd1=ThSCD1, thscd2=ThSCD2)
	if SourceMatch < 3:
		match3 = match2
	elif MatchTR2 <= 0:
		match3 = match3Update
	elif MatchTR2 == 1:
		match3 = core.std.Merge(match3Degrain1, match3Update, weight=0.25)
	else:
		match3 = core.std.Merge(core.std.Merge(match3Degrain1, match3Degrain2, weight=0.2), match3Update, weight=0.0625)

	# Apply difference calculated in source-match refinement
	return core.std.MergeDiff(match1Shp, match3)

def QTGMC_SetUserGlobal(Prefix: str, Name: str, Value: typing.Union[vs.VideoNode, None]) -> None:
	'''Set global variable called "Prefix_Name" to "Value".'''
	global QTGMC_globals
	QTGMC_globals[f'{Prefix}_{Name}'] = Value

def QTGMC_GetUserGlobal(Prefix: str, Name: str) -> typing.Union[vs.VideoNode, None]:
	'''Return value of global variable called "Prefix_Name". Returns None if it doesn't exist'''
	global QTGMC_globals
	return QTGMC_globals.get(f'{Prefix}_{Name}')



#-------------------------------------------------------------------#
#                                                                   #
#                    QTGMC 3.33, by Vit, 2012                       #
#                                                                   #
#   A high quality deinterlacer using motion-compensated temporal   #
#  smoothing, with a range of features for quality and convenience  #
#          Originally based on TempGaussMC_beta2 by Didée           #
#                                                                   #
#-------------------------------------------------------------------#
#
# Full documentation is in the 'QTGMC' html file that comes with this script
#
# --- LATEST CHANGES ---
#
# v3.33
# - Increased maximum value for Rep0, Rep1 and Rep2 to 7 (from 5). Higher values help with flicker on static detail, potential for minor motion blur
# - Bug fix for the fact that Bob always outputs a BFF clip regardless of field order of input (thanks ajp_anton)
# - Improved generation of noise (NoiseDeint="Generate") for noise bypass / EZKeepGrain
# - Minor change to denoising
#
# --- REQUIREMENTS ---
#
# Core plugins:
#   MVTools
#   Miscellaneous Filters
#   znedi3
#   RGVS
#   fmtconv
#
# Additional plugins:
#   eedi3m - if selected directly or via a source-match preset
#   FFT3DFilter - if selected for noise processing
#   DFTTest - if selected for noise processing
#       For FFT3DFilter & DFTTest you also need the FFTW3 library (FFTW.org). On Windows the file needed for both is libfftw3f-3.dll.
#       Put the file in your System32 or SysWow64 folder
#   KNLMeansCL - if selected for noise processing
#   AddGrain - if NoiseDeint="Generate" selected for noise bypass
#
# --- GETTING STARTED ---
#
# The "Preset" used selects sensible settings for a given encoding speed. Choose a preset from:
#   "Placebo", "Very Slow", "Slower", "Slow", "Medium", "Fast", "Faster", "Very Fast", "Super Fast", "Ultra Fast" & "Draft"
# The default preset is "Slower"
# Don't be obsessed with using slower settings as the differences can be small. HD material benefits little from extreme settings (and will be very slow)
# For much faster speeds read the full documentation, the section on 'Multi-threading'
#
# There are many settings for tweaking the script, full details in the main documentation. You can display settings currently being used with "ShowSettings":
#   QTGMC( Preset="Slow", ShowSettings=True )

def QTGMC_obs_Scale(value, peak):
	def _cround(x):
		return math.floor(x + 0.5) if x > 0 else math.ceil(x - 0.5)

	return _cround(value * peak / 255) if peak != 1 else value / 255

def QTGMC_obs_Weave(clip, tff):
	if not isinstance(clip, vs.VideoNode):
		raise vs.Error('QTGMC_obs_Weave: this is not a clip')

	return clip.std.DoubleWeave(tff=tff)[::2]

## MOD (1d114642a453b17ea4dc08c5415c20cfee222e1a)
def QTGMC_obs(
		Input, Preset='Slower', TR0=None, TR1=None, TR2=None, Rep0=None, Rep1=0, Rep2=None, EdiMode=None, RepChroma=True, NNSize=None, NNeurons=None, EdiQual=1, EdiMaxD=None, ChromaEdi='',
		EdiExt=None, Sharpness=None, SMode=None, SLMode=None, SLRad=None, SOvs=0, SVThin=0.0, Sbb=None, SrchClipPP=None, SubPel=None, SubPelInterp=2, BlockSize=None, Overlap=None, Search=None,
		SearchParam=None, PelSearch=None, ChromaMotion=None, TrueMotion=False, Lambda=None, LSAD=None, PNew=None, PLevel=None, GlobalMotion=True, DCT=0, ThSAD1=640, ThSAD2=256, ThSCD1=180, ThSCD2=98,
		SourceMatch=0, MatchPreset=None, MatchEdi=None, MatchPreset2=None, MatchEdi2=None, MatchTR2=1, MatchEnhance=0.5, Lossless=0, NoiseProcess=None, EZDenoise=None, EZKeepGrain=None,
		NoisePreset='Fast', Denoiser=None, FftThreads=1, DenoiseMC=None, NoiseTR=None, Sigma=None, ChromaNoise=False, ShowNoise=0.0, GrainRestore=None, NoiseRestore=None, NoiseDeint=None,
		StabilizeNoise=None, InputType=0, ProgSADMask=None, FPSDivisor=1, ShutterBlur=0, ShutterAngleSrc=180, ShutterAngleOut=180, SBlurLimit=4, Border=False, Precise=None, Tuning='None',
		ShowSettings=False, ForceTR=0, TFF=None, pscrn=None, int16_prescreener=None, int16_predictor=None, exp=None, alpha=None, beta=None, gamma=None, nrad=None, vcheck=None, opencl=False, device=None):

	global dfttest2
	if dfttest2 is None :
		import dfttest2
	if LooseVersion(dfttest2.__version__) < LooseVersion("0.3.3") :
		raise EnvironmentError("依赖 dfttest2 的版本号过低，至少 0.3.3")

	def _Clamp(clip, bright_limit, dark_limit, overshoot=0, undershoot=0, planes=None):
		if not (isinstance(clip, vs.VideoNode) and isinstance(bright_limit, vs.VideoNode) and isinstance(dark_limit, vs.VideoNode)):
			raise vs.Error('_Clamp: this is not a clip')
		if bright_limit.format.id != clip.format.id or dark_limit.format.id != clip.format.id:
			raise vs.Error('_Clamp: clips must have the same format')
		if planes is None:
			planes = list(range(clip.format.num_planes))
		elif isinstance(planes, int):
			planes = [planes]
		expr = f'x y {overshoot} + > y {overshoot} + x ? z {undershoot} - < z {undershoot} - x y {overshoot} + > y {overshoot} + x ? ?'
		return core.std.Expr([clip, bright_limit, dark_limit], expr=[expr if i in planes else '' for i in range(clip.format.num_planes)])

	def _DitherLumaRebuild(src, s0=2.0, c=0.0625, chroma=True):
		if not isinstance(src, vs.VideoNode):
			raise vs.Error('_DitherLumaRebuild: this is not a clip')
		if src.format.color_family == vs.RGB:
			raise vs.Error('_DitherLumaRebuild: RGB format is not supported')
		isGray = (src.format.color_family == vs.GRAY)
		isInteger = (src.format.sample_type == vs.INTEGER)
		shift = src.format.bits_per_sample - 8
		neutral = 128 << shift if isInteger else 0.0
		k = (s0 - 1) * c
		t = f'x {16 << shift if isInteger else 16 / 255} - {219 << shift if isInteger else 219 / 255} / 0 max 1 min'
		e = f'{k} {1 + c} {(1 + c) * c} {t} {c} + / - * {t} 1 {k} - * + {256 << shift if isInteger else 256 / 255} *'
		return src.std.Expr(expr=[e] if isGray else [e, f'x {neutral} - 128 * 112 / {neutral} +' if chroma else ''])

	def _Gauss(clip, p=None, sigma=None, planes=None):
		if not isinstance(clip, vs.VideoNode):
			raise vs.Error('_Gauss: this is not a clip')
		if p is None and sigma is None:
			raise vs.Error('_Gauss: must have p or sigma')
		if p is not None and not 0.385 <= p <= 64.921:
			raise vs.Error('_Gauss: p must be between 0.385 and 64.921 (inclusive)')
		if sigma is not None and not 0.334 <= sigma <= 4.333:
			raise vs.Error('_Gauss: sigma must be between 0.334 and 4.333 (inclusive)')
		if sigma is None and p is not None:
			# Translate AviSynth parameter to standard parameter.
			sigma = math.sqrt(1.0 / (2.0 * (p / 10.0) * math.log(2)))
		# 6 * sigma + 1 rule-of-thumb.
		taps = int(math.ceil(sigma * 6 + 1))
		if not taps % 2:
			taps += 1
		# Gaussian kernel.
		kernel = []
		for x in range(int(math.floor(taps / 2))):
			kernel.append(1.0 / (math.sqrt(2.0 * math.pi) * sigma) * math.exp(-(x * x) / (2 * sigma * sigma)))
		# Renormalize to -1023...1023.
		for i in range(1, len(kernel)):
			kernel[i] *= 1023 / kernel[0]
		kernel[0] = 1023
		# Symmetry.
		kernel = kernel[::-1] + kernel[1:]
		return clip.std.Convolution(matrix=kernel, planes=planes, mode='hv')

	#---------------------------------------
	# Presets

	# Select presets / tuning
	Preset = Preset.lower()
	presets = ['placebo', 'very slow', 'slower', 'slow', 'medium', 'fast', 'faster', 'very fast', 'super fast', 'ultra fast', 'draft']
	try:
		pNum = presets.index(Preset)
	except:
		raise vs.Error("QTGMC: 'Preset' choice is invalid")

	if MatchPreset is None:
		mpNum1 = pNum + 3 if pNum + 3 <= 9 else 9
		MatchPreset = presets[mpNum1]
	else:
		try:
			mpNum1 = presets[:10].index(MatchPreset.lower())
		except:
			raise vs.Error("QTGMC: 'MatchPreset' choice is invalid/unsupported")

	if MatchPreset2 is None:
		mpNum2 = mpNum1 + 2 if mpNum1 + 2 <= 9 else 9
		MatchPreset2 = presets[mpNum2]
	else:
		try:
			mpNum2 = presets[:10].index(MatchPreset2.lower())
		except:
			raise vs.Error("QTGMC: 'MatchPreset2' choice is invalid/unsupported")

	try:
		npNum = presets[2:7].index(NoisePreset.lower())
	except:
		raise vs.Error("QTGMC: 'NoisePreset' choice is invalid")

	try:
		tNum = ['none', 'dv-sd', 'dv-hd'].index(Tuning.lower())
	except:
		raise vs.Error("QTGMC: 'Tuning' choice is invalid")

	# Tunings only affect blocksize in this version
	bs = [16, 16, 32][tNum]
	bs2 = 32 if bs >= 16 else bs * 2

	#                                                   Very                                                        Very      Super     Ultra
	# Preset groups:                          Placebo   Slow      Slower    Slow      Medium    Fast      Faster    Fast      Fast      Fast      Draft
	if TR0          is None: TR0          = [ 2,        2,        2,        2,        2,        2,        1,        1,        1,        1,        0      ][pNum]
	if TR1          is None: TR1          = [ 2,        2,        2,        1,        1,        1,        1,        1,        1,        1,        1      ][pNum]
	if TR2 is not None:
		TR2X = TR2
	else:
		TR2X                              = [ 3,        2,        1,        1,        1,        0,        0,        0,        0,        0,        0      ][pNum]
	if Rep0         is None: Rep0         = [ 4,        4,        4,        4,        3,        3,        0,        0,        0,        0,        0      ][pNum]
	if Rep2         is None: Rep2         = [ 4,        4,        4,        4,        4,        4,        4,        4,        3,        3,        0      ][pNum]
	if EdiMode is not None:
		EdiMode = EdiMode.lower()
	else:
		EdiMode                           = ['nnedi3', 'nnedi3', 'nnedi3', 'nnedi3', 'nnedi3', 'nnedi3', 'nnedi3', 'nnedi3', 'nnedi3', 'nnedi3', 'bob'   ][pNum]
	if NNSize       is None: NNSize       = [ 1,        1,        1,        1,        5,        5,        4,        4,        4,        4,        4      ][pNum]
	if NNeurons     is None: NNeurons     = [ 2,        2,        1,        1,        1,        0,        0,        0,        0,        0,        0      ][pNum]
	if EdiMaxD      is None: EdiMaxD      = [ 12,       10,       8,        7,        7,        6,        6,        5,        4,        4,        4      ][pNum]
	ChromaEdi = ChromaEdi.lower()
	if SMode        is None: SMode        = [ 2,        2,        2,        2,        2,        2,        2,        2,        2,        2,        0      ][pNum]
	if SLMode is not None:
		SLModeX = SLMode
	else:
		SLModeX                           = [ 2,        2,        2,        2,        2,        2,        2,        2,        0,        0,        0      ][pNum]
	if SLRad        is None: SLRad        = [ 3,        1,        1,        1,        1,        1,        1,        1,        1,        1,        1      ][pNum]
	if Sbb          is None: Sbb          = [ 3,        1,        1,        0,        0,        0,        0,        0,        0,        0,        0      ][pNum]
	if SrchClipPP   is None: SrchClipPP   = [ 3,        3,        3,        3,        3,        2,        2,        2,        1,        1,        0      ][pNum]
	if SubPel       is None: SubPel       = [ 2,        2,        2,        2,        1,        1,        1,        1,        1,        1,        1      ][pNum]
	if BlockSize    is None: BlockSize    = [ bs,       bs,       bs,       bs,       bs,       bs,       bs2,      bs2,      bs2,      bs2,      bs2    ][pNum]
	bs = BlockSize
	if Overlap      is None: Overlap      = [ bs // 2,  bs // 2,  bs // 2,  bs // 2,  bs // 2,  bs // 2,  bs // 2,  bs // 4,  bs // 4,  bs // 4,  bs // 4][pNum]
	if Search       is None: Search       = [ 5,        4,        4,        4,        4,        4,        4,        4,        0,        0,        0      ][pNum]
	if SearchParam  is None: SearchParam  = [ 2,        2,        2,        2,        2,        2,        2,        1,        1,        1,        1      ][pNum]
	if PelSearch    is None: PelSearch    = [ 2,        2,        2,        2,        1,        1,        1,        1,        1,        1,        1      ][pNum]
	if ChromaMotion is None: ChromaMotion = [ True,     True,     True,     False,    False,    False,    False,    False,    False,    False,    False  ][pNum]
	if Precise      is None: Precise      = [ True,     True,     False,    False,    False,    False,    False,    False,    False,    False,    False  ][pNum]
	if ProgSADMask  is None: ProgSADMask  = [ 10.0,     10.0,     10.0,     10.0,     10.0,     0.0,      0.0,      0.0,      0.0,      0.0,      0.0    ][pNum]

	# Noise presets                               Slower      Slow       Medium     Fast      Faster
	if Denoiser is not None:
		Denoiser = Denoiser.lower()
	else:
		Denoiser                              = ['dfttest',  'dfttest', 'dfttest', 'fft3df', 'fft3df'][npNum]
	if DenoiseMC      is None: DenoiseMC      = [ True,       True,      False,     False,    False  ][npNum]
	if NoiseTR        is None: NoiseTR        = [ 2,          1,         1,         1,        0      ][npNum]
	if NoiseDeint is not None:
		NoiseDeint = NoiseDeint.lower()
	else:
		NoiseDeint                            = ['generate', 'bob',      '',        '',       ''     ][npNum]
	if StabilizeNoise is None: StabilizeNoise = [ True,       True,      True,      False,    False  ][npNum]

	# The basic source-match step corrects and re-runs the interpolation of the input clip. So it initialy uses same interpolation settings as the main preset
	MatchNNSize = NNSize
	MatchNNeurons = NNeurons
	MatchEdiQual = EdiQual
	MatchEdiMaxD = EdiMaxD

	# However, can use a faster initial interpolation when using source-match allowing the basic source-match step to "correct" it with higher quality settings
	if SourceMatch > 0 and mpNum1 < pNum:
		raise vs.Error("QTGMC: 'MatchPreset' cannot use a slower setting than 'Preset'")
	# Basic source-match presets
	if SourceMatch > 0:
		#                     Very                                            Very   Super   Ultra
		#           Placebo   Slow   Slower   Slow   Medium   Fast   Faster   Fast   Fast    Fast
		NNSize   = [1,        1,     1,       1,     5,       5,     4,       4,     4,      4][mpNum1]
		NNeurons = [2,        2,     1,       1,     1,       0,     0,       0,     0,      0][mpNum1]
		EdiQual  = [1,        1,     1,       1,     1,       1,     1,       1,     1,      1][mpNum1]
		EdiMaxD  = [12,       10,    8,       7,     7,       6,     6,       5,     4,      4][mpNum1]
	TempEdi = EdiMode # Main interpolation is actually done by basic-source match step when enabled, so a little swap and wriggle is needed
	if SourceMatch > 0 and MatchEdi is not None:
		EdiMode = MatchEdi.lower()
	MatchEdi = TempEdi

	#                                             Very                                                        Very      Super    Ultra
	# Refined source-match presets      Placebo   Slow      Slower    Slow      Medium    Fast      Faster    Fast      Fast     Fast
	if MatchEdi2 is not None:
		MatchEdi2 = MatchEdi2.lower()
	else:
		MatchEdi2                   = ['nnedi3', 'nnedi3', 'nnedi3', 'nnedi3', 'nnedi3', 'nnedi3', 'nnedi3', 'nnedi3', 'nnedi3', ''][mpNum2]
	MatchNNSize2                    = [ 1,        1,        1,        1,        5,        5,        4,        4,        4,       4 ][mpNum2]
	MatchNNeurons2                  = [ 2,        2,        1,        1,        1,        0,        0,        0,        0,       0 ][mpNum2]
	MatchEdiQual2                   = [ 1,        1,        1,        1,        1,        1,        1,        1,        1,       1 ][mpNum2]
	MatchEdiMaxD2                   = [ 12,       10,       8,        7,        7,        6,        6,        5,        4,       4 ][mpNum2]

	#---------------------------------------
	# Settings

	if not isinstance(Input, vs.VideoNode):
		raise vs.Error('QTGMC: this is not a clip')

	if EdiExt is not None and (not isinstance(EdiExt, vs.VideoNode) or EdiExt.format.id != Input.format.id):
		raise vs.Error("QTGMC: 'EdiExt' must be the same format as input")

	if InputType != 1 and not isinstance(TFF, bool):
		raise vs.Error("QTGMC: 'TFF' must be set when InputType!=1. Setting TFF to true means top field first and false means bottom field first")

	isGray = (Input.format.color_family == vs.GRAY)

	neutral = 1 << (Input.format.bits_per_sample - 1)
	peak = (1 << Input.format.bits_per_sample) - 1

	SOvs = QTGMC_obs_Scale(SOvs, peak)

	# Core defaults
	if SourceMatch > 0:
		if TR2 is None:
			TR2 = 1 if TR2X <= 0 else TR2X # ***TR2 defaults always at least 1 when using source-match***
	else:
		TR2 = TR2X

	# Source-match defaults
	MatchTR1 = TR1

	# Sharpness defaults. Sharpness default is always 1.0 (0.2 with source-match), but adjusted to give roughly same sharpness for all settings
	if Sharpness is not None and Sharpness <= 0:
		SMode = 0
	if SourceMatch > 0:
		if SLMode is None:
			SLMode = 0 # ***Sharpness limiting disabled by default for source-match***
	else:
		SLMode = SLModeX
	if SLRad <= 0:
		SLMode = 0
	spatialSL = SLMode in [1, 3]
	temporalSL = SLMode in [2, 4]
	if Sharpness is None:
		Sharpness = 0.0 if SMode <= 0 else 0.2 if SourceMatch > 0 else 1.0 # Default sharpness is 1.0, or 0.2 if using source-match
	sharpMul = 2 if temporalSL else 1.5 if spatialSL else 1 # Adjust sharpness based on other settings
	sharpAdj = Sharpness * (sharpMul * (0.2 + TR1 * 0.15 + TR2 * 0.25) + (0.1 if SMode == 1 else 0)) # [This needs a bit more refinement]
	if SMode <= 0:
		Sbb = 0

	# Noise processing settings
	if EZDenoise is not None and EZDenoise > 0 and EZKeepGrain is not None and EZKeepGrain > 0:
		raise vs.Error("QTGMC: EZDenoise and EZKeepGrain cannot be used together")
	if NoiseProcess is None:
		if EZDenoise is not None and EZDenoise > 0:
			NoiseProcess = 1
		elif (EZKeepGrain is not None and EZKeepGrain > 0) or Preset in ['placebo', 'very slow']:
			NoiseProcess = 2
		else:
			NoiseProcess = 0
	if GrainRestore is None:
		if EZDenoise is not None and EZDenoise > 0:
			GrainRestore = 0.0
		elif EZKeepGrain is not None and EZKeepGrain > 0:
			GrainRestore = 0.3 * math.sqrt(EZKeepGrain)
		else:
			GrainRestore = [0.0, 0.7, 0.3][NoiseProcess]
	if NoiseRestore is None:
		if EZDenoise is not None and EZDenoise > 0:
			NoiseRestore = 0.0
		elif EZKeepGrain is not None and EZKeepGrain > 0:
			NoiseRestore = 0.1 * math.sqrt(EZKeepGrain)
		else:
			NoiseRestore = [0.0, 0.3, 0.1][NoiseProcess]
	if Sigma is None:
		if EZDenoise is not None and EZDenoise > 0:
			Sigma = EZDenoise
		elif EZKeepGrain is not None and EZKeepGrain > 0:
			Sigma = 4.0 * EZKeepGrain
		else:
			Sigma = 2.0
	if isinstance(ShowNoise, bool):
		ShowNoise = 10.0 if ShowNoise else 0.0
	if ShowNoise > 0:
		NoiseProcess = 2
		NoiseRestore = 1.0
	if NoiseProcess <= 0:
		NoiseTR = 0
		GrainRestore = 0.0
		NoiseRestore = 0.0
	totalRestore = GrainRestore + NoiseRestore
	if totalRestore <= 0:
		StabilizeNoise = False
	noiseTD = [1, 3, 5][NoiseTR]
	noiseCentre = 128.5 * 2 ** (Input.format.bits_per_sample - 8) if Denoiser in ['fft3df', 'fft3dfilter'] else neutral

	# MVTools settings
	if Lambda is None:
		Lambda = (1000 if TrueMotion else 100) * BlockSize * BlockSize // 64
	if LSAD is None:
		LSAD = 1200 if TrueMotion else 400
	if PNew is None:
		PNew = 50 if TrueMotion else 25
	if PLevel is None:
		PLevel = 1 if TrueMotion else 0

	# Motion blur settings
	if ShutterAngleOut * FPSDivisor == ShutterAngleSrc:
		ShutterBlur = 0 # If motion blur output is same as input

	# Miscellaneous
	if InputType < 2:
		ProgSADMask = 0.0

	# Get maximum temporal radius needed
	maxTR = SLRad if temporalSL else 0
	maxTR = max(maxTR, MatchTR2, TR1, TR2, NoiseTR)
	if (ProgSADMask > 0 or StabilizeNoise or ShutterBlur > 0) and maxTR < 1:
		maxTR = 1
	maxTR = max(maxTR, ForceTR)

	#---------------------------------------
	# Pre-Processing

	w = Input.width
	h = Input.height
	epsilon = 1e-6

	# Reverse "field" dominance for progressive repair mode 3 (only difference from mode 2)
	if InputType >= 3:
		TFF = not TFF

	# Pad vertically during processing (to prevent artefacts at top & bottom edges)
	if Border:
		h += 8
		clip = Input.resize.Point(w, h, src_top=-4, src_height=h)
	else:
		clip = Input

	hpad = BlockSize
	vpad = BlockSize

	#---------------------------------------
	# Motion Analysis

	# Bob the input as a starting point for motion search clip
	if InputType <= 0:
		bobbed = clip.resize.Bob(tff=TFF, filter_param_a=0, filter_param_b=0.5)
	elif InputType == 1:
		bobbed = clip
	else:
		bobbed = clip.std.Convolution(matrix=[1, 2, 1], mode='v')

	if ChromaMotion and not isGray:
		CMplanes = [0, 1, 2]
		CMts = 255 << (Input.format.bits_per_sample - 8)
	else:
		CMplanes = [0]
		CMts = 0

	# The bobbed clip will shimmer due to being derived from alternating fields. Temporally smooth over the neighboring frames using a binomial kernel. Binomial
	# kernels give equal weight to even and odd frames and hence average away the shimmer. The two kernels used are [1 2 1] and [1 4 6 4 1] for radius 1 and 2.
	# These kernels are approximately Gaussian kernels, which work well as a prefilter before motion analysis (hence the original name for this script)
	# Create linear weightings of neighbors first                                      -2    -1    0     1     2
	luma_threshold = 255 << (Input.format.bits_per_sample - 8)
	if TR0 > 0: ts1 = bobbed.focus2.TemporalSoften2(1, luma_threshold, CMts, 28, 2)  # 0.00  0.33  0.33  0.33  0.00
	if TR0 > 1: ts2 = bobbed.focus2.TemporalSoften2(2, luma_threshold, CMts, 28, 2)  # 0.20  0.20  0.20  0.20  0.20

	# Combine linear weightings to give binomial weightings - TR0=0: (1), TR0=1: (1:2:1), TR0=2: (1:4:6:4:1)
	if TR0 <= 0:
		binomial0 = bobbed
	elif TR0 == 1:
		binomial0 = core.std.Merge(ts1, bobbed, weight=[0.25] if ChromaMotion or isGray else [0.25, 0])
	else:
		binomial0 = core.std.Merge(core.std.Merge(ts1, ts2, weight=[0.357] if ChromaMotion or isGray else [0.357, 0]), bobbed, weight=[0.125] if ChromaMotion or isGray else [0.125, 0])

	# Remove areas of difference between temporal blurred motion search clip and bob that are not due to bob-shimmer - removes general motion blur
	if Rep0 <= 0:
		repair0 = binomial0
	else:
		repair0 = QTGMC_obs_KeepOnlyBobShimmerFixes(binomial0, bobbed, Rep0, RepChroma and ChromaMotion)

	# Blur image and soften edges to assist in motion matching of edge blocks. Blocks are matched by SAD (sum of absolute differences between blocks), but even
	# a slight change in an edge from frame to frame will give a high SAD due to the higher contrast of edges
	if SrchClipPP == 1:
		spatialBlur = repair0.resize.Bilinear(w // 2, h // 2).std.Convolution(matrix=[1, 2, 1, 2, 4, 2, 1, 2, 1], planes=CMplanes).resize.Bilinear(w, h)
	elif SrchClipPP >= 2:
		spatialBlur = _Gauss(repair0.std.Convolution(matrix=[1, 2, 1, 2, 4, 2, 1, 2, 1], planes=CMplanes), p=2.35)
	if SrchClipPP > 1:
		spatialBlur = core.std.Merge(spatialBlur, repair0, weight=[0.1] if ChromaMotion or isGray else [0.1, 0])
	if SrchClipPP <= 0:
		srchClip = repair0
	elif SrchClipPP < 3:
		srchClip = spatialBlur
	else:
		expr = 'x {i} + y < x {i} + x {i} - y > x {i} - y ? ?'.format(i=QTGMC_obs_Scale(3, peak))
		tweaked = core.std.Expr([repair0, bobbed], expr=[expr] if ChromaMotion or isGray else [expr, ''])
		expr = 'x {i} + y < x {j} + x {i} - y > x {j} - x 51 * y 49 * + 100 / ? ?'.format(i=QTGMC_obs_Scale(7, peak), j=QTGMC_obs_Scale(2, peak))
		srchClip = core.std.Expr([spatialBlur, tweaked], expr=[expr] if ChromaMotion or isGray else [expr, ''])

	# Calculate forward and backward motion vectors from motion search clip
	if maxTR > 0:
		analyse_args = dict(blksize=BlockSize, overlap=Overlap, search=Search, searchparam=SearchParam, pelsearch=PelSearch, truemotion=TrueMotion, lambda_=Lambda, lsad=LSAD, pnew=PNew, plevel=PLevel,
							global_=GlobalMotion, dct=DCT, chroma=ChromaMotion)
		srchSuper = _DitherLumaRebuild(srchClip, s0=1, chroma=ChromaMotion).mv.Super(pel=SubPel, sharp=SubPelInterp, hpad=hpad, vpad=vpad, chroma=ChromaMotion)
		bVec1 = srchSuper.mv.Analyse(isb=True, delta=1, **analyse_args)
		fVec1 = srchSuper.mv.Analyse(isb=False, delta=1, **analyse_args)
	if maxTR > 1:
		bVec2 = srchSuper.mv.Analyse(isb=True, delta=2, **analyse_args)
		fVec2 = srchSuper.mv.Analyse(isb=False, delta=2, **analyse_args)
	if maxTR > 2:
		bVec3 = srchSuper.mv.Analyse(isb=True, delta=3, **analyse_args)
		fVec3 = srchSuper.mv.Analyse(isb=False, delta=3, **analyse_args)

	#---------------------------------------
	# Noise Processing

	# Expand fields to full frame size before extracting noise (allows use of motion vectors which are frame-sized)
	if NoiseProcess > 0:
		if InputType > 0:
			fullClip = clip
		else:
			fullClip = clip.resize.Bob(tff=TFF, filter_param_a=0, filter_param_b=1)
	if NoiseTR > 0:
		fullSuper = fullClip.mv.Super(pel=SubPel, levels=1, hpad=hpad, vpad=vpad, chroma=ChromaNoise) #TEST chroma OK?

	CNplanes = [0, 1, 2] if ChromaNoise and not isGray else [0]

	# Create a motion compensated temporal window around current frame and use to guide denoisers
	if NoiseProcess > 0:
		if not DenoiseMC or NoiseTR <= 0:
			noiseWindow = fullClip
		elif NoiseTR == 1:
			noiseWindow = core.std.Interleave([core.mv.Compensate(fullClip, fullSuper, fVec1, thscd1=ThSCD1, thscd2=ThSCD2), fullClip,
				core.mv.Compensate(fullClip, fullSuper, bVec1, thscd1=ThSCD1, thscd2=ThSCD2)])
		else:
			noiseWindow = core.std.Interleave([core.mv.Compensate(fullClip, fullSuper, fVec2, thscd1=ThSCD1, thscd2=ThSCD2),
				core.mv.Compensate(fullClip, fullSuper, fVec1, thscd1=ThSCD1, thscd2=ThSCD2), fullClip,
				core.mv.Compensate(fullClip, fullSuper, bVec1, thscd1=ThSCD1, thscd2=ThSCD2),
				core.mv.Compensate(fullClip, fullSuper, bVec2, thscd1=ThSCD1, thscd2=ThSCD2)])
		if Denoiser == 'dfttest':
			dnWindow = dfttest2.DFTTest(clip=noiseWindow, sigma=Sigma * 4, tbsize=noiseTD, planes=CNplanes) #TODO:GPU
		elif Denoiser == 'knlmeanscl':
			if ChromaNoise and not isGray:
				dnWindow = KNLMeansCL(noiseWindow, d=NoiseTR, h=Sigma)
			else:
				dnWindow = noiseWindow.knlm.KNLMeansCL(d=NoiseTR, h=Sigma)
		else:
			dnWindow = noiseWindow.fft3dfilter.FFT3DFilter(sigma=Sigma, planes=CNplanes, bt=noiseTD, ncpu=FftThreads)

		# Rework denoised clip to match source format - various code paths here: discard the motion compensation window, discard doubled lines (from point resize)
		# Also reweave to get interlaced noise if source was interlaced (could keep the full frame of noise, but it will be poor quality from the point resize)
		if not DenoiseMC:
			if InputType > 0:
				denoised = dnWindow
			else:
				denoised = QTGMC_obs_Weave(dnWindow.std.SeparateFields(tff=TFF).std.SelectEvery(cycle=4, offsets=[0, 3]), tff=TFF)
		elif InputType > 0:
			if NoiseTR <= 0:
				denoised = dnWindow
			else:
				denoised = dnWindow.std.SelectEvery(cycle=noiseTD, offsets=[NoiseTR])
		else:
			denoised = QTGMC_obs_Weave(dnWindow.std.SeparateFields(tff=TFF).std.SelectEvery(cycle=noiseTD * 4, offsets=[NoiseTR * 2, NoiseTR * 6 + 3]), tff=TFF)

	# Get actual noise from difference. Then 'deinterlace' where we have weaved noise - create the missing lines of noise in various ways
	if NoiseProcess > 0 and totalRestore > 0:
		noise = core.std.MakeDiff(clip, denoised, planes=CNplanes)
		if InputType > 0:
			deintNoise = noise
		elif NoiseDeint == 'bob':
			deintNoise = noise.resize.Bob(tff=TFF, filter_param_a=0, filter_param_b=0.5)
		elif NoiseDeint == 'generate':
			deintNoise = QTGMC_obs_Generate2ndFieldNoise(noise, denoised, ChromaNoise, TFF)
		else:
			deintNoise = noise.std.SeparateFields(tff=TFF).std.DoubleWeave(tff=TFF)

		# Motion-compensated stabilization of generated noise
		if StabilizeNoise:
			noiseSuper = deintNoise.mv.Super(pel=SubPel, sharp=SubPelInterp, levels=1, hpad=hpad, vpad=vpad, chroma=ChromaNoise)
			mcNoise = core.mv.Compensate(deintNoise, noiseSuper, bVec1, thscd1=ThSCD1, thscd2=ThSCD2)
			expr = f'x {neutral} - abs y {neutral} - abs > x y ? 0.6 * x y + 0.2 * +'
			finalNoise = core.std.Expr([deintNoise, mcNoise], expr=[expr] if ChromaNoise or isGray else [expr, ''])
		else:
			finalNoise = deintNoise

	# If NoiseProcess=1 denoise input clip. If NoiseProcess=2 leave noise in the clip and let the temporal blurs "denoise" it for a stronger effect
	innerClip = denoised if NoiseProcess == 1 else clip

	#---------------------------------------
	# Interpolation

	# Support badly deinterlaced progressive content - drop half the fields and reweave to get 1/2fps interlaced stream appropriate for QTGMC processing
	if InputType > 1:
		ediInput = QTGMC_obs_Weave(innerClip.std.SeparateFields(tff=TFF).std.SelectEvery(cycle=4, offsets=[0, 3]), tff=TFF)
	else:
		ediInput = innerClip

	# Create interpolated image as starting point for output
	if EdiExt is not None:
		edi1 = EdiExt.resize.Point(w, h, src_top=(EdiExt.height - h) // 2, src_height=h)
	else:
		edi1 = QTGMC_obs_Interpolate(ediInput, InputType, EdiMode, NNSize, NNeurons, EdiQual, EdiMaxD, pscrn, int16_prescreener, int16_predictor, exp, alpha, beta, gamma, nrad, vcheck, bobbed, ChromaEdi, TFF, opencl, device)

	# InputType=2,3: use motion mask to blend luma between original clip & reweaved clip based on ProgSADMask setting. Use chroma from original clip in any case
	if InputType < 2:
		edi = edi1
	elif ProgSADMask <= 0:
		if not isGray:
			edi = core.std.ShufflePlanes([edi1, innerClip], planes=[0, 1, 2], colorfamily=Input.format.color_family)
		else:
			edi = edi1
	else:
		inputTypeBlend = core.mv.Mask(srchClip, bVec1, kind=1, ml=ProgSADMask)
		edi = core.std.MaskedMerge(innerClip, edi1, inputTypeBlend, planes=[0])

	# Get the max/min value for each pixel over neighboring motion-compensated frames - used for temporal sharpness limiting
	if TR1 > 0 or temporalSL:
		ediSuper = edi.mv.Super(pel=SubPel, sharp=SubPelInterp, levels=1, hpad=hpad, vpad=vpad)
	if temporalSL:
		bComp1 = core.mv.Compensate(edi, ediSuper, bVec1, thscd1=ThSCD1, thscd2=ThSCD2)
		fComp1 = core.mv.Compensate(edi, ediSuper, fVec1, thscd1=ThSCD1, thscd2=ThSCD2)
		tMax = core.std.Expr([core.std.Expr([edi, fComp1], expr=['x y max']), bComp1], expr=['x y max'])
		tMin = core.std.Expr([core.std.Expr([edi, fComp1], expr=['x y min']), bComp1], expr=['x y min'])
		if SLRad > 1:
			bComp3 = core.mv.Compensate(edi, ediSuper, bVec3, thscd1=ThSCD1, thscd2=ThSCD2)
			fComp3 = core.mv.Compensate(edi, ediSuper, fVec3, thscd1=ThSCD1, thscd2=ThSCD2)
			tMax = core.std.Expr([core.std.Expr([tMax, fComp3], expr=['x y max']), bComp3], expr=['x y max'])
			tMin = core.std.Expr([core.std.Expr([tMin, fComp3], expr=['x y min']), bComp3], expr=['x y min'])

	#---------------------------------------
	# Create basic output

	# Use motion vectors to blur interpolated image (edi) with motion-compensated previous and next frames. As above, this is done to remove shimmer from
	# alternate frames so the same binomial kernels are used. However, by using motion-compensated smoothing this time we avoid motion blur. The use of
	# MDegrain1 (motion compensated) rather than TemporalSmooth makes the weightings *look* different, but they evaluate to the same values
	# Create linear weightings of neighbors first                                                                      -2    -1    0     1     2
	if TR1 > 0: degrain1 = core.mv.Degrain1(edi, ediSuper, bVec1, fVec1, thsad=ThSAD1, thscd1=ThSCD1, thscd2=ThSCD2) # 0.00  0.33  0.33  0.33  0.00
	if TR1 > 1: degrain2 = core.mv.Degrain1(edi, ediSuper, bVec2, fVec2, thsad=ThSAD1, thscd1=ThSCD1, thscd2=ThSCD2) # 0.33  0.00  0.33  0.00  0.33

	# Combine linear weightings to give binomial weightings - TR1=0: (1), TR1=1: (1:2:1), TR1=2: (1:4:6:4:1)
	if TR1 <= 0:
		binomial1 = edi
	elif TR1 == 1:
		binomial1 = core.std.Merge(degrain1, edi, weight=[0.25])
	else:
		binomial1 = core.std.Merge(core.std.Merge(degrain1, degrain2, weight=[0.2]), edi, weight=[0.0625])

	# Remove areas of difference between smoothed image and interpolated image that are not bob-shimmer fixes: repairs residual motion blur from temporal smooth
	if Rep1 <= 0:
		repair1 = binomial1
	else:
		repair1 = QTGMC_obs_KeepOnlyBobShimmerFixes(binomial1, edi, Rep1, RepChroma)

	# Apply source match - use difference between output and source to succesively refine output [extracted to function to clarify main code path]
	if SourceMatch <= 0:
		match = repair1
	else:
		match = QTGMC_obs_ApplySourceMatch(
			repair1, InputType, ediInput, bVec1 if maxTR > 0 else None, fVec1 if maxTR > 0 else None, bVec2 if maxTR > 1 else None, fVec2 if maxTR > 1 else None, SubPel,
			SubPelInterp, hpad, vpad, ThSAD1, ThSCD1, ThSCD2, SourceMatch, MatchTR1, MatchEdi, MatchNNSize, MatchNNeurons, MatchEdiQual, MatchEdiMaxD, MatchTR2, MatchEdi2,
			MatchNNSize2, MatchNNeurons2, MatchEdiQual2, MatchEdiMaxD2, MatchEnhance, pscrn, int16_prescreener, int16_predictor, exp, alpha, beta, gamma, nrad, vcheck,
			TFF, opencl, device)

	# Lossless=2 - after preparing an interpolated, de-shimmered clip, restore the original source fields into it and clean up any artefacts
	# This mode will not give a true lossless result because the resharpening and final temporal smooth are still to come, but it will add further detail
	# However, it can introduce minor combing. This setting is best used together with source-match (it's effectively the final source-match stage)
	if Lossless >= 2:
		lossed1 = QTGMC_obs_MakeLossless(match, innerClip, InputType, TFF)
	else:
		lossed1 = match

	#---------------------------------------
	# Resharpen / retouch output

	# Resharpen to counteract temporal blurs. Little sharpening needed for source-match mode since it has already recovered sharpness from source
	if SMode <= 0:
		resharp = lossed1
	elif SMode == 1:
		resharp = core.std.Expr([lossed1, lossed1.std.Convolution(matrix=[1, 2, 1, 2, 4, 2, 1, 2, 1])], expr=[f'x x y - {sharpAdj} * +'])
	else:
		vresharp1 = core.std.Merge(lossed1.std.Maximum(coordinates=[0, 1, 0, 0, 0, 0, 1, 0]), lossed1.std.Minimum(coordinates=[0, 1, 0, 0, 0, 0, 1, 0]))
		if Precise:
			vresharp = core.std.Expr([vresharp1, lossed1], expr=['x y < x {i} + x y > x {i} - x ? ?'.format(i=QTGMC_obs_Scale(1, peak))]) # Precise mode: reduce tiny overshoot
		else:
			vresharp = vresharp1
		resharp = core.std.Expr([lossed1, vresharp.std.Convolution(matrix=[1, 2, 1, 2, 4, 2, 1, 2, 1])], expr=[f'x x y - {sharpAdj} * +'])

	# Slightly thin down 1-pixel high horizontal edges that have been widened into neigboring field lines by the interpolator
	SVThinSc = SVThin * 6.0
	if SVThin > 0:
		expr = f'y x - {SVThinSc} * {neutral} +'
		vertMedD = core.std.Expr([lossed1, lossed1.rgvs.VerticalCleaner(mode=[1] if isGray else [1, 0])], expr=[expr] if isGray else [expr, ''])
		vertMedD = vertMedD.std.Convolution(matrix=[1, 2, 1], planes=[0], mode='h')
		expr = f'y {neutral} - abs x {neutral} - abs > y {neutral} ?'
		neighborD = core.std.Expr([vertMedD, vertMedD.std.Convolution(matrix=[1, 2, 1, 2, 4, 2, 1, 2, 1], planes=[0])], expr=[expr] if isGray else [expr, ''])
		thin = core.std.MergeDiff(resharp, neighborD, planes=[0])
	else:
		thin = resharp

	# Back blend the blurred difference between sharpened & unsharpened clip, before (1st) sharpness limiting (Sbb == 1,3). A small fidelity improvement
	if Sbb not in [1, 3]:
		backBlend1 = thin
	else:
		backBlend1 = core.std.MakeDiff(thin, _Gauss(core.std.MakeDiff(thin, lossed1, planes=[0]).std.Convolution(matrix=[1, 2, 1, 2, 4, 2, 1, 2, 1], planes=[0]), p=5), planes=[0])

	# Limit over-sharpening by clamping to neighboring (spatial or temporal) min/max values in original
	# Occurs here (before final temporal smooth) if SLMode == 1,2. This location will restrict sharpness more, but any artefacts introduced will be smoothed
	if SLMode == 1:
		if SLRad <= 1:
			sharpLimit1 = core.rgvs.Repair(backBlend1, edi, mode=[1])
		else:
			sharpLimit1 = core.rgvs.Repair(backBlend1, core.rgvs.Repair(backBlend1, edi, mode=[12]), mode=[1])
	elif SLMode == 2:
		sharpLimit1 = _Clamp(backBlend1, tMax, tMin, SOvs, SOvs)
	else:
		sharpLimit1 = backBlend1

	# Back blend the blurred difference between sharpened & unsharpened clip, after (1st) sharpness limiting (Sbb == 2,3). A small fidelity improvement
	if Sbb < 2:
		backBlend2 = sharpLimit1
	else:
		backBlend2 = core.std.MakeDiff(sharpLimit1, _Gauss(core.std.MakeDiff(sharpLimit1, lossed1, planes=[0]).std.Convolution(matrix=[1, 2, 1, 2, 4, 2, 1, 2, 1], planes=[0]), p=5), planes=[0])

	# Add back any extracted noise, prior to final temporal smooth - this will restore detail that was removed as "noise" without restoring the noise itself
	# Average luma of FFT3DFilter extracted noise is 128.5, so deal with that too
	if GrainRestore <= 0:
		addNoise1 = backBlend2
	else:
		expr = f'x {noiseCentre} - {GrainRestore} * {neutral} +'
		addNoise1 = core.std.MergeDiff(backBlend2, finalNoise.std.Expr(expr=[expr] if ChromaNoise or isGray else [expr, '']), planes=CNplanes)

	# Final light linear temporal smooth for denoising
	if TR2 > 0:
		stableSuper = addNoise1.mv.Super(pel=SubPel, sharp=SubPelInterp, levels=1, hpad=hpad, vpad=vpad)
	if TR2 <= 0:
		stable = addNoise1
	elif TR2 == 1:
		stable = core.mv.Degrain1(addNoise1, stableSuper, bVec1, fVec1, thsad=ThSAD2, thscd1=ThSCD1, thscd2=ThSCD2)
	elif TR2 == 2:
		stable = core.mv.Degrain2(addNoise1, stableSuper, bVec1, fVec1, bVec2, fVec2, thsad=ThSAD2, thscd1=ThSCD1, thscd2=ThSCD2)
	else:
		stable = core.mv.Degrain3(addNoise1, stableSuper, bVec1, fVec1, bVec2, fVec2, bVec3, fVec3, thsad=ThSAD2, thscd1=ThSCD1, thscd2=ThSCD2)

	# Remove areas of difference between final output & basic interpolated image that are not bob-shimmer fixes: repairs motion blur caused by temporal smooth
	if Rep2 <= 0:
		repair2 = stable
	else:
		repair2 = QTGMC_obs_KeepOnlyBobShimmerFixes(stable, edi, Rep2, RepChroma)

	# Limit over-sharpening by clamping to neighboring (spatial or temporal) min/max values in original
	# Occurs here (after final temporal smooth) if SLMode == 3,4. Allows more sharpening here, but more prone to introducing minor artefacts
	if SLMode == 3:
		if SLRad <= 1:
			sharpLimit2 = core.rgvs.Repair(repair2, edi, mode=[1])
		else:
			sharpLimit2 = core.rgvs.Repair(repair2, core.rgvs.Repair(repair2, edi, mode=[12]), mode=[1])
	elif SLMode >= 4:
		sharpLimit2 = _Clamp(repair2, tMax, tMin, SOvs, SOvs)
	else:
		sharpLimit2 = repair2

	# Lossless=1 - inject source fields into result and clean up inevitable artefacts. Provided NoiseRestore=0.0 or 1.0, this mode will make the script result
	# properly lossless, but this will retain source artefacts and cause some combing (where the smoothed deinterlace doesn't quite match the source)
	if Lossless == 1:
		lossed2 = QTGMC_obs_MakeLossless(sharpLimit2, innerClip, InputType, TFF)
	else:
		lossed2 = sharpLimit2

	# Add back any extracted noise, after final temporal smooth. This will appear as noise/grain in the output
	# Average luma of FFT3DFilter extracted noise is 128.5, so deal with that too
	if NoiseRestore <= 0:
		addNoise2 = lossed2
	else:
		expr = f'x {noiseCentre} - {NoiseRestore} * {neutral} +'
		addNoise2 = core.std.MergeDiff(lossed2, finalNoise.std.Expr(expr=[expr] if ChromaNoise or isGray else [expr, '']), planes=CNplanes)

	#---------------------------------------
	# Post-Processing

	# Shutter motion blur - get level of blur depending on output framerate and blur already in source
	blurLevel = (ShutterAngleOut * FPSDivisor - ShutterAngleSrc) * 100 / 360
	if blurLevel < 0:
		raise vs.Error('QTGMC: cannot reduce motion blur already in source: increase ShutterAngleOut or FPSDivisor')
	if blurLevel > 200:
		raise vs.Error('QTGMC: exceeded maximum motion blur level: decrease ShutterAngleOut or FPSDivisor')

	# ShutterBlur mode 2,3 - get finer resolution motion vectors to reduce blur "bleeding" into static areas
	rBlockDivide = [1, 1, 2, 4][ShutterBlur]
	rBlockSize = BlockSize // rBlockDivide
	rOverlap = Overlap // rBlockDivide
	rBlockSize = max(rBlockSize, 4)
	rOverlap = max(rOverlap, 2)
	rBlockDivide = BlockSize // rBlockSize
	rLambda = Lambda // (rBlockDivide * rBlockDivide)
	if ShutterBlur > 1:
		recalculate_args = dict(thsad=ThSAD1, blksize=rBlockSize, overlap=rOverlap, search=Search, searchparam=SearchParam, truemotion=TrueMotion, lambda_=rLambda, pnew=PNew, dct=DCT, chroma=ChromaMotion)
		sbBVec1 = core.mv.Recalculate(srchSuper, bVec1, **recalculate_args)
		sbFVec1 = core.mv.Recalculate(srchSuper, fVec1, **recalculate_args)
	elif ShutterBlur > 0:
		sbBVec1 = bVec1
		sbFVec1 = fVec1

	# Shutter motion blur - use MFlowBlur to blur along motion vectors
	if ShutterBlur > 0:
		sblurSuper = addNoise2.mv.Super(pel=SubPel, sharp=SubPelInterp, levels=1, hpad=hpad, vpad=vpad)
		sblur = core.mv.FlowBlur(addNoise2, sblurSuper, sbBVec1, sbFVec1, blur=blurLevel, thscd1=ThSCD1, thscd2=ThSCD2)

	# Shutter motion blur - use motion mask to reduce blurring in areas of low motion - also helps reduce blur "bleeding" into static areas, then select blur type
	if ShutterBlur <= 0:
		sblurred = addNoise2
	elif SBlurLimit <= 0:
		sblurred = sblur
	else:
		sbMotionMask = core.mv.Mask(srchClip, bVec1, kind=0, ml=SBlurLimit)
		sblurred = core.std.MaskedMerge(addNoise2, sblur, sbMotionMask)

	# Reduce frame rate
	if FPSDivisor > 1:
		decimated = sblurred.std.SelectEvery(cycle=FPSDivisor, offsets=[0])
	else:
		decimated = sblurred

	# Crop off temporary vertical padding
	if Border:
		cropped = decimated.std.Crop(top=4, bottom=4)
	else:
		cropped = decimated

	# Show output of choice + settings
	if ShowNoise <= 0:
		output = cropped
	else:
		expr = f'x {neutral} - {ShowNoise} * {neutral} +'
		output = finalNoise.std.Expr(expr=[expr] if ChromaNoise or isGray else [expr, repr(neutral)])
	output = output.std.SetFieldBased(value=0)
	if not ShowSettings:
		return output
	else:
		text = f"TR0={TR0} | TR1={TR1} | TR2={TR2} | Rep0={Rep0} | Rep1={Rep1} | Rep2={Rep2} | RepChroma={RepChroma} | EdiMode='{EdiMode}' | NNSize={NNSize} | NNeurons={NNeurons} | " + \
			f"EdiQual={EdiQual} | EdiMaxD={EdiMaxD} | ChromaEdi='{ChromaEdi}' | Sharpness={Sharpness} | SMode={SMode} | SLMode={SLMode} | SLRad={SLRad} | SOvs={SOvs} | SVThin={SVThin} | " + \
			f"Sbb={Sbb} | SrchClipPP={SrchClipPP} | SubPel={SubPel} | SubPelInterp={SubPelInterp} | BlockSize={BlockSize} | Overlap={Overlap} | Search={Search} | SearchParam={SearchParam} | " + \
			f"PelSearch={PelSearch} | ChromaMotion={ChromaMotion} | TrueMotion={TrueMotion} | Lambda={Lambda} | LSAD={LSAD} | PNew={PNew} | PLevel={PLevel} | GlobalMotion={GlobalMotion} | " + \
			f"DCT={DCT} | ThSAD1={ThSAD1} | ThSAD2={ThSAD2} | ThSCD1={ThSCD1} | ThSCD2={ThSCD2} | SourceMatch={SourceMatch} | MatchPreset='{MatchPreset}' | MatchEdi='{MatchEdi}' | " + \
			f"MatchPreset2='{MatchPreset2}' | MatchEdi2='{MatchEdi2}' | MatchTR2={MatchTR2} | MatchEnhance={MatchEnhance} | Lossless={Lossless} | NoiseProcess={NoiseProcess} | " + \
			f"Denoiser='{Denoiser}' | FftThreads={FftThreads} | DenoiseMC={DenoiseMC} | NoiseTR={NoiseTR} | Sigma={Sigma} | ChromaNoise={ChromaNoise} | ShowNoise={ShowNoise} | " + \
			f"GrainRestore={GrainRestore} | NoiseRestore={NoiseRestore} | NoiseDeint='{NoiseDeint}' | StabilizeNoise={StabilizeNoise} | InputType={InputType} | ProgSADMask={ProgSADMask} | " + \
			f"FPSDivisor={FPSDivisor} | ShutterBlur={ShutterBlur} | ShutterAngleSrc={ShutterAngleSrc} | ShutterAngleOut={ShutterAngleOut} | SBlurLimit={SBlurLimit} | Border={Border} | " + \
			f"Precise={Precise} | Preset='{Preset}' | Tuning='{Tuning}' | ForceTR={ForceTR}"
		return output.text.Text(text=text)

#---------------------------------------
# Helpers

# Interpolate input clip using method given in EdiMode. Use Fallback or Bob as result if mode not in list. If ChromaEdi string if set then interpolate chroma
# separately with that method (only really useful for EEDIx). The function is used as main algorithm starting point and for first two source-match stages
def QTGMC_obs_Interpolate(
		Input, InputType, EdiMode, NNSize, NNeurons, EdiQual, EdiMaxD, pscrn, int16_prescreener, int16_predictor, exp, alpha, beta, gamma, nrad, vcheck,
		Fallback=None, ChromaEdi='', TFF=None, opencl=False, device=None):
	if opencl:
		nnedi3 = functools.partial(core.nnedi3cl.NNEDI3CL, nsize=NNSize, nns=NNeurons, qual=EdiQual, pscrn=pscrn, device=device)
		eedi3 = functools.partial(core.eedi3m.EEDI3CL, alpha=alpha, beta=beta, gamma=gamma, nrad=nrad, mdis=EdiMaxD, vcheck=vcheck, device=device)
	else:
		nnedi3 = functools.partial(core.znedi3.nnedi3, nsize=NNSize, nns=NNeurons, qual=EdiQual, pscrn=pscrn, int16_prescreener=int16_prescreener, int16_predictor=int16_predictor, exp=exp)
		eedi3 = functools.partial(core.eedi3m.EEDI3, alpha=alpha, beta=beta, gamma=gamma, nrad=nrad, mdis=EdiMaxD, vcheck=vcheck)

	isGray = (Input.format.color_family == vs.GRAY)
	if isGray:
		ChromaEdi = ''
	planes = [0, 1, 2] if ChromaEdi == '' and not isGray else [0]
	field = 3 if TFF else 2

	if InputType == 1:
		return Input
	elif EdiMode == 'nnedi3':
		interp = nnedi3(Input, field=field, planes=planes)
	elif EdiMode == 'eedi3+nnedi3':
		interp = eedi3(Input, field=field, planes=planes, sclip=nnedi3(Input, field=field, planes=planes))
	elif EdiMode == 'eedi3':
		interp = eedi3(Input, field=field, planes=planes)
	else:
		if isinstance(Fallback, vs.VideoNode):
			interp = Fallback
		else:
			interp = Input.resize.Bob(tff=TFF, filter_param_a=0, filter_param_b=0.5)

	if ChromaEdi == 'nnedi3':
		interpuv = nnedi3(Input, field=field, planes=[1, 2], nsize=4, nns=0, qual=1)
	elif ChromaEdi == 'bob':
		interpuv = Input.resize.Bob(tff=TFF, filter_param_a=0, filter_param_b=0.5)
	else:
		return interp

	return core.std.ShufflePlanes([interp, interpuv], planes=[0, 1, 2], colorfamily=Input.format.color_family)

# Helper function: Compare processed clip with reference clip: only allow thin, horizontal areas of difference, i.e. bob shimmer fixes
# Rough algorithm: Get difference, deflate vertically by a couple of pixels or so, then inflate again. Thin regions will be removed
#                  by this process. Restore remaining areas of difference back to as they were in reference clip
def QTGMC_obs_KeepOnlyBobShimmerFixes(Input, Ref, Rep=1, Chroma=True):
	isGray = (Input.format.color_family == vs.GRAY)
	planes = [0, 1, 2] if Chroma and not isGray else [0]

	neutral = 1 << (Input.format.bits_per_sample - 1)
	peak = (1 << Input.format.bits_per_sample) - 1

	# ed is the erosion distance - how much to deflate then reflate to remove thin areas of interest: 0 = minimum to 6 = maximum
	# od is over-dilation level  - extra inflation to ensure areas to restore back are fully caught:  0 = none to 3 = one full pixel
	# If Rep < 10, then ed = Rep and od = 0, otherwise ed = 10s digit and od = 1s digit (nasty method, but kept for compatibility with original TGMC)
	ed = Rep if Rep < 10 else Rep // 10
	od = 0 if Rep < 10 else Rep % 10

	diff = core.std.MakeDiff(Ref, Input)

	# Areas of positive difference                                                              # ed = 0 1 2 3 4 5 6 7
	choke1 = diff.std.Minimum(planes=planes, coordinates=[0, 1, 0, 0, 0, 0, 1, 0])              #      x x x x x x x x    1 pixel   \
	if ed > 2: choke1 = choke1.std.Minimum(planes=planes, coordinates=[0, 1, 0, 0, 0, 0, 1, 0]) #      . . . x x x x x    1 pixel    |  Deflate to remove thin areas
	if ed > 5: choke1 = choke1.std.Minimum(planes=planes, coordinates=[0, 1, 0, 0, 0, 0, 1, 0]) #      . . . . . . x x    1 pixel   /
	if ed % 3 != 0: choke1 = choke1.std.Deflate(planes=planes)                                  #      . x x . x x . x    A bit more deflate & some horizonal effect
	if ed in [2, 5]: choke1 = choke1.std.Median(planes=planes)                                  #      . . x . . x . .    Local median
	choke1 = choke1.std.Maximum(planes=planes, coordinates=[0, 1, 0, 0, 0, 0, 1, 0])            #      x x x x x x x x    1 pixel  \
	if ed > 1: choke1 = choke1.std.Maximum(planes=planes, coordinates=[0, 1, 0, 0, 0, 0, 1, 0]) #      . . x x x x x x    1 pixel   | Reflate again
	if ed > 4: choke1 = choke1.std.Maximum(planes=planes, coordinates=[0, 1, 0, 0, 0, 0, 1, 0]) #      . . . . . x x x    1 pixel  /

	# Over-dilation - extra reflation up to about 1 pixel
	if od == 1:
		choke1 = choke1.std.Inflate(planes=planes)
	elif od == 2:
		choke1 = choke1.std.Inflate(planes=planes).std.Inflate(planes=planes)
	elif od >= 3:
		choke1 = choke1.std.Maximum(planes=planes)

	# Areas of negative difference (similar to above)
	choke2 = diff.std.Maximum(planes=planes, coordinates=[0, 1, 0, 0, 0, 0, 1, 0])
	if ed > 2: choke2 = choke2.std.Maximum(planes=planes, coordinates=[0, 1, 0, 0, 0, 0, 1, 0])
	if ed > 5: choke2 = choke2.std.Maximum(planes=planes, coordinates=[0, 1, 0, 0, 0, 0, 1, 0])
	if ed % 3 != 0: choke2 = choke2.std.Inflate(planes=planes)
	if ed in [2, 5]: choke2 = choke2.std.Median(planes=planes)
	choke2 = choke2.std.Minimum(planes=planes, coordinates=[0, 1, 0, 0, 0, 0, 1, 0])
	if ed > 1: choke2 = choke2.std.Minimum(planes=planes, coordinates=[0, 1, 0, 0, 0, 0, 1, 0])
	if ed > 4: choke2 = choke2.std.Minimum(planes=planes, coordinates=[0, 1, 0, 0, 0, 0, 1, 0])

	if od == 1:
		choke2 = choke2.std.Deflate(planes=planes)
	elif od == 2:
		choke2 = choke2.std.Deflate(planes=planes).std.Deflate(planes=planes)
	elif od >= 3:
		choke2 = choke2.std.Minimum(planes=planes)

	# Combine above areas to find those areas of difference to restore
	expr1 = f'x {QTGMC_obs_Scale(129, peak)} < x y {neutral} < {neutral} y ? ?'
	expr2 = f'x {QTGMC_obs_Scale(127, peak)} > x y {neutral} > {neutral} y ? ?'
	restore = core.std.Expr([core.std.Expr([diff, choke1], expr=[expr1] if Chroma or isGray else [expr1, '']), choke2], expr=[expr2] if Chroma or isGray else [expr2, ''])

	return core.std.MergeDiff(Input, restore, planes=planes)

# Given noise extracted from an interlaced source (i.e. the noise is interlaced), generate "progressive" noise with a new "field" of noise injected. The new
# noise is centered on a weighted local average and uses the difference between local min & max as an estimate of local variance
def QTGMC_obs_Generate2ndFieldNoise(Input, InterleavedClip, ChromaNoise=False, TFF=None):
	isGray = (Input.format.color_family == vs.GRAY)
	planes = [0, 1, 2] if ChromaNoise and not isGray else [0]

	neutral = 1 << (Input.format.bits_per_sample - 1)
	peak = (1 << Input.format.bits_per_sample) - 1

	origNoise = Input.std.SeparateFields(tff=TFF)
	noiseMax = origNoise.std.Maximum(planes=planes).std.Maximum(planes=planes, coordinates=[0, 0, 0, 1, 1, 0, 0, 0])
	noiseMin = origNoise.std.Minimum(planes=planes).std.Minimum(planes=planes, coordinates=[0, 0, 0, 1, 1, 0, 0, 0])
	random = InterleavedClip.std.SeparateFields(tff=TFF).std.BlankClip(color=[neutral] * Input.format.num_planes).grain.Add(var=1800, uvar=1800 if ChromaNoise else 0)
	expr = f'x {neutral} - y * {QTGMC_obs_Scale(256, peak)} / {neutral} +'
	varRandom = core.std.Expr([core.std.MakeDiff(noiseMax, noiseMin, planes=planes), random], expr=[expr] if ChromaNoise or isGray else [expr, ''])
	newNoise = core.std.MergeDiff(noiseMin, varRandom, planes=planes)

	return QTGMC_obs_Weave(core.std.Interleave([origNoise, newNoise]), tff=TFF)

# Insert the source lines into the result to create a true lossless output. However, the other lines in the result have had considerable processing and won't
# exactly match source lines. There will be some slight residual combing. Use vertical medians to clean a little of this away
def QTGMC_obs_MakeLossless(Input, Source, InputType, TFF):
	if InputType == 1:
		raise vs.Error('QTGMC: lossless modes are incompatible with InputType=1')

	neutral = 1 << (Input.format.bits_per_sample - 1)

	# QTGMC_obs_Weave the source fields and the "new" fields that have generated in the input
	if InputType <= 0:
		srcFields = Source.std.SeparateFields(tff=TFF)
	else:
		srcFields = Source.std.SeparateFields(tff=TFF).std.SelectEvery(cycle=4, offsets=[0, 3])
	newFields = Input.std.SeparateFields(tff=TFF).std.SelectEvery(cycle=4, offsets=[1, 2])
	processed = QTGMC_obs_Weave(core.std.Interleave([srcFields, newFields]).std.SelectEvery(cycle=4, offsets=[0, 1, 3, 2]), tff=TFF)

	# Clean some of the artefacts caused by the above - creating a second version of the "new" fields
	vertMedian = processed.rgvs.VerticalCleaner(mode=[1])
	vertMedDiff = core.std.MakeDiff(processed, vertMedian)
	vmNewDiff1 = vertMedDiff.std.SeparateFields(tff=TFF).std.SelectEvery(cycle=4, offsets=[1, 2])
	expr = f'x {neutral} - y {neutral} - * 0 < {neutral} x {neutral} - abs y {neutral} - abs < x y ? ?'
	vmNewDiff2 = core.std.Expr([vmNewDiff1.rgvs.VerticalCleaner(mode=[1]), vmNewDiff1], expr=[expr])
	vmNewDiff3 = core.rgvs.Repair(vmNewDiff2, vmNewDiff2.rgvs.RemoveGrain(mode=[2]), mode=[1])

	# Reweave final result
	return QTGMC_obs_Weave(core.std.Interleave([srcFields, core.std.MakeDiff(newFields, vmNewDiff3)]).std.SelectEvery(cycle=4, offsets=[0, 1, 3, 2]), tff=TFF)

# Source-match, a three stage process that takes the difference between deinterlaced input and the original interlaced source, to shift the input more towards
# the source without introducing shimmer. All other arguments defined in main script
def QTGMC_obs_ApplySourceMatch(
		Deinterlace, InputType, Source, bVec1, fVec1, bVec2, fVec2, SubPel, SubPelInterp, hpad, vpad, ThSAD1, ThSCD1, ThSCD2, SourceMatch,
		MatchTR1, MatchEdi, MatchNNSize, MatchNNeurons, MatchEdiQual, MatchEdiMaxD, MatchTR2, MatchEdi2, MatchNNSize2, MatchNNeurons2, MatchEdiQual2, MatchEdiMaxD2, MatchEnhance,
		pscrn, int16_prescreener, int16_predictor, exp, alpha, beta, gamma, nrad, vcheck, TFF, opencl, device):
	# Basic source-match. Find difference between source clip & equivalent fields in interpolated/smoothed clip (called the "error" in formula below). Ideally
	# there should be no difference, we want the fields in the output to be as close as possible to the source whilst remaining shimmer-free. So adjust the
	# *source* in such a way that smoothing it will give a result closer to the unadjusted source. Then rerun the interpolation (edi) and binomial smooth with
	# this new source. Result will still be shimmer-free and closer to the original source.
	# Formula used for correction is P0' = P0 + (P0-P1)/(k+S(1-k)), where P0 is original image, P1 is the 1st attempt at interpolation/smoothing , P0' is the
	# revised image to use as new source for interpolation/smoothing, k is the weighting given to the current frame in the smooth, and S is a factor indicating
	# "temporal similarity" of the error from frame to frame, i.e. S = average over all pixels of [neighbor frame error / current frame error] . Decreasing
	# S will make the result sharper, sensible range is about -0.25 to 1.0. Empirically, S=0.5 is effective [will do deeper analysis later]
	errorTemporalSimilarity = 0.5 # S in formula described above
	errorAdjust1 = [1.0, 2.0 / (1.0 + errorTemporalSimilarity), 8.0 / (3.0 + 5.0 * errorTemporalSimilarity)][MatchTR1]
	if SourceMatch < 1 or InputType == 1:
		match1Clip = Deinterlace
	else:
		match1Clip = QTGMC_obs_Weave(Deinterlace.std.SeparateFields(tff=TFF).std.SelectEvery(cycle=4, offsets=[0, 3]), tff=TFF)
	if SourceMatch < 1 or MatchTR1 <= 0:
		match1Update = Source
	else:
		match1Update = core.std.Expr([Source, match1Clip], expr=[f'x {errorAdjust1 + 1} * y {errorAdjust1} * -'])
	if SourceMatch > 0:
		match1Edi = QTGMC_obs_Interpolate(match1Update, InputType, MatchEdi, MatchNNSize, MatchNNeurons, MatchEdiQual, MatchEdiMaxD, pscrn, int16_prescreener, int16_predictor, exp, alpha, beta, gamma,
										nrad, vcheck, TFF=TFF, opencl=opencl, device=device)
		if MatchTR1 > 0:
			match1Super = match1Edi.mv.Super(pel=SubPel, sharp=SubPelInterp, levels=1, hpad=hpad, vpad=vpad)
			match1Degrain1 = core.mv.Degrain1(match1Edi, match1Super, bVec1, fVec1, thsad=ThSAD1, thscd1=ThSCD1, thscd2=ThSCD2)
		if MatchTR1 > 1:
			match1Degrain2 = core.mv.Degrain1(match1Edi, match1Super, bVec2, fVec2, thsad=ThSAD1, thscd1=ThSCD1, thscd2=ThSCD2)
	if SourceMatch < 1:
		match1 = Deinterlace
	elif MatchTR1 <= 0:
		match1 = match1Edi
	elif MatchTR1 == 1:
		match1 = core.std.Merge(match1Degrain1, match1Edi, weight=[0.25])
	else:
		match1 = core.std.Merge(core.std.Merge(match1Degrain1, match1Degrain2, weight=[0.2]), match1Edi, weight=[0.0625])

	if SourceMatch < 2:
		return match1

	# Enhance effect of source-match stages 2 & 3 by sharpening clip prior to refinement (source-match tends to underestimate so this will leave result sharper)
	if SourceMatch > 1 and MatchEnhance > 0:
		match1Shp = core.std.Expr([match1, match1.std.Convolution(matrix=[1, 2, 1, 2, 4, 2, 1, 2, 1])], expr=[f'x x y - {MatchEnhance} * +'])
	else:
		match1Shp = match1

	# Source-match refinement. Find difference between source clip & equivalent fields in (updated) interpolated/smoothed clip. Interpolate & binomially smooth
	# this difference then add it back to output. Helps restore differences that the basic match missed. However, as this pass works on a difference rather than
	# the source image it can be prone to occasional artefacts (difference images are not ideal for interpolation). In fact a lower quality interpolation such
	# as a simple bob often performs nearly as well as advanced, slower methods (e.g. NNEDI3)
	if SourceMatch < 2 or InputType == 1:
		match2Clip = match1Shp
	else:
		match2Clip = QTGMC_obs_Weave(match1Shp.std.SeparateFields(tff=TFF).std.SelectEvery(cycle=4, offsets=[0, 3]), tff=TFF)
	if SourceMatch > 1:
		match2Diff = core.std.MakeDiff(Source, match2Clip)
		match2Edi = QTGMC_obs_Interpolate(match2Diff, InputType, MatchEdi2, MatchNNSize2, MatchNNeurons2, MatchEdiQual2, MatchEdiMaxD2, pscrn, int16_prescreener, int16_predictor, exp, alpha, beta, gamma,
										nrad, vcheck, TFF=TFF, opencl=opencl, device=device)
		if MatchTR2 > 0:
			match2Super = match2Edi.mv.Super(pel=SubPel, sharp=SubPelInterp, levels=1, hpad=hpad, vpad=vpad)
			match2Degrain1 = core.mv.Degrain1(match2Edi, match2Super, bVec1, fVec1, thsad=ThSAD1, thscd1=ThSCD1, thscd2=ThSCD2)
		if MatchTR2 > 1:
			match2Degrain2 = core.mv.Degrain1(match2Edi, match2Super, bVec2, fVec2, thsad=ThSAD1, thscd1=ThSCD1, thscd2=ThSCD2)
	if SourceMatch < 2:
		match2 = match1
	elif MatchTR2 <= 0:
		match2 = match2Edi
	elif MatchTR2 == 1:
		match2 = core.std.Merge(match2Degrain1, match2Edi, weight=[0.25])
	else:
		match2 = core.std.Merge(core.std.Merge(match2Degrain1, match2Degrain2, weight=[0.2]), match2Edi, weight=[0.0625])

	# Source-match second refinement - correct error introduced in the refined difference by temporal smoothing. Similar to error correction from basic step
	errorAdjust2 = [1.0, 2.0 / (1.0 + errorTemporalSimilarity), 8.0 / (3.0 + 5.0 * errorTemporalSimilarity)][MatchTR2]
	if SourceMatch < 3 or MatchTR2 <= 0:
		match3Update = match2Edi
	else:
		match3Update = core.std.Expr([match2Edi, match2], expr=[f'x {errorAdjust2 + 1} * y {errorAdjust2} * -'])
	if SourceMatch > 2:
		if MatchTR2 > 0:
			match3Super = match3Update.mv.Super(pel=SubPel, sharp=SubPelInterp, levels=1, hpad=hpad, vpad=vpad)
			match3Degrain1 = core.mv.Degrain1(match3Update, match3Super, bVec1, fVec1, thsad=ThSAD1, thscd1=ThSCD1, thscd2=ThSCD2)
		if MatchTR2 > 1:
			match3Degrain2 = core.mv.Degrain1(match3Update, match3Super, bVec2, fVec2, thsad=ThSAD1, thscd1=ThSCD1, thscd2=ThSCD2)
	if SourceMatch < 3:
		match3 = match2
	elif MatchTR2 <= 0:
		match3 = match3Update
	elif MatchTR2 == 1:
		match3 = core.std.Merge(match3Degrain1, match3Update, weight=[0.25])
	else:
		match3 = core.std.Merge(core.std.Merge(match3Degrain1, match3Degrain2, weight=[0.2]), match3Update, weight=[0.0625])

	# Apply difference calculated in source-match refinement
	return core.std.MergeDiff(match1Shp, match3)



def QTGMCv2(
	input : vs.VideoNode,
	fps_in : float = 23.976,
	obs : bool = True,
	deint_lv : typing.Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] = 6,
	src_type : typing.Literal[0, 1, 2, 3] = 0,
	deint_den : typing.Literal[1, 2] = 1,
	tff : typing.Literal[0, 1, 2] = 0,
	cpu : bool = True,
	gpu : typing.Literal[-1, 0, 1, 2] = -1,
) -> vs.VideoNode:

	##TODO: 依赖检查

	if not tff :
		field_src = getattr(input.get_frame(0).props, "_FieldBased", 1)
		if field_src == 0 :
			field_order = 1
		else :
			field_order = field_src
	else :
		field_order = tff
	preset_val = ["Draft", "Ultra Fast", "Super Fast", "Very Fast", "Faster", "Fast", "Medium", "Slow", "Slower", "Very Slow", "Placebo"][deint_lv - 1]
	fps_out = (fps_in / deint_den) * 1e6
	if src_type == 0 :
		fps_out = fps_out * 2

	src = core.std.AssumeFPS(clip=input, fpsnum=int(fps_in * 1e6), fpsden=1e6)
	if obs :
		clip = QTGMC_obs(Input=src, Preset=preset_val, InputType=src_type, FPSDivisor=deint_den, TFF=True if field_order==1 else False, opencl=not cpu, device=gpu)
	else :
		clip = QTGMC(Input=src, Preset=preset_val, InputType=src_type, FPSDivisor=deint_den, TFF=True if field_order==1 else False, opencl=not cpu, device=gpu)
	output = core.std.AssumeFPS(clip=clip, fpsnum=int(fps_out), fpsden=1e6)

	return output

