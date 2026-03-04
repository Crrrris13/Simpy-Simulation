import simpy
import random
import statistics
import matplotlib.pyplot as plt

RANDOM_SEED = 59
TOTAL_RAM = 100
CPU_SPEED = 3
CPU_COUNTS = 1

class ProcessSimulation:
    def __init__(self, interval, process, ram, cpu_speed, cpu_count):
        self.interval = interval
        self.process = process
        self.env = simpy.Environment()
        self.ram = simpy.Container(self.env, init=ram, capacity=ram)
        self.cpu_speed = cpu_speed
        self.cpu = simpy.Resource(self.env, capacity=cpu_count)
        self.result = []

    def run(self):
        self.env.process(self.process_generator())
        self.env.run()

        promedio = statistics.mean(self.result)
        desviacion = statistics.stdev(self.result) if len(self.result) > 1 else 0

        return promedio, desviacion
    
    def process_generator(self):
        for i in range(self.process):
            self.env.process(self.process_task(i))
            yield self.env.timeout(random.expovariate(1.0 / self.interval))

    def process_task(self, pid):
        arrive = self.env.now
        ram_needed = random.randint(1, 10)
        instructions = random.randint(1, 10)

        yield self.ram.get(ram_needed)

        while instructions > 0:
            with self.cpu.request() as request:
                yield request
                execute = min(instructions, self.cpu_speed)
                yield self.env.timeout(1)
                instructions -= execute

            if instructions > 0:
                event = random.randint(1, 21)

                if event == 1:
                    yield self.env.timeout(random.randint(1, 5))

        yield self.ram.put(ram_needed)

        total_time = self.env.now - arrive
        self.result.append(total_time)

def experiments():
    random.seed(RANDOM_SEED)

    process_count = [25, 50, 100, 150, 200]
    intervals = [10, 5, 1]

    strategies = {
        "Base": {"ram": TOTAL_RAM, "cpu_speed": 3, "cpu_count": 1},
        "More_RAM": {"ram": TOTAL_RAM * 2, "cpu_speed": 3, "cpu_count": 1}, 
        "Better_CPU": {"ram": TOTAL_RAM, "cpu_speed": 6, "cpu_count": 1},
        "More_Threads": {"ram": TOTAL_RAM, "cpu_speed": 3, "cpu_count": 2},
    }

    for name, param in strategies.items():
        for interval in intervals:

            average = []
            deviation = []

            print(f"\nIntervalo = {interval} - Estrategia: {name}")

            for count in process_count:
                sim = ProcessSimulation(interval, 
                    count, 
                    param["ram"], 
                    param["cpu_speed"], 
                    param["cpu_count"]
                    )
                
                avg, dev = sim.run()

                average.append(avg)
                deviation.append(dev)
                
                print(f"Procesos={count:3d} | Promedio={avg:8.2f} | Std={dev:8.2f}")

            plt.figure()
            plt.errorbar(process_count, average, yerr=deviation, marker='o')
            plt.title(f"Metodo: {name} | Intervalo = {interval}")
            plt.xlabel("Cantidad de Procesos")
            plt.ylabel("Tiempo Promedio")
            plt.grid(True)
            plt.show()

experiments()