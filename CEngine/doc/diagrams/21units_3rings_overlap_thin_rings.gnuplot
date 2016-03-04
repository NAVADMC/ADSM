set encoding iso_8859_1
set xrange [-2:4]
set yrange [-3:3]
set size square
set xlabel "km (E-W)"
set ylabel "km (N-S)"
set arrow from -2,0 to 4,0 nohead lt 0
set arrow from 0,-3 to 0,3 nohead lt 0
set label "A" at -0.425,-0.2 left
set label "B" at 0.825,-0.2 left
set label "C" at 2.075,-0.2 left
set label "1" at -0.425,0.8 left
set label "2" at 0.44103,0.3 left
set label "3" at 0.44103,-0.7 left
set label "4" at -0.425,-1.2 left
set label "5" at -1.29103,-0.7 left
set label "6" at -1.29103,0.3 left
set label "7" at 0.825,0.8 left
set label "8" at 1.69103,0.3 left
set label "9" at 1.69103,-0.7 left
set label "10" at 0.825,-1.2 left
set label "11" at -0.04103,-0.7 left
set label "12" at -0.04103,0.3 left
set label "13" at 2.075,0.8 left
set label "14" at 2.94103,0.3 left
set label "15" at 2.94103,-0.7 left
set label "16" at 2.075,-1.2 left
set label "17" at 1.20897,-0.7 left
set label "18" at 1.20897,0.3 left
set parametric
plot [0:2*pi] '-' notitle w p lt 6 pt 7 ps 2.2, \
'-' notitle w p lt 6 pt 7 ps 2.2, \
'-' notitle w p lt 6 pt 7 ps 2.2, \
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
'-' notitle w p lt 7 pt 71 ps 3, \
'-' notitle w p lt 7 pt 71 ps 2.6, \
'-' notitle w p lt 7 pt 71 ps 2.2, \
'-' notitle w p lt 7 pt 71 ps 1.8, \
'-' notitle w p lt 7 pt 71 ps 1.4, \
'-' notitle w p lt 7 pt 71 ps 1, \
0.875*sin(t)-0.625, 0.875*cos(t)+0 notitle w l lt 3 lw 3, \
1.125*sin(t)-0.625, 1.125*cos(t)+0 notitle w l lt 3 lw 3, \
0.875*sin(t)+0.625, 0.875*cos(t)+0 notitle w l lt 3 lw 3, \
1.125*sin(t)+0.625, 1.125*cos(t)+0 notitle w l lt 3 lw 3, \
0.875*sin(t)+1.875, 0.875*cos(t)+0 notitle w l lt 3 lw 3, \
1.125*sin(t)+1.875, 1.125*cos(t)+0 notitle w l lt 3 lw 3
-0.625 0
e
0.625 0
e
1.875 0
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
1.875 1
e
2.74103 0.5
e
2.74103 -0.5
e
1.875 -1
e
1.00897 -0.5
e
1.00897 0.5
e
