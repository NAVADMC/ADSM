set encoding iso_8859_1
set xrange [-4:4]
set yrange [-4:4]
set size square
set xlabel "km (E-W)"
set ylabel "km (N-S)"
set arrow from -4,0 to 4,0 nohead lt 0
set arrow from 0,-4 to 0,4 nohead lt 0
set label "G" at 0.266667,-0.266667 left
set label "A1" at 1.04312,2.63111 left
set label "A2" at 0.84901,1.90666 left
set label "A3" at 2.38799,1.85465 left
set label "A4" at 1.85766,1.32432 left
set label "B1" at 3.16445,0.50979 left
set label "B2" at 2.44,0.315676 left
set label "B3" at 3.16445,-1.04312 left
set label "B4" at 2.44,-0.84901 left
set label "C1" at 2.38799,-2.38799 left
set label "C2" at 1.85766,-1.85766 left
set label "C3" at 1.04312,-3.16445 left
set label "C4" at 0.84901,-2.44 left
set label "D1" at -0.50979,-3.16445 left
set label "D2" at -0.315676,-2.44 left
set label "D3" at -1.85465,-2.38799 left
set label "D4" at -1.32432,-1.85766 left
set label "E1" at -2.63111,-1.04312 left
set label "E2" at -1.90666,-0.84901 left
set label "E3" at -2.63111,0.50979 left
set label "E4" at -1.90666,0.315676 left
set label "F1" at -1.85465,1.85465 left
set label "F2" at -1.32432,1.32432 left
set label "F3" at -0.50979,2.63111 left
set label "F4" at -0.315676,1.90666 left
set label "H" at 0.266667,3.23333 left
set parametric
plot [0:2*pi] '-' notitle w p lt 6 pt 7 ps 2, \
'-' notitle w p lt 7 pt 71 ps 3, \
'-' notitle w p lt 7 pt 71 ps 3, \
'-' notitle w p lt 7 pt 71 ps 1, \
'-' notitle w p lt 7 pt 71 ps 1, \
'-' notitle w p lt 7 pt 71 ps 3, \
'-' notitle w p lt 7 pt 71 ps 3, \
'-' notitle w p lt 7 pt 71 ps 1, \
'-' notitle w p lt 7 pt 71 ps 1, \
'-' notitle w p lt 7 pt 71 ps 3, \
'-' notitle w p lt 7 pt 71 ps 3, \
'-' notitle w p lt 7 pt 71 ps 1, \
'-' notitle w p lt 7 pt 71 ps 1, \
'-' notitle w p lt 7 pt 71 ps 3, \
'-' notitle w p lt 7 pt 71 ps 3, \
'-' notitle w p lt 7 pt 71 ps 1, \
'-' notitle w p lt 7 pt 71 ps 1, \
'-' notitle w p lt 7 pt 71 ps 3, \
'-' notitle w p lt 7 pt 71 ps 3, \
'-' notitle w p lt 7 pt 71 ps 1, \
'-' notitle w p lt 7 pt 71 ps 1, \
'-' notitle w p lt 7 pt 71 ps 3, \
'-' notitle w p lt 7 pt 71 ps 3, \
'-' notitle w p lt 7 pt 71 ps 1, \
'-' notitle w p lt 7 pt 71 ps 1, \
'-' notitle w p lt 6 pt 7 ps 2, \
4.25*sin(t)+0, 4.25*cos(t)+3.5 notitle w l lt 3 lw 3, \
3.2*sin(t)+0, 3.2*cos(t)+0 notitle w l lt 3 lw 3
0 0
e
0.776457 2.89778
e
0.582343 2.17333
e
2.12132 2.12132
e
1.59099 1.59099
e
2.89778 0.776457
e
2.17333 0.582343
e
2.89778 -0.776457
e
2.17333 -0.582343
e
2.12132 -2.12132
e
1.59099 -1.59099
e
0.776457 -2.89778
e
0.582343 -2.17333
e
-0.776457 -2.89778
e
-0.582343 -2.17333
e
-2.12132 -2.12132
e
-1.59099 -1.59099
e
-2.89778 -0.776457
e
-2.17333 -0.582343
e
-2.89778 0.776457
e
-2.17333 0.582343
e
-2.12132 2.12132
e
-1.59099 1.59099
e
-0.776457 2.89778
e
-0.582343 2.17333
e
0 3.5
e
