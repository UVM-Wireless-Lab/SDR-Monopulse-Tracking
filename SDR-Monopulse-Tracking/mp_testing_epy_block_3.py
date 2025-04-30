"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
import pmt
from gnuradio import gr


class MPSweep(gr.sync_block):  
    """Sweep block to sweep phase and measure 4 quantities. Output is saved as two .npy files. 
    _x_out.npy contains the phase for each measurement and _data.npy has the input data stored 
    as a 4xn matrix where each row is the corresponding input. 
    \n Inputs:
    \n Sweep - Boolean, when true, sweep is initiated
    \n Start - Starting Value
    \n Stop - Ending Value
    \n Step - Resolution of sweep
    \n sample_buffer - This sets a number of data-buffers to be discarded in between measurements
    \n Average - Number of measurements to average when saveing data
    \n Prefix - String to append to the start of filename"""

    def __init__(self, Sweep = False,Start = 0,Stop =12,Step = 0.5,sample_buffer=10, Average = 1,Spacing = 1,Prefix = ""):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Sweep Controller 03',   
            in_sig=[np.float32,np.float32,np.float32,np.float32],

            out_sig=None
        )


        self.message_port_register_out(pmt.intern('out'))
        
        #self.message_port_register_in(pmt.intern('Value_Set'))
        #self.set_msg_handler(pmt.intern('Value_Set'), self.handle_msg)

        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).

        inputs = 4   # Used in construction only to define array sizes

        
        self.Sweep = Sweep
        self.Start = Start
        self.Spacing = Spacing
        self.Stop = Stop
        self.Step = Step
        self.Average = Average
        self.avgVec = np.empty((inputs,Average))
        #print("avgVec Size",self.avgVec.shape,"\n")
        self.Prefix = Prefix

        

        
        self.state = 0
        self.steering_angle = np.arange(self.Start,self.Stop+self.Step,self.Step)
        self.steering_phase = 2*np.pi*self.Spacing*np.sin(np.deg2rad(self.steering_angle))
        self.SwpVar = self.steering_phase[0]
        self.data = np.empty((inputs,len(self.steering_phase)))
        #print("data Size",self.data.shape,"\n")

        self.sample_buffer = sample_buffer
        self.counter  = sample_buffer
        self.index = 0


    def work(self, input_items, output_items):


        match self.state:
            case 0:
                if self.Sweep == True: #Log initial value
                    #self.message_port_pub(pmt.intern("out"), pmt.cons(pmt.intern("shift"),pmt.to_pmt(np.deg2rad(self.SwpVar))))
                    self.message_port_pub(pmt.intern("out"), pmt.cons(pmt.intern("shift"),pmt.to_pmt(self.SwpVar)))

                    self.counter = self.sample_buffer
                    self.state = 2  

                    print("\nDatapoints: ",len(self.steering_phase))
                    print("Size of Output: ",np.shape(self.data))
                    print("Running Sweep... \n")


            case 1: # Update phase value

                    #self.SwpVar += self.Step
                    self.SwpVar = self.steering_phase[self.index]
                    #self.message_port_pub(pmt.intern("out"), pmt.cons(pmt.intern("shift"),pmt.to_pmt(np.deg2rad(self.SwpVar))))
                    self.message_port_pub(pmt.intern("out"), pmt.cons(pmt.intern("shift"),pmt.to_pmt(self.SwpVar)))

                    self.counter = self.sample_buffer
                    self.state = 2


            case 2: #Wait for buffer time
                self.counter -= 1
                if self.counter < 0:
                    self.counter = self.Average
                    self.state = 5


            case 5: #Average values
                self.counter -= 1
                in0 = np.sum(input_items[0])/len(input_items[0])#input_items[0][0]
                in1 = np.sum(input_items[1])/len(input_items[1])#input_items[1][0]
                in2 = np.sum(input_items[2])/len(input_items[2])#input_items[2][0]
                in3 = np.sum(input_items[3])/len(input_items[3])#input_items[3][0]
                self.avgVec[:,self.counter] = np.array([[in0],[in1],[in2],[in3]])[:,0]

                if self.counter < 0:
                    self.state = 3

            case 3: #Log value
                #print("Phase",self.SwpVar,"\n")
                #print("Sample Vector: ",self.avgVec,"\n")
                avg = (np.divide(np.sum(self.avgVec,axis=1),len(self.avgVec[0,:])))
                #print("Saving value:  ",avg.reshape(4,1),"\n")

                self.data[:,self.index] = avg.reshape(4,1)[:,0]
                #print("Saved:  ",self.data[:,self.index],"\n")
                self.index+=1
                #print("Index",self.index," of ",len(self.steering_phase),"\n")
                if self.index>=len(self.steering_phase):
                    self.state = 4
                else:
                    self.state = 1

                
            case 4: #Write data to files
                out = np.concatenate((self.steering_phase.reshape(1,-1),self.data),axis=0)

                np.save(f"{self.Prefix}_data.npy",out)

                print("Data Saved! Sweep Complete \n")
                
                self.state = 6

            case 6: # Wait for sweep to be reinitialized
                if self.Sweep:
                    pass

                else:
                    self.SwpVar = self.steering_phase[0]
                    #self.steering_phase = np.arange(self.Start,self.Stop+self.Step,self.Step)
                    #self.data = np.empty((inputs,len(self.steering_phase)))
                    #self.sample_buffer = sample_buffer
                    #self.counter  = sample_buffer

                    self.index = 0
                    print("Reset! Ready to sweep again\n")
                    self.state = 0
                    
        return len(input_items[0])
