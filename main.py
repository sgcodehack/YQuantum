############# Imports #############
import functions
import matplotlib
import numpy as np
from qiskit.circuit import library as circ_lib

############# Program Start #############
input = "Hello, World!"

binary_arr = functions.get_bits_from_string(input)
binary_str = ''.join(str(bit) for bit in binary_arr) ## Potentially unnecessary

rotated_on_y_theta_arr = []
#[np.pi*(sum(binary_arr)/len(binary_arr))]
for bit in binary_arr:
    temp = np.pi*(bit/len(binary_arr))
    rotated_on_y_theta_arr.append(circ_lib. RYGate(temp))


print(rotated_on_y_theta_arr)


