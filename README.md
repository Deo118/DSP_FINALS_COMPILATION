DSP Final Project (Online) Discussion Notes
Compilation of Laboratories
- not a compilation of files
- application wherein you can use all Laboratory activities
- Has a landing page
- Executable File (No Vs code/Pycharm execution reliance)
- Compilation consists of ALL Laboratories (1-8)
- checking around 3rd week of May (21-22)  25-29 tentative written exam
- same midterm group
- Landing page contains routes to all labs
- Opening a lab will create a new window
- matlotlib output will be inside the lab window instead of a new pop-up window 
- Language using anything python based
Criteria: 
- Completeness (Are all Laboratories There?)
- Functionality (Do all laboratories function as intended?)
- Optimization (Program run time, load time, overall page transition/output "speed")
- Creativity (GUI; neat, symmetrical, visually pleasing, etc.)


Run this in the project terminal to compile into one main.exe file:
pyinstaller --onefile --windowed --hidden-import=labs
--hidden-import=labs.lab1_sampling --hidden-import=labs.lab2
--hidden-import=labs.lab3_filters --hidden-import=labs.lab4_ztransform
--hidden-import=labs.lab5_6_dft --hidden-import=labs.lab7_windowing
--hidden-import=scipy --hidden-import=scipy.signal
--hidden-import=sounddevice --hidden-import=soundfile
--hidden-import=librosa --hidden-import=pydub
--collect-all=numpy --collect-all=matplotlib
main.py
