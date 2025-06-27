import os
import time
import shutil
import multiprocessing
import psutil

# return the time in hours, minutes and seconds format. Input in seconds

def hms(var):
    hrs = int((var - var%3600)/3600)
    mnt = int(((var%3600) - (var%3600)%60)/60)
    sec = int((var%3600)%60)
    return hrs,mnt,sec




# Function logger() would store the cpu utilization and memory utilization 
# into files cpu.txt and mem.txt respectively at an interval of 5 minutes. 

def logger():

    while(1):
        os.system("free | grep Mem >> mem.txt")
        reading = psutil.cpu_percent(interval=2)
        cmd = "echo '"+str(reading)+"' >> cpu.txt"
        os.system(cmd)
        time.sleep(300)




# runMake() function will trigger the compilation process on numProc processors

def runMake(numProc):
    loc = os.getcwd()
    os.chdir(loc+"/linux-5.19.3")
    print("\nRunning make command")
    command = "make -j "+str(numProc)
    os.system(command)
    print("\nFinished compilation")
    



# If the linux kernel is present inside the '/zip' directory: it is copied into
#       the present working directory
# Else: The directory '/zip' is created and the linux kernel is downloaded and copied
#       into the present working directory

def downloadKernel():
    zipDir = os.getcwd() + '/zip'
    target = os.getcwd()
    if(os.path.exists(zipDir)):
        # If the .zip file is already downloaded
        print("ZIP already present\n")
    else:
        # Need to donwload the zip and place it in /zip folder
        print("ZIP file not present. Downloading ...\n")
        os.mkdir(zipDir)
        os.chdir(zipDir)
        os.system("wget https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.19.3.tar.xz")
        print("Download Completed\n")
        os.chdir(target)
    shutil.copy(zipDir+"/linux-5.19.3.tar.xz",target+"/linux-5.19.3.tar.xz")




# utilization() command will calculate the aggregate CPU and Memory Utilization
# for single iteration of the experiment

def utilization():

    memptr = open("mem.txt","r")
    mlines = memptr.readlines()
    memptr.close()

    cpuptr = open("cpu.txt","r")
    clines = cpuptr.readlines()
    cpuptr.close()

    # ------- finding avg memory utilization ---------------

    total_readings = len(mlines)
    total_mem_used = 0

    for itm in mlines:
        temp = " ".join(itm.split()).split(" ")
        total_mem_used += int(temp[2])

    avg_mem_utilization  = total_mem_used/total_readings
    mem_utilization_perc = (avg_mem_utilization/total_RAM_available) * 100
    
    # ------- finding avg cpu utilization -------------------
    
    total_readings = len(clines)
    total_cpu_used = 0

    for itm in clines:
        temp = " ".join(itm.split()).split(" ")
        total_cpu_used += float(temp[0])

    avg_cpu_utilization = total_cpu_used/total_readings
    
    fname = open("perf.txt","a")
    print("average cpu utilization : ",avg_cpu_utilization," %\n")
    fname.write("average cpu utilization : "+str(avg_cpu_utilization)+" %\n")
    print("average mem utilization : ",mem_utilization_perc," %\n------------\n")
    fname.write("average mem utilization : "+str(mem_utilization_perc)+" %\n------------\n")
    fname.close()




# The run() function will run our experiment: donwload the linux kernel (if needed), perform the
# compilation and clean-up all the generated file, once the compilation process is completed.

#                         *** PARAMETERS ***

# numProc       : number of processors you wish to assign for the compilation task
# numIterations : number of times you wish to repeat the experiment

def run(numProc,numIterations):
    
    for i in range(numIterations):

        # Download the kernel

        downloadKernel()

        # tar.xz --> .tar --> extracting the .tar file

        print("\n.tar.xz to .tar")
        os.system("unxz -v linux-5.19.3.tar.xz")
        print("\nExtracting .tar file")
        os.system("tar xvf linux-5.19.3.tar")
        print("\nExtraction completed")

        # moving .config to extracted folder

        print("\n\ncopying .config file to linux-5.19.3 directory")
        os.system("cp .config linux-5.19.3")

        # changing directory

        loc = os.getcwd()
        
        # running the make command

        # -------------------------------------------------
        # create two independent processes:
        # 1. To trigger the make command
        # 2. To track the cpu and memory utilization
        # -------------------------------------------------

        make = multiprocessing.Process(target=runMake,args=(numProc,))
        log = multiprocessing.Process(target=logger)
        
        start_time = time.time()
        make.start()
        log.start()

        make.join()
        end_time = time.time()
        log.terminate()
        log.join()

        print("make process is alive: {}".format(make.is_alive()))
        print("log  process is alive: {}".format(log.is_alive()))

        # -------------------------------------------------
        # Wait for the process 1 (make commnad) to finish
        # Terminate the process 2 (which tracks memory and
        #                          cpu utilization)
        # -------------------------------------------------

        # Displaying and storing the performance

        hrs,mnt,sec = hms(end_time-start_time)

        fname = open("perf.txt","a")
        fname.write("Time taken for the compilation process:"+str(hrs)+":"+str(mnt)+":"+str(sec)+"\n")
        fname.close()
        print("Time taken for the compilation process:",hrs,":",mnt,":",sec,"\n")
        utilization()

        # Clean-up
        
        print("\n\nStarting cleanup")
        os.chdir(loc+"/linux-5.19.3")
        os.system("make clean")
        os.system("make distclean")

        # Coming outside the directory and deleting the linux directory

        os.chdir(loc)
        shutil.rmtree(loc+"/linux-5.19.3")
        os.remove(loc+"/mem.txt")
        os.remove(loc+"/cpu.txt")
        os.remove(loc+"/linux-5.19.3.tar")
        print("\n\nClean-up completed")



# * * * * * * * * * * * * * * * * * * * CODE BEGINS * * * * * * * * * * * * * * * * * * * * * * * * 


print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
print("*                                                                                     *")
print("*   This script is designed to perform the following set of tasks:                    *")
print("*   1. Download (if not already downloaded) and extract the linux kernel source code. *")
print("*   2. Compile the linux kernel source code.                                          *")
print("*   3. Cleaning up the generated data once the compilation is completed.              *")
print("*   The script will evaluate performance of the system for the compilation process    *")
print("*   in terms of: CPU utilization percentage, Memory utilization percentage and        *")
print("*   runtime.                                                                          *")
print("*                                                                                     *")
print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *\n")

cpuCount = os.cpu_count()
numProc = int(input("Enter number of processors you want to utilize for the experiment (between 1 and "+str(cpuCount-1)+"): "))

while(numProc > cpuCount-1 or numProc < 1):
    numProc = int(input("Invalid input. Please give input in the defined range: "))
    

numIterations = int(input("\nEnter number of iterations for the experiment (between 1 and 10): "))

while(numIterations > 10 or numIterations < 1):
    numIterations = int(input("Invalid input. Please give input in the defined range: "))



initial_cpu_utilization = psutil.cpu_percent(interval=5)    
print("Initial CPU utilization: ",initial_cpu_utilization)

os.system("free | grep Mem > temp.txt")
fptr = open("temp.txt","r")
init = fptr.readlines()
fptr.close()
temp = " ".join(init[0].split()).split(" ")
total_RAM_available     = int(temp[1])               
loc = os.getcwd()
os.remove(loc+"/temp.txt")
print("Total RAM Available: ",total_RAM_available," MB")

run(numProc,numIterations)
