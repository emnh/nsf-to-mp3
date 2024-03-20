#!/usr/bin/env python3

from pydub import AudioSegment
import random
import os
import multiprocessing
import concurrent.futures
import subprocess
import concurrent.futures

def chunk_random_segment(args):
    i, opus_file, segment_length, speed_factor, temp_file = args
    # Convert Opus file to WAV
    temp_audio_file = "temp_audio_" + str(i) + ".wav"
    if os.path.exists(temp_audio_file):
        os.remove(temp_audio_file)
    atempo = f'"atempo={speed_factor}"'
    cmd = f"ffmpeg -i {opus_file} -filter:a {atempo} {temp_audio_file}"
    print("CMD", cmd)
    os.system(cmd)

    # Load the WAV file
    audio = AudioSegment.from_file(temp_audio_file, format="wav")

    # Calculate the maximum start time to ensure the segment doesn't go beyond the audio length
    segment_length = min(segment_length, len(audio))
    max_start_time = len(audio) - segment_length

    # Generate a random start time within the valid range
    start_time = random.randint(0, max_start_time)

    # Extract the segment
    segment = audio[start_time:start_time + segment_length]
    #segment = segment.speedup(playback_speed=speed_factor)

    # Export the segment to a temporary file (you can skip this step if you prefer not to save the segment)
    #temp_file = "temp_segment.wav"
    segment.export(temp_file, format="mp3")

    # Use your system's default audio player to play the segment
    #os.system("mplayer " + temp_file)

    # Clean up temporary files
    os.remove(temp_audio_file)
    #os.remove(temp_file)

def my_function(argument):
    # Your function logic here
    return argument * argument

def pmap(func, args, num_processes):
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_processes) as executor:
        results = list(executor.map(func, args))
    return results

def get_cpu_cores():
    return multiprocessing.cpu_count()

def main():
    # Example usage
    outdir = 'out_chunks_2'
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    infnames = os.listdir()
    fnames = []
    for i in range(20):
        random.shuffle(infnames)
        fnames.extend(infnames)
    i = 0
    num_cores = get_cpu_cores()
    print("Number of CPU cores:", num_cores)
    num_processes = num_cores
    max_workers = num_cores
    arguments = []
    for fname in fnames:
        if fname.endswith('.opus'):
            length = random.randrange(10000, 30000) # random.uniform(0.75, 4.25) * 1000
            speed_factor = random.randrange(1000, 2000) / 1000 # random.uniform(0.75, 4.25) * 1000
            title = os.path.splitext(fname)[0]
            it = (i, fname, length, speed_factor, os.path.join(outdir, str(i) + '_' + title + '.mp3'))
            i += 1
            arguments.append(it)
    results = pmap(chunk_random_segment, arguments, num_processes)

main()
