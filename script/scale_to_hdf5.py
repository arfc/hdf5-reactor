import numpy as np
import h5py

class scale_reader:
    def __init__(self, filepath, vol):
        timeseries_dict = {}
        with open(filepath, 'r') as f:
            lines = f.readlines()
            for line in lines[:5]:
                print(line)
            # first 6 lines are unnecessary
            for line in lines[6:]:
                line = line.split()
                iso_name = line[0].capitalize()
                timeseries_dict[iso_name] = np.array([float(x) for x in line[1:]])
        self.iso_names = list(timeseries_dict.keys())

        timesteps = len(timeseries_dict['U238'])
        print(timesteps)
        tot_time = 3 * timesteps
        print(tot_time, ' days')

        self.array = self.timseries_dict_to_array(timeseries_dict)


    def timseries_dict_to_array(self, timeseries_dict):
        num_isotopes = len(self.iso_names)
        timesteps = len(timeseries_dict[self.iso_names[0]])
       
        shape = (timesteps, num_isotopes)
        
        array = np.zeros(shape)

        for i in range(timesteps):
            iso_array = np.zeros(num_isotopes)
            for iso, mdens in timeseries_dict.items():
                iso_indx = self.iso_names.index(iso)
                iso_array[iso_indx] = mdens[i] * self.vol * 1e-3
            array[i] = iso_array
        print(array.shape)
        return array


# volume in cm^3
# returns mass in kg

core = scale_reader('./rebus_core', 1)
waste = scale_reader('./rebus_watste', 1)