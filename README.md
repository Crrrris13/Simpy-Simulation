# SIMULACION DE PROCESOS CON SIMPY

Cristopher Chavez - 25199

Este programa implementa una simulación de un sistema operativo de tiempo compartido utilizando SimPy en Python.

La simulación modela cómo los procesos llegan al sistema, solicitan memoria RAM, utilizan el CPU y finalmente terminan su ejecución.

## Funcionamiento
- Los procesos llegan con una distribución exponencial.
- Cada proceso solicita entre 1 y 10 unidades de memoria.
- El CPU ejecuta hasta 3 instrucciones por unidad de tiempo.
- Puede haber estados de espera (I/O).
- Al finalizar, el proceso libera la memoria utilizada.

Estrategia recomendada: More_Threads o mas nucleos, agregar un nucleo ya que esto permite que dos procesos se ejecuten simultáneamente, lo cual reduce significativamente los tiempos de espera y disminuye el tiempo promedio en el sistema.