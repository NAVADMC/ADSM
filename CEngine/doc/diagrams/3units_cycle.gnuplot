set xrange [-6:6]
set yrange [-1.5:10.5]
set size square
set xlabel "km (E-W)"
set ylabel "km (N-S)"
set arrow from -6,0 to 6,0 nohead lt 0
set arrow from 0,-1.5 to 0,10.5 nohead lt 0
set label "direction\nof contacts" at 0,1.5 center
set arrow from -4,0 to 4,0 lt -1 lw 2
set arrow from 4.42265,1 to 0.57735,7.66026 lt -1 lw 2
set arrow from -0.57735,7.66026 to -4.42265,1 lt -1 lw 2
set label "0" at -4.6,-0.4 left
set label "1" at 5.4,-0.4 left
set label "2" at 0.4,8.26026 left
plot '-' notitle w p lt 6 pt 7 ps 1, \
'-' notitle w p lt 6 pt 7 ps 1.75, \
'-' notitle w p lt 6 pt 7 ps 3
-5 0
e
5 0
e
0 8.66026
e
