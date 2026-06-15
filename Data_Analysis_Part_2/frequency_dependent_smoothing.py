import numpy as np
from typing import Optional, Tuple, Union

def asd2(time_series: np.ndarray, ts: float, n_ave: int = 1) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute the Amplitude Spectral Density (ASD) of a time series.

    Parameters
    ----------
    time_series : np.ndarray
        Input time series (1D array).
    ts : float
        Time step (seconds).
    n_ave : int
        Number of averages (non-overlapping segments). Default is 1.

    Returns
    -------
    asd : np.ndarray
        Amplitude spectral density.
    f : np.ndarray
        Frequency vector (Hz), starting from 0.
    """
    n = len(time_series)
    seg_len = n // n_ave

    psds = []
    for i in range(n_ave):
        segment = time_series[i * seg_len:(i + 1) * seg_len]
        window = np.hanning(seg_len)
        # Correct for window power loss
        scale = np.sqrt(2 / (np.sum(window ** 2) / seg_len))
        fft_vals = np.fft.rfft(segment * window) / seg_len
        psd = (np.abs(fft_vals) * scale) ** 2
        psds.append(psd)

    mean_psd = np.mean(psds, axis=0)
    asd = np.sqrt(mean_psd)

    f = np.fft.rfftfreq(seg_len, d=ts)
    return asd, f

def asd_smooth(
    time_series_in: np.ndarray,
    ts: Union[float, np.ndarray],
    log_step: Optional[int] = None,
    n_ave: Optional[int] = None,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute a log-smoothed Amplitude Spectral Density (ASD).

    Produces spectra that are smooth across the full frequency range by
    stitching together sections with increasing frequency-domain averaging.
    This avoids the jaggedness of standard linear-frequency ASDs at high
    frequencies while retaining ASD2-style frequency-domain averaging.

    Parameters
    ----------
    time_series_in : np.ndarray
        Input time series (1D), OR an existing ASD vector when `ts` is also
        a vector (frequency domain mode).
    ts : float or np.ndarray
        If a scalar: the time step (seconds) of the time series.
        If a 1D array: treated as the frequency vector corresponding to
        `time_series_in` (which is then interpreted as an ASD).
    log_step : int, optional
        The multiplicative frequency factor at which to increase the number
        of averages. Default is 9 (time-series input) or 8 (ASD input).
    n_ave : int, optional
        The factor by which averaging increases at each step.
        Should be a positive odd integer. Default is 3 (time-series) or 2 (ASD).

    Returns
    -------
    asd_out : np.ndarray
        Smoothed ASD values.
    f_out : np.ndarray
        Corresponding frequency vector.

    Notes
    -----
    When passing an existing ASD, the input frequency vector must be linear
    and start from zero. The output will be truncated to avoid partially
    filling the final bin.

    Examples
    --------
    Time-series input:
        asd_out, f_out = asd_smooth(my_signal, dt)

    ASD input (recommended log_step=8, n_ave=2):
        asd_out, f_out = asd_smooth(my_asd, my_freq, log_step=8, n_ave=2)
    """
    time_series_in = np.asarray(time_series_in, dtype=float).squeeze()
    if time_series_in.ndim != 1:
        raise ValueError("Input time series / ASD must be a 1D array.")

    input_was_column = time_series_in.shape == (len(time_series_in),)  # always True for 1D

    ts = np.asarray(ts, dtype=float)

    # --- Determine input mode ---
    if ts.ndim >= 1 and ts.size > 1:
        # Frequency-domain mode
        import warnings
        warnings.warn(
            "\n Both inputs are arrays and asd_smooth will now\n"
            " treat the inputs as an ASD and frequency vector\n"
            " and perform RMS averaging over neighbouring bins.\n\n"
            " If you intended to take the spectrum of a time-series\n"
            " please ensure the second input is a scalar.\n",
            UserWarning,
            stacklevel=2,
        )
        f_in = ts.squeeze()
        asd_in = time_series_in

        if f_in.shape != asd_in.shape:
            raise ValueError("Frequency and ASD vectors must be the same size.")

        if log_step is None:
            log_step = 8
        if n_ave is None:
            n_ave = 2

    else:
        # Time-domain mode: compute ASD with no averaging first
        asd_in, f_in = asd2(time_series_in, float(ts), n_ave=1)

        if log_step is None:
            log_step = 9
        if n_ave is None:
            n_ave = 3

    # --- Validate frequency vector ---
    df = f_in[1] - f_in[0]
    diffs = np.diff(f_in)
    if not np.allclose(diffs, df, rtol=1e-4):
        raise ValueError("asd_smooth only works with linear frequency vectors.")
    if not np.isclose(f_in[0], 0.0) and not np.isclose(f_in[0], df):
        raise ValueError("Frequency vector should start from zero.")

    if log_step <= n_ave:
        n_ave = log_step - 1
        import warnings
        warnings.warn(
            f"n_ave should be less than log_step. Setting n_ave = log_step - 1 = {n_ave}",
            UserWarning,
            stacklevel=2,
        )

    # --- Break spectrum into chunks ---
    y = (log_step // n_ave) * n_ave

    # Number of sections (from MATLAB derivation via Wolfram Alpha)
    m = len(f_in) * (y - 1) / y + 1
    z = np.log(m) / np.log(y)
    n_stitch = int(np.ceil(z))

    n_vec = np.arange(1, n_stitch + 1)
    n_pts = y ** n_vec[:n_stitch - 1]          # Points in all fully-filled chunks
    n_fin = len(f_in) - int(np.sum(n_pts))     # Remaining points for final chunk
    n_sec_fin = int(n_fin // n_ave ** (n_stitch - 1))
    n_pts = np.append(n_pts, n_sec_fin * n_ave ** (n_stitch - 1))
    n_pts = n_pts.astype(int)

    n_sec = n_pts / n_ave ** (n_vec - 1)       # Number of smooth-sections per chunk
    n_sec = n_sec.astype(int)

    # Truncate data
    total_pts = int(np.sum(n_pts))
    f_in = f_in[:total_pts]
    asd_in = asd_in[:total_pts]

    # Chunk start / end indices
    b1 = np.concatenate(([0], np.cumsum(n_pts[:-1])))
    b2 = np.cumsum(n_pts)

    # --- Build output ---
    asd_out = []
    f_out = []

    for k in range(n_stitch):
        width = int(n_ave ** k)
        sec = int(n_sec[k])

        f_chunk = f_in[b1[k]:b2[k]].reshape(width, sec, order='F')
        asd_chunk = asd_in[b1[k]:b2[k]].reshape(width, sec, order='F') ** 2

        f_out.append(np.mean(f_chunk, axis=0))
        asd_out.append(np.sqrt(np.mean(asd_chunk, axis=0)))

    f_out = np.concatenate(f_out)
    asd_out = np.concatenate(asd_out)

    return asd_out, f_out

# ---------------------------------------------------------------------------
# Quick demo / sanity check
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(42)
    fs = 4096          # Hz
    duration = 60      # seconds
    ts = 1.0 / fs

    t = np.arange(0, duration, ts)
    # White noise + a small sine tone at 100 Hz
    signal = rng.standard_normal(len(t)) + 0.5 * np.sin(2 * np.pi * 100 * t)

    asd_out, f_out = asd_smooth(signal, ts)

    plt.figure(figsize=(10, 5))
    plt.semilogy(f_out, asd_out)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("ASD (1/√Hz)")
    plt.title("asd_smooth demo")
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig("/mnt/user-data/outputs/asd_smooth_demo.png", dpi=150)
    plt.show()
    print("Done. Output saved to asd_smooth_demo.png")