import parselmouth

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

base_line_color =  'white'
line_color = 'black'
tone_choice = 'G'

class Tonality:
    base_diff = [0, 2, 4, 5, 7, 9, 11]
    tones = ['A', 'A#', 'B','C','C#','D','D#','E','F','F#','G','G#']
    def __init__(self, tone):
        assert tone in self. tones
        self.base_freq = self.tone_to_freq(tone)

    def tone_to_freq(self, tone):
        A_freq = 440
        return A_freq * (2 ** (self. tones. index(tone) / 12))

    def get_freq(self) :
        ret = []
        for r in range (0, 2):
            base = self.base_freq * (2 ** r)
            ret.extend ([base * (2 ** (diff / 12)) for diff in self.base_diff])
        return ret
    
    def get_base(self) :
        ret = []
        for r in range (0,2):
            base = self.base_freq * (2 ** r)
            ret.append(base)
        return ret

def draw_pitch(pitch):
    # Extract selected pitch contour, and
    # replace unvoiced samples by NaN to not plot
    pitch_values = pitch.selected_array['frequency']
    pitch_values[pitch_values==0] = np.nan
    plt.plot(pitch.xs(), pitch_values, 'o', markersize=5, color='w')
    plt.plot(pitch.xs(), pitch_values, 'o', markersize=2)
    plt.grid(False)
    plt.ylim(0, pitch.ceiling)
    plt.ylabel("fundamental frequency [Hz]")

def draw_spectrogram(spectrogram, dynamic_range=70):
    X, Y = spectrogram.x_grid(), spectrogram.y_grid()
    sg_db = 10 * np.log10(spectrogram.values)
    plt.pcolormesh(X, Y, sg_db, vmin=sg_db.max() - dynamic_range, cmap='afmhot')
    plt.ylim([spectrogram.ymin, spectrogram.ymax])
    plt.xlabel("time [s]")
    plt.ylabel("frequency [Hz]")

def draw_standard(tone):
    for f in Tonality(tone).get_freq():
        plt.axline((0, f), (1, f),color=line_color, lw=2)
    for f in Tonality(tone).get_base():
        plt.axline((0, f), (1, f),color=base_line_color, lw=3)

sns.set() # Use seaborn's default style to make attractive graphs

# Plot nice figures using Python's "standard" matplotlib library
snd = parselmouth.Sound("/Users/shchy/Desktop/3.mp3")



pitch = snd.to_pitch()
# If desired, pre-emphasize the sound fragment before calculating the spectrogram
pre_emphasized_snd = snd.copy()
pre_emphasized_snd.pre_emphasize()
spectrogram = pre_emphasized_snd.to_spectrogram(window_length=0.03, maximum_frequency=3000)

plt.figure()
draw_spectrogram(spectrogram)
draw_standard(tone_choice)
#plt.twinx()
plt.xlim([snd.xmin, snd.xmax])
plt.show() # or 
plt.savefig("spectrogram_0.03.png")

