from abc import ABC, abstractmethod
import psychopy.visual
import psychopy.event
import psychopy.monitors
import yaml

class BaseExperiment(ABC):
    def __init__(self, monitor_config_filename, save_settings_config_filename, exp_config_filename,):
        self.monitor = None
        self.monitor_settings = None
        self.window = None

        self.save_settings = None
        self.save_settings_config_filename = save_settings_config_filename

        self.exp_parameters = None
        self.exp_parameters_filename = exp_config_filename
        
        self.clock = psychopy.core.Clock()
        self.master_clock = psychopy.core.Clock()
        self.absolute_total_time = 0

        self.load_monitor(monitor_config_filename)
        self.load_window()

        self.create_photodiode_square()


    def __del__(self):
        self.window.close()

    
    def load_monitor(self, monitor_config_filename):

        #Constructor loads the parameters for the VS experiment
        with open(monitor_config_filename, 'r') as file:
            self.monitor_settings = yaml.load(file, Loader=yaml.FullLoader)
        
        monitor_name = self.monitor_settings['monitor_name']
        monitor_width_pixels = self.monitor_settings['monitor_width_pixels']
        monitor_height_pixels = self.monitor_settings['monitor_height_pixels']
        monitor_width_cm = self.monitor_settings['monitor_width_cm']
        viewing_distance_cm = self.monitor_settings['viewing_distance_cm']
        monitor_gamma = self.monitor_settings['monitor_gamma']



        self.monitor = psychopy.monitors.Monitor(monitor_name, width=monitor_width_cm, distance=viewing_distance_cm, gamma=monitor_gamma)
        self.monitor.setSizePix((monitor_width_pixels, monitor_height_pixels))

        
        # TODO  check if monitor needs to get saved in win
        #mon.save()

    def load_window(self):
        self.window = psychopy.visual.Window(monitor=self.monitor, 
                                            size=(self.monitor_settings['monitor_width_pixels'],
                                                  self.monitor_settings['monitor_height_pixels']),
                                            color='gray',
                                            colorSpace='rgb',
                                            units='deg',
                                            screen=self.monitor_settings['screen_id'],
                                            allowGUI=False,
                                            fullscr=True)

    def create_photodiode_square(self):
        # Load the settings of the square that goes on the photodiode
        self.square_size = self.monitor_settings['square_size']
        self.square_position = self.monitor_settings['square_position']
        self.square_color_off = self.monitor_settings['square_color_off']
        self.square_color_on = self.monitor_settings['square_color_on']

        self.photodiode_square = psychopy.visual.Rect(win=self.window, pos=self.square_position, width=self.square_size[0], height=self.square_size[1], 
                                                      units='pix', color=self.square_color_off)


    @abstractmethod
    def load_experiment_config(self, ):
        pass

    @abstractmethod
    def run_experiment(self,):
        pass