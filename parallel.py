#!/usr/bin/env python3

import os
import sys
import multiprocessing
import concurrent.futures
import subprocess

def execute_command(command):
    # Execute the command using subprocess
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Wait for the process to complete and capture the output
    stdout, stderr = process.communicate()
    # Print the output
    print(f"Command '{command}' executed with output:")
    print(stdout.decode())
    # Print any errors
    if stderr:
        print(stderr.decode())

def main(file_path, max_workers):
    # Read commands from the file
    with open(file_path, 'r') as file:
        commands = file.read().splitlines()

    # Use ThreadPoolExecutor to execute commands in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit each command to the executor
        futures = [executor.submit(execute_command, command) for command in commands]

        # Wait for all commands to complete
        for future in concurrent.futures.as_completed(futures):
            future.result()  # This will raise any exception occurred during execution

def get_cpu_cores():
    return multiprocessing.cpu_count()

if __name__ == "__main__":
    dname = sys.argv[1]
    if not os.path.exists(dname):
        print("Error: arg1 not path")
    else:
        fnames = os.listdir(dname)
        for fname in fnames:
            if not fname.endswith('.nsf')
                continue
            bname = os.path.basename(fname)
            songs = 

        file_path = 'commands.txt'
        num_cores = get_cpu_cores()
        print("Number of CPU cores:", num_cores)
        max_workers = num_cores
        main(file_path, max_workers)
