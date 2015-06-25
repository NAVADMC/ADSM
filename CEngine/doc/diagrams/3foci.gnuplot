set xrange [-1:4]
set yrange [-2:3]
set size square
set xlabel "km (E-W)"
set ylabel "km (N-S)"
set arrow from -1,0 to 4,0 nohead lt 0
set arrow from 0,-2 to 0,3 nohead lt 0
set label "0" at 0.166667,-0.166667 left
set label "1" at 1.16667,-0.166667 left
set label "2" at 1.66667,1.33333 left
set label "3" at 2.16667,-0.166667 left
set label "4" at 3.16667,-0.166667 left
set parametric
plot [0:2*pi] 1.25*sin(t),1.25*cos(t) notitle w l lt 7 lw 3, \
1.25*sin(t)+1.5,1.25*cos(t)+1.5 notitle w l lt 7 lw 3, \
1.25*sin(t)+3,1.25*cos(t) notitle w l lt 7 lw 3, \
'-' notitle w p lt 6 pt 7 ps 2, \
'-' notitle w p lt 6 pt 7 ps 2, \
'-' notitle w p lt 6 pt 7 ps 2, \
'-' notitle w p lt 7 pt 71 ps 2, \
'-' notitle w p lt 6 pt 7 ps 2
0 0
e
1 0
e
1.5 1.5
e
2 0
e
3 0
e
