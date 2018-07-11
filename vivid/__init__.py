from vivid.sound import PygameBackend
import time

from matplotlib import pyplot as plt
import numpy as np
from scipy.signal import stft
from scipy.stats import zscore
from scipy.interpolate import interp1d

import peakutils


# adapted from http://scipy-cookbook.readthedocs.io/items/SignalSmooth.html
def smooth(signal, window_length):
    signal_windows = np.r_[signal[window_length-1::-1], signal, signal[0:window_length-1]]
    window = np.hamming(window_length)
    return np.convolve(window / window.sum(), signal_windows, mode='valid')[(window_length//2):-(window_length//2+window_length%2)]


def flatten(x, factor):
    x = x.copy()
    x -= np.min(x)
    x **= factor
    x /= np.max(x)
    return x


SAMPLING_FREQ = 44100
STFT_SEG_LEN = 2048
SMOOTHING_LEN = 5  # in seconds

LOW_FREQUENCY = 20
HIGH_FREQUENCY = 15000

NUM_LEDS = 30


file = "audio/test.wav"

backend = PygameBackend()
backend.init(SAMPLING_FREQ)

data = backend.load_sound(file)[:,0]
freqs, times, Z = stft(data, SAMPLING_FREQ, nperseg=STFT_SEG_LEN)
volumes = np.abs(Z)

log_freqs = np.log(freqs)

normalized_volumes = zscore(volumes, axis=1)

saturations = normalized_volumes.sum(axis=0)
smoothed_saturations = smooth(saturations, SMOOTHING_LEN * SAMPLING_FREQ * 2 // STFT_SEG_LEN)


freq_perc = np.exp(np.linspace(np.log(LOW_FREQUENCY), np.log(HIGH_FREQUENCY), freqs.size))
volumes_perc = interp1d(log_freqs[1:], volumes[1:, :], fill_value='extrapolate', kind='quadratic', axis=0)(np.log(freq_perc))
normalized_volumes_perc = zscore(volumes_perc, axis=1)
saturations_perc = normalized_volumes_perc.sum(axis=0)
smoothed_saturations_perc = smooth(saturations_perc, SMOOTHING_LEN * SAMPLING_FREQ * 2 // STFT_SEG_LEN)

indexes = peakutils.indexes(smooth(np.gradient(smoothed_saturations_perc), SMOOTHING_LEN * 10 * SAMPLING_FREQ * 2 // STFT_SEG_LEN), min_dist=100)




# plt.pcolormesh(t, f, np.abs(Zxx), vmin=0, vmax=100)
# plt.title('STFT Magnitude')
# plt.ylabel('Frequency [Hz]')
# plt.xlabel('Time [sec]')
# plt.show()

# backend.play_sound(file)

# while True:
#     print(backend.get_position())
#     time.sleep(.1)