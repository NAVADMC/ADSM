set encoding iso_8859_1
set xrange [-5.5:5.5]
set yrange [-4:7]
set size square
set xlabel "km (E-W)"
set ylabel "km (N-S)"
set arrow from -5.5,0 to 5.5,0 nohead lt 0
set arrow from 0,-4 to 0,7 nohead lt 0
set label "G" at 0.366667,-0.366667 left
set label "A1" at 1.14312,2.53111 left
set label "A2" at 0.94901,1.80666 left
set label "A3" at 2.48799,1.75465 left
set label "A4" at 1.95766,1.22432 left
set label "B1" at 3.26445,0.40979 left
set label "B2" at 2.54,0.215676 left
set label "B3" at 3.26445,-1.14312 left
set label "B4" at 2.54,-0.94901 left
set label "C1" at 2.48799,-2.48799 left
set label "C2" at 1.95766,-1.95766 left
set label "C3" at 1.14312,-3.26445 left
set label "C4" at 0.94901,-2.54 left
set label "D1" at -0.40979,-3.26445 left
set label "D2" at -0.215676,-2.54 left
set label "D3" at -1.75465,-2.48799 left
set label "D4" at -1.22432,-1.95766 left
set label "E1" at -2.53111,-1.14312 left
set label "E2" at -1.80666,-0.94901 left
set label "E3" at -2.53111,0.40979 left
set label "E4" at -1.80666,0.215676 left
set label "F1" at -1.75465,1.75465 left
set label "F2" at -1.22432,1.22432 left
set label "F3" at -0.40979,2.53111 left
set label "F4" at -0.215676,1.80666 left
set label "H" at 0.366667,5.88333 left
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
6.75*sin(t)+0, 6.75*cos(t)+6.25 notitle w l lt 3 lw 3, \
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
0 6.25
e
