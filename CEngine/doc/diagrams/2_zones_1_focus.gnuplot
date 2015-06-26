set xrange [-6:6]
set yrange [-6:6]
set size square
set xlabel "km (E-W)"
set ylabel "km (N-S)"
set arrow from -6,0 to 6,0 nohead lt 0
set arrow from 0,-6 to 0,6 nohead lt 0
set label "0" at 0.4,-0.4 left
set label "High risk" at 1,-0.75 left tc lt 1
set label "Low risk" at 0.75,-2.5 left tc lt 8
set label "Background" at 0,4 center
set parametric
plot [0:2*pi] 1*sin(t),1*cos(t) notitle w l lt 1 lw 3,\
2*sin(t),2*cos(t) notitle w l lt 8 lw 3,\
'-' notitle w p lt 6 pt 7 ps 2
0 0
e
