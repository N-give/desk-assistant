# Raspberry Pi Setup

## Enable SPI

1. `# raspi-config`
2. Choose Interfacing Options
3. SPI
4. Yes - enable SPI Interface
5. Reboot

## Install Python Dependencies

1. `# apt install python3-pip python3-pil python3-numpy`
2. `# pip3 install RPi.GPIO spidev`

## Download Example Code (Optional)

- `git clone https://github.com/waveshare/e-Paper`
- Waveshare example code found in `RaspberryPi&JetsonNano/python/examples`
- Run with `# python3 epd_<size>_<example>.py`


