To run this program:
1. Install tsp_solver using "pip install python-tsp"
2. Install matplotlib using "pip install matplotlib"
3. Install pillow using "pip install Pillow"

Using VSCode:
4. Open the algorithm that you want to test. IDA* is AIPlayer.py
5. Run python file in dedicated terminal.

The algorithms should be setup to use them with the TSP and Total Distance heuristic.
If you want to change heuristic, open AIPlayer and uncomment the wanted heuristic. Comment out the currently used heuristic.
Not all tests conducted will be available, such as original TSP heuristic. Some changes must be made in order to complete every test conducted. I tried to keep as many algorithms and heuristics in the code as possible.

Levels folder contains all levels of Johnny the Ghost, as well as a test level.
Tests folder contains data found from experiments.
Assets folder contains all used assets. All rights are reserved to Harald & Marcus Gitzel.

levels.py opens the level editor.
evaluation.py contains code generating graphs used in the report.
states.py holds the find_next_states() method. Can be tested on an individual state by uncommenting the commented code and running the program.

Timeouts are set to 5 minutes, change in parameters of algorithm functions.