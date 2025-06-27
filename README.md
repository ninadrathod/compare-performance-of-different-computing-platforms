# Linux Kernel Compilation Performance Benchmarking

## Problem Description

Compare the performance of different computing platforms when compiling the Linux kernel source code. Performance will be evaluated based on the following metrics:

* **Time taken to complete the kernel compilation task:** Measures the total duration of the compilation process.
* **Average CPU usage of the compilation process:** Tracks the average percentage of CPU utilized during compilation.
* **Average memory usage of the compilation process:** Monitors the average percentage of memory consumed during compilation.

## What Does This Program Do?

This program is designed to automate and measure the performance of Linux kernel compilation. Specifically, it performs the following tasks:

1.  **Download and Extract Linux Kernel Source Code:** It checks for the presence of the Linux kernel source code. If not found, it downloads the source to a dedicated `/zip` directory, then copies and extracts it to the present working directory.
2.  **Compile the Linux Kernel Source Code:** It initiates the kernel compilation process.
3.  **Clean Up Generated Data:** After compilation, it removes the files generated during the process to ensure a clean state for subsequent runs.

The script evaluates the system's performance for the compilation process in terms of CPU utilization, memory utilization, and runtime. The entire process can be repeated multiple times based on user input, and the user also has to specify the number of processors to be engaged in the compilation.

## How This Program Works (Logic)

The program follows a structured approach as outlined below:

1.  **User Input:** The program first prompts the user to enter:
    * The number of iterations to run the experiment.
    * The number of processors to be used for compilation.

2.  **Source Code Management:**
    * It checks for the Linux kernel source code within the `/zip` directory of the current working directory.
    * If the source code is not found, it downloads it into the `/zip` directory, then copies it to the present working directory and extracts it.

3.  **Parallel Execution and Monitoring:**
    * The current timestamp is recorded as the `start_time`.
    * Two parallel processes are then initiated:
        * **Process-1:** Executes the kernel compilation command.
        * **Process-2:** Monitors and captures system-wide memory and CPU utilization at regular intervals (every 5 minutes) while Process-1 is running.
    * Once Process-1 (compilation) completes, Process-2 is terminated.
    * The `end_time` is recorded to calculate the total runtime of the compilation process.

4.  **Performance Aggregation:**
    * All the CPU and memory utilization readings logged during the compilation process by Process-2 are averaged to obtain the aggregate CPU and Memory utilization percentages for that particular run.

5.  **Cleanup:**
    * The files generated during the compilation process are deleted as part of a clean-up operation to ensure a fresh environment for subsequent iterations.

These five steps are repeated for the number of iterations specified by the user. The results of each experiment run (runtime, average CPU usage, average memory usage) are appended to a file named `perf.txt` in the present working directory.

## How to Compile and Run This Program

Before running the program, several dependency packages and commands need to be installed.

---

## How to Compile and Run This Program

Before running the program, you'll need to install several dependency packages and commands.

**1. Install Dependencies:**

Open your terminal and execute the following commands:

```bash
$ sudo apt-get update$ sudo apt-get install python3
$ sudo apt-get install build-essential libncurses-dev bison flex libssl-dev libelf-dev sysstat bc
$ sudo apt-get install wget
$ sudo apt-get install pip
$ pip install psutil
```

NOTE: Make sure that no other applications are running on the system while running the
experiment.

**2. Running the script:**
To run the program:
1. Place the pyScript.py file and config file at any directory location. Rename the config file to .config.
2. Open the terminal from the present working directory.
3. Run the program using the command: $python3 pyScript.py
4. Enter the number of processors.
5. Enter the number of iterations.
