#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.1.1

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import eng_notation
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
import math
import pmt
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import filter
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import uhd
import time
import mp_testing_epy_block_1 as epy_block_1  # embedded python block
import mp_testing_epy_block_2 as epy_block_2  # embedded python block
import mp_testing_epy_block_3 as epy_block_3  # embedded python block



from gnuradio import qtgui

class mp_testing(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "mp_testing")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.RxShift = RxShift = 0.2e6
        self.FTx = FTx = 915e6
        self.samp_rate_src = samp_rate_src = 2e6
        self.prefix = prefix = 'Date_Test'
        self.Track = Track = False
        self.StartSwp = StartSwp = False
        self.Length = Length = 1024
        self.GTx = GTx = 60
        self.GRx = GRx = 30
        self.FRx = FRx = 2*FTx-RxShift
        self.Decimation = Decimation = 20

        ##################################################
        # Blocks
        ##################################################
        self._prefix_tool_bar = Qt.QToolBar(self)
        self._prefix_tool_bar.addWidget(Qt.QLabel("File Name" + ": "))
        self._prefix_line_edit = Qt.QLineEdit(str(self.prefix))
        self._prefix_tool_bar.addWidget(self._prefix_line_edit)
        self._prefix_line_edit.returnPressed.connect(
            lambda: self.set_prefix(str(str(self._prefix_line_edit.text()))))
        self.top_layout.addWidget(self._prefix_tool_bar)
        _Track_check_box = Qt.QCheckBox("Begin Tracking")
        self._Track_choices = {True: True, False: False}
        self._Track_choices_inv = dict((v,k) for k,v in self._Track_choices.items())
        self._Track_callback = lambda i: Qt.QMetaObject.invokeMethod(_Track_check_box, "setChecked", Qt.Q_ARG("bool", self._Track_choices_inv[i]))
        self._Track_callback(self.Track)
        _Track_check_box.stateChanged.connect(lambda i: self.set_Track(self._Track_choices[bool(i)]))
        self.top_layout.addWidget(_Track_check_box)
        _StartSwp_check_box = Qt.QCheckBox("Start Sweep?")
        self._StartSwp_choices = {True: True, False: False}
        self._StartSwp_choices_inv = dict((v,k) for k,v in self._StartSwp_choices.items())
        self._StartSwp_callback = lambda i: Qt.QMetaObject.invokeMethod(_StartSwp_check_box, "setChecked", Qt.Q_ARG("bool", self._StartSwp_choices_inv[i]))
        self._StartSwp_callback(self.StartSwp)
        _StartSwp_check_box.stateChanged.connect(lambda i: self.set_StartSwp(self._StartSwp_choices[bool(i)]))
        self.top_layout.addWidget(_StartSwp_check_box)
        self._GTx_tool_bar = Qt.QToolBar(self)
        self._GTx_tool_bar.addWidget(Qt.QLabel("Transmit Gain [dBFS?]" + ": "))
        self._GTx_line_edit = Qt.QLineEdit(str(self.GTx))
        self._GTx_tool_bar.addWidget(self._GTx_line_edit)
        self._GTx_line_edit.returnPressed.connect(
            lambda: self.set_GTx(eng_notation.str_to_num(str(self._GTx_line_edit.text()))))
        self.top_layout.addWidget(self._GTx_tool_bar)
        self._GRx_tool_bar = Qt.QToolBar(self)
        self._GRx_tool_bar.addWidget(Qt.QLabel("Receive Gain [dBFS?]" + ": "))
        self._GRx_line_edit = Qt.QLineEdit(str(self.GRx))
        self._GRx_tool_bar.addWidget(self._GRx_line_edit)
        self._GRx_line_edit.returnPressed.connect(
            lambda: self.set_GRx(eng_notation.str_to_num(str(self._GRx_line_edit.text()))))
        self.top_layout.addWidget(self._GRx_tool_bar)
        self.variable_qtgui_azelplot_0 = _distance_radar_variable_qtgui_azelplot_0 = qtgui.AzElPlot('', "white", "ro", self)
        self.variable_qtgui_azelplot_0 = _distance_radar_variable_qtgui_azelplot_0

        self.top_layout.addWidget(_distance_radar_variable_qtgui_azelplot_0)
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,2)),
            ),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate_src)
        self.uhd_usrp_source_0.set_time_unknown_pps(uhd.time_spec(0))

        self.uhd_usrp_source_0.set_center_freq(FRx, 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.uhd_usrp_source_0.set_rx_agc(False, 0)
        self.uhd_usrp_source_0.set_gain(GRx, 0)

        self.uhd_usrp_source_0.set_center_freq(FRx, 1)
        self.uhd_usrp_source_0.set_antenna("RX2", 1)
        self.uhd_usrp_source_0.set_rx_agc(False, 1)
        self.uhd_usrp_source_0.set_gain(GRx, 1)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,2)),
            ),
            "",
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate_src)
        _last_pps_time = self.uhd_usrp_sink_0.get_time_last_pps().get_real_secs()
        # Poll get_time_last_pps() every 50 ms until a change is seen
        while(self.uhd_usrp_sink_0.get_time_last_pps().get_real_secs() == _last_pps_time):
            time.sleep(0.05)
        # Set the time to PC time on next PPS
        self.uhd_usrp_sink_0.set_time_next_pps(uhd.time_spec(int(time.time()) + 1.0))
        # Sleep 1 second to ensure next PPS has come
        time.sleep(1)

        self.uhd_usrp_sink_0.set_center_freq(FTx, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0.set_gain(GTx, 0)

        self.uhd_usrp_sink_0.set_center_freq(FTx, 1)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 1)
        self.uhd_usrp_sink_0.set_gain(-40, 1)
        self.qtgui_number_sink_2 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_NONE,
            1,
            None # parent
        )
        self.qtgui_number_sink_2.set_update_time(0.10)
        self.qtgui_number_sink_2.set_title("")

        labels = ['Steering Angle', '', '', '', '',
            '', '', '', '', '']
        units = ['degrees', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_2.set_min(i, -1)
            self.qtgui_number_sink_2.set_max(i, 1)
            self.qtgui_number_sink_2.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_2.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_2.set_label(i, labels[i])
            self.qtgui_number_sink_2.set_unit(i, units[i])
            self.qtgui_number_sink_2.set_factor(i, factor[i])

        self.qtgui_number_sink_2.enable_autoscale(False)
        self._qtgui_number_sink_2_win = sip.wrapinstance(self.qtgui_number_sink_2.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_number_sink_2_win)
        self.qtgui_freq_sink_x_1 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            FRx+RxShift, #fc
            samp_rate_src/Decimation, #bw
            "Inputs", #name
            2,
            None # parent
        )
        self.qtgui_freq_sink_x_1.set_update_time(0.10)
        self.qtgui_freq_sink_x_1.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_1.enable_grid(False)
        self.qtgui_freq_sink_x_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_1.enable_control_panel(False)
        self.qtgui_freq_sink_x_1.set_fft_window_normalized(False)



        labels = ['Source 1', 'Source 2', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_1_win)
        self.qtgui_freq_sink_x_0_1 = qtgui.freq_sink_f(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            2*FTx, #fc
            samp_rate_src/Decimation, #bw
            "Im{Monopulse Ratio}", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_1.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_1.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_1.enable_grid(False)
        self.qtgui_freq_sink_x_0_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_1.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_1.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_0_1.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_1_win)
        self.low_pass_filter_0_0 = filter.fir_filter_ccf(
            Decimation,
            firdes.low_pass(
                1,
                samp_rate_src,
                100e3,
                20e3,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            Decimation,
            firdes.low_pass(
                1,
                samp_rate_src,
                100e3,
                20e3,
                window.WIN_HAMMING,
                6.76))
        self.fft_vxx_0_2_0 = fft.fft_vcc(Length, True, window.blackmanharris(1024), True, 1)
        self.fft_vxx_0_2 = fft.fft_vcc(Length, True, window.blackmanharris(1024), True, 1)
        self.fft_vxx_0_0 = fft.fft_vfc(Length, True, window.blackmanharris(Length), True, 1)
        self.fft_vxx_0 = fft.fft_vfc(Length, True, window.blackmanharris(Length), True, 1)
        self.epy_block_3 = epy_block_3.MPSweep(Sweep=StartSwp, Start=-30, Stop=30, Step=0.5, sample_buffer=5, Average=10, Spacing=1, Prefix=prefix)
        self.epy_block_2 = epy_block_2.Tracker(Track=Track, Spacing=1, Tolerance=0.01, alpha=0.005)
        self.epy_block_1 = epy_block_1.PhaseDiff(Length=Length, CenterFreq=1.83e9, SignalFreq=1.83e9, BW=1e3, samp_rate=samp_rate_src/Decimation)
        self.blocks_sub_xx_2 = blocks.sub_cc(1)
        self.blocks_sub_xx_1 = blocks.sub_ff(1)
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_stream_to_vector_0_2_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, Length)
        self.blocks_stream_to_vector_0_2 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, Length)
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_float*1, Length)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_float*1, Length)
        self.blocks_phase_shift_0_0 = blocks.phase_shift(0, True)
        self.blocks_phase_shift_0 = blocks.phase_shift(0, True)
        self.blocks_nlog10_ff_0_2_0 = blocks.nlog10_ff(10, Length, 0)
        self.blocks_nlog10_ff_0_2 = blocks.nlog10_ff(10, Length, 0)
        self.blocks_nlog10_ff_0_0 = blocks.nlog10_ff(10, Length, 0)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, Length, 0)
        self.blocks_multiply_xx_0_2 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0_1_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0_1 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0_0_1 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0_0_0_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0_0_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_multiply_const_xx_0_2_0 = blocks.multiply_const_cc(1/1024, Length)
        self.blocks_multiply_const_xx_0_2 = blocks.multiply_const_cc(1/1024, Length)
        self.blocks_multiply_const_xx_0_0 = blocks.multiply_const_cc(1/Length, Length)
        self.blocks_multiply_const_xx_0 = blocks.multiply_const_cc(1/Length, Length)
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.intern("TEST"), 100)
        self.blocks_max_xx_1_1_0_0 = blocks.max_ff(Length, 1)
        self.blocks_max_xx_1_1_0 = blocks.max_ff(Length, 1)
        self.blocks_max_xx_1_0 = blocks.max_ff(Length, 1)
        self.blocks_max_xx_1 = blocks.max_ff(Length, 1)
        self.blocks_freqshift_cc_0_0 = blocks.rotator_cc(2.0*math.pi*-1*RxShift/samp_rate_src)
        self.blocks_freqshift_cc_0 = blocks.rotator_cc(2.0*math.pi*-1*(RxShift)/samp_rate_src)
        self.blocks_divide_xx_0_0 = blocks.divide_ff(1)
        self.blocks_divide_xx_0 = blocks.divide_ff(1)
        self.blocks_complex_to_mag_squared_0_1_0_0 = blocks.complex_to_mag_squared(Length)
        self.blocks_complex_to_mag_squared_0_1_0 = blocks.complex_to_mag_squared(Length)
        self.blocks_complex_to_mag_squared_0_0 = blocks.complex_to_mag_squared(Length)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(Length)
        self.blocks_complex_to_float_0_0 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.blocks_add_xx_1 = blocks.add_vcc(1)
        self.blocks_add_xx_0_0_0 = blocks.add_vff(1)
        self.blocks_add_xx_0_0 = blocks.add_vff(1)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.analog_sig_source_x_1 = analog.sig_source_f(samp_rate_src/Decimation, analog.GR_CONST_WAVE, 0, 0, 0, 0)
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate_src, analog.GR_CONST_WAVE, 0, 0, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate_src, analog.GR_CONST_WAVE, 0, 1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.epy_block_2, 'Ts'))
        self.msg_connect((self.epy_block_2, 'steer_angle'), (self.analog_sig_source_x_1, 'cmd'))
        self.msg_connect((self.epy_block_2, 'phase'), (self.blocks_phase_shift_0, 'shift'))
        self.msg_connect((self.epy_block_2, 'az'), (self.variable_qtgui_azelplot_0, 'azel'))
        self.msg_connect((self.epy_block_3, 'out'), (self.blocks_phase_shift_0, 'shift'))
        self.connect((self.analog_sig_source_x_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.uhd_usrp_sink_0, 1))
        self.connect((self.analog_sig_source_x_1, 0), (self.qtgui_number_sink_2, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_divide_xx_0, 0))
        self.connect((self.blocks_add_xx_0_0, 0), (self.blocks_divide_xx_0, 1))
        self.connect((self.blocks_add_xx_0_0_0, 0), (self.blocks_divide_xx_0_0, 1))
        self.connect((self.blocks_add_xx_1, 0), (self.blocks_complex_to_float_0_0, 0))
        self.connect((self.blocks_add_xx_1, 0), (self.blocks_stream_to_vector_0_2_0, 0))
        self.connect((self.blocks_complex_to_float_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_complex_to_float_0, 1), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.blocks_complex_to_float_0, 0), (self.blocks_multiply_xx_0_0_1, 0))
        self.connect((self.blocks_complex_to_float_0, 1), (self.blocks_multiply_xx_0_2, 0))
        self.connect((self.blocks_complex_to_float_0_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_complex_to_float_0_0, 1), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.blocks_complex_to_float_0_0, 1), (self.blocks_multiply_xx_0_0_0, 1))
        self.connect((self.blocks_complex_to_float_0_0, 1), (self.blocks_multiply_xx_0_0_0, 0))
        self.connect((self.blocks_complex_to_float_0_0, 1), (self.blocks_multiply_xx_0_0_0_0, 1))
        self.connect((self.blocks_complex_to_float_0_0, 1), (self.blocks_multiply_xx_0_0_0_0, 0))
        self.connect((self.blocks_complex_to_float_0_0, 1), (self.blocks_multiply_xx_0_0_1, 1))
        self.connect((self.blocks_complex_to_float_0_0, 0), (self.blocks_multiply_xx_0_1, 0))
        self.connect((self.blocks_complex_to_float_0_0, 0), (self.blocks_multiply_xx_0_1, 1))
        self.connect((self.blocks_complex_to_float_0_0, 0), (self.blocks_multiply_xx_0_1_0, 1))
        self.connect((self.blocks_complex_to_float_0_0, 0), (self.blocks_multiply_xx_0_1_0, 0))
        self.connect((self.blocks_complex_to_float_0_0, 0), (self.blocks_multiply_xx_0_2, 1))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0_0, 0), (self.blocks_nlog10_ff_0_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0_1_0, 0), (self.blocks_nlog10_ff_0_2, 0))
        self.connect((self.blocks_complex_to_mag_squared_0_1_0_0, 0), (self.blocks_nlog10_ff_0_2_0, 0))
        self.connect((self.blocks_divide_xx_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_divide_xx_0_0, 0), (self.blocks_stream_to_vector_0_0, 0))
        self.connect((self.blocks_divide_xx_0_0, 0), (self.qtgui_freq_sink_x_0_1, 0))
        self.connect((self.blocks_freqshift_cc_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_freqshift_cc_0_0, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.blocks_max_xx_1, 0), (self.epy_block_3, 1))
        self.connect((self.blocks_max_xx_1_0, 0), (self.epy_block_2, 0))
        self.connect((self.blocks_max_xx_1_0, 0), (self.epy_block_3, 0))
        self.connect((self.blocks_max_xx_1_1_0, 0), (self.blocks_sub_xx_1, 0))
        self.connect((self.blocks_max_xx_1_1_0_0, 0), (self.blocks_sub_xx_1, 1))
        self.connect((self.blocks_multiply_const_xx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.blocks_multiply_const_xx_0_0, 0), (self.blocks_complex_to_mag_squared_0_0, 0))
        self.connect((self.blocks_multiply_const_xx_0_2, 0), (self.blocks_complex_to_mag_squared_0_1_0, 0))
        self.connect((self.blocks_multiply_const_xx_0_2, 0), (self.epy_block_1, 0))
        self.connect((self.blocks_multiply_const_xx_0_2_0, 0), (self.blocks_complex_to_mag_squared_0_1_0_0, 0))
        self.connect((self.blocks_multiply_const_xx_0_2_0, 0), (self.epy_block_1, 1))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_multiply_xx_0_0_0, 0), (self.blocks_add_xx_0_0, 1))
        self.connect((self.blocks_multiply_xx_0_0_0_0, 0), (self.blocks_add_xx_0_0_0, 1))
        self.connect((self.blocks_multiply_xx_0_0_1, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.blocks_multiply_xx_0_1, 0), (self.blocks_add_xx_0_0, 0))
        self.connect((self.blocks_multiply_xx_0_1_0, 0), (self.blocks_add_xx_0_0_0, 0))
        self.connect((self.blocks_multiply_xx_0_2, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.blocks_max_xx_1, 0))
        self.connect((self.blocks_nlog10_ff_0_0, 0), (self.blocks_max_xx_1_0, 0))
        self.connect((self.blocks_nlog10_ff_0_2, 0), (self.blocks_max_xx_1_1_0, 0))
        self.connect((self.blocks_nlog10_ff_0_2_0, 0), (self.blocks_max_xx_1_1_0_0, 0))
        self.connect((self.blocks_phase_shift_0, 0), (self.blocks_add_xx_1, 1))
        self.connect((self.blocks_phase_shift_0, 0), (self.blocks_sub_xx_2, 1))
        self.connect((self.blocks_phase_shift_0_0, 0), (self.blocks_add_xx_1, 0))
        self.connect((self.blocks_phase_shift_0_0, 0), (self.blocks_sub_xx_2, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.fft_vxx_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0_2, 0), (self.fft_vxx_0_2, 0))
        self.connect((self.blocks_stream_to_vector_0_2_0, 0), (self.fft_vxx_0_2_0, 0))
        self.connect((self.blocks_sub_xx_0, 0), (self.blocks_divide_xx_0_0, 0))
        self.connect((self.blocks_sub_xx_1, 0), (self.epy_block_3, 2))
        self.connect((self.blocks_sub_xx_2, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.blocks_sub_xx_2, 0), (self.blocks_stream_to_vector_0_2, 0))
        self.connect((self.epy_block_1, 0), (self.epy_block_2, 1))
        self.connect((self.epy_block_1, 0), (self.epy_block_3, 3))
        self.connect((self.fft_vxx_0, 0), (self.blocks_multiply_const_xx_0, 0))
        self.connect((self.fft_vxx_0_0, 0), (self.blocks_multiply_const_xx_0_0, 0))
        self.connect((self.fft_vxx_0_2, 0), (self.blocks_multiply_const_xx_0_2, 0))
        self.connect((self.fft_vxx_0_2_0, 0), (self.blocks_multiply_const_xx_0_2_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_phase_shift_0_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_freq_sink_x_1, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.blocks_phase_shift_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.qtgui_freq_sink_x_1, 1))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_freqshift_cc_0, 0))
        self.connect((self.uhd_usrp_source_0, 1), (self.blocks_freqshift_cc_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "mp_testing")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_RxShift(self):
        return self.RxShift

    def set_RxShift(self, RxShift):
        self.RxShift = RxShift
        self.set_FRx(2*self.FTx-self.RxShift)
        self.blocks_freqshift_cc_0.set_phase_inc(2.0*math.pi*-1*(self.RxShift)/self.samp_rate_src)
        self.blocks_freqshift_cc_0_0.set_phase_inc(2.0*math.pi*-1*self.RxShift/self.samp_rate_src)
        self.qtgui_freq_sink_x_1.set_frequency_range(self.FRx+self.RxShift, self.samp_rate_src/self.Decimation)

    def get_FTx(self):
        return self.FTx

    def set_FTx(self, FTx):
        self.FTx = FTx
        self.set_FRx(2*self.FTx-self.RxShift)
        self.qtgui_freq_sink_x_0_1.set_frequency_range(2*self.FTx, self.samp_rate_src/self.Decimation)
        self.uhd_usrp_sink_0.set_center_freq(self.FTx, 0)
        self.uhd_usrp_sink_0.set_center_freq(self.FTx, 1)

    def get_samp_rate_src(self):
        return self.samp_rate_src

    def set_samp_rate_src(self, samp_rate_src):
        self.samp_rate_src = samp_rate_src
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate_src)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate_src)
        self.analog_sig_source_x_1.set_sampling_freq(self.samp_rate_src/self.Decimation)
        self.blocks_freqshift_cc_0.set_phase_inc(2.0*math.pi*-1*(self.RxShift)/self.samp_rate_src)
        self.blocks_freqshift_cc_0_0.set_phase_inc(2.0*math.pi*-1*self.RxShift/self.samp_rate_src)
        self.epy_block_1.samp_rate = self.samp_rate_src/self.Decimation
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate_src, 100e3, 20e3, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate_src, 100e3, 20e3, window.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_0_1.set_frequency_range(2*self.FTx, self.samp_rate_src/self.Decimation)
        self.qtgui_freq_sink_x_1.set_frequency_range(self.FRx+self.RxShift, self.samp_rate_src/self.Decimation)
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate_src)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate_src)

    def get_prefix(self):
        return self.prefix

    def set_prefix(self, prefix):
        self.prefix = prefix
        Qt.QMetaObject.invokeMethod(self._prefix_line_edit, "setText", Qt.Q_ARG("QString", str(self.prefix)))
        self.epy_block_3.Prefix = self.prefix

    def get_Track(self):
        return self.Track

    def set_Track(self, Track):
        self.Track = Track
        self._Track_callback(self.Track)
        self.epy_block_2.Track = self.Track

    def get_StartSwp(self):
        return self.StartSwp

    def set_StartSwp(self, StartSwp):
        self.StartSwp = StartSwp
        self._StartSwp_callback(self.StartSwp)
        self.epy_block_3.Sweep = self.StartSwp

    def get_Length(self):
        return self.Length

    def set_Length(self, Length):
        self.Length = Length
        self.blocks_multiply_const_xx_0.set_k(1/self.Length)
        self.blocks_multiply_const_xx_0_0.set_k(1/self.Length)
        self.epy_block_1.Length = self.Length

    def get_GTx(self):
        return self.GTx

    def set_GTx(self, GTx):
        self.GTx = GTx
        Qt.QMetaObject.invokeMethod(self._GTx_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.GTx)))
        self.uhd_usrp_sink_0.set_gain(self.GTx, 0)

    def get_GRx(self):
        return self.GRx

    def set_GRx(self, GRx):
        self.GRx = GRx
        Qt.QMetaObject.invokeMethod(self._GRx_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.GRx)))
        self.uhd_usrp_source_0.set_gain(self.GRx, 0)
        self.uhd_usrp_source_0.set_gain(self.GRx, 1)

    def get_FRx(self):
        return self.FRx

    def set_FRx(self, FRx):
        self.FRx = FRx
        self.qtgui_freq_sink_x_1.set_frequency_range(self.FRx+self.RxShift, self.samp_rate_src/self.Decimation)
        self.uhd_usrp_source_0.set_center_freq(self.FRx, 0)
        self.uhd_usrp_source_0.set_center_freq(self.FRx, 1)

    def get_Decimation(self):
        return self.Decimation

    def set_Decimation(self, Decimation):
        self.Decimation = Decimation
        self.analog_sig_source_x_1.set_sampling_freq(self.samp_rate_src/self.Decimation)
        self.epy_block_1.samp_rate = self.samp_rate_src/self.Decimation
        self.qtgui_freq_sink_x_0_1.set_frequency_range(2*self.FTx, self.samp_rate_src/self.Decimation)
        self.qtgui_freq_sink_x_1.set_frequency_range(self.FRx+self.RxShift, self.samp_rate_src/self.Decimation)




def main(top_block_cls=mp_testing, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
