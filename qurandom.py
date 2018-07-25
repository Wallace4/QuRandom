#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  qurandom.py
#  
#  Copyright 2018 Michele De Quattro <mikde4@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

from projectq.ops import H, Measure
from projectq import MainEngine
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

#params
N = 10000
n_digits = 3

def qurandom (quantum_engine):
	qubit = quantum_engine.allocate_qubit()		#allocate the qubit
	H | qubit									#use the H port to give 1/2 of probability to be either 0 or 1
	Measure | qubit								#mmeasure the qubit and let him collapse
	random_number = int(qubit)
	return random_number

def get_random_number (n):						#n is the number of binary digits we want the number to be
	random_number = 0
	quantum_engine = MainEngine()				#creation of the Quantum Engine
	for i in range(n):
		random_number = random_number << 1		#move the last generate 1 or 0 into a more significant digit
		quvalue = qurandom(quantum_engine)		#generation of 0 or 1
		random_number += quvalue				#the last digit (the unit) is now the random generated numer
	quantum_engine.flush()
	return random_number

def optimize_plot(iteration, lim, multiplier, global_lim):	#this is a function that help visualize the graph in a log scale
															#taken from https://github.com/SqrtMinusOne/Euler-s-number/ and thanks to the author
	if iteration < lim and iteration % multiplier == 0:
		return True
	elif lim < global_lim:
		return optimize_plot(iteration, lim * 2, multiplier * 2, global_lim)
	else:
		return False

def filewriter ():						#the function that calculate all the numbers and write them in the Histogram
	count_list [] #list where i put all the random generated numbers
	
	fig = plt.figure()
	
	total_axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
	
	data = range (2**n_digits)			#the max random number that can be generated is 2^n_digits
	data = np.array(data)
	
	d = np.diff(np.unique(data)).min()
	left_of_first_bin = data.min() - float(d)/2		#all this is black magic to align the hist better
	right_of_last_bin = data.max() + float(d)/2
	
	for i in range(N):
		qrn = get_random_number(n_digits)			#generation of the number
		
		count_list.append(qrn)						#append the number in the list
		
		is_time_for_show = optimize_plot(i, 20, 1, N)	#se if the number is high enough to change the rateo of visualization
		
		if (is_time_for_show or i == N-1): #Histogram generation
			total_axes.clear()
			total_axes.hist(count_list, np.arange(left_of_first_bin, right_of_last_bin + d, d), color='purple')
			total_axes.set_title("Number of generations = {0}".format(i))
		
			plt.savefig('figures/fig{0:5}'.format(i))	#save each frame into a different image to be then converted in a gif
		
	plt.show()

filewriter ()			#call of the main function
