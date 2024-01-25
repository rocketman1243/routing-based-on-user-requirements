# Routing based on User Requirements

This is the codebase that accompanies my master's thesis on the subject of internet routing based on user requirements.

Please check out the license before using this in your projects. TL:DR; The code is free and open source, and you may only use it if the things you do with it are free and open source as well.

This repository is not really a full end user application, it is more like a test bench. The repo contains tools to quickly generate the files needed for experiments, and the `main.py` is set up to run experiments.

Below are steps to install the code, set up an experiment, run an experiment, and analyze the results.

The code is mainly set up to set up and run the same experiments many times

## How to install

1. Clone the git repository or download a zip of the code
2. Install python version 3.10
3. Install networkx using `pip install networkx`
4. Install any other needed python dependencies using `pip install <dependency>`

## How to set up an experiment

1. Go to the folder of the stage you want to set up an experiment for, either `/1_limit_stage` or `/2_comparison_stage`. This folder is the stage folder.
2. Create a sub-folder with the name of your experiment in both the `nio_files` and `pro_files` folders. The folder you create is the experiment folder.
    - For example, if you want to create an experiment for the limit stage called `scalability`, you create the following folders:
      - `/limit_stage/pro_files/scalability`
      - `/limit_stage/nio_files/scalability`
3. Go back to the stage folder, and open the `generate_nio_files.py` script.
5. Select the desired experiment by setting the `experiment` value equal to to the name of the experiment folder.
   - To continue the example, you would set `experiment = "scalability"`
6. Select the minimum and maximum number of features that each node in the graph supports.
7. Set up the graph model. If you selected an experiment for which the graph model is created already, your are done. If not:
   1. Create a networkx graph for your experiment
   2. Update the `output_path` variable such that it points to your sub-folder in the `nio_files`. Use a relative part starting at the root folder, similar to how the other experiment output_path variables are defined.
8. Close the file and go back to the root folder of the project
9. Create the node information files by running the `generate_nio_files.py` script.
   - For the limit stage for example, this would be running `$ python ./1_limit_stage/generate_nio_files.py`
10. Go to the stage folder, and open the `generate_pro_files.py` script.
11. Again, set the `experiment` variable to the name of your experiment folder
12. Select the desired values for:
    -  The number of best effort requirements that each path request is allowed to request (`best_effort_min_amount` and `best_effort_max_amount`)
    -  The maximum number of strict requirements (`max_number_of_strict_requirements`)
    -  The total number of features that the requirements are selected from (`nr_of_features`)
    -  The number of path requests (`num_objects`)
13. Close the script, then run it from the root of the project

## How to run an experiment

Open `main.py` and go through the setup:

0. Set the preamble flags to your liking
1. Select the limits you want to assign to the heuristic. If you created a new experiment, add a new if statement below the setup that selects your set of limits based on the name of your experiment.
2. Set the `experiments` variable to the name of your experiment folder. The system supports running multiple experiments back-to-back by adding their names to the list of experiments
3. Select which stage you want to run by uncommenting the correct assignment of `CHOSEN_PATH`
4. Enable the algorithms you want to run. If you want to run both algorithms, set both variables to True.

Close `main.py` and run it from the root folder using `$ python main.py`, then watch the magic unfold!

## How to analyze the results

1. Ensure that you wrote the results to a file by setting in `main.py` in the preamble the `printInsteadOfWriteToFile` variable to `False`.
2. Go to the stage folder you want to analyze results of
3. Look in the `/results` folder and note the name of the file with the results
4. Open the `convert_output_to_stats.py` script
5. Set the `experiment` variable to the name of your experiment results file
6. Adjust the matplotlib code to display the results you want