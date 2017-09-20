# SpeedCubeTimer
#### A lightweight, terminal based timer for speedcubing.

## Options 
Options and arguments can be available from both the command line and the configuration file.
#### Command Line Options
-h, --help:   Prints help and the arguments specified below.  
-c, --no_countdown:   Omits the countdown function.  
-f, --file FILE:    Specifies a file to export the sessions' times.  
-o, --config FILE:    Specifies a different configuration file to be used.  
-r, --scrambles LENGTH:   Specifies a preferred length for the scrambles.  
-s, --stats:    Prints statistics for the stored solves. (e.g. Mean of 3, Average of 5 etc.)  

## Usage
Run the script with your preferred options. If no command line options are specified,  
the program will run with the default options found in the configuration file *sctimer.conf*  

Here are some examples:  
`./sctimer.py -o myconfigfile.conf -r 15`  
>This will run the program with options found in the 'myconfigfile.conf' and a scramble length of 15 moves.

`./sctimer.py -s -f mytimes.txt`  
>This will print statistics of the times found inside the 'mytimes.txt' file. Output will look like:  
>Your last 5 solves are: ['DNF', '1.19', '2.85', '1.62', '7.35', '6.51', '2.45', '0.85', '0.85', '0.98', '1.52', '0.71']  
>Your mean of the last 3 solves is: DNF  
>Your average of the last 5 solves is: 3.94  
>Your average of the last 12 solves is: 2.62  
>Your average of the last 100 solves is: --:--  
#### Controls
While the program is running:
>~ Use [SPACEBAR] to end a phase (e.g. Reveil the scramble/Start the countdown/Start or stop the stopwatch etc.)  
>~ Use [ESCAPE] to exit the session except for when the stopwatch is running.  
>~ If the **stopwatch is running** and you press [ESCAPE], a **'DNF'** solve will be appended to your time storing file.

##### The program is following the official WCA Regulations which cann be found here:
>https://www.worldcubeassociation.org/regulations/
