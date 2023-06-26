#name=Tascam US-428

import transport
import mixer
import ui
import midi
import time
import math
import device
import playlist
import channels
import patterns
import utils
import general

channel_offset = 0

channel_select = 1

fader_max_value = 0.8

record_toggle = False
	

def OnControlChange(event):
  
  global channel_offset

	global record_toggle

  #Volume Fader
	if(event.data1 == 0x40):
		mixer.setTrackVolume(channel_offset + 1, (event.data2 / 128 * fader_max_value))
	if(event.data1 == 0x41):
		mixer.setTrackVolume(channel_offset + 2, (event.data2 / 128 * fader_max_value))
	if(event.data1 == 0x42):
		mixer.setTrackVolume(channel_offset + 3, (event.data2 / 128 * fader_max_value))
	if(event.data1 == 0x43):
		mixer.setTrackVolume(channel_offset + 4, (event.data2 / 128 * fader_max_value))
	if(event.data1 == 0x44):
		mixer.setTrackVolume(channel_offset + 5, (event.data2 / 128 * fader_max_value))
	if(event.data1 == 0x45):
		mixer.setTrackVolume(channel_offset + 6, (event.data2 / 128 * fader_max_value))
	if(event.data1 == 0x46):
		mixer.setTrackVolume(channel_offset + 7, (event.data2 / 128 * fader_max_value))
	if(event.data1 == 0x47):
		mixer.setTrackVolume(channel_offset + 8, (event.data2 / 128 * fader_max_value))
	if(event.data1 == 0x4B):
		mixer.setTrackVolume(0, (event.data2 / 128 * fader_max_value))
		
  #Bank Buttons
	if(event.data1 == 0x10 or event.data1 == 0x11):
		updateBank(event.data1, event.data2)

	#REW
	if(event.data1 == 0x13):
		if(event.data2 == 0x7F):
			transport.rewind(2)
			device.midiOutSysex(bytes([0xF0, 0x4E, 0x00, 0x12, 0x01, 0x13, 0x7F, 0xF7]))
		if(event.data2 == 0x00):
			transport.rewind(0)
			device.midiOutSysex(bytes([0xF0, 0x4E, 0x00, 0x12, 0x01, 0x13, 0x00, 0xF7]))

	#FFWD
	if(event.data1 == 0x14):
		if(event.data2 == 0x7F):
			transport.fastForward(2)
			device.midiOutSysex(bytes([0xF0, 0x4E, 0x00, 0x12, 0x01, 0x14, 0x7F, 0xF7]))
		if(event.data2 == 0x00):
			transport.fastForward(0)
			device.midiOutSysex(bytes([0xF0, 0x4E, 0x00, 0x12, 0x01, 0x14, 0x00, 0xF7]))

	#STOP
	if(event.data1 == 0x15):
		if(event.data2 == 0x7F):
			transport.stop()
			#Turn of play led
			device.midiOutSysex(bytes([0xF0, 0x4E, 0x00, 0x12, 0x01, 0x16, 0x00, 0xF7]))

	#Play
	if(event.data1 == 0x16):
		if(event.data2 == 0x7F):
			transport.start()
		if(transport.isPlaying):
			device.midiOutSysex(bytes([0xF0, 0x4E, 0x00, 0x12, 0x01, 0x16, 0x7F, 0xF7]))
		else:
			device.midiOutSysex(bytes([0xF0, 0x4E, 0x00, 0x12, 0x01, 0x16, 0x00, 0xF7]))

	#RECORD
	if(event.data1 == 0x17):
		if(event.data2 == 0x7F):
			transport.record()
			if(record_toggle):
				device.midiOutSysex(bytes([0xF0, 0x4E, 0x00, 0x12, 0x01, 0x17, 0x00, 0xF7]))
			else:
				device.midiOutSysex(bytes([0xF0, 0x4E, 0x00, 0x12, 0x01, 0x17, 0x7F, 0xF7]))
			record_toggle = not record_toggle



def updateBank(data1, data2):
	print("Change Bank")

def OnUpdateBeatIndicator(value):
	if(value > 0):
		device.midiOutSysex(bytes([0xF0, 0x4E, 0x00, 0x12, 0x01, 0x16, 0x7F, 0xF7]))
	else:
		device.midiOutSysex(bytes([0xF0, 0x4E, 0x00, 0x12, 0x01, 0x16, 0x00, 0xF7]))
