""" Simple example of digital output

    This example outputs the values of data on line 0 to 7
"""
from sys import platform
import numpy as np
from time import sleep, time
from datetime import datetime

from DAQ import DAQ
from SimpleOrientationExperiment import SimpleOrientationExperiment

bool_DEBUG = True

def create_experiment_name():
    if not bool_DEBUG:
        experiment_id = input("Enter Experiment name: (MXXXX_XXXXX_XX): ")
        mouse_id = input("Enter mouse ID (XXXXX): ")
    else:
        # when debugging we make a fake tag 
        now = datetime.now()
        date = str(now).split(" ")[0].replace("-", "")[2:]
        experiment_id = "M{}_12346_FB".format(date)

        mouse_id = "12345"

    return experiment_id, mouse_id


if __name__ == "__main__":
    try:
        experiment_id, mouse_id = create_experiment_name()
        data_aq = DAQ(experiment_id)

        exp = SimpleOrientationExperiment(experiment_id, mouse_id, data_aq, "monitor_config.yaml", "save_settings_config.yaml", "simple_orientation_config.yaml", debug=bool_DEBUG)

        exp.load_experiment_config()
        exp.start_data_acquisition()

        exp.run_experiment()

        exp.stop_data_acquisition()

        print("ALL DONE with experiment {}! ".format(experiment_id))
    except KeyboardInterrupt:
        print("Received CTRL-C event")
        if exp.experiment_running:
            # We need to run the stopping functions.
            pass
        if exp.acquisition_running:
            exp.stop_data_acquisition()
    finally:
        del exp.data_aq

