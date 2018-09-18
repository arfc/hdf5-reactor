import numpy as np
import h5py
from pyne import nucname
from pyne.material import Material

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


def adens_to_mass(fuel_vol, array, iso_names):
    shape = array.shape
    mass_array = np.zeros(shape)
    for num, row in enumerate(array):
        mat_dict = {}
        mass_comp = np.zeros(len(row))
        for indx, val in enumerate(row):
            mat_dict[iso_names[indx]] = val
        mat = Material()
        mat.from_atom_frac(mat_dict)
        # mat.comp is mass density
        for key, val in mat.comp.items():
            key = nucname.name(key)
            iso_indx = list(iso_names).index(key)
            # mass = mass density * volume * unit(barns)
            mass_comp[indx] = val * fuel_vol * 1e24
        mass_array[num] = mass_comp

        # you still there?
        if num == (len(array) // 2):
            print('halfway there')
    return mass_array


# get initial composition of msbr:
mat = Material()
mat_dict = {'Li7': 71.85, 
            'Be9': 16,
            'Th232': 12,
            'U233': 0.25,
            'F19': 71.85+16*2+12*4+0.25*4}
mat.from_atom_frac(mat_dict)
init_mass_comp = mat.comp
init_mass_comp_array = np.zeros(len(iso_names))
for key,  val in init_mass_comp.items():
    key = nucname.name(key)
    indx = list(iso_names).index(key)
    init_mass_comp_array[indx] = val

# msbr [cm3]
fuel_vol = 48.7e6
# msbr [g/cm3]
mass_dens = 3.35

core_mass_after = adens_to_mass(fuel_vol, core_adensity_after,
                                iso_names)
print('PROGRESS?')
core_mass_before = adens_to_mass(fuel_vol, core_adensity_before,
                                iso_names)
print('PROGRESS?')
th_mass = adens_to_mass(fuel_vol, th_tank_adensity, iso_names)
noble_mass = adens_to_mass(fuel_vol, noble_adensity, iso_names)                                

# write
k = h5py.File('new_msbr.hdf5', 'w')
k.create_dataset('blanket composition after reproc', data=np.zeros(shape))
k.create_dataset('blanket composition before reproc', data=np.zeros(shape))
k.create_dataset('blanket refill tank composition', data=np.zeros(shape))

k.create_dataset('driver composition before reproc', data=core_mass_before)
k.create_dataset('driver composition after reproc', data=core_mass_after)
k.create_dataset('driver refill tank composition', data=th_mass)

k.create_database('fissile tank composition', data=np.zeros(shape))

k.create_database('iso names', data=iso_names)
k.create_database('iso zai', data=iso_zai)

k.create_database('keff_BOC', data=keff_boc)
k.create_database('keff_EOC', data=keff_eoc)

k.create_database('siminfo_driver_init_comp', data= init_mass_comp_array)
k.create_database('siminfo_driver_mass_density', data=3.35)

k.create_database('siminfo_timestep', data=3)
k.create_database('siminfo_totstps', data=int(365*40/3))

k.create_database('waste tank composition', data=noble_mass)
