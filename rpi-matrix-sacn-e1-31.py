# Based off https://github.com/darknessii/rpi-matrix-acn-e1-31

import time
import sacn
import logging

from rgbmatrix import RGBMatrix, RGBMatrixOptions

# RGBMatrix Panel
number_of_rows_per_panel = 32
number_of_columns_per_panel = 32
number_of_panels = 2
parallel = 2

display_size_x = 64
display_size_y = 64

### RGBMatrixSetting

def rgbmatrix_options():
  options = RGBMatrixOptions()
  options.multiplexing = 6 
  options.row_address_type = 0
  options.brightness = 80
  options.rows = number_of_rows_per_panel
  options.cols = number_of_columns_per_panel
  options.chain_length = number_of_panels
  options.parallel = parallel
  options.hardware_mapping = 'regular'
  options.inverse_colors = False
  options.led_rgb_sequence = "BGR"
  options.gpio_slowdown = 1
  options.pwm_lsb_nanoseconds = 130
  options.show_refresh_rate = 0
  options.disable_hardware_pulsing = False
  options.scan_mode = 0
  options.pwm_bits = 11
  options.daemon = 0
  options.drop_privileges = 0
  return options;

options = rgbmatrix_options()
display = RGBMatrix(options=options)


# enable logging of sacn module
logging.basicConfig(level=logging.DEBUG)

receiver = sacn.sACNreceiver()
receiver.start()  # start the receiving thread

@receiver.listen_on('availability')  # check for availability of universes
def callback_available(universe, changed):
    print(f'universe {universe}: {changed}')

@receiver.listen_on('universe', universe=1) 

def callback(packet):  # packet type: sacn.DataPacket
    print(f'{packet.universe}: {packet.dmxData[:8]}')  # print the received DMX data, but only the first 8 values
    self.showDisplay(display_size_x,display_size_y,packet.dmxData)

def showDisplay(self, display_size_x, display_size_y, datastream):
      idx = 0
      x = 0
      y = 0
      rgb_length = len(datastream) 
      while ((idx < (rgb_length)) and (y < (display_size_y - 1))):
          r = datastream[idx]
          idx += 1
          g = datastream[idx]
          idx += 1
          b = datastream[idx]
          idx += 1
          display.SetPixel(x, y, r, g, b)
          x += 1
          if (x > (display_size_x - 1)):
              x = 0
              y += 1    

receiver.join_multicast(1)

print("Running")