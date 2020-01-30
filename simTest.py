#!/usr/bin/python3

import multiprocessing
import os
import platform
import subprocess
import time

MAX_ITERATION = 10
SCENARIO_NAME = "960_Texas_Exaggerated_MemoryError.db"
#SCENARIO_NAME = "Texas455_badandmemoryerror.db"

# linux options
executable = 'adsm_simulation'
system     = 'Linux'

# windows options
#executable = 'adsm_simulation.exe'
#system     = 'Darwin'


def simulation_process(iteration_number, adsm_cmd, log_path):
    start = time.time()
    # Start logging
    with open(os.path.join(log_path, 'iteration%s.log' % iteration_number), 'w') as log_file:
        simulation = subprocess.Popen(adsm_cmd,
                                      shell=(platform.system() != "Darwin"),
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE,
                                      bufsize=1)
        # Popen is non-blocking, and all the readlines below read the process output in real time as it buffers
        # Calling communicate IS blocking, so we don't want to do that until this process is done
        # Ideally we would run communicate first so we can get any errors, but this would prevent us from updating progress of this simulation in real time.
        headers = simulation.stdout.readline().decode()
        log_file.write("LOG: HEADERS:\n")
        log_file.write("%s\n" % headers)

        while True:
            line = simulation.stdout.readline()  # TODO: Has the potential to lock up if CEngine crashes (blocking io)
            line = line.decode().strip()
            if not line:
                break
            log_file.write("%s\n" % line)
            prev_line = line

        prev_line = ''
        unit_stats_headers = simulation.stdout.readline().decode()  # TODO: Currently we don't use the headers to find which row to insert into.
        log_file.write("LOG: UNIT STAT HEADERS:\n")
        log_file.write("%s\n" % unit_stats_headers)
        for line in simulation.stdout.readlines():
            line = line.decode().strip()
            log_file.write(line)
            prev_line = line

        outs, errors = simulation.communicate()  # close p.stdout, wait for the subprocess to exit
        log_file.write("LOG: FINAL OUTS:\n")
        log_file.write("%s\n" % outs)
        if errors:  # this will only print out error messages after the simulation has halted
            log_file.write("LOG: FINAL ERRORS:\n")
            log_file.write("%s\n" % errors)
            print(errors)
    # End logging

    end = time.time()

    return iteration_number, end - start


class Simulation(multiprocessing.Process):
    def __init__(self, max_iteration, scenario_name="activeSession.db", **kwargs):
        super(Simulation, self).__init__(**kwargs)
        self.max_iteration = max_iteration
        self.scenario_name = scenario_name

    def run(self):
        pid = os.getpid()

        try:
            print("Starting run")

            # Clean out previous iteration logs
            log_path = os.path.dirname(os.path.abspath(__file__))
            logs_to_delete = [f for f in os.listdir(log_path) if f.startswith('iteration') and os.path.isfile(os.path.join(log_path, f))]
            for f in logs_to_delete:
                os.remove(os.path.join(log_path, f))

            num_cores = multiprocessing.cpu_count()
            # if num_cores > 2:  # Standard processor saturation
            #     num_cores -= 1
            if num_cores > 3:  # Lets you do other work while running sims
                num_cores -= 2
            executable_cmd = [os.path.join(log_path, executable), os.path.join(log_path, self.scenario_name), '--output-dir', os.path.join(log_path, 'Supplemental-Output-Files')]

            statuses = []
            pool = multiprocessing.Pool(num_cores)
            for iteration in range(1, self.max_iteration + 1):
                adsm_cmd = executable_cmd + ['-i', str(iteration)]
                print(adsm_cmd)
                res = pool.apply_async(func=simulation_process, args=(iteration, adsm_cmd, log_path))
                statuses.append(res)

            pool.close()

            simulation_times = []
            for status in statuses:
                iteration_number, s_time = status.get()
                simulation_times.append(round(s_time))

            print(''.join(str(s) + 's, ' for s in simulation_times))
            print("Average Time:", round(sum(simulation_times) / len(simulation_times), 2), 'seconds')
        except:
            raise


def main():
    sim = Simulation(max_iteration=MAX_ITERATION, scenario_name=SCENARIO_NAME)
    sim.start()


if __name__ == "__main__":
    main()