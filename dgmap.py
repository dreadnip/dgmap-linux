import gi, autopy, sys # Import all dependencies. 
from time import sleep # Uses AutoPy to take the screenshot and search it as a Bitmap, 
gi.require_version('Gtk', '3.0') # Gtk3 for the overlay, GdkPixbuf to convert the Bitmap to an image,
from gi.repository import Gtk, GdkPixbuf # PyXHook to listen for the key event when the map opens
sys.path.insert(1,"pyxhook.py")
import pyxhook 

class DGMap(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title="DGMap")
		self.overlay = Gtk.Overlay()
		self.map_img = Gtk.Image() # Put an empty image on the overlay
		self.grid_img = Gtk.Image() # Put an empty image on the overlay
		self.grid_img.set_from_file("/home/sander/Dropbox/Public/DGMap/img/grid.png")
		self.map_img.set_halign(Gtk.Align.START)
		self.map_img.set_valign(Gtk.Align.START)
		self.grid_img.set_halign(Gtk.Align.START)
		self.grid_img.set_valign(Gtk.Align.START)
		self.overlay.add_overlay(self.map_img)
		self.overlay.add_overlay(self.grid_img)
		self.add(self.overlay)
		self.checkpoint = autopy.bitmap.Bitmap.open('/home/sander/Dropbox/Public/DGMap/img/checkpoint.png') # Open the reference 'X' picture for later

	def close(event, self, widget): # Close event
		hookman.cancel()
		Gtk.main_quit()

	def bm2pixbuf(self,bitmap): # Bitmap to image conversion
		bitmap.save('/home/sander/Dropbox/Public/DGMap/img/slice.png')
		return GdkPixbuf.Pixbuf.new_from_file('/home/sander/Dropbox/Public/DGMap/img/slice.png')

	def scanScreen(self, event): # Main function
		if event.Ascii == 109: # if 'm' is pressed (to open the floor map in dg)
			for i in range(8):
				screenshot = autopy.bitmap.capture_screen() # take screenshot
				pos = screenshot.find_bitmap(self.checkpoint, 0.3) # locate the closing X in the screenshot

				if pos: #locate the top left corner and select the map portion of the screenshot based on that coordinate
					right = pos[0] - 10
					top = pos[1] + 15
					left = right - 270
					top_left_corner = (left, top)
					map_slice = screenshot.get_portion(top_left_corner, (270, 270)) # slice the map out of the complete screenshot
					map_slice = self.bm2pixbuf(map_slice) # convert the sliced bitmap to an image
					self.map_img.set_from_pixbuf(map_slice) # set the image source on the overlay to the newly cut slice
					break
				else:
					print "Error: No map found on screen"
					sleep(0.25) # try again in 0.25s

win = DGMap()
win.connect("delete-event", win.close)
win.resize(270, 270) # set size
win.show_all()
win.set_keep_above(True) # always on top
hookman = pyxhook.HookManager()
hookman.KeyDown = win.scanScreen # listen for key press (to keep track id 'm' is pressed)
hookman.HookKeyboard()
hookman.start()
Gtk.main() # go