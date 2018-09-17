import numpy as np
import h5py
from pyne import nucname

f = h5py.File('./db_saltproc_40years.hdf5', 'r')

th_tank_adensity = np.array(f['Th tank adensity'])
core_adensity_after = np.array(f['core adensity after reproc'])
core_adensity_before = np.array(f['core adensity before reproc'])
keff_boc = np.array(f['keff_BOC'])
keff_eoc = np.array(f['keff_EOC'])
tank_adensity = np.array(f['tank adensity'])
noble_adensity = np.array([])
iso_codes = np.array(f['iso_codes'])
iso_zai = []
iso_names = []
for code in iso_codes:
    code = code.decode()
    if '.09c' in code:
        code = code.replace('.09c', '')
        code = nucname.zzzaaa_to_id(int(code))
    else:
        code = nucname.zzaaam_to_id(int(code))
    iso_zai.append(nucname.zzaaam(code))
    iso_names.append(nucname.name(code))
iso_zai = np.array(iso_zai)
iso_names = np.array(iso_names)

shape = core_adensity_after.shape


# way to convert adensity to mass



# write
k = h5py.File('new_msbr.hdf5', 'w')
k.create_dataset('blanket composition after reproc', data=np.zeros(shape))
k.create_dataset('blanket composition before reproc', data=np.zeros(shape))
k.create_dataset('blanket refill tank composition', data=np.zeros(shape))

k.create_dataset('driver composition before reproc', data=core_adensity_before)
k.create_dataset('driver composition after reproc', data=core_adensity_after)
k.create_dataset('driver refill tank composition', data=th_tank_adensity)

k.create_database('fissile tank composition', data=np.zeros(shape))

k.create_database('iso names', data=iso_names)
k.create_database('iso zai', data=iso_zai)

k.create_database('keff_BOC', data=keff_boc)
k.create_database('keff_EOC', data=keff_eoc)

k.create_database('siminfo_driver_init_comp', data= )
k.create_database('siminfo_driver_mass_density', data=)

k.create_database('siminfo_timestep', data=3)
k.create_database('siminfo_totstps', data=int(365*40/3))

k.create_database('waste tank composition', data=noble_adensity)
