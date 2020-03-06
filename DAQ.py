from sys import platform

# control NI dacs only on windows
if platform == "win32":
    import nidaqmx as ni


# TODO consider making a BaseDAQ such that one can use the pco system too
class DAQ:
    def __init__(self):
        pass

    def data_read_callback(self):
        pass

    def start_cameras(self):
        pass

    def stop_cameras(self):
        pass

    def start_2p(self):
        pass

    def wait_for_2p_aq(self):
        return True
    
    def stop_2p(self):
        pass

    def start_logging(self):
        pass

    def stop_logging(self):
        pass

if __name__ == "__main__":
    data = []

    DEBUG = True

    def callback(task_handle, every_n_samples_event_type,
                    number_of_samples, callback_data):
        print('Every N Samples callback invoked.')

        samples = task.read(number_of_samples_per_channel=1000)
        data.append(samples)

        return 0

    task = ni.Task()
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0:7")
    task.timing.cfg_samp_clk_timing(rate=1000, sample_mode=ni.constants.AcquisitionType.CONTINUOUS)
    task.register_every_n_samples_acquired_into_buffer_event(1000, callback)

    out_ttl_task = ni.Task()
    out_ttl_task.do_channels.add_do_chan("Dev1/port0/line1", line_grouping=ni.constants.LineGrouping.CHAN_FOR_ALL_LINES)

    in_ttl_task = ni.Task()
    in_ttl_task.di_channels.add_di_chan("Dev1/port0/line3", line_grouping=ni.constants.LineGrouping.CHAN_FOR_ALL_LINES)
    in_ttl_task.di_channels.add_di_chan("Dev1/port1/line0", line_grouping=ni.constants.LineGrouping.CHAN_FOR_ALL_LINES)

    # start analog input acquisition
    task.start()
    sleep(1)

    # send ttl to 2p
    out_ttl_task.write([True])

    # check for 2p acquisition signal:
    while (not in_ttl_task.read()[0]):
        sleep(0.001)
    print(in_ttl_task.read())

    sleep(5)

    # stop the 2p aq.
    out_ttl_task.write([False])
    sleep(1)
    data = np.asarray(data)
    print(data.shape)

    #np.save("data-1-1005.npy", data)

    out_ttl_task.close()
    in_ttl_task.close()
    task.close()
    # task = ni.Task()
    # task.ai_channels.add_ai_voltage_chan("Dev0/ai1:7")
    # task.CreateDOChan("/TestDevice/port0/line2","",PyDAQmx.DAQmx_Val_ChanForAllLines)
    # task.StartTask()
    # task.WriteDigitalLines(1,1,10.0,PyDAQmx.DAQmx_Val_GroupByChannel,data,None,None)
    # task.StopTask()
