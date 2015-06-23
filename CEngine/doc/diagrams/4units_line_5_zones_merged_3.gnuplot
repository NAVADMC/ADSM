set encoding iso_8859_1
set xrange [-4:4]
set yrange [-4:4]
set size square
set xlabel "km (E-W)"
set ylabel "km (N-S)"
set arrow from -4,0 to 4,0 nohead lt 0
set arrow from 0,-4 to 0,4 nohead lt 0
set label "0" at -2.73333,-0.266667 left
set label "1" at -1.73333,-0.266667 left
set label "2" at 1.26667,-0.266667 left
set label "3" at 3.26667,-0.266667 left
set parametric
plot [0:2*pi] 0.5*sin(t)-3,0.5*cos(t) notitle w l lt 1 lw 3,\
 0.5*sin(t)+3,0.5*cos(t) notitle w l lt 1 lw 3,\
 1.5*sin(t)-3,1.5*cos(t) notitle w l lt 8 lw 3,\
 1.5*sin(t)+3,1.5*cos(t) notitle w l lt 8 lw 3,\
 3.5*sin(t)-3,3.5*cos(t) notitle w l lt 6 lw 3,\
 3.5*sin(t)+3,3.5*cos(t) notitle w l lt 6 lw 3,\
 '-' notitle w p lt 6 pt 7 ps 2, \
 '-' notitle w p lt 7 pt 71 ps 2, \
 '-' notitle w p lt 6 pt 7 ps 2, \
 '-' notitle w p lt 6 pt 7 ps 2
-3 0
e
-2 0
e
1 0
e
3 0
e
