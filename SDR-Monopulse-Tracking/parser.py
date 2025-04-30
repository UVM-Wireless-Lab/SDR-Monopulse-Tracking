import numpy as np
import matplotlib.pyplot as plt 


def calcTheta(phase,freq,d):
    # angle is theta = arcsin(c*deltaphase/(2*pi*f*d)
    arcsin_arg = np.deg2rad(phase)*3E8/(2*np.pi*freq*d)
    #arcsin_arg = max(min(1, arcsin_arg), -1)     # arcsin argument must be between 1 and -1, or numpy will throw a warning
    calc_theta = np.rad2deg(np.arcsin(arcsin_arg))
    return calc_theta

freq = 1.83e9
d = 0.17

# x4 = np.load('0807phase_xout.npy')
# y4 = np.load('0807phase_yout.npy')

x1 = calcTheta(np.load('0807Sum_xout.npy'),freq,d)
y1 = np.load('0807Sum_yout.npy')

x2 = calcTheta(np.load('0807Diff_xout.npy'),freq,d)
y2 = np.load('0807Diff_yout.npy')

x3 = calcTheta(np.load('0807Full_xout.npy'),freq,d)
y3 = np.load('0807Full_yout.npy')

x4 = calcTheta(np.load('0807phase_xout.npy'),freq,d)
y4 = np.load('0807phase_yout.npy')*(180/np.pi)

# data = np.column_stack((x1,y1,y2,y3,y4))
# np.savetxt('0807_Sweep_Data.csv', data, delimiter=',', header='Phase,Sum,Difference,Ratio,Phase Shift', comments='', fmt='%d')

fig,(ax1,ax2,ax3,ax4)= plt.subplots(4,1)
ax1.scatter(x1,y1)
ax2.scatter(x2,y2)
ax3.scatter(x3,y3)
ax4.scatter(x4,y4)

ax1.set_title("Sum")
ax1.set_ylabel("Relative Amplitude [dB]")
ax2.set_title("Difference")
ax2.set_ylabel("Relative Amplitude [dB]")
ax3.set_title("Ratio")
ax3.set_ylabel("Relative Amplitude [dB]")
ax4.set_xlabel("Relative Steering Angle [Degrees]")

ax4.set_title("Phase Difference")
ax4.set_ylabel("Phase Difference [rad]")

# ax1= plt.subplot(3,1,1)
# ax2= plt.subplot(3,1,2)
# ax3= plt.subplot(3,1,3)
# # ax.scatter(x,y)
# ax1.scatter(x1,y1)
# ax2.scatter(x2,y2)
# ax1.set_title("Del")
# ax2.set_title("Sum")

# ax.set_title("C/SB vs Hack RF Gain, Amp ")
# ax.set_xlabel("Hack RF Gain [dB]")
# ax.set_ylabel("C/SB in Transmitted Signal [dB]")

plt.show()


