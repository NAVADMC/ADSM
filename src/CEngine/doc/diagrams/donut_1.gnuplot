set xrange [-1:4]
set yrange [-2.5:2.5]
set size square
set xlabel "km (E-W)"
set ylabel "km (N-S)"
set arrow from -1,0 to 4,0 nohead lt 0
set arrow from 0,-2.5 to 0,2.5 nohead lt 0
set label "0" at 0.166667,-0.166667 left
set label "1" at 1.16667,0.833333 left
set label "2" at 1.16667,-1.16667 left
set label "3" at 2.16667,-0.166667 left
set label "4" at 1.16667,-0.166667 left
set label "5" at 3.16667,-0.166667 left
set parametric
plot [0:2*pi] 0.75*sin(t),0.75*cos(t) notitle w l lt 7 lw 3, \
0.75*sin(t)+1,0.75*cos(t)+1 notitle w l lt 7 lw 3, \
0.75*sin(t)+1,0.75*cos(t)-1 notitle w l lt 7 lw 3, \
0.75*sin(t)+2,0.75*cos(t) notitle w l lt 7 lw 3, \
'-' notitle w p lt 6 pt 7 ps 2, \
'-' notitle w p lt 6 pt 7 ps 2, \
'-' notitle w p lt 6 pt 7 ps 2, \
'-' notitle w p lt 6 pt 7 ps 2, \
'-' notitle w p lt 6 pt 7 ps 2, \
'-' notitle w p lt 7 pt 71 ps 2
0 0
e
1 1
e
1 -1
e
2 0
e
1 0
e
3 0
e
