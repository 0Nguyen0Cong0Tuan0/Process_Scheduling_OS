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
            current_time = process.arrival_time
            return True
    return False

def write_output(file_name, scheduling, turnaround_time, waiting_time):
    with open(file_name, 'w') as f:
        f.write("Scheduling: ")

        for event in scheduling:
            f.write(f"| {event[0]} ~ {event[1]} ~ {event[2]} ")

        f.write("\n\n")

        for i in range(num_processes):
            f.write(f"{processes_group[i].name}: \n")
            f.write(f"TT = {turnaround_time[i]}  WT = {waiting_time[i]}\n")

        average_turnaround_time = sum(turnaround_time) / num_processes
        average_waiting_time = sum(waiting_time) / num_processes

        f.write(f"Average: \n")
        f.write(f"TT = {average_turnaround_time:.2f} \t WT = {average_waiting_time:.2f}\n")

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

    write_output("FCFS.txt", scheduling, turnaround_time, waiting_time)

def RR():
    processes_group.sort(key=lambda x: x.arrival_time) # sort arrival_time for all processes

    scheduling = []
    remaining_processes = processes_group[:]

    start_quantum_time_of_process = 0
    end_quantum_time_of_process = 0

    process_done = 0

    is_any_process_did = False

    while remaining_processes:
        for process in range(len(remaining_processes)):
            if remaining_processes[process].arrival_time <= end_quantum_time_of_process:
                if remaining_processes[process].remaining_time > quantum_time:
                    is_any_process_did = True

                    start_quantum_time_of_process = end_quantum_time_of_process
                    end_quantum_time_of_process += quantum_time

                    scheduling.append((start_quantum_time_of_process, remaining_processes[process].name, end_quantum_time_of_process))

                    remaining_processes[process].remaining_time -= quantum_time

                else:
                    is_any_process_did = True
                    start_quantum_time_of_process = end_quantum_time_of_process
                    end_quantum_time_of_process += remaining_processes[process].remaining_time
                        
                    scheduling.append((start_quantum_time_of_process, remaining_processes[process].name, end_quantum_time_of_process))

                    remaining_processes[process].remaining_time = 0
                    remaining_processes[process].set_completion_time(end_quantum_time_of_process)

                    process_done += 1

        remaining_processes = [process for process in remaining_processes if process.remaining_time > 0]

        if process_done < num_processes and is_any_process_did == False:
            start_quantum_time_of_process = end_quantum_time_of_process
            end_quantum_time_of_process += 1

        is_any_process_did = False

    waiting_time = calculate_waiting_time([process.completion_time for process in processes_group])
    turnaround_time = calculate_turnaround_time([process.completion_time for process in processes_group])

    write_output("RR.txt", scheduling, turnaround_time, waiting_time)

    for i in range(num_processes):
        processes_group[i].set_remaining_time_again()

def SJF():
    processes_group.sort(key=lambda x: x.arrival_time) # Sort processes by arrival time

    scheduling = []
    remaining_processes = processes_group[:]
    current_time = 0

    while remaining_processes:
        arriving_processes = [process for process in remaining_processes if process.arrival_time <= current_time]
        
        if arriving_processes:
            process_min_cpu_burst = min(arriving_processes, key=lambda process: process.cpu_burst)
            
            start_of_process = current_time
            end_of_process = current_time + process_min_cpu_burst.cpu_burst
            
            scheduling.append((start_of_process, process_min_cpu_burst.name, end_of_process))
            
            current_time = end_of_process
            
            remaining_processes.remove(process_min_cpu_burst)
        else:
            current_time += 1

    waiting_time = calculate_waiting_time([process.completion_time for process in processes_group])
    turnaround_time = calculate_turnaround_time([process.completion_time for process in processes_group])

    write_output("SJF.txt", scheduling, turnaround_time, waiting_time)

    for process in processes_group:
        process.set_remaining_time_again()


def SRTN():
    processes_group.sort(key=lambda x: x.arrival_time)  # Sort processes by arrival time

    scheduling = []
    remaining_processes = []

    current_time = 0
    start_time = 0

    process_loaded_number = 0
    id_current_process = processes_group[process_loaded_number]

    while process_loaded_number < num_processes or remaining_processes:
        while process_loaded_number < num_processes and processes_group[process_loaded_number].arrival_time == current_time:
            remaining_processes.append(processes_group[process_loaded_number])
            process_loaded_number += 1

        if remaining_processes:
            process_min_remaining_time = min(remaining_processes, key=lambda process: process.remaining_time)

            if id_current_process != process_min_remaining_time:
                if start_time != current_time and id_current_process in remaining_processes:
                    scheduling.append((start_time, id_current_process.name, current_time))
                start_time = current_time
                id_current_process = process_min_remaining_time

            process_min_remaining_time.remaining_time -= 1
            current_time += 1

            if not remaining_processes:
                id_current_process = processes_group[process_loaded_number]

            if process_min_remaining_time.remaining_time == 0:
                scheduling.append((start_time, id_current_process.name, current_time))
                id_current_process.set_completion_time(current_time)
                start_time = current_time
                remaining_processes.remove(process_min_remaining_time)

        else:
            current_time += 1


    waiting_time = calculate_waiting_time([process.completion_time for process in processes_group])
    turnaround_time = calculate_turnaround_time([process.completion_time for process in processes_group])

    write_output("SRTN.txt", scheduling, turnaround_time, waiting_time)

    for process in processes_group:
        process.set_remaining_time_again()

def Priority():
    processes_group.sort(key=lambda x: x.arrival_time)  # Sort processes by arrival time

    scheduling = []
    remaining_processes = []

    current_time = 0
    start_time = 0

    process_loaded_number = 0
    id_current_process = processes_group[process_loaded_number]

    while process_loaded_number < num_processes or remaining_processes:
        while process_loaded_number < num_processes and processes_group[process_loaded_number].arrival_time == current_time:
            remaining_processes.append(processes_group[process_loaded_number])
            process_loaded_number += 1

        if remaining_processes:
            process_highest_priority = min(remaining_processes, key=lambda process: process.priority)

            if id_current_process != process_highest_priority:
                if start_time != current_time and id_current_process in remaining_processes:
                    scheduling.append((start_time, id_current_process.name, current_time))
                start_time = current_time
                id_current_process = process_highest_priority

            process_highest_priority.remaining_time -= 1
            current_time += 1

            if not remaining_processes:
                id_current_process = processes_group[process_loaded_number]

            if process_highest_priority.remaining_time == 0:
                scheduling.append((start_time, id_current_process.name, current_time))
                start_time = current_time
                remaining_processes.remove(process_highest_priority)

        else:
            current_time += 1

    waiting_time = calculate_waiting_time([process.completion_time for process in processes_group])
    turnaround_time = calculate_turnaround_time([process.completion_time for process in processes_group])

    write_output("Priority.txt", scheduling, turnaround_time, waiting_time)

def main():
    load_processes_from_file('Input.txt')
    FCFS()
    RR()
    SJF()
    SRTN()
    Priority()

if __name__ == "__main__":
    main()







