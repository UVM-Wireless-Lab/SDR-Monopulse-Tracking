import numpy as np
import matplotlib.pyplot as plt 


def calcTheta(phase,freq,d):
    arcsin_arg = (phase)*3E8/(2*np.pi*freq*d)
    calc_theta = np.rad2deg(np.arcsin(arcsin_arg))
    return calc_theta

freq = 1.83e9
wvl = 3e8/freq
d = 1*wvl#0.09 #0.17

# Notes:
# For signal generator testing signal seen ~1.82999628GHz
# 0712_HP settings - sg power of 12dBm Rx gain of 0dB average of 6

# x = calcTheta(np.load("0715_Corrected_Tx_xout.npy"),freq=freq,d=d)
# Dat = np.load("0715_Corrected_Tx_data.npy")

Dat = np.load("/home/snow_lab/Rye Work/0826_1lambda/15deg_g55_data.npy")
x = calcTheta(Dat[0,:],freq=freq,d=d)


# RatMag = 10**(0.1*Dat[1,:])
# theta = np.arccos(1/(2*np.pi)*np.arctan(RatMag))
y1 = Dat[1,:]   # Diff

y2 = Dat[2,:]  #Sum

y3 = Dat[3,:]   # Ratio

y4 = np.rad2deg(Dat[4,:])#np.cos(Dat[3,:])   # Phase

#fname = "/home/snow_lab/Rye Work/0805_Tests/Angle_cal_curves/0805_post_0degXXXXX"
# #data = np.column_stack((x,y1,y2,y3,y4))
# np.savetxt(f"{fname}.csv", Dat, delimiter=',', header='Steering Angle,Re{Ratio},Im{Ratio},Full Ratio,Phase Shift', comments='', fmt='%d')
#np.save(f"{fname}.npy",Dat)


fig,(ax1,ax2,ax3,ax4)= plt.subplots(4,1)
ax1.scatter(x,y1,label = "|Diff|")
ax2.scatter(x,y2,label = "|Sum|")
ax3.scatter(x,y3,label = "|Im{d/s}|")
ax4.scatter(x,y4,label = "phase")
ax1.legend()
ax2.legend()
ax3.legend()
ax4.legend()
#ax1.set_title("|Im{d/s}|")
#ax1.set_title("Re{Ratio}")
ax1.set_ylabel("Relative Amplitude [dB]")
#ax2.set_title("|Re{d/s}|")
#ax2.set_title("Im{Ratio}")
ax2.set_ylabel("Relative Amplitude [dB]")
#ax3.set_title("|d/s| Direct")
ax3.set_ylabel("Relative Amplitude [dB]")
ax4.set_xlabel("Steering Angle [Degrees]")

#ax4.set_title("|d/s| from IQ")
ax4.set_ylabel("Relative Amplitude [dB]")
# ax4.set_title("Phase Difference")
# ax4.set_ylabel("Phase Difference [rad]")
# fig1,(ax1,ax2) = plt.subplots(2,1)
# ax1.scatter(x,y2)
# ax2.scatter(x,y4)
# ax1.set_title("Im{Ratio}")
# ax1.set_ylabel("Relative Amplitude [dB]")

# ax2.set_title("Diff-Sum Phase Difference")
# ax2.set_ylabel("Phase [degrees]")
# ax2.set_xlabel("Steering Angle [Degrees]")

# DatA = np.load("Tape_A.npy")
# DatB = np.load("Tape_B.npy")
# DatC = np.load("Tape_B_Ant2.npy")
# fig3,ax31 = plt.subplots(1,1)
# ax31.scatter(calcTheta(DatA[0,:],freq=freq,d=d),DatA[3,:],label = "Left")
# ax31.scatter(calcTheta(DatB[0,:],freq=freq,d=d),DatB[3,:],label = "Right")
# ax31.scatter(calcTheta(DatC[0,:],freq=freq,d=d),DatC[3,:],label = "Right, new ant")
# ax31.legend()
plt.show()


