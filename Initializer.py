import pandas as pd
import numpy as np

class Orbiter:
	sc_antenna_gain_downlink = 0
	grnd_antenna_gain_downlink = 0
	sc_antenna_gain_uplink = 0
	grnd_antenna_gain_uplink = 0
	sc_EIRP = 0
	grnd_EIRP = 0
	sc_alpha_half_power = 0
	grnd_alpha_half_power = 0
	loss_transmission_pointing_downlink = 0
	loss_transmission_pointing_uplink = 0
	max_distance = 0
	loss_free_space_downlink = 0
	loss_free_space_uplink = 0
	sc_required_data_rate = 0
	grnd_required_data_rate = 0
	gain_coding = 0
	downlink_received_Eb_N0 = 0
	uplink_received_Eb_N0 = 0
	downlink_req_Eb_N0 = 0
	uplink_req_Eb_N0 = 0
	downlink_margin = 0
	uplink_margin = 0



	def __init__(self, P_total, P_t_sc, P_t_grnd, L_transmitter, L_receiver, f_downlink, f_up_down_ration, D_sc, D_grnd,
		h_orbit, elongation_angle, e_tx, R_uplink, swath_angle, pixel_size, bits_per_pixel, duty_cycle, 
		downlink_time_per_day, encoding_type, BER, sc_antnenna_efficiency, grnd_antnenna_efficiency, sc_antenna_T,
		grnd_antenna_T, celestial_object, elevation_angle): 
		
		self.P_total = P_total
		self.P_t_sc = P_t_sc
		self.P_t_grnd = P_t_grnd
		self.L_transmitter = L_transmitter
		self.L_receiver = L_receiver
		self.f_downlink = f_downlink
		self.f_uplink = f_downlink * f_up_down_ration
		self.f_up_down_ration = f_up_down_ration
		self.D_sc = D_sc
		self.D_grnd = D_grnd
		self.h_orbit = h_orbit
		self.elongation_angle = elongation_angle
		self.e_tx = e_tx
		self.R_uplink = R_uplink
		self.swath_angle = swath_angle
		self.pixel_size = pixel_size
		self.bits_per_pixel = bits_per_pixel
		self.duty_cycle = duty_cycle
		self.downlink_time_per_day = downlink_time_per_day
		self.encoding_type = encoding_type
		self.BER = BER
		self.sc_antnenna_efficiency = sc_antnenna_efficiency
		self.grnd_antnenna_efficiency = grnd_antnenna_efficiency
		self.sc_antenna_T = sc_antenna_T
		self.grnd_antenna_T = grnd_antenna_T
		self.celestial_object = celestial_object
		self.elevation_angle = elevation_angle
 
	def PrintAll(self):
		print("Total spacecraft power", self.P_total)
		print("Transmitter power (spacecraft)", self.P_t_sc)
		print("Transmitter power (ground station)", self.P_t_grnd)
		print("Loss factor transmitter", self.L_transmitter)
		print("Loss factor receiver", self.L_receiver)
		print("Downlink frequency", self.f_downlink)
		print("Turn around ratio (uplink/downlink frequency)", self.f_up_down_ration)
		print("Antenna diameter spacecraft", self.D_sc)
		print("Antenna diameter ground station", self.D_grnd)
		print("Orbit altitude", self.h_orbit)
		print("Elongation angle", self.elongation_angle)
		print("Pointing offset angle (spacecraft)", self.e_tx)
		print("Required uplink data rate", self.R_uplink)
		print("Payload swath width angle", self.swath_angle)
		print("Payload pixel size", self.pixel_size)
		print("Payload bits per pixel", self.bits_per_pixel)
		print("Payload duty cycle (fraction)", self.duty_cycle)
		print("Payload downlink time per day (fraction)", self.downlink_time_per_day)
		print("Modulation/coding type", self.encoding_type)
		print("Required BER", self.BER)
		print("Efficiency of sc antenna", self.sc_antnenna_efficiency)
		print("Efficiency of ground antenna", self.grnd_antnenna_efficiency)
		print("Temperature of sc antenna", self.sc_antenna_T)
		print("Temperature of ground antenna", self.grnd_antenna_T)
		print("Celestial object to be orbited", self.celestial_object)
		print("Elevation angle", self.elevation_angle)



def GetOrbiters():
	df = pd.read_csv('Better TCS data.csv', index_col=0)
	orbiters = {}
	for i in range(len(df.columns) - 1):
		name = list(df.columns)[i+1]
		P_total = float(df[name]["Total spacecraft power"])
		P_t_sc = float(df[name]["Transmitter power (spacecraft)"])
		P_t_grnd = float(df[name]["Transmitter power (ground station)"])
		L_transmitter = float(df[name]["Loss factor transmitter"])
		L_receiver = float(df[name]["Loss factor receiver"])
		f_downlink = float(df[name]["Downlink frequency"]) 
		f_downlink = f_downlink * 10**9  # In GHz
		f_up_down_ration = float(df[name]["Turn around ratio (uplink/downlink frequency)"])
		D_sc = float(df[name]["Antenna diameter spacecraft"])
		D_grnd = float(df[name]["Antenna diameter ground station"])
		h_orbit = float(df[name]["Orbit altitude"])
		h_orbit= h_orbit* 1000  # in km
		try:
			elongation_angle = float(df[name]["Elongation angle"]) # in degrees
		except ValueError:
			elongation_angle = -1
		e_tx = float(df[name]["Pointing offset angle (spacecraft)"])  # in degrees
		R_uplink = float(df[name]["Required uplink data rate"])
		swath_angle = float(df[name]["Payload swath width angle"])  # in degrees
		pixel_size = float(df[name]["Payload pixel size"])  # in arcminutes
		pixel_size = pixel_size / 60 #in degrees
		bits_per_pixel = float(df[name]["Payload bits per pixel"])
		duty_cycle = float(df[name]["Payload duty cycle (fraction)"])
		downlink_time_per_day = float(df[name]["Payload downlink time per day (fraction)"])
		encoding_type = df[name]["Modulation/coding type"]
		BER = float(df[name]["Required BER"])
		sc_antnenna_efficiency = float(df[name]["Efficiency of sc antenna"])
		grnd_antnenna_efficiency = float(df[name]["Efficiency of ground antenna"])
		sc_antenna_T = float(df[name]["Temperature of sc antenna"])
		grnd_antenna_T = float(df[name]["Temperature of ground antenna"])
		celestial_object = df[name]["Celestial object to be orbited"]
		try:
			elevation_angle = float(df[name]["Elevation angle"])  # in degrees
		except ValueError:
			elevation_angle = -1
			print("ooba gooba")
		

		#allthings = [P_total, P_t_sc, P_t_grnd, L_transmitter, L_receiver, f_downlink, f_up_down_ration, D_sc, D_grnd, h_orbit, elongation_angle, e_tx, R_uplink, swath_angle, pixel_size, bits_per_pixel, duty_cycle, downlink_time_per_day, encoding_type, BER, sc_antnenna_efficiency, grnd_antnenna_efficiency, sc_antenna_T, grnd_antenna_T, celestial_object, elevation_angle]
		orbiterrr = Orbiter(P_total, P_t_sc, P_t_grnd, L_transmitter, L_receiver, f_downlink, f_up_down_ration, D_sc, D_grnd, h_orbit, elongation_angle, e_tx, R_uplink, swath_angle, pixel_size, bits_per_pixel, duty_cycle, downlink_time_per_day, encoding_type, BER, sc_antnenna_efficiency, grnd_antnenna_efficiency, sc_antenna_T, grnd_antenna_T, celestial_object, elevation_angle)
		
		orbiters.setdefault(name, orbiterrr) 

	return orbiters




#orbiters["Case 1: Earth LEO (Starlink)"].PrintAll()





#P_total - total spacecraft power
#P_t_sc - power for the transmitter on spacecraft
#P_t_grnd - power for the transmitter on the ground
#L_transmitter - transmitter loss factor(doesnt matter earth or sc, not specified, in any case in formula they are multiplied)
#L_receiver - receiver loss factor --"--
#f_downlink - downlink frequency
#f_uplink - uplink frequency
#f_up_down_ration - uplink/downlink frequency turnaround ratio
#D_sc - spacecraft antenna diameter
#D_grnd - ground antenna diameter
#h_orbit - orbit height
#elongation_angle - angle elongation
# e_tx - pointing offset sc
# R_uplink - uplink data rate
# swath_angle - swath angle of camera
# pixel_size - pixel size in arcminutes
# bits_per_pixel - bits per pixel
# duty_cycle - amount og time working vs not working
# downlink_time_per_day - downlink time per day
# encoding_type - encoding type
# BER - bit error rate 
# sc_antnenna_efficiency - spacecraft antenna efficiency
# grnd_antnenna_efficiency - ground antenna efficiency
# sc_antenna_T - spacecraft antenna temperature
# grnd_antenna_T - ground antenna temperature
# celestial_object - celestial object (Earth, Venus, ...)
# elevation_angle - elevation angle