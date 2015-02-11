set xrange [0:5]
set yrange [-2:3]
set size square
set xlabel "km (E-W)"
set ylabel "km (N-S)"
set arrow from 0,0 to 5,0 nohead lt 0
set arrow from 0,-2 to 0,3 nohead lt 0
set label "0" at 3.66666,0.333333 left
set label "1" at 1.16667,-0.166667 left
set label "2" at 2.16667,-0.166667 left
set label "3" at 3.16667,-0.166667 left
set label "4" at 3.16667,0.833333 left
set label "5" at 4.16667,0.833333 left
set label "6*" at 4.16667,-0.166667 left
set label "vaccination\nring" at 3.5,1.8 center tc lt 3
set parametric
plot [0:2*pi] 0.75*sin(t)+3.5, 0.75*cos(t)+0.5 notitle w l lt 3 lw 3,\
'-' notitle w p lt 6 pt 7 ps 2, \
'-' notitle w p lt 1 pt 7 ps 2, \
'-' notitle w p lt 1 pt 7 ps 2, \
'-' notitle w p lt 1 pt 7 ps 2, \
'-' notitle w p lt 7 pt 71 ps 2, \
'-' notitle w p lt 7 pt 71 ps 2, \
'-' notitle w p lt 7 pt 71 ps 2
3.5 0.499999
e
1 0
e
2 0
e
3 0
e
3 1
e
4 1
e
4 0
e
