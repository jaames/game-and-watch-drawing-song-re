from sys import argv
import wave

# custom index table
indexTable = [
    -4, -3, -2, -1, 2, 4, 8, 16,
    -4, -3, -2, -1, 2, 4, 8, 16
]

# standard IMA-ADPCM step table
stepTable = [
    7, 8, 9, 10, 11, 12, 13, 14, 16, 17,
    19, 21, 23, 25, 28, 31, 34, 37, 41, 45,
    50, 55, 60, 66, 73, 80, 88, 97, 107, 118,
    130, 143, 157, 173, 190, 209, 230, 253, 279, 307,
    337, 371, 408, 449, 494, 544, 598, 658, 724, 796,
    876, 963, 1060, 1166, 1282, 1411, 1552, 1707, 1878, 2066,
    2272, 2499, 2749, 3024, 3327, 3660, 4026, 4428, 4871, 5358,
    5894, 6484, 7132, 7845, 8630, 9493, 10442, 11487, 12635, 13899,
    15289, 16818, 18500, 20350, 22385, 24623, 27086, 29794, 32767
]

predictor = 0
stepIndex = 40

# clamp between min and max
def saturate(n, min, max):
    if n < min: n = min
    if n > max: n = max
    return n

# decode ADPCM sample
def decodeSample(sample):
    global predictor, stepIndex

    step = stepTable[stepIndex]
    diff = step >> 3
    
    if sample & 1: diff += step >> 2
    if sample & 2: diff += step >> 1
    if sample & 4: diff += step
    if sample & 8: diff = -diff
    
    predictor += diff
    predictor = saturate(predictor, -32768, 32767)
    
    stepIndex += indexTable[sample]
    stepIndex = saturate(stepIndex, 0, 88)
    
    return predictor

# decode ADPCM buffer
def decodeBuffer(samples):
    out = bytearray()

    for i in range(len(samples)):
        s1 = decodeSample(samples[i] & 0xf)
        s2 = decodeSample(samples[i] >> 4)
    
        # 1st sample
        out.append(s1 & 0xff)
        out.append((s1 >> 8) & 0xff)
        # 1st sample again for nearest neighbour interpolation
        out.append(s1 & 0xff)
        out.append((s1 >> 8) & 0xff)
        # 2nd sample
        out.append(s2 & 0xff)
        out.append((s2 >> 8) & 0xff)
        # 2nd sample again for nearest neighbour interpolation
        out.append(s2 & 0xff)
        out.append((s2 >> 8) & 0xff)
    
    return out
    
with open(argv[1], 'rb') as flash, open(argv[2], 'wb') as outfile:
    flash.seek(0x2fa64)
    out = decodeBuffer(bytearray(flash.read(0x5a120)))
    
    # write output WAV
    wav = wave.open(outfile, 'wb')   
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(48000)
    wav.writeframes(out)
    wav.close()