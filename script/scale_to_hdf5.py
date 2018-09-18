import numpy as np
import h5py

class scale_reader:
    def __init__(self, file_list, vol):
        self.file_list = file_list
        self.vol = vol
        self.check_input_files()

        self.timeseries_dict = {}

        for file in file_list:
            print('READING FILE ', file)
            self.get_timeseries_dict(file)

        self.array_dict = {}
        for key, val in self.timeseries_dict.items():
            self.array_dict[key] = self.timseries_dict_to_array(val)

    def get_timeseries_dict(self, file):
        filename = file.split('/')[-1]
        self.timeseries_dict[filename] = {}
        with open(file, 'r') as f:
            lines = f.readlines()
            unit = lines[2]
            if self.get_suffix(unit) != self.suffix:
                raise ValueError('Units are different here')

            for line in lines[6:]:
                line = line.split()
                iso_name = line[0].capitalize()
                if 'total' in iso_name:
                    continue
                self.timeseries_dict[filename][iso_name] = np.array([float(x) for x in line[1:]])

    def timseries_dict_to_array(self, timeseries_dict):
        shape = (self.timesteps, self.num_isotopes)

        array = np.zeros(shape)
        for i in range(self.timesteps):
            iso_array = np.zeros(self.num_isotopes)
            for iso, mdens in timeseries_dict.items():
                iso_indx = self.iso_names.index(iso)
                iso_array[iso_indx] = mdens[i] * self.suffix
            array[i] = iso_array
        return array

    def get_suffix(self, unit):
        unit = unit.strip()
        if unit == 'g/cm3':
            suffix = self.vol * 1e-3
        elif unit == 'grams':
            suffix = 1e-3
        else:
            print(unit)
            raise ValueError('What is this unit')
        return suffix

    def check_input_files(self):
        self.iso_names = []
        timestep_lists = []
        unit_lists = []
        time_lists = []
        for file in self.file_list:
            with open(file, 'r') as f:
                lines = f.readlines()
                for line in lines[6:]:
                    iso = line.split()[0]
                    iso = iso.capitalize()
                    self.iso_names.append(iso)

                # collect timesteps
                timestep_val = int(lines[4].split()[0])
                timestep_lists.append(timestep_val)

                # collect units
                unit_val = lines[2].strip()
                unit_lists.append(unit_val)

                # collect time units
                time_val = lines[1].strip()
                time_lists.append(time_val)

        # check if they all coincide
        timestep_lists = list(set(timestep_lists))
        unit_lists = list(set(unit_lists))
        time_lists = list(set(time_lists))

        if len(timestep_lists) != 1:
            raise ValueError('Timesteps do not match')
        if len(unit_lists) != 1:
            raise ValueError('Units do not match')
        if len(time_lists) != 1:
            raise ValueError('time units do not match')

        self.timesteps = timestep_lists[0]
        self.suffix = self.get_suffix(unit_lists[0])

        self.iso_names = sorted(list(set(self.iso_names)))
        self.num_isotopes = len(self.iso_names)



#############################################################################

# volume in cm^3
# returns mass in kg

rebus = scale_reader(['../db/rebus_core', '../db/rebus_waste'], 36.9*1e6)
print(rebus.array_dict.keys())
print(rebus.array_dict)
print(rebus.iso_names)

# create hdf5 database
def render_hdf5(reader_object):
    k = h5py.File('rebus_scale.hdf5', 'w')
    k.create_dataset('blanket composition after reproc', data=np.zeros(shape))
    k.create_dataset('blanket composition before reproc', data=np.zeros(shape))
    k.create_dataset('blanket refill tank composition', data=np.zeros(shape))

    k.create_dataset('driver composition before reproc', data=core.array)
    k.create_dataset('driver composition after reproc', data=core.array)
    k.create_dataset('driver refill tank composition', data=th_mass)

    k.create_database('fissile tank composition', data=np.zeros(shape))

    k.create_database('iso names', data=core.iso_names)
    k.create_database('iso zai', data=iso_zai)

    k.create_database('keff_BOC', data=keff_boc)
    k.create_database('keff_EOC', data=keff_eoc)

    k.create_database('siminfo_driver_init_comp', data= init_mass_comp_array)
    k.create_database('siminfo_driver_mass_density', data=3.35)

    k.create_database('siminfo_timestep', data=3)
    k.create_database('siminfo_totstps', data=int(365*40/3))

    k.create_database('waste tank composition', data=noble_mass)
