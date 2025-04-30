"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt

class Tracker(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Controller to track signal by minimizing monopulse ratio. Input 1 should be the log magnitude of the monopulse
    ratio and Input 2 the phase shift between difference and sum. Input message (Ts) determines when
    controller is updated and should be polled regularly, actual message content is irrelevant. 
    Output phase is in radians and computed tracking angle in degrees, formatted for az/el sink.

    \n Inputs:
    \n Track - Boolean to activate/deactivate tracking
    \n Spacing - Element spacing in wavelengths 
    \n Tolerance - Phase tolerance for target lock"""

    def __init__(self, Track = False,Spacing = 0.5,Tolerance = 0.005,alpha = 0.1 ):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Tracking Controller',   # will show up in GRC
            in_sig=[np.float32,np.float32],
            out_sig=None
        )

        self.message_port_register_out(pmt.intern('phase'))
        self.message_port_register_out(pmt.intern('az'))
        self.message_port_register_out(pmt.intern('Lock'))
        self.message_port_register_out(pmt.intern('steer_angle'))

        self.message_port_register_in(pmt.intern('Ts'))

        self.set_msg_handler(pmt.intern('Ts'), self.handle_msg)

        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.Track = Track
        self.phase = 0          # Phase shift applied to steer beam
        self.Lock = False
        self.Spacing = Spacing
        self.Tolerance = Tolerance
        #self.null = null
        self.mp1 = 100
        self.alpha = alpha  
        
    def handle_msg(self,msg):
        ang_deg = np.rad2deg(np.arcsin(self.phase/(2*np.pi*self.Spacing)))
        self.message_port_pub(pmt.intern("az"), pmt.cons(pmt.to_pmt({"az": ang_deg, "el": 0}),pmt.to_pmt(None)))

        if self.Track:
            self.message_port_pub(pmt.intern("phase"), pmt.cons(pmt.intern("shift"),pmt.to_pmt(self.phase)))
            self.message_port_pub(pmt.intern("steer_angle"), pmt.cons(pmt.intern("ampl"),pmt.to_pmt(ang_deg)))
            self.message_port_pub(pmt.intern("Lock"), pmt.cons(pmt.intern("ampl"),pmt.to_pmt(self.Lock)))

            if self.Lock:
                print("Target Found")
            

        return

    def work(self, input_items, output_items):
        if self.Track:

            self.Lock = False
            # if (abs(input_items[1][0]) <self.Tolerance)and(input_items[0][0]< self.null):
            #     self.Lock = True

            # elif input_items[1][0]<0:
            #     self.phase = self.phase-0.005
            # elif input_items[1][0]>0:
            #     self.phase = self.phase+0.005
            # if abs(self.phase)>180:
            #     print("Boundary reached, rotate array")
            side = np.sign(input_items[1][0])

            if input_items[0][0]<self.mp1:
                self.phase +=side*self.alpha
            self.mp1 = input_items[0][0]

        return len(input_items[0])