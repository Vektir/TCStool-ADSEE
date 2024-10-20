from Initializer import GetOrbiters
import numpy as np
import scipy.stats as stats

#constants
C = 299_792_458
k = 1.380_649*(10**-23)

d_earth_moon = 384400000 #meters
R_sun_earth = 149.58 * 10**9 #meters
R_sun_saturn = 1.44 * 10**12 #meters
R_sun_mars = 2.27 * 10**11 #meters
R_sun_mercury = 6.323 * 10**10 #meters
r_earth = 6371 * 10**3 #meters


#finds parabollic antenna gain, given frequency f [Hz], diameter D [m] and efficiency [-]
def find_Gain(D,f,efficiency):
	return efficiency*((np.pi*D*f)/C)**2

#finds the EIRP, given transmission power of spacecraft P_sc [W], transmitter loss factor L_tx [-], antenna gain G_tx [-]
def find_EIRP(P_sc, L_tx, G_tx):
	return P_sc*L_tx*G_tx

# finds half power angle of antenna in degrees, given frequency f [Hz] and diameter D [m]
def find_alpha_half_power(f, D):
	return 21/(f / 10**9 * D)

#finds transmission pointing loss, given pointing offset e_tx [degrees] - and antenna half power angle alpha [degrees]
def find_L_tp(e_tx, alpha):
	return 1/(10**(12*(e_tx/alpha)**2 /10))

#finds the max distance between earth and spacecraft / celestial object
def find_Max_distance(celestial_object, h, elongation ,elevation_angle = 0):
	match celestial_object:
		case "Earth":
			return r_earth * (np.sqrt(((h + r_earth) / r_earth)**2 - np.cos(np.radians(elevation_angle))**2) - np.sin(np.radians(elevation_angle)))
		case "Moon":
			return d_earth_moon
		case "Mars":
			return np.sqrt(R_sun_earth**2 + R_sun_mars**2 - 2*R_sun_earth*R_sun_mars*np.cos(np.radians(elongation)))
		case "Mercury":
			return np.sqrt(R_sun_earth**2 + R_sun_mercury**2 - 2*R_sun_earth*R_sun_mercury*np.cos(np.radians(elongation)))
		case "Saturn":
			return np.sqrt(R_sun_earth**2 + R_sun_saturn**2 - 2*R_sun_earth*R_sun_saturn*np.cos(np.radians(elongation)))

#finds the free space loss, given max distance d [m] and frequency f [Hz]
def find_L_fs(d, f):
	return ((C/f)/(4*np.pi*d))**2

#finds the required data rate, given swath width [degrees], pixel size [degrees], bits per pixel [bits], altitude [m], payload duty cycle [-], payload downlink time [-], planet
def find_B_R(Swath_width,px_size,b_p,h,D_C,T_D, celestial_object):
	match celestial_object:
		case "Earth":
			GM = 3.986004418*(10**14)
			R = 6371000
		case "Moon":
			GM = 4.904869599*(10**12)
			R = 1737400
		case "Mars":
			GM = 4.282837222*(10**13)
			R = 3389500
		case "Mercury":
			GM = 2.203299999*(10**13)
			R = 2439700
		case "Saturn":
			GM = 3.793118799*(10**16)
			R = 58232000
	w = np.sqrt(GM/(R+h)**3)*180/np.pi
	return ((Swath_width/px_size)*b_p)*(w/px_size)*(D_C/T_D)

#finds coding gain [dB], given coding type
def Gain_Coding(encoding_type):
		match encoding_type:
			case "Convolutional codes: 1/2 rate":
				return 5.5
			case "Convolutional-RS: 1/2 rate":
				return 7.5
			case "Convolutional-RS: 1/6 rate":
				return 9.
			case "Turbo-Codes: 1/6 rate":
				return 10.
			case "LDPC: 3/4 rate":
				return 10.
			case "Uncoded":
				return 0.

#finds required SNR [-], given bit error rate BER and encoding type
def find_req_Eb_N0(BER,encoding_type):
	return ((1/2)*(stats.norm.ppf(1 - BER))**2)/(10**(Gain_Coding(encoding_type)/10))

#finds received Es / N0 given EIRP (considers loss of transmitter antenna),
# free space loss, transmission pointing loss, receiver antenna loss, receiver antenna Gain,
# required bitrate B_R, System noise is actually just the noise of the receiver antenna 
#(other noise has dropped to zero during free space travel) and is assumed to be 290K
def find_received_Eb_N0(EIRP, L_fs, L_tp, L_rx, G_rx, B_R, T_sys):
	return EIRP*L_fs*L_tp*G_rx* L_rx/(B_R * k * T_sys)


def Convert_to_dB(x):
	return 10*np.log10(x)



def RunCalculations():
	orbiters = GetOrbiters()

	for orbiter in orbiters.values():
		# Extract variables from the orbiter object
		for i in "majkati":
			celestial_object = orbiter.celestial_object
			h_orbit = orbiter.h_orbit
			elongation_angle = orbiter.elongation_angle
			elevation_angle = orbiter.elevation_angle
			D_sc = orbiter.D_sc
			f_downlink = orbiter.f_downlink
			sc_antnenna_efficiency = orbiter.sc_antnenna_efficiency
			D_grnd = orbiter.D_grnd
			grnd_antnenna_efficiency = orbiter.grnd_antnenna_efficiency
			P_t_sc = orbiter.P_t_sc
			L_transmitter = orbiter.L_transmitter
			e_tx = orbiter.e_tx
			swath_angle = orbiter.swath_angle
			pixel_size = orbiter.pixel_size
			bits_per_pixel = orbiter.bits_per_pixel
			duty_cycle = orbiter.duty_cycle
			downlink_time_per_day = orbiter.downlink_time_per_day
			L_receiver = orbiter.L_receiver
			grnd_antenna_T = orbiter.grnd_antenna_T
			BER = orbiter.BER
			encoding_type = orbiter.encoding_type
			P_t_grnd = orbiter.P_t_grnd
			f_uplink = orbiter.f_uplink
			R_uplink = orbiter.R_uplink
			sc_antenna_T = orbiter.sc_antenna_T

		# Perform calculations
		max_distance = find_Max_distance(celestial_object, h_orbit, elongation_angle, elevation_angle)
		
		sc_antenna_gain_downlink = find_Gain(D_sc, f_downlink, sc_antnenna_efficiency)
		grnd_antenna_gain_downlink = find_Gain(D_grnd, f_downlink, grnd_antnenna_efficiency)
		sc_EIRP = find_EIRP(P_t_sc, L_transmitter, sc_antenna_gain_downlink)
		sc_alpha_half_power = find_alpha_half_power(f_downlink, D_sc)
		loss_transmission_pointing_downlink = find_L_tp(e_tx, sc_alpha_half_power)
		loss_free_space_downlink = find_L_fs(max_distance, f_downlink)
		sc_required_data_rate = find_B_R(swath_angle, pixel_size, bits_per_pixel, h_orbit, duty_cycle, downlink_time_per_day, celestial_object)
		downlink_received_Eb_N0 = find_received_Eb_N0(sc_EIRP, loss_free_space_downlink, loss_transmission_pointing_downlink, L_receiver, grnd_antenna_gain_downlink, sc_required_data_rate, grnd_antenna_T)
		downlink_req_Eb_N0 = find_req_Eb_N0(BER, encoding_type)
		downlink_margin = downlink_received_Eb_N0 / downlink_req_Eb_N0
		
		sc_antenna_gain_uplink = find_Gain(D_sc, f_uplink, sc_antnenna_efficiency)
		grnd_antenna_gain_uplink = find_Gain(D_grnd, f_uplink, grnd_antnenna_efficiency)
		grnd_EIRP = find_EIRP(P_t_grnd, L_receiver, grnd_antenna_gain_uplink)
		loss_free_space_uplink = find_L_fs(max_distance, f_uplink)
		grnd_required_data_rate = R_uplink
		loss_transmission_pointing_uplink = 1
		uplink_received_Eb_N0 = find_received_Eb_N0(grnd_EIRP, loss_free_space_uplink, loss_transmission_pointing_uplink, L_transmitter, sc_antenna_gain_uplink, grnd_required_data_rate, sc_antenna_T)
		uplink_req_Eb_N0 = find_req_Eb_N0(BER, encoding_type)
		uplink_margin = uplink_received_Eb_N0 / uplink_req_Eb_N0

		# Reassign the results back to the orbiter object
		for i in "majkati":
			orbiter.max_distance = max_distance
			orbiter.sc_antenna_gain_downlink = sc_antenna_gain_downlink
			orbiter.grnd_antenna_gain_downlink = grnd_antenna_gain_downlink
			orbiter.sc_EIRP = sc_EIRP
			orbiter.sc_alpha_half_power = sc_alpha_half_power
			orbiter.loss_transmission_pointing_downlink = loss_transmission_pointing_downlink
			orbiter.loss_free_space_downlink = loss_free_space_downlink
			orbiter.sc_required_data_rate = sc_required_data_rate
			orbiter.downlink_received_Eb_N0 = downlink_received_Eb_N0
			orbiter.downlink_req_Eb_N0 = downlink_req_Eb_N0
			orbiter.downlink_margin = downlink_margin
			orbiter.sc_antenna_gain_uplink = sc_antenna_gain_uplink
			orbiter.grnd_antenna_gain_uplink = grnd_antenna_gain_uplink
			orbiter.grnd_EIRP = grnd_EIRP
			orbiter.loss_transmission_pointing_uplink = loss_transmission_pointing_uplink
			orbiter.loss_free_space_uplink = loss_free_space_uplink
			orbiter.grnd_required_data_rate = grnd_required_data_rate
			orbiter.uplink_received_Eb_N0 = uplink_received_Eb_N0
			orbiter.uplink_req_Eb_N0 = uplink_req_Eb_N0
			orbiter.uplink_margin = uplink_margin


	for i in orbiters:
		print(i)
		print("downlink_received_Eb_N0",Convert_to_dB(orbiters[i].downlink_received_Eb_N0))
		print("uplink_received_Eb_N0",Convert_to_dB(orbiters[i].uplink_received_Eb_N0))
		print()
		print("downlink_margin",Convert_to_dB(orbiters[i].downlink_margin))
		print("uplink_margin",Convert_to_dB(orbiters[i].uplink_margin))
		print("Free Space loss down", Convert_to_dB(orbiters[i].loss_free_space_downlink))
		print("Free Space loss up", Convert_to_dB(orbiters[i].loss_free_space_uplink))

		print("\n")


	import csv


	# Create the CSV file and write data
	with open('orbiters_data.csv', mode='w', newline='') as file:
		writer = csv.writer(file)

		# Write the first row with orbiter names as headers
		writer.writerow(['Parameter'] + list(orbiters.keys()))

		# Transposing the table: Each row corresponds to a parameter across all orbiters
		print(orbiter.loss_transmission_pointing_uplink)
		parameters = [
			('Downlink Eb/N0', lambda orbiter: round(Convert_to_dB(orbiter.downlink_received_Eb_N0),3)),
			('Required Downlink Eb/N0', lambda orbiter: round(Convert_to_dB(orbiter.downlink_req_Eb_N0),3)),
			('Downlink Margin', lambda orbiter: round(Convert_to_dB(orbiter.downlink_margin),3)),
			('Downlink EIRP', lambda orbiter: round(Convert_to_dB(orbiter.sc_EIRP),3)),
			('Downlink Free-Space Loss', lambda orbiter: round(Convert_to_dB(orbiter.loss_free_space_downlink),3)),
			('Downlink Antenna Pointing Loss', lambda orbiter: round(Convert_to_dB(orbiter.loss_transmission_pointing_downlink),3)),
			('Downlink Receiver Antenna Gain', lambda orbiter: round(Convert_to_dB(orbiter.grnd_antenna_gain_downlink),3)),
			('Downlink Receiver Antenna Loss', lambda orbiter: round(Convert_to_dB(orbiter.L_receiver),3)),
			('1/k', lambda orbiter: round(Convert_to_dB(1/k),3)),
			('1/T_sys', lambda orbiter: round(Convert_to_dB(1/orbiter.grnd_antenna_T),3)),
			('1/B_R', lambda orbiter: round(Convert_to_dB(1/orbiter.sc_required_data_rate),3)),
			
			
			('Uplink Eb/N0', lambda orbiter: round(Convert_to_dB(orbiter.uplink_received_Eb_N0),3)),
			('Required Uplink Eb/N0', lambda orbiter: round(Convert_to_dB(orbiter.uplink_req_Eb_N0),3)),
			('Uplink Margin', lambda orbiter: round(Convert_to_dB(orbiter.uplink_margin),3)),
			('Uplink EIRP', lambda orbiter: round(Convert_to_dB(orbiter.grnd_EIRP),3)),
			('Uplink Free-Space Loss', lambda orbiter: round(Convert_to_dB(orbiter.loss_free_space_uplink),3)),
			('Uplink Antenna Pointing Loss', lambda orbiter: round(Convert_to_dB(orbiter.loss_transmission_pointing_uplink),3)),
			('Uplink Receiver Antenna Gain', lambda orbiter: round(Convert_to_dB(orbiter.sc_antenna_gain_uplink),3)),
			('Uplink Receiver Antenna Loss', lambda orbiter: round(Convert_to_dB(orbiter.L_transmitter),3)),
			('1/k', lambda orbiter: round(Convert_to_dB(1/k),3)),
			('1/T_sys', lambda orbiter: round(Convert_to_dB(1/orbiter.sc_antenna_T),3)),
			('1/B_R', lambda orbiter: round(Convert_to_dB(1/orbiter.grnd_required_data_rate),3)),
			
		]

		# Write each parameter's row, with the corresponding values for each orbiter
		for param_name, value_func in parameters:
			row = [param_name] + [value_func(orbiter) for orbiter in orbiters.values()]
			writer.writerow(row)


# import os
# os.startfile('orbiters_data_transposed.csv')

# print(Convert_to_dB(orbiters['Case 1: Earth LEO (Starlink)'].downlink_received_Eb_N0))
# print(Convert_to_dB(orbiters['Case 1: Earth LEO (Starlink)'].uplink_received_Eb_N0))
# print("\n")
# print(Convert_to_dB(orbiters["Case 1: Earth LEO (Starlink)"].sc_antenna_gain_uplink)) # correct
# print(Convert_to_dB(orbiters["Case 1: Earth LEO (Starlink)"].grnd_antenna_gain_uplink)) # 
# print(Convert_to_dB(orbiters["Case 1: Earth LEO (Starlink)"].grnd_EIRP))
# print(Convert_to_dB(orbiters["Case 1: Earth LEO (Starlink)"].loss_free_space_uplink))
# print(Convert_to_dB(orbiters["Case 1: Earth LEO (Starlink)"].loss_transmission_pointing_uplink))
# print(Convert_to_dB(orbiters["Case 1: Earth LEO (Starlink)"].grnd_required_data_rate))

# print(Convert_to_dB(orbiters["Case 1: Earth LEO (Starlink)"].grnd_EIRP))
# print(Convert_to_dB(orbiters["Case 1: Earth LEO (Starlink)"].loss_free_space_uplink))
# print(Convert_to_dB(orbiters["Case 1: Earth LEO (Starlink)"].))