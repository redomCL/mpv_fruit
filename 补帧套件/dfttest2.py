__version__ = "0.4.0"

from dataclasses import dataclass
import math
from string import Template
import typing

import vapoursynth as vs
from vapoursynth import core


__all__ = ["DFTTest", "DFTTest2", "Backend"]


class Backend:
    @dataclass(frozen=False)
    class cuFFT:
        device_id: int = 0
        in_place: bool = True

    @dataclass(frozen=False)
    class NVRTC:
        device_id: int = 0
        num_streams: int = 1

    @dataclass(frozen=False)
    class CPU:
        opt: int = 0

    @dataclass(frozen=False)
    class GCC:
        pass

    @dataclass(frozen=False)
    class hipFFT:
        device_id: int = 0
        in_place: bool = True

    @dataclass(frozen=False)
    class HIPRTC:
        device_id: int = 0
        num_streams: int = 1

backendT = typing.Union[Backend.cuFFT, Backend.NVRTC, Backend.CPU, Backend.GCC, Backend.hipFFT, Backend.HIPRTC]


def init_backend(backend: backendT) -> backendT:
    if backend is Backend.cuFFT: # type: ignore
        backend = Backend.cuFFT()
    elif backend is Backend.NVRTC: # type: ignore
        backend = Backend.NVRTC()
    elif backend is Backend.CPU: # type: ignore
        backend = Backend.CPU()
    elif backend is Backend.GCC: # type: ignore
        backend = Backend.GCC()
    elif backend is Backend.hipFFT: # type: ignore
        backend = Backend.hipFFT()
    elif backend is Backend.HIPRTC: # type: ignore
        backend = Backend.HIPRTC()
    return backend


# https://github.com/HomeOfVapourSynthEvolution/VapourSynth-DFTTest/blob/
# bc5e0186a7f309556f20a8e9502f2238e39179b8/DFTTest/DFTTest.cpp#L518
def normalize(
    window: typing.Sequence[float],
    size: int,
    step: int
) -> typing.List[float]:

    nw = [0.0] * size
    for q in range(size):
        for h in range(q, -1, -step):
            nw[q] += window[h] ** 2
        for h in range(q + step, size, step):
            nw[q] += window[h] ** 2
    return [window[q] / math.sqrt(nw[q]) for q in range(size)]


# https://github.com/HomeOfVapourSynthEvolution/VapourSynth-DFTTest/blob/
# bc5e0186a7f309556f20a8e9502f2238e39179b8/DFTTest/DFTTest.cpp#L462
def get_window_value(location: float, size: int, mode: int, beta: float) -> float:
    temp = math.pi * location / size
    if mode == 0: # hanning
        return 0.5 * (1 - math.cos(2 * temp))
    elif mode == 1: # hamming
        return 0.53836 - 0.46164 * math.cos(2 * temp)
    elif mode == 2: # blackman
        return 0.42 - 0.5 * math.cos(2 * temp) + 0.08 * math.cos(4 * temp)
    elif mode == 3: # 4 term blackman-harris
        return (
            0.35875
            - 0.48829 * math.cos(2 * temp)
            + 0.14128 * math.cos(4 * temp)
            - 0.01168 * math.cos(6 * temp)
        )
    elif mode == 4: # kaiser-bessel
        def i0(p: float) -> float:
            p /= 2
            n = t = d = 1.0
            k = 1
            while True:
                n *= p
                d *= k
                v = n / d
                t += v * v
                k += 1
                if k >= 15 or v <= 1e-8:
                    break
            return t
        v = 2 * location / size - 1
        return i0(math.pi * beta * math.sqrt(1 - v * v)) / i0(math.pi * beta)
    elif mode == 5: # 7 term blackman-harris
        return (
            0.27105140069342415
            - 0.433297939234486060 * math.cos(2 * temp)
            + 0.218122999543110620 * math.cos(4 * temp)
            - 0.065925446388030898 * math.cos(6 * temp)
            + 0.010811742098372268 * math.cos(8 * temp)
            - 7.7658482522509342e-4 * math.cos(10 * temp)
            + 1.3887217350903198e-5 * math.cos(12 * temp)
        )
    elif mode == 6: # flat top
        return (
            0.2810639
            - 0.5208972 * math.cos(2 * temp)
            + 0.1980399 * math.cos(4 * temp)
        )
    elif mode == 7: # rectangular
        return 1.0
    elif mode == 8: # Bartlett
        return 1 - 2 * abs(location - size / 2) / size
    elif mode == 9: # bartlett-hann
        return 0.62 - 0.48 * (location / size - 0.5) - 0.38 * math.cos(2 * temp)
    elif mode == 10: # nuttall
        return (
            0.355768
            - 0.487396 * math.cos(2 * temp)
            + 0.144232 * math.cos(4 * temp)
            - 0.012604 * math.cos(6 * temp)
        )
    elif mode == 11: # blackman-nuttall
        return (
            0.3635819
            - 0.4891775 * math.cos(2 * temp)
            + 0.1365995 * math.cos(4 * temp)
            - 0.0106411 * math.cos(6 * temp)
        )
    else:
        raise ValueError("unknown window")


# https://github.com/HomeOfVapourSynthEvolution/VapourSynth-DFTTest/blob/
# bc5e0186a7f309556f20a8e9502f2238e39179b8/DFTTest/DFTTest.cpp#L461
def get_window(
    radius: int,
    block_size: int,
    block_step: int,
    spatial_window_mode: int,
    spatial_beta: float,
    temporal_window_mode: int,
    temporal_beta: float
) -> typing.List[float]:

    temporal_window = [
        get_window_value(
            location = i + 0.5,
            size = 2 * radius + 1,
            mode = temporal_window_mode,
            beta = temporal_beta
        ) for i in range(2 * radius + 1)
    ]

    spatial_window = [
        get_window_value(
            location = i + 0.5,
            size = block_size,
            mode = spatial_window_mode,
            beta = spatial_beta
        ) for i in range(block_size)
    ]

    spatial_window = normalize(
        window=spatial_window,
        size=block_size,
        step=block_step
    )

    window = []
    for t_val in temporal_window:
        for s_val1 in spatial_window:
            for s_val2 in spatial_window:
                value = t_val * s_val1 * s_val2

                # normalize for unnormalized FFT implementation
                value /= math.sqrt(2 * radius + 1) * block_size

                window.append(value)

    return window


# https://github.com/HomeOfVapourSynthEvolution/VapourSynth-DFTTest/blob/
# bc5e0186a7f309556f20a8e9502f2238e39179b8/DFTTest/DFTTest.cpp#L581
def get_location(
    position: float,
    length: int
) -> float:

    if length == 1:
        return 0.0
    elif position > length // 2:
        return (length - position) / (length // 2)
    else:
        return position / (length // 2)


# https://github.com/HomeOfVapourSynthEvolution/VapourSynth-DFTTest/blob/
# bc5e0186a7f309556f20a8e9502f2238e39179b8/DFTTest/DFTTest.cpp#L581
def get_sigma(
    position: float,
    length: int,
    func: typing.Callable[[float], float]
) -> float:

    if length == 1:
        return 1.0
    else:
        return func(get_location(position, length))


def DFTTest2(
    clip: vs.VideoNode,
    ftype: typing.Literal[0, 1, 2, 3, 4] = 0,
    sigma: typing.Union[float, typing.Sequence[typing.Callable[[float], float]]] = 8.0,
    sigma2: float = 8.0,
    pmin: float = 0.0,
    pmax: float = 500.0,
    sbsize: int = 16,
    sosize: int = 12,
    tbsize: int = 3,
    swin: typing.Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] = 0,
    twin: typing.Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] = 7,
    sbeta: float = 2.5,
    tbeta: float = 2.5,
    zmean: bool = True,
    f0beta: float = 1.0,
    ssystem: typing.Literal[0, 1] = 0,
    planes: typing.Optional[typing.Union[int, typing.Sequence[int]]] = None,
    backend: backendT = Backend.cuFFT()
) -> vs.VideoNode:
    """ this interface is not stable """

    # translate parameters
    if ftype == 0:
        if abs(f0beta - 1) < 0.00005:
            filter_type = 0
        elif abs(f0beta - 0.5) < 0.0005:
            filter_type = 6
        else:
            filter_type = 5
    else:
        filter_type = ftype

    radius = (tbsize - 1) // 2
    block_size = sbsize
    block_step = sbsize - sosize
    spatial_window_mode = swin
    temporal_window_mode = twin
    spatial_beta = sbeta
    temporal_beta = tbeta
    zero_mean = zmean
    backend = init_backend(backend)

    if isinstance(backend, (Backend.CPU, Backend.NVRTC, Backend.GCC, Backend.HIPRTC)):
        if radius not in range(4):
            raise ValueError("invalid radius (tbsize)")
        if block_size != 16:
            raise ValueError("invalid block_size (sbsize)")

    # compute constants
    try:
        sigma_scalar = float(sigma) # type: ignore
        sigma_is_scalar = True
    except:
        # compute sigma_array

        sigma_is_scalar = False

        sigma_funcs = typing.cast(typing.Sequence[typing.Callable[[float], float]], sigma)
        if callable(sigma_funcs):
            sigma_funcs = [sigma_funcs]
        else:
            sigma_funcs = list(sigma_funcs)
        sigma_funcs.extend([sigma_funcs[-1]] * 3)
        sigma_func_x, sigma_func_y, sigma_func_t = sigma_funcs[:3]

        sigma_array = []

        if ssystem == 0:
            for t in range(2 * radius + 1):
                sigma_t = get_sigma(position=t, length=2*radius+1, func=sigma_func_t)
                for y in range(block_size):
                    sigma_y = get_sigma(position=y, length=block_size, func=sigma_func_y)
                    for x in range(block_size // 2 + 1):
                        sigma_x = get_sigma(position=x, length=block_size, func=sigma_func_x)

                        sigma = sigma_t * sigma_y * sigma_x
                        sigma_array.append(sigma)
        else:
            for t in range(2 * radius + 1):
                loc_t = get_location(position=t, length=2*radius+1)
                for y in range(block_size):
                    loc_y = get_location(position=y, length=block_size)
                    for x in range(block_size // 2 + 1):
                        loc_x = get_location(position=x, length=block_size)

                        ndim = 3 if radius > 0 else 2
                        location = math.sqrt((loc_t * loc_t + loc_y * loc_y + loc_x * loc_x) / ndim)
                        sigma = sigma_func_t(location)
                        sigma_array.append(sigma)

    window = get_window(
        radius=radius,
        block_size=block_size,
        block_step=block_step,
        spatial_window_mode=spatial_window_mode,
        temporal_window_mode=temporal_window_mode,
        spatial_beta=spatial_beta,
        temporal_beta=temporal_beta
    )

    wscale = math.fsum(w * w for w in window)

    if ftype < 2:
        if sigma_is_scalar:
            sigma_scalar *= wscale
        else:
            sigma_array = [s * wscale for s in sigma_array]
        sigma2 *= wscale

    pmin *= wscale
    pmax *= wscale

    if isinstance(backend, Backend.cuFFT):
        rdft = core.dfttest2_cuda.RDFT
    elif isinstance(backend, Backend.NVRTC):
        rdft = core.dfttest2_nvrtc.RDFT
    elif isinstance(backend, Backend.CPU):
        rdft = core.dfttest2_cpu.RDFT
    elif isinstance(backend, Backend.GCC):
        rdft = core.dfttest2_gcc.RDFT
    elif isinstance(backend, Backend.hipFFT):
        rdft = core.dfttest2_hip.RDFT
    elif isinstance(backend, Backend.HIPRTC):
        rdft = core.dfttest2_hiprtc.RDFT
    else:
        raise TypeError("unknown backend")

    if radius == 0:
        window_freq = rdft(
            data=[w * 255 for w in window],
            shape=(block_size, block_size)
        )
    else:
        window_freq = rdft(
            data=[w * 255 for w in window],
            shape=(2 * radius + 1, block_size, block_size)
        )

    if isinstance(backend, Backend.CPU):
        return core.dfttest2_cpu.DFTTest(
            clip,
            window=window,
            sigma=[sigma_scalar] * (2 * radius + 1) * block_size * (block_size // 2 + 1) if sigma_is_scalar else sigma_array,
            sigma2=sigma2,
            pmin=pmin,
            pmax=pmax,
            radius=radius,
            block_size=block_size,
            block_step=block_step,
            planes=planes,
            filter_type=filter_type,
            window_freq=window_freq,
            opt=backend.opt
        )
    elif isinstance(backend, Backend.GCC):
        return core.dfttest2_gcc.DFTTest(
            clip,
            window=window,
            sigma=[sigma_scalar] * (2 * radius + 1) * block_size * (block_size // 2 + 1) if sigma_is_scalar else sigma_array,
            sigma2=sigma2,
            pmin=pmin,
            pmax=pmax,
            radius=radius,
            block_size=block_size,
            block_step=block_step,
            planes=planes,
            filter_type=filter_type,
            window_freq=window_freq
        )

    if isinstance(backend, Backend.cuFFT):
        to_single = core.dfttest2_cuda.ToSingle
    elif isinstance(backend, Backend.NVRTC):
        to_single = core.dfttest2_nvrtc.ToSingle
    elif isinstance(backend, Backend.hipFFT):
        to_single = core.dfttest2_hip.ToSingle
    elif isinstance(backend, Backend.HIPRTC):
        to_single = core.dfttest2_hiprtc.ToSingle
    else:
        raise TypeError("unknown backend")

    kernel = Template(
    """
    #define FILTER_TYPE ${filter_type}
    #define ZERO_MEAN ${zero_mean}
    #define SIGMA_IS_SCALAR ${sigma_is_scalar}

    #if ZERO_MEAN
    __device__ static const float window_freq[] { ${window_freq} };
    #endif // ZERO_MEAN

    __device__ static const float window[] { ${window} };

    __device__
    static void filter(float2 & value, int x, int y, int t) {
    #if SIGMA_IS_SCALAR
        float sigma = static_cast<float>(${sigma});
    #else // SIGMA_IS_SCALAR
        __device__ static const float sigma_array[] { ${sigma} };
        float sigma = sigma_array[(t * BLOCK_SIZE + y) * (BLOCK_SIZE / 2 + 1) + x];
    #endif // SIGMA_IS_SCALAR
        [[maybe_unused]] float sigma2 = static_cast<float>(${sigma2});
        [[maybe_unused]] float pmin = static_cast<float>(${pmin});
        [[maybe_unused]] float pmax = static_cast<float>(${pmax});
        [[maybe_unused]] float multiplier {};

    #if FILTER_TYPE == 2
        value.x *= sigma;
        value.y *= sigma;
        return ;
    #endif

        float psd = value.x * value.x + value.y * value.y;

    #if FILTER_TYPE == 1
        if (psd < sigma) {
            value.x = 0.0f;
            value.y = 0.0f;
        }
        return ;
    #elif FILTER_TYPE == 0
        multiplier = fmaxf((psd - sigma) / (psd + 1e-15f), 0.0f);
    #elif FILTER_TYPE == 3
        if (psd >= pmin && psd <= pmax) {
            multiplier = sigma;
        } else {
            multiplier = sigma2;
        }
    #elif FILTER_TYPE == 4
        multiplier = sigma * sqrtf(psd * (pmax / ((psd + pmin) * (psd + pmax) + 1e-15f)));
    #elif FILTER_TYPE == 5
        multiplier = powf(fmaxf((psd - sigma) / (psd + 1e-15f), 0.0f), pmin);
    #else
        multiplier = sqrtf(fmaxf((psd - sigma) / (psd + 1e-15f), 0.0f));
    #endif

        value.x *= multiplier;
        value.y *= multiplier;
    }
    """
    ).substitute(
        sigma_is_scalar=int(sigma_is_scalar),
        sigma=(
            to_single(sigma_scalar)
            if sigma_is_scalar
            else ','.join(str(to_single(x)) for x in sigma_array)
        ),
        sigma2=to_single(sigma2),
        pmin=to_single(pmin),
        pmax=to_single(pmax),
        filter_type=int(filter_type),
        window_freq=','.join(str(to_single(x)) for x in window_freq),
        zero_mean=int(zero_mean),
        window=','.join(str(to_single(x)) for x in window),
    )

    if isinstance(backend, Backend.cuFFT):
        return core.dfttest2_cuda.DFTTest(
            clip,
            kernel=kernel,
            radius=radius,
            block_size=block_size,
            block_step=block_step,
            planes=planes,
            in_place=backend.in_place,
            device_id=backend.device_id
        )
    elif isinstance(backend, Backend.NVRTC):
        return core.dfttest2_nvrtc.DFTTest(
            clip,
            kernel=kernel,
            radius=radius,
            block_size=block_size,
            block_step=block_step,
            planes=planes,
            in_place=False,
            device_id=backend.device_id,
            num_streams=backend.num_streams
        )
    if isinstance(backend, Backend.hipFFT):
        return core.dfttest2_hip.DFTTest(
            clip,
            kernel=kernel,
            radius=radius,
            block_size=block_size,
            block_step=block_step,
            planes=planes,
            in_place=backend.in_place,
            device_id=backend.device_id
        )
    elif isinstance(backend, Backend.HIPRTC):
        return core.dfttest2_hiprtc.DFTTest(
            clip,
            kernel=kernel,
            radius=radius,
            block_size=block_size,
            block_step=block_step,
            planes=planes,
            in_place=False,
            device_id=backend.device_id,
            num_streams=backend.num_streams
        )
    else:
        raise TypeError("unknown backend")


def select_backend(
    backend: typing.Optional[backendT],
    sbsize: int,
    tbsize: int
) -> backendT:

    if backend is not None:
        return backend

    if sbsize == 16 and tbsize in [1, 3, 5, 7]:
        if hasattr(core, "dfttest2_nvrtc"):
            return Backend.NVRTC()
        elif hasattr(core, "dfttest2_hiprtc"):
            return Backend.HIPRTC()
        elif hasattr(core, "dfttest2_cuda"):
            return Backend.cuFFT()
        elif hasattr(core, "dfttest2_hip"):
            return Backend.hipFFT()
        elif hasattr(core, "dfttest2_cpu"):
            return Backend.CPU()
        else:
            return Backend.GCC()
    else:
        if hasattr(core, "dfttest2_cuda"):
            return Backend.cuFFT()
        else:
            return Backend.hipFFT()


FREQ = float
SIGMA = float
def flatten(
    data: typing.Optional[typing.Union[
        typing.Sequence[typing.Tuple[FREQ, SIGMA]],
        typing.Sequence[float]
    ]]
) -> typing.Optional[typing.List[float]]:

    import itertools as it
    import numbers

    if data is None:
        return None
    elif isinstance(data[0], numbers.Real):
        return data
    else:
        data = typing.cast(typing.Sequence[typing.Tuple[FREQ, SIGMA]], data)
        return list(it.chain.from_iterable(data))


def to_func(
    data: typing.Optional[typing.Sequence[float]],
    norm: typing.Callable[[float], float],
    sigma: float
) -> typing.Callable[[float], float]:

    if data is None:
        return lambda _: norm(sigma)

    locations = data[::2]
    sigmas = data[1::2]
    packs = list(zip(locations, sigmas))
    packs = sorted(packs, key=lambda group: group[0])

    def func(x: float) -> float:
        length = len(packs)
        for i in range(length - 1):
            if x <= packs[i + 1][0]:
                weight = (x - packs[i][0]) / (packs[i + 1][0] - packs[i][0])
                return (1 - weight) * norm(packs[i][1]) + weight * norm(packs[i + 1][1])
        raise ValueError()

    return func


def DFTTest(
    clip: vs.VideoNode,
    ftype: typing.Literal[0, 1, 2, 3, 4] = 0,
    sigma: float = 8.0,
    sigma2: float = 8.0,
    pmin: float = 0.0,
    pmax: float = 500.0,
    sbsize: int = 16,
    smode: typing.Literal[0, 1] = 1,
    sosize: int = 12,
    tbsize: int = 3,
    # tmode=0, tosize=0
    swin: typing.Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] = 0,
    twin: typing.Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] = 7,
    sbeta: float = 2.5,
    tbeta: float = 2.5,
    zmean: bool = True,
    f0beta: float = 1.0,
    nlocation: typing.Optional[typing.Sequence[int]] = None,
    alpha: typing.Optional[float] = None,
    slocation: typing.Optional[typing.Union[
        typing.Sequence[typing.Tuple[FREQ, SIGMA]],
        typing.Sequence[float]
    ]] = None,
    ssx: typing.Optional[typing.Union[
        typing.Sequence[typing.Tuple[FREQ, SIGMA]],
        typing.Sequence[float]
    ]] = None,
    ssy: typing.Optional[typing.Union[
        typing.Sequence[typing.Tuple[FREQ, SIGMA]],
        typing.Sequence[float]
    ]] = None,
    sst: typing.Optional[typing.Union[
        typing.Sequence[typing.Tuple[FREQ, SIGMA]],
        typing.Sequence[float]
    ]] = None,
    ssystem: typing.Literal[0, 1] = 0,
    planes: typing.Optional[typing.Union[int, typing.Sequence[int]]] = None,
    backend: typing.Optional[backendT] = None
) -> vs.VideoNode:
    """ 2D/3D frequency domain denoiser

    The interface is compatible with core.dfttest.DFTTest by HolyWu.

    Args:
        clip: Clip to process.

            Any format with either integer sample type of 8-16 bit depth
            or float sample type of 32 bit depth is supported.

        ftype: Controls the filter type.

            Possible settings are:
                0: generalized wiener filter
                    mult = max((psd - sigma) / psd, 0) ^ f0beta

                1: hard threshold
                    mult = psd < sigma ? 0.0 : 1.0

                2: multiplier
                    mult = sigma

                3: multiplier switched based on psd value
                    mult = (psd >= pmin && psd <= pmax) ? sigma : sigma2

                4: multiplier modified based on psd value and range
                    mult = sigma * sqrt((psd * pmax) / ((psd + pmin) * (psd + pmax)))

            The real and imaginary parts of each complex dft coefficient are multiplied
            by the corresponding 'mult' value.

            ** psd = magnitude squared = real*real + imag*imag

        sigma, sigma2: Value of sigma and sigma2.
            If using the slocation parameter then the sigma parameter is ignored.

        pmin, pmax: Used as described in the ftype parameter description.

        sbsize: Sets the length of the sides of the spatial window.
            Must be 1 or greater. Must be odd if using smode=0.

        smode: Sets the mode for spatial operation.
            Currently only tmode=1 is implemented.

        sosize: Sets the spatial overlap amount.
            Must be in the range 0 to sbsize-1 (inclusive).
            If sosize is greater than sbsize>>1, then sbsize%(sbsize-sosize) must equal 0.
            In other words, overlap greater than 50% requires that sbsize-sosize be a divisor of sbsize.

        tbsize: Sets the length of the temporal dimension (i.e. number of frames).
            Must be at least 1. Must be odd if using tmode=0.

        tmode: Sets the mode for temporal operation.
            Currently only tmode=0 is implemented.

        tosize: Sets the temporal overlap amount.
            Must be in the range 0 to tbsize-1 (inclusive).
            If tosize is greater than tbsize>>1, then tbsize%(tbsize-tosize) must equal 0.
            In other words, overlap greater than 50% requires that tbsize-tosize be a divisor of tbsize.

        swin, twin: Sets the type of analysis/synthesis window to be used for spatial (swin) and
            temporal (twin) processing. Possible settings:

            0: hanning
            1: hamming
            2: blackman
            3: 4 term blackman-harris
            4: kaiser-bessel
            5: 7 term blackman-harris
            6: flat top
            7: rectangular
            8: Bartlett
            9: Bartlett-Hann
            10: Nuttall
            11: Blackman-Nuttall

        sbeta,tbeta: Sets the beta value for kaiser-bessel window type.
            sbeta goes with swin, tbeta goes with twin.
            Not used unless the corresponding window value is set to 4.

        zmean: Controls whether the window mean is subtracted out (zero'd)
            prior to filtering in the frequency domain.

        f0beta: Power term in ftype=0.

        nlocation: Currently not implemented.

        slocation/ssx/ssy/sst: Used to specify functions of sigma based on frequency.
            Check the original documentation for details.

            Note that in current implementation,
            "slocation = [(0.0, 1.0), (1.0, 10.0)]"
            is equivalent to
            "slocation = [0.0, 1.0, 1.0, 10.0]"

        ssystem: Method of sigma computation.
            Check the original documentation for details.

        planes: Sets which planes will be processed.
            Any unprocessed planes will be simply copied.

        backend: Backend implementation to use.
            All available backends can be found in the dfttest2.Backend "namespace":
                dfttest2.Backend.{CPU, cuFFT, NVRTC, GCC, hipFFT, HIPRTC}

            The CPU, NVRTC and GCC backends require sbsize=16.
            The cuFFT and NVRTC backends require a CUDA-enabled system.
            The hipFFT and HIPRTC backends require a CUDA-enabled system.

            Speed: NVRTC == HIPRTC >> cuFFT > hipFFT > CPU == GCC
    """

    if (
        not isinstance(clip, vs.VideoNode) or
        clip.width == 0 or
        clip.height == 0 or
        clip.format is None or
        (clip.format.sample_type == vs.INTEGER and clip.format.bits_per_sample > 16) or
        (clip.format.sample_type == vs.FLOAT and clip.format.bits_per_sample != 32)
    ):
        raise ValueError("only constant format 8-16 bit integer and 32 bit float input supported")

    if ftype < 0 or ftype > 4:
        raise ValueError("ftype must be 0, 1, 2, 3, or 4")

    if sbsize < 1:
        raise ValueError("sbsize must be greater than or equal to 1")

    if smode != 1:
        raise ValueError('"smode" must be 1')

    if sosize > sbsize // 2 and (sbsize % (sbsize - sosize) != 0):
        raise ValueError("spatial overlap greater than 50% requires that sbsize-sosize is a divisor of sbsize")

    if tbsize < 1:
        raise ValueError('"tbsize" must be at least 1')

    if swin < 0 or swin > 11:
        raise ValueError("swin must be between 0 and 11 (inclusive)")

    if twin < 0 or twin > 11:
        raise ValueError("twin must be between 0 and 11 (inclusive)")

    if nlocation is not None:
        raise ValueError('"nlocation" must be None')

    if slocation and len(slocation) % 2 != 0:
        raise ValueError("number of elements in slocation must be a multiple of 2")

    if ssx and len(ssx) % 2 != 0:
        raise ValueError("number of elements in ssx must be a multiple of 2")

    if ssy and len(ssy) % 2 != 0:
        raise ValueError("number of elements in ssy must be a multiple of 2")

    if sst and len(sst) % 2 != 0:
        raise ValueError("number of elements in sst must be a multiple of 2")

    if ssystem < 0 or ssystem > 1:
        raise ValueError("ssystem must be 0 or 1")

    def norm(x: float) -> float:
        if slocation is not None and ssystem == 1:
            return x
        elif tbsize == 1:
            return math.sqrt(x)
        else:
            return x ** (1 / 3)

    _sigma: typing.Union[float, typing.Sequence[typing.Callable[[float], float]]]

    if slocation is not None:
        _sigma = [to_func(flatten(slocation), norm, sigma)] * 3
    elif any(ss is not None for ss in (ssx, ssy, sst)):
        _sigma = [to_func(flatten(ss), norm, sigma) for ss in (ssx, ssy, sst)]
    else:
        _sigma = sigma

    return DFTTest2(
        clip = clip,
        ftype = ftype,
        sigma = _sigma,
        sigma2 = sigma2,
        pmin = pmin,
        pmax = pmax,
        sbsize = sbsize,
        sosize = sosize,
        tbsize = tbsize,
        swin = swin,
        twin = twin,
        sbeta = sbeta,
        tbeta = tbeta,
        zmean = zmean,
        f0beta = f0beta,
        ssystem = ssystem,
        planes = planes,
        backend = select_backend(backend, sbsize, tbsize)
    )
