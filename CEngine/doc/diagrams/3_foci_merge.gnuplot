set xrange [-1:4]
set yrange [-2.5:2.5]
set size square
set xlabel "km (E-W)"
set ylabel "km (N-S)"
set arrow from -1,0 to 4,0 nohead lt 0
set arrow from 0,-2.5 to 0,2.5 nohead lt 0
set label "0" at 0.166667,-0.166667 left
set label "1" at 1.16667,-0.166667 left
set label "2" at 2.16667,-0.166667 left
set label "3" at 3.16667,-0.166667 left
set label "Added\nday 3" at -0.33,1.75 center tc lt 1
set label "Added\nday 3" at 3.33,1.75 center tc lt 1
set label "Added\nday 4" at 1,-1.5 center tc lt 1
set parametric
plot [0:2*pi] 1.25*sin(t),1.25*cos(t) notitle w l lt 1 lw 3,\
 1.25*sin(t)+3,1.25*cos(t) notitle w l lt 1 lw 3,\
 1.25*sin(t)+1,1.25*cos(t) notitle w l lt 1 lw 3,\
 '-' notitle w p lt 6 pt 7 ps 2, \
 '-' notitle w p lt 6 pt 7 ps 2, \
 '-' notitle w p lt 7 pt 71 ps 2, \
 '-' notitle w p lt 6 pt 7 ps 2
0 0
e
1 0
e
2 0
e
3 0
e
