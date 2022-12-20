from optparse import OptionParser
import glob
import time
from grand.io.root_trees import *
from CorsikaInfoFuncs import *

# TODO: check if the IDs in SIM.reas and RUN.inp match

###############
# option parser
parser = OptionParser()
parser.add_option("--directory", "--dir", "-d", type="str", dest="dir")
(options, args) = parser.parse_args()
# make sure that the last character of dir is a slash
if (options.dir[-1]!="/"):
    options.dir = options.dir + "/"
print("Checking", options.dir, "for *.reas and *.inp files (shower info).")
print("Checking subdirectories for *.dat files (traces).")


#######################
# load Corsika files  #
#######################

# ********** load SIM.reas and RUN.inp **********
if glob.glob(options.dir + "SIM??????-*.reas"):
    available_reas_files = glob.glob(options.dir + "SIM??????-*.reas")
else:
    available_reas_files = glob.glob(options.dir + "SIM??????.reas")
available_inp_files = glob.glob(options.dir + "RUN??????.inp")

# reas status messages
if len(available_reas_files) == 0:
  print("[ERROR] No reas file found in this directory. Please check directory and try again.")
  quit()
elif len(available_reas_files) > 1:
  print("Found", available_reas_files)
  print("[WARNING] More than one reas file found in directory. Only reas file", available_reas_files[0], "will be used.")
  reas_input = available_reas_files[0]
else:
  print("Found", available_reas_files)
  reas_input = available_reas_files[0]
  print("Converting reas file", reas_input, "to GRANDroot.")
print("*****************************************")

# inp status messages
if len(available_inp_files) == 0:
  print("[ERROR] No input file found in this directory. Please check directory and try again.")
  quit()
elif len(available_inp_files) > 1:
  print("Found", available_inp_files)
  print("[WARNING] More than one input file found in directory. Only input file", available_inp_files[0], "will be used.")
  inp_input = available_inp_files[0]
else:
  print("Found", available_inp_files)
  inp_input = available_inp_files[0]
  print("Converting input file", inp_input, "to GRANDroot.")


# ********** load traces **********
available_traces = glob.glob(options.dir + "SIM??????_coreas/*.dat")
print("Found", len(available_traces), "*.dat files (traces).")
print("*****************************************")
# in each dat file:
# time stamp and the north-, west-, and vertical component of the electric field

# prepare traces as in DataStoringExample.py
filename = reas_input.split(".reas")[0] + ".root"
event_count = 1
adc_traces = []
traces = []
for ev in range(event_count):
    adc_traces.append([])
    traces.append([])
    for i, file in enumerate(available_traces):
        adc_traces[-1].append(
            (
                np.genfromtxt(file)[:,0].astype(np.int16),
                np.genfromtxt(file)[:,1].astype(np.int16),
                np.genfromtxt(file)[:,2].astype(np.int16),
                np.genfromtxt(file)[:,3].astype(np.int16),
            )
        )
        traces[-1].append(
            (
                (adc_traces[-1][i][0] * 0.9 / 8192).astype(np.float32),
                (adc_traces[-1][i][1] * 0.9 / 8192).astype(np.float32),
                (adc_traces[-1][i][2] * 0.9 / 8192).astype(np.float32),
            )
        )


#######################
# Generate ROOT Trees #
#######################

# ********** Generate Run Tree ****************
print("Storing run info...")
# Create the Run tree
trun = RunTree()
trun.run_number = read_params(reas_input, "RunNumber")
trun.site = "Dunhuang"
trun.fill()
trun.write(filename)
print("Completed storing run info in trun.")
print("*****************************************")

# ********** ADC Counts ****************
print("Storing ADC traces...")
# Create the ADC counts tree
tadccounts = ADCEventTree()

# !!!
# !!! i commented out some info that i think we dont have in corsika
# !!!

# fill the tree with the generated events
for ev in range(event_count):
    tadccounts.run_number = read_params(reas_input, "RunNumber")
    tadccounts.event_number = read_params(reas_input, "EventNumber")
    # First data unit in the event
    tadccounts.first_du = 0
    # As the event time add the current time
    tadccounts.time_seconds = read_params(reas_input, "GPSSecs")
    # Event nanoseconds 0 for now
    tadccounts.time_nanoseconds = read_params(reas_input, "GPSNanoSecs")
    # Triggered event
    tadccounts.event_type = 0x8000 # not sure we even have this in corsika, so i'll keep the dummy number
    # The number of antennas in the event
    tadccounts.du_count = len(traces[ev])

    # Loop through the event's traces
    du_id = []
    # du_seconds = []
    # du_nanoseconds = []
    # trigger_position = []
    # trigger_flag = []
    # atm_temperature = []
    # atm_pressure = []
    # atm_humidity = []
    # acceleration_x = []
    # acceleration_y = []
    # acceleration_z = []
    trace_0 = []
    trace_1 = []
    trace_2 = []
    trace_3 = []
    for i, trace in enumerate(adc_traces[ev]):
      du_id.append(i)
        # du_seconds.append(tadccounts.time_seconds)
        # du_nanoseconds.append(tadccounts.time_nanoseconds)
        # trigger_position.append(i // 2)
        # trigger_flag.append(tadccounts.event_type)
        # atm_temperature.append(20 + ev // 2)
        # atm_pressure.append(1024 + ev // 2)
        # atm_humidity.append(50 + ev // 2)
        # acceleration_x.append(ev // 2)
        # acceleration_y.append(ev // 3)
        # acceleration_z.append(ev // 4)
      trace_0.append(trace[0] + 1)
      trace_1.append(trace[1] + 2)
      trace_2.append(trace[2] + 3)
      trace_3.append(trace[3] + 4)

    tadccounts.du_id = du_id
        # tadccounts.du_seconds = du_seconds
        # tadccounts.du_nanoseconds = du_nanoseconds
        # tadccounts.trigger_position = trigger_position
        # tadccounts.trigger_flag = trigger_flag
        # tadccounts.atm_temperature = atm_temperature
        # tadccounts.atm_pressure = atm_pressure
        # tadccounts.atm_humidity = atm_humidity
        # tadccounts.acceleration_x = acceleration_x
        # tadccounts.acceleration_y = acceleration_y
        # tadccounts.acceleration_z = acceleration_z
    tadccounts.trace_0 = trace_0
    tadccounts.trace_1 = trace_1
    tadccounts.trace_2 = trace_2
    tadccounts.trace_3 = trace_3

    tadccounts.fill()

# write the tree to the storage
tadccounts.write(filename)
print("Completed storing ADC traces in tadccounts.")
print("*****************************************")

# ********** Voltage ****************
print("Storing voltage info...")
# Voltage has the same data as ADC counts tree, but recalculated to "real" (usually float) values

# Recalculate ADC counts to voltage, just with a dummy conversion now: 0.9 V is equal to 8192 counts for XiHu data
adc2v = 0.9 / 8192

# Create the ADC counts tree
tvoltage = VoltageEventTree()

# fill the tree with the generated events
for ev in range(event_count):
    tvoltage.run_number = read_params(reas_input, "RunNumber")
    tvoltage.event_number = read_params(reas_input, "EventNumber")
    tvoltage.first_du = 0
    tvoltage.time_seconds = int(time.mktime(time.gmtime()))
    tvoltage.time_nanoseconds = read_params(reas_input, "GPSNanoSecs")
    # Triggered event
    tvoltage.event_type = 0x8000
    # The number of antennas in the event
    tvoltage.du_count = len(traces[ev])

    # Loop through the event's traces
    du_id = []
    du_seconds = []
    du_nanoseconds = []
    # trigger_position = []
    # trigger_flag = []
    # atm_temperature = []
    # atm_pressure = []
    # atm_humidity = []
    # acceleration_x = []
    # acceleration_y = []
    # acceleration_z = []
    trace_x = []
    trace_y = []
    trace_z = []
    for i, trace in enumerate(traces[ev]):
        du_id.append(i)
        du_seconds.append(tvoltage.time_seconds)
        du_nanoseconds.append(tvoltage.time_nanoseconds)
        # trigger_position.append(i // 2)
        # trigger_flag.append(tvoltage.event_type)
        # atm_temperature.append(20 + ev / 2)
        # atm_pressure.append(1024 + ev / 2)
        # atm_humidity.append(50 + ev / 2)
        # acceleration_x.append(ev / 2)
        # acceleration_y.append(ev / 3)
        # acceleration_z.append(ev / 4)

        trace_x.append(trace[0])
        trace_y.append(trace[1])
        trace_z.append(trace[2])

    tvoltage.du_id = du_id
    tvoltage.du_seconds = du_seconds
    tvoltage.du_nanoseconds = du_nanoseconds
    # tvoltage.trigger_position = trigger_position
    # tvoltage.trigger_flag = trigger_flag
    # tvoltage.atm_temperature = atm_temperature
    # tvoltage.atm_pressure = atm_pressure
    # tvoltage.atm_humidity = atm_humidity
    # tvoltage.acceleration_x = acceleration_x
    # tvoltage.acceleration_y = acceleration_y
    # tvoltage.acceleration_z = acceleration_z
    tvoltage.trace_x = trace_x
    tvoltage.trace_y = trace_y
    tvoltage.trace_z = trace_z

    tvoltage.fill()

# write the tree to the storage
tvoltage.write(filename)

print("Completed storing voltage info in tvoltage.")
print("*****************************************")

# ********** Efield ****************
print("Storing Efield info...")
# Efield has some of the Voltage tree data + FFTs
from scipy import fftpack

# Recalculate Voltage to Efield - just an example, so just multiply by a dumb value
# Here the GRANDlib Efield computation function with antenna model should be used
v2ef = 1.17

# Create the ADC counts tree
tefield = EfieldEventTree()

# fill the tree with every second of generated events - dumb selection
for ev in range(0, event_count, 2):
    tefield.run_number = read_params(reas_input, "RunNumber")
    tefield.event_number = read_params(reas_input, "EventNumber")
    # First data unit in the event
    tefield.first_du = 0
    # As the event time add the current time
    tefield.time_seconds = int(time.mktime(time.gmtime()))
    # Event nanoseconds 0 for now
    tefield.time_nanoseconds = read_params(reas_input, "GPSNanoSecs")
    # Triggered event
    tefield.event_type = 0x8000
    # The number of antennas in the event
    tefield.du_count = len(traces[ev])

    # Loop through the event's traces
    du_id = []
    du_seconds = []
    du_nanoseconds = []
    trigger_position = []
    trigger_flag = []
    atm_temperature = []
    atm_pressure = []
    atm_humidity = []
    trace_xs = []
    trace_ys = []
    trace_zs = []
    fft_mag_xs = []
    fft_mag_ys = []
    fft_mag_zs = []
    fft_phase_xs = []
    fft_phase_ys = []
    fft_phase_zs = []

    for i, trace in enumerate(traces[ev]):
        # print(ev,i, len(trace[0]))

        # Dumb values just for filling
        du_id.append(i)
        du_seconds.append(tefield.time_seconds)
        du_nanoseconds.append(tefield.time_nanoseconds)
        trigger_position.append(i // 2)
        trigger_flag.append(tefield.event_type)
        atm_temperature.append(20 + ev / 2)
        atm_pressure.append(1024 + ev / 2)
        atm_humidity.append(50 + ev / 2)

        # To multiply a list by a number elementwise, convert to a numpy array and back
        # Here a real ComputeEfield() function should be called instead of multiplying adc2v
        # ToDo: better read the Voltage trace from the TTree
        trace_xs.append((np.array(trace[0]) * v2ef).astype(np.float32).tolist())
        trace_ys.append((np.array(trace[1]) * v2ef).astype(np.float32).tolist())
        trace_zs.append((np.array(trace[2]) * v2ef).astype(np.float32).tolist())

        # FFTS
        fft = fftpack.fft(trace[0])
        fft_mag_xs.append(np.abs(fft))
        # ToDo: recall how to calculate the phase easily
        fft_phase_xs.append(np.abs(fft))
        fft = fftpack.fft(trace[1])
        fft_mag_ys.append(np.abs(fft))
        # ToDo: recall how to calculate the phase easily
        fft_phase_ys.append(np.abs(fft))
        fft = fftpack.fft(trace[2])
        fft_mag_zs.append(np.abs(fft))
        # ToDo: recall how to calculate the phase easily
        fft_phase_zs.append(np.abs(fft))

    tefield.du_id = du_id
    tefield.du_seconds = du_seconds
    tefield.du_nanoseconds = du_nanoseconds
    # tefield.trigger_position = trigger_position
    # tefield.trigger_flag = trigger_flag
    # tefield.atm_temperature = atm_temperature
    # tefield.atm_pressure = atm_pressure
    # tefield.atm_humidity = atm_humidity
    # tefield.trace_x = trace_xs
    # tefield.trace_y = trace_ys
    # tefield.trace_z = trace_zs
    # tefield.fft_mag_x = fft_mag_xs
    # tefield.fft_mag_y = fft_mag_ys
    # tefield.fft_mag_z = fft_mag_zs
    # tefield.fft_phase_x = fft_phase_xs
    # tefield.fft_phase_y = fft_phase_ys
    # tefield.fft_phase_z = fft_phase_zs

    tefield.fill()

tefield.write(filename)

print("Completed storing Efield info in tefield.")
print("*****************************************")

# ********** Shower Event Tree ****************
print("Storing shower info...")
# Generation of shower data for each event - this should be reonstruction, but here just dumb values
tshower = ShowerEventTree()

tshower.run_number = tefield.run_number
tshower.event_number = tefield.event_number

tshower.shower_type = read_params(reas_input, "PrimaryParticleType")
tshower.shower_energy = read_params(reas_input, "PrimaryParticleEnergy")
tshower.shower_azimuth = read_params(reas_input, "ShowerAzimuthAngle")
tshower.shower_zenith = read_params(reas_input, "ShowerZenithAngle")
tshower.shower_core_pos = 0
tshower.atmos_model = read_atmos(inp_input)
# tshower.atmos_model_param = np.random.random(3)
tshower.magnetic_field = read_params(reas_input, "MagneticFieldStrength")
# tshower.date = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
# tshower.ground_alt = 3000.0 + np.random.randint(0, 1000)
# tshower.xmax_grams = np.random.random(1) * 500
# tshower.xmax_pos_shc = np.random.random(3)
# tshower.xmax_alt = np.random.randint(3000, 5000) * 1.0
# tshower.gh_fit_param = np.random.random(3)
# tshower.core_time = np.random.randint(0, 10000) * 1.0

tshower.fill()

tshower.write(filename)

print("Completed storing shower info in tshower.")
print("*****************************************")
##############

print("Successfully converted input file", reas_input) 
print("to GRANDroot file", filename)
#python3 ../examples/io/DataReadingExample.py ./000004/SIM000004-000553859-000000001.root