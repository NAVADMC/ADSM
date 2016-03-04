set encoding iso_8859_1
set xrange [-4:4]
set yrange [-2:6]
set size square
set xlabel "km (E-W)"
set ylabel "km (N-S)"
set arrow from -4,0 to 4,0 nohead lt 0
set arrow from 0,-2 to 0,6 nohead lt 0
set label "A" at -2.73333,-0.266667 left
set label "F" at 3.26667,-0.266667 left
set label "B" at -2.73333,1.23333 left
set label "C" at -2.73333,2.23333 left
set label "D" at -2.73333,3.23333 left
set label "E" at -2.73333,4.23333 left
set label "G" at 3.26667,1.23333 left
set label "H" at 3.26667,2.23333 left
set label "J" at 3.26667,3.23333 left
set label "K" at 3.26667,4.23333 left
set parametric
plot [0:2*pi] '-' notitle w p lt 6 pt 7 ps 3, \
'-' notitle w p lt 6 pt 7 ps 3, \
'-' notitle w p lt 7 pt 71 ps 1, \
'-' notitle w p lt 7 pt 71 ps 1, \
'-' notitle w p lt 7 pt 71 ps 1, \
'-' notitle w p lt 7 pt 71 ps 1, \
'-' notitle w p lt 7 pt 71 ps 1, \
'-' notitle w p lt 7 pt 71 ps 1, \
'-' notitle w p lt 7 pt 71 ps 1, \
'-' notitle w p lt 7 pt 71 ps 1, \
5*sin(t)-3, 5*cos(t)+0 notitle w l lt 3 lw 3, \
5*sin(t)+3, 5*cos(t)+0 notitle w l lt 3 lw 3
-3 0
e
3 0
e
-3 1.5
e
-3 2.5
e
-3 3.5
e
-3 4.5
e
3 1.5
e
3 2.5
e
3 3.5
e
3 4.5
e
