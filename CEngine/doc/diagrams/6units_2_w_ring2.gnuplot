set encoding iso_8859_1
set xrange [-1:3]
set yrange [-2:2]
set size square
set xlabel "km (E-W)"
set ylabel "km (N-S)"
set arrow from -1,0 to 3,0 nohead lt 0
set arrow from 0,-2 to 0,2 nohead lt 0
set label "0 Cattle" at 0.133333,-0.133333 left
set label "1 Pigs" at 2.13333,-0.133333 left
set label "2 Cattle" at 0.133333,0.866666 left
set label "3 Pigs" at 0.133333,-1.13333 left
set label "4 Cattle" at 2.13333,0.866666 left
set label "5 Pigs" at 2.13333,-1.13333 left
set label "vaccination\nring" at 1.9,1.7 center tc lt 3
set parametric
plot [0:2*pi] 2.05*sin(t), 2.05*cos(t) notitle w l lt 3 lw 3, \
'-' notitle w p lt 6 pt 7 ps 2, \
'-' notitle w p lt 6 pt 7 ps 2, \
'-' notitle w p lt 7 pt 71 ps 2, \
'-' notitle w p lt 7 pt 71 ps 2, \
'-' notitle w p lt 7 pt 71 ps 2, \
'-' notitle w p lt 7 pt 71 ps 2
0 0
e
2 0
e
0 1
e
0 -1
e
2 1
e
2 -1
e
