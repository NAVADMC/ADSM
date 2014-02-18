set xrange [-14:14]
set yrange [-14:14]
set size square
set xlabel "km (E-W)"
set ylabel "km (N-S)"
set arrow from -14,0 to 14,0 nohead lt 0
set arrow from 0,-14 to 0,14 nohead lt 0
set label "A" at -7.96026,4.3 left
set label "B" at -7.96026,-5.7 left
set label "C" at 0.7,-0.7 left
set label "D1" at 9.36026,4.3 left
set label "D2" at 11.0923,-6.7 left
set label "direct" at -4.5,3.5 left
set label "indirect" at 0.5,-4.5 left
set arrow from -6,3.5 to -1.3,0.75 lt -1 lw 2
set arrow from -7.36,-4.25 to -1.3,-0.75 lt 0 lw 2
set arrow from 1.3,0.75 to 7.36,4.25 lt -1 lw 2
set arrow from 2.6,-1.5 to 9.1,-5.25 lt 0 lw 2
plot '-' notitle w p lt 6 pt 7 ps 2, \
'-' notitle w p lt 6 pt 7 ps 2, \
'-' notitle w p lt 7 pt 71 ps 2, \
'-' notitle w p lt 7 pt 71 ps 2, \
'-' notitle w p lt 7 pt 71 ps 2
-8.66026 5
e
-8.66026 -5
e
0 0
e
8.66026 5
e
10.3923 -6
e
