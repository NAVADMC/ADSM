set xrange [-2:2]
set yrange [-2:2]
set size square
set xlabel "km (E-W)"
set ylabel "km (N-S)"
set arrow from -2,0 to 2,0 nohead lt 0
set arrow from 0,-2 to 0,2 nohead lt 0
set label "0" at 0.133333,-0.133333 left
set label "1" at 0.633893,0.733661 left
set label "2" at 1.00033,0.367226 left
set label "3" at 1.13445,-0.133333 left
set label "4" at 1.00033,-0.633893 left
set label "5" at 0.633893,-1.00033 left
set label "6" at 0.133333,-1.13445 left
set label "7" at -0.367226,-1.00033 left
set label "8" at -0.733661,-0.633893 left
set label "9" at -0.867785,-0.133333 left
set label "10" at -0.733661,0.367226 left
set label "11" at -0.367226,0.733661 left
set label "12" at 0.133333,0.867785 left
set label "Background" at 0,1.66 center
set label "High\nrisk" at 1.25,0.75 left tc lt 1
set parametric
rad(x) = x * pi / 180
plot [0:2*pi] 0.2*sin(t),0.2*cos(t) notitle w l lt 1 lw 3,\
  0.2*sin(t)+sin(rad(30)),0.2*cos(t)+cos(rad(30)) notitle w l lt 1 lw 3,\
  0.2*sin(t)+sin(rad(60)),0.2*cos(t)+cos(rad(60)) notitle w l lt 1 lw 3,\
  0.2*sin(t)+1,0.2*cos(t) notitle w l lt 1 lw 3,\
  0.2*sin(t)+sin(rad(60)),0.2*cos(t)-cos(rad(60)) notitle w l lt 1 lw 3,\
  0.2*sin(t)+sin(rad(30)),0.2*cos(t)-cos(rad(30)) notitle w l lt 1 lw 3,\
  0.2*sin(t),0.2*cos(t)-1 notitle w l lt 1 lw 3,\
  0.2*sin(t)-sin(rad(30)),0.2*cos(t)-cos(rad(30)) notitle w l lt 1 lw 3,\
  0.2*sin(t)-sin(rad(60)),0.2*cos(t)-cos(rad(60)) notitle w l lt 1 lw 3,\
  0.2*sin(t)-1,0.2*cos(t) notitle w l lt 1 lw 3,\
  0.2*sin(t)-sin(rad(60)),0.2*cos(t)+cos(rad(60)) notitle w l lt 1 lw 3,\
  0.2*sin(t)-sin(rad(30)),0.2*cos(t)+cos(rad(30)) notitle w l lt 1 lw 3,\
  0.2*sin(t),0.2*cos(t)+1 notitle w l lt 1 lw 3,\
  '-' notitle w p lt 6 pt 7 ps 2, \
  '-' notitle w p lt 7 pt 71 ps 2, \
  '-' notitle w p lt 7 pt 71 ps 2, \
  '-' notitle w p lt 7 pt 71 ps 2, \
  '-' notitle w p lt 7 pt 71 ps 2, \
  '-' notitle w p lt 7 pt 71 ps 2, \
  '-' notitle w p lt 7 pt 71 ps 2, \
  '-' notitle w p lt 7 pt 71 ps 2, \
  '-' notitle w p lt 7 pt 71 ps 2, \
  '-' notitle w p lt 7 pt 71 ps 2, \
  '-' notitle w p lt 7 pt 71 ps 2, \
  '-' notitle w p lt 7 pt 71 ps 2, \
  '-' notitle w p lt 7 pt 71 ps 2
0 0
e
0.500559 0.866994
e
0.866994 0.500559
e
1.00112 0
e
0.866994 -0.500559
e
0.500559 -0.866994
e
0 -1.00112
e
-0.500559 -0.866994
e
-0.866994 -0.500559
e
-1.00112 0
e
-0.866994 0.500559
e
-0.500559 0.866994
e
0 1.00112
e
