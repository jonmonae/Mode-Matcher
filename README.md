# Mode-Matcher

### Contents
  Lens_Solve.py:
    Contains functions required to do mode matching
  
  ModeMatcher.py:
    Opens user interface for Lens_Solve.py
  

### Requirements:
  "pip install streamlit"

### How to run UI:
  "streamlit run ModeMatcher.py"

### Parameter Descriptions:  (*** are required)

lenses: Array of available focal lengths ***

lam0: Wavelength of beam  ***

s0 and sF: Initial and final beam spot size ***

r0 and rF: Initial and final radius of curvature


d0: Distance between start and lens1

d1: Distance between lens1 and lens2

d2: Distance between lens2 and end

dtotmax: Desired max total distance


### Notes:
All inputs in meters. Can input using python scientific e.g. 3e-5 


r0, rf default to 10**10m (collimated beam)

d0/d1/d2 min/max default to 0

dtotmax default to 0




