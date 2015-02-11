set xrange [-6:6]
set yrange [-1:11]
set size square
set xlabel "km (E-W)"
set ylabel "km (N-S)"
set arrow from -6,0 to 6,0 nohead lt 0
set arrow from 0,-1 to 0,11 nohead lt 0
set label "0" at 0.4,-0.4 left
set label "1" at 0.4,9.6 left
set label "High risk" at 1.25,10 left tc lt 1
set label "High risk" at 1.25,0.5 left tc lt 1
set label "Background" at 0,5 center
set parametric
plot [0:2*pi] 1*sin(t),1*cos(t) notitle w l lt 1 lw 3,\
 1*sin(t),1*cos(t)+10 notitle w l lt 1 lw 3,\
 '-' notitle w p lt 6 pt 7 ps 2, \
 '-' notitle w p lt 6 pt 7 ps 2
0 0
e
0 10
e
