# HDF5 Reactor

This Cyclus Reactor module is created in order to model
Molten Salt Reactors (MSRs) in Cyclus.

The reactor module will read the HDF5 file and
will do the following:
1. Request:
  * Initial fuel
  * Fertile Material
2. Offer:
  * surplus fissile stream
  * reprocessed waste stream
  * end-of-life discharge fuel

The user needs to specify the power capacity of the reactor,
and the commodity names for each stream coming in and out of the
reactor. The quantity and composition are all imported from the
HDF5 file.
