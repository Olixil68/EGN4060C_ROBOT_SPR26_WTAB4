# test_fire.py
from fire_controller import FireController

fc = FireController()

input("Press ENTER to fire...")
fc.fire()

fc.cleanup()