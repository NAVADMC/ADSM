set xrange [-1:3]
set yrange [-1.5:2.5]
set size square
set xlabel "km (E-W)"
set ylabel "km (N-S)"
set arrow from -1,0 to 3,0 nohead lt 0
set arrow from 0,-1.5 to 0,2.5 nohead lt 0
set label "0" at 0.133333,-0.133333 left
set label "1" at 1.13333,-0.133333 left
set label "2" at 2.13333,-0.133333 left
set label "3" at 0.633334,0.866666 left
set parametric
plot [0:2*pi] 1.5*sin(t)+0.5,1.5*cos(t)+1 notitle w l lt 7 lw 3, \
'-' notitle w p lt 7 pt 71 ps 2, \
'-' notitle w p lt 6 pt 7 ps 2, \
'-' notitle w p lt 7 pt 71 ps 2, \
'-' notitle w p lt 6 pt 7 ps 2
0 0
e
1 0
e
2 0
e
0.5 1
e
