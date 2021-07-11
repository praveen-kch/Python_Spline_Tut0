''' ***********************************************************************************
The Python Script to Compute Area Properties of a Ship Section

Area Properties to be computed:
-------------------------------

    >> Immersed Areas of section at various drafts
    >> Vertical Moments of the section at various drafts

************************************************************************************'''

''' -----------------------------------------------------------------------------------
A Quick Note on Comments:
------------------------------------------------------------------------------------'''

''' Green Font Text Written between Triple Quotes are Main Comments '''
# Yellow font text lines followed by # are Secondary Comments
''' Both the above types of comments are not part of executed script
    Comments are just to help readers understand the code / communicate with the reader '''

''' ************************************************************************************
The SCript can be divided into four main parts:
*************************************************************************************'''

# PArt 1 : Reading the Section Curve Point Data from the file
# PArt 2 : Fit spline curve to given points and plot the section
# PArt 3 : Compute and plot Immersed Section Area vs Draft
# PArt 4 : Compute and Plot vertical moments of the immersed section vs draft

''' ------------------------------------------------------------------------------------
PArt 1 : Reading the Section Curve Point Data from the file
-------------------------------------------------------------------------------------'''

# Just Prin a Status Message on console
print("\nReading Section Geometry Data From the File ...")

# Open File to read the Section Geometry
fp=open("sec_geom.txt")

# Read all lines from the file into the list named "lines"
# "lines" is a List of Strings
# Each string in the list contains each line from the file
lines=fp.readlines()

# Now that we finished reading the file lets close it
fp.close()

# Count the number of lines in the file and from that compute the no of points on the curve
# Total No of Lines = No of Elements in the list "lines" = len(lines)
# substract 2 from total number of lines to get total number of points on the curve
# Because first two lines in the sec_geom.txt file are headers
# They dont contain any curve point offsets
nPts=len(lines)-2
print('The no of Points=',nPts)

# Import Numpy Module as "np",
# Numpy is required to create arrays in python
import numpy as np

# Create Arrays to store curve point offsets
z=np.zeros(nPts)    # Z ordinates of curvve points are stored in this array as floating point numbers
y=np.zeros(nPts)    # Y ordinates of curve points are stored in this array as floating point numbers

# Process the list "lines" which contians the read lines from the file
# For each line number, i =2 to 2+npts
# Do the following ...
for i in range(2,nPts+2,1):

    # Each line in the file/list is a string with two numbers seperated by a tab
    # Split each string in "lines", into two sub strings, by identifying Tab as a seperator
    offsets=lines[i].split('\t')

    # the variable "offsets" is a list of two strings
    # First String has Z ordinate of a curve point
    # Second string has Y ordinate of a curve point
    z[i-2]=float(offsets[0]) # Convert the number in string format to a float data type
    y[i-2]=float(offsets[1]) # Convert the number in string format to a float data type

    # Print each point Cordinates on to the console
    print("Curve point %4d : (%10.5f,%10.5f)"%(i-2,z[i-2],y[i-2]))

    # The For Loop Ends Here
    # PArt 1 Ends Here ..............................................................................

''' -----------------------------------------------------------------------------------------------
PArt 2 : Fit spline curve to given points and plot the section
------------------------------------------------------------------------------------------------'''

# Print the status Message
print("\n Computing the Spline Fit ... ")

# Import the submodule "interpolate" from scipy
# this module contains functions to fit and evaluate splines
from scipy import interpolate

# Fit a Spline Curve to the curve point data in (z,y)
# y=f(z)
Spline_fit_curve = interpolate.splrep(z,y,k=2,s=0.1)

#----------------------------------------------------------------------
# Interpolate Offsets using the spline fit data in "Spline_fit_curve"
#----------------------------------------------------------------------
# zSpl is an array of 100 Z ordinates evenly spaced along the height of the curve
zSpl = np.linspace(z[0],z[-1],100,endpoint=True)

# Use "splev" function to evaluate the "Spline_fit_curve"
# Interpolate Y ordinates for each Z ordinate in the array "zSpl"
ySpl=interpolate.splev(zSpl,Spline_fit_curve,der=0)

# der=0 means no derivative of y is to be computed

# Plotting the Spline Fit on the Curve Points
import matplotlib.pyplot as plt
plt.figure()
plt.plot(y,z,'or',ySpl,zSpl,'-b')
plt.legend(['Curve Points','Spline Fit'])
plt.axis("square")
plt.xlabel("y")
plt.ylabel("z")
plt.title("section curve")

# YOu can Plau with the order/degree of the spline fit "k" and the smoothness tolerance "s"
# choose a set of (k,s) that best fits the curve points ...
# End of PArt 2 .......................

''' ----------------------------------------------------------------------------------------------
PART 3 : Compute and plot Immersed Section Area vs Draft
-----------------------------------------------------------------------------------------------'''

# Print the status message
print("\nComputing the Immersed Section Areas ...")

# Create an array of Drafts
# Range of Drafts starts from 0 and increment in steps of 0.5 till maximum Z value
drafts=np.arange(0,max(z),0.5)

# Create an array to store the Immersed Areas at each draft
Areas = np.zeros((len(drafts)))

# For each draft in the array of drafts compute the immersed section area
for i in range(len(drafts)):

    # Use Function "splint" to integrate "Spline_fit_curve"
    # Limits of integration from z=0 --> z=drafts[i]
    # Area of complete section = 2* Area of Half Section
    Areas[i]=2*interpolate.splint(0,drafts[i],Spline_fit_curve)

    # Print the Immersed Section Area at each draft
    print("At Draft %10.5f : Immersed Sec. Area = %10.5f"%(drafts[i],Areas[i]))

    # the for loop ends here indentation stops from here

# Plot the Section Area vs draft
plt.figure()
plt.plot(Areas,drafts,'-g')
plt.xlabel("Area")
plt.ylabel("Draft")
plt.title("Immersed Section Area")


# End of PArt 3 .......................................................................

''' ------------------------------------------------------------------------------------
Part 4: Compute and Plot vertical moments of the immersed section vs draft
-------------------------------------------------------------------------------------'''

# Print the Status Message
print("\nComputing the Vertical Moments ...")

# Create an array to store vertical Moments at each draft
VM = np.zeros((len(drafts)))

# Vertical Moment of Horizontal Strip of height "dz" is given by
# dVM = y*z*dz at point (z,y)
# Vertical Moment, VM is computed about Base Line i.e., about line z=0
# Compute : dVM/dz = y*z @ each curve point (z,y)
dVM_dz = np.zeros(nPts)
dVM_dz = y*z

# Fit Spline Function for "dVM/dz = f(z)"
Spline_fit_dvm_dz = interpolate.splrep(z,dVM_dz,k=3)

# For each draft compute the verical moment
for i in range(len(drafts)):

    # Use Function splint to integrate "Spline_fit_dVM_dz"
    # Limits of integration from z=0 --> to z=drafts[i]
    # VM of complete section = 2 * VM of Half Section
    VM[i]=2*interpolate.splint(0,drafts[i],Spline_fit_dvm_dz)

    # Printing the Immersed Section Area at Each Draft
    print("At Draft %10.5f : Vertical Moment (abt BL) = %10.5f"%(drafts[i],VM[i]))

    # The for loop ends here

plt.figure()
plt.plot(VM,drafts,'-g')
plt.xlabel("VM")
plt.ylabel("Drafts")
plt.title("Vertical Moment about Base Line (Z=0) ")
plt.show()


# The PArt 4 is completed ................................................................

# END OF SCRIPT --------------------------------------------------------------------------











































