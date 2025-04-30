"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
import pmt
from gnuradio import gr


class SweepControl(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Sweep controller for CSB measurements"""

    def __init__(self, Sweep = False,Start = 0,Stop =12,Step = 0.5,sample_buffer=10, Average = 1,prefix = ""):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Sweep Controller',   # will show up in GRC
            in_sig=[np.float32],
            out_sig=None#,np.short]
        )

        self.message_port_register_out(pmt.intern('out'))
        #self.message_port_register_in(pmt.intern('Value_Set'))
        #self.set_msg_handler(pmt.intern('Value_Set'), self.handle_msg)

        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.Sweep = Sweep
        #self.Start = Start
        self.Stop = Stop
        self.Step = Step
        self.Average = Average
        self.avgVec = np.empty(Average)
        self.prefix = prefix

        

        self.SwpVar = Start
        self.state = 0
        self.xAxe = np.arange(Start,Stop,Step)
        self.data = np.empty(len(self.xAxe))#int((Stop-Start)/Step))
        self.sample_buffer = sample_buffer
        self.counter  = sample_buffer
        self.index = 0


    def work(self, input_items, output_items):


        match self.state:
            case 0:
                if self.Sweep == True:
                    self.state = 2  #Log initial value
                    self.message_port_pub(pmt.intern("out"), pmt.cons(pmt.intern("shift"),pmt.to_pmt(self.SwpVar)))
                    self.counter = self.sample_buffer

                #output_items[0][:] = np.nan

            case 1: #Data has been saved, adjust gain
                #print("updating gain\n")
                #if self.SwpVar >= self.Stop:
                    #self.state = 4

                #else:
                    self.SwpVar += self.Step
                    self.message_port_pub(pmt.intern("out"), pmt.cons(pmt.intern("shift"),pmt.to_pmt(self.SwpVar)))
                    self.counter = self.sample_buffer
                    self.state = 2
                #output_items[0][:] = np.nan

            case 2: #Wait for buffer time
               # print("waiting\n")
                self.counter += -1
                if self.counter < 0:
                    self.state = 5
                    self.counter = self.Average
                    #print("wait finished\n")
                #output_items[0][:] = np.nan

            case 5: #Average values
                self.counter += -1
                self.avgVec[self.counter] = input_items[0][0]

                if self.counter < 0:
                    self.state = 3

                #output_items[0][:] = np.nan

            case 3: #Log value
                print("Phase",self.SwpVar,"\n")
                print("saving value",np.sum(self.avgVec)/len(self.avgVec),"\n")
                self.data[self.index] = np.sum(self.avgVec)/len(self.avgVec)#input_items[0][0]
                self.index+=1
                print("Index",self.index," of ",len(self.data),"\n")
                if self.index>=len(self.data):
                    self.state = 4
                else:
                    self.state = 1

                
            case 4: #Do nothing
                np.save(f"{self.prefix}_xout.npy",self.xAxe)
                np.save(f"{self.prefix}_yout.npy",self.data)
                print("Data Saved! Sweep Complete \n")
                self. state = 6

            case 6: # Do Nothing
                pass

        return len(input_items[0])
