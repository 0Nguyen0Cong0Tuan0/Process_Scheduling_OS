class Process:
    def __init__(self, name, arrival_time, cpu_burst, priority=None):
        self.name = name
        self.arrival_time = arrival_time
        self.cpu_burst = cpu_burst
        self.priority = priority
        self.remaining_time = cpu_burst
    
    def set_completion_time(self, completion_time):
        self.completion_time = completion_time

    def set_remaining_time_again(self):
        self.remaining_time = self.cpu_burst
    

processes_group = []

def load_processes_from_file(file_name):
    global num_processes
    global quantum_time

    with open(file_name, 'r') as file:
        num_processes, quantum_time= map(int, file.readline().split())

        for _ in range(num_processes):
            process_data = file.readline().split()

            if len(process_data) == 3:
                name, arrival_time, cpu_burst = process_data
                processes_group.append(Process(name, int(arrival_time), int(cpu_burst)))
            elif len(process_data) == 4:
                name, arrival_time, cpu_burst, priority = process_data
                processes_group.append(Process(name, int(arrival_time), int(cpu_burst),  int(priority)))

def calculate_waiting_time(completion_time):
    waiting_time = [0] * num_processes

    for i in range(num_processes):
        waiting_time[i] = completion_time[i] - processes_group[i].arrival_time - processes_group[i].cpu_burst

    return waiting_time

def calculate_turnaround_time(completion_time):
    turnaround_time = [0] * num_processes

    for i in range(num_processes):
        turnaround_time[i] =  completion_time[i] - processes_group[i].arrival_time

    return turnaround_time

def calculate_total_cpu_burst():
    total_cpu_burst = 0

    for process in range(num_processes):
        total_cpu_burst += processes_group[process].cpu_burst
    
    return total_cpu_burst

def check_load_process(current_time):
    for process in processes_group:
        if process.arrival_time <= current_time:
            return True
    return False

def FCFS():
    processes_group.sort(key=lambda x: x.arrival_time) # sort arrival_time for all processes

    scheduling = []

    start_time_of_process = 0
    end_time_of_process = 0

    for i in range(num_processes):
        start_time_of_process = max(end_time_of_process, processes_group[i].arrival_time)
        end_time_of_process = start_time_of_process + processes_group[i].cpu_burst

        scheduling.append((start_time_of_process, processes_group[i].name, end_time_of_process))
        
        processes_group[i].set_completion_time(end_time_of_process)

    waiting_time = calculate_waiting_time([process.completion_time for process in processes_group])
    turnaround_time = calculate_turnaround_time([process.completion_time for process in processes_group])

    # write_output("FCFS.txt", scheduling, processes_group, turnaround_time, waiting_time)

def RR():
    processes_group.sort(key=lambda x: x.arrival_time) # sort arrival_time for all processes

    scheduling = []
    remaining_processes = []

    num_processes_loaded = 0

    start_quantum_time_of_process = 0
    end_quantum_time_of_process = 0

    current_time = 0

    while num_processes_loaded != num_processes:
        if check_load_process(current_time):
            remaining_processes.append(processes_group[num_processes_loaded])
            num_processes_loaded += 1
        
        for process in range(len(remaining_processes)):
            if remaining_processes[process].remaining_time > 0:
                if remaining_processes[process].remaining_time > quantum_time:
                    start_quantum_time_of_process = end_quantum_time_of_process
                    end_quantum_time_of_process += quantum_time

                    scheduling.append((start_quantum_time_of_process, remaining_processes[process].name, end_quantum_time_of_process))
                
                    remaining_processes[process].remaining_time -= quantum_time

                    if remaining_processes[process].remaining_time <= 0:
                        remaining_processes[process].remaining_time = 0
                        remaining_processes[process].set_completion_time(end_quantum_time_of_process)

        current_time += quantum_time

        remaining_processes = [process for process in remaining_processes if process.remaining_time > 0]

    waiting_time = calculate_waiting_time([process.completion_time for process in processes_group])
    turnaround_time = calculate_turnaround_time([process.completion_time for process in processes_group])
    
    print(scheduling)
    # write_output("RR.txt", scheduling, processes, turnaround_time, waiting_time)

    for i in range(num_processes):
        processes_group[i].set_remaining_time_again()

# def SJF():
#     processes_group.sort(key=lambda x: x.arrival_time) # Sort processes by arrival time

#     scheduling = []
#     remaining_processes = []

#     start_time_of_process = 0
#     end_time_of_process = 0

#     total_cpu_burst = 0
#     current_time = 0

#     for process in range(len(processes_group)):
#         total_cpu_burst += processes_group[process].cpu_burst

#     while total_cpu_burst != 0:

#         if (curre)




#         total_cpu_burst -= 1
#         current_time += 1


    # while remaining_processes:
    #     for process in range(num_processes - 1):
    #         start_time_of_process = remaining_processes[process].arrival_time
    #         end_time_of_process = remaining_processes[process + 1].arrival_time

    #         shortest_job = min(remaining_processes, key=lambda x: x.cpu_burst)  # Find process with shortest burst time
    #         remaining_processes.remove(shortest_job)  # Remove the selected process from the remaining processes

    #         start_time = max(current_time, shortest_job.arrival_time)
    #         end_time = start_time + shortest_job.cpu_burst

    #         scheduling.append((start_time, shortest_job.name, end_time))
    #         shortest_job.set_completion_time(end_time)

    #         current_time = end_time

    # waiting_time = calculate_waiting_time([process.completion_time for process in processes_group])
    # turnaround_time = calculate_turnaround_time([process.completion_time for process in processes_group])

    # print(scheduling)

    # write_output("SJF.txt", scheduling, processes_group, turnaround_time, waiting_time)

    # for process in processes_group:
    #     process.set_remaining_time_again()


def main():
    load_processes_from_file('Input.txt')
    # FCFS()
    RR()
    #SJF()
    # Priority(processes)

if __name__ == "__main__":
    main()



def write_output(file_name, scheduling, processes, turnaround_time, waiting_time):
    with open(file_name, 'w') as f:
        f.write("Scheduling chart: ")
        for event in scheduling:
            f.write(f"{event[0]} ~{event[1]}~ {event[2]} ")
        f.write("\n\n")
        for i in range(len(processes)):
            f.write(f"{processes[i].name}: \n")
            f.write(f"TT = {turnaround_time[i]} \t WT = {waiting_time[i]}\n")
        average_turnaround_time = sum(turnaround_time) / len(processes)
        average_waiting_time = sum(waiting_time) / len(processes)
        f.write(f"Average: \n")
        f.write(f"TT = {average_turnaround_time:.2f} \t WT = {average_waiting_time:.2f}\n")




def Priority(processes):
    pass