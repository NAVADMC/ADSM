set encoding iso_8859_1
set xrange [-2:2]
set yrange [-2:2]
set size square
set xlabel "km (E-W)"
set ylabel "km (N-S)"
set arrow from -2,0 to 2,0 nohead lt 0
set arrow from 0,-2 to 0,2 nohead lt 0
set label "A" at -0.491667,-0.133333 left
set label "B" at 0.758333,-0.133333 left
set label "1" at -0.491667,0.866667 left
set label "2" at 0.374363,0.366667 left
set label "3" at 0.374363,-0.633333 left
set label "4" at -0.491667,-1.13333 left
set label "5" at -1.3577,-0.633333 left
set label "6" at -1.3577,0.366667 left
set label "7" at 0.758333,0.866667 left
set label "8" at 1.62436,0.366667 left
set label "9" at 1.62436,-0.633333 left
set label "10" at 0.758333,-1.13333 left
set label "11" at -0.107697,-0.633333 left
set label "12" at -0.107697,0.366667 left
set parametric
plot [0:2*pi] '-' notitle w p lt 6 pt 7 ps 2.6, \
'-' notitle w p lt 6 pt 7 ps 2.6, \
'-' notitle w p lt 7 pt 71 ps 3, \
'-' notitle w p lt 7 pt 71 ps 2.6, \
'-' notitle w p lt 7 pt 71 ps 2.2, \
'-' notitle w p lt 7 pt 71 ps 1.8, \
'-' notitle w p lt 7 pt 71 ps 1.4, \
'-' notitle w p lt 7 pt 71 ps 1, \
'-' notitle w p lt 7 pt 71 ps 3, \
'-' notitle w p lt 7 pt 71 ps 2.6, \
'-' notitle w p lt 7 pt 71 ps 2.2, \
'-' notitle w p lt 7 pt 71 ps 1.8, \
'-' notitle w p lt 7 pt 71 ps 1.4, \
'-' notitle w p lt 7 pt 71 ps 1, \
0.875*sin(t)-0.625, 0.875*cos(t)+0 notitle w l lt 3 lw 3, \
1.125*sin(t)-0.625, 1.125*cos(t)+0 notitle w l lt 3 lw 3, \
0.875*sin(t)+0.625, 0.875*cos(t)+0 notitle w l lt 3 lw 3, \
1.125*sin(t)+0.625, 1.125*cos(t)+0 notitle w l lt 3 lw 3
-0.625 0
e
0.625 0
e
-0.625 1
e
0.24103 0.5
e
0.24103 -0.5
e
-0.625 -1
e
-1.49103 -0.5
e
-1.49103 0.5
e
0.625 1
e
1.49103 0.5
e
1.49103 -0.5
e
0.625 -1
e
-0.24103 -0.5
e
-0.24103 0.5
e
