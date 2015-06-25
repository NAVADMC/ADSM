set encoding iso_8859_1
set xrange [-1:4]
set yrange [-1:4]
set size square
set xlabel "km (E-W)"
set ylabel "km (N-S)"
set arrow from -1,0 to 4,0 nohead lt 0
set arrow from 0,-1 to 0,4 nohead lt 0
set label "0" at 0.166667,-0.166667 left
set label "1" at 1.16667,-0.166667 left
set label "2" at 2.16667,-0.166667 left
set label "3" at 3.16667,-0.166667 left
set label "4" at 0.166667,0.833333 left
set label "5" at 1.16667,0.833333 left
set label "6" at 2.16667,0.833333 left
set label "7" at 3.16667,0.833333 left
set label "8" at 0.166667,1.83333 left
set label "9" at 1.16667,1.83333 left
set label "10" at 2.16667,1.83333 left
set label "11" at 3.16667,1.83333 left
set label "12" at 0.166667,2.83334 left
set label "13" at 1.16667,2.83334 left
set label "14" at 2.16667,2.83334 left
set label "15" at 3.16667,2.83334 left
set label "vaccination\nring" at 1.45,1.55 right tc lt 3
set parametric
plot [0:2*pi] '-' notitle w p lt 7 pt 71 ps 2, \
'-' notitle w p lt 7 pt 71 ps 2, \
'-' notitle w p lt 7 pt 71 ps 2, \
'-' notitle w p lt 7 pt 71 ps 2, \
'-' notitle w p lt 7 pt 71 ps 2, \
'-' notitle w p lt 7 pt 71 ps 2, \
'-' notitle w p lt 6 pt 7 ps 2, \
'-' notitle w p lt 7 pt 71 ps 2, \
'-' notitle w p lt 7 pt 71 ps 2, \
'-' notitle w p lt 7 pt 71 ps 2, \
'-' notitle w p lt 7 pt 71 ps 2, \
'-' notitle w p lt 7 pt 71 ps 2, \
'-' notitle w p lt 7 pt 71 ps 2, \
'-' notitle w p lt 7 pt 71 ps 2, \
'-' notitle w p lt 7 pt 71 ps 2, \
'-' notitle w p lt 7 pt 71 ps 2, \
0.5*sin(t)+2, 0.5*cos(t)+1 notitle w l lt 3 lw 3
0 0
e
1 0
e
2 0
e
3 0
e
0 1
e
1 1
e
2 1
e
3 1
e
0 2
e
1 2
e
2 2
e
3 2
e
0 3
e
1 3
e
2 3
e
3 3
e
