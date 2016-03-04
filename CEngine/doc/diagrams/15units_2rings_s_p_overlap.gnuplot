set encoding iso_8859_1
set xrange [-8:10]
set yrange [-9:9]
set size square
set xlabel "km (E-W)"
set ylabel "km (N-S)"
set arrow from -8,0 to 10,0 nohead lt 0
set arrow from 0,-9 to 0,9 nohead lt 0
set label "1" at -6,-0.725 center
set label "2" at -5,-0.725 center
set label "3" at -4,-0.725 center
set label "4" at -3,-0.725 center
set label "5" at -2,-0.725 center
set label "6" at -1,-0.725 center
set label "7" at 0,-0.725 center
set label "8" at 1,-0.725 center
set label "9" at 2,-0.725 center
set label "10" at 3,-0.725 center
set label "11" at 4,-0.725 center
set label "12" at 5,-0.725 center
set label "13" at 6,-0.725 center
set label "14" at 7,-0.725 center
set label "15" at 8,-0.725 center
set parametric
plot [0:2*pi] '-' notitle w p lt 7 pt 71 ps 3, \
'-' notitle w p lt 7 pt 71 ps 2.85714, \
'-' notitle w p lt 7 pt 71 ps 2.71429, \
'-' notitle w p lt 7 pt 71 ps 2.57143, \
'-' notitle w p lt 7 pt 71 ps 2.42857, \
'-' notitle w p lt 7 pt 71 ps 2.28571, \
'-' notitle w p lt 6 pt 7 ps 2.14286, \
'-' notitle w p lt 7 pt 71 ps 2, \
'-' notitle w p lt 7 pt 71 ps 1.85714, \
'-' notitle w p lt 7 pt 71 ps 1.71429, \
'-' notitle w p lt 7 pt 71 ps 1.57143, \
'-' notitle w p lt 6 pt 7 ps 1.42857, \
'-' notitle w p lt 7 pt 71 ps 1.28571, \
'-' notitle w p lt 7 pt 71 ps 1.14286, \
'-' notitle w p lt 7 pt 71 ps 1, \
6.5*sin(t)+0, 6.5*cos(t)+0 notitle w l lt 3 lw 3, \
4.5*sin(t)+0, 4.5*cos(t)+0 notitle w l lt 3 lw 3, \
3.33333*sin(t)+0, 3.333*cos(t)+0 notitle w l lt 5 lw 3, \
3.5*sin(t)+5, 3.5*cos(t)+0 notitle w l lt 3 lw 3, \
2.5*sin(t)+5, 2.5*cos(t)+0 notitle w l lt 3 lw 3, \
1.33333*sin(t)+5, 1.333*cos(t)+0 notitle w l lt 5 lw 3
-6 0
e
-5 0
e
-4 0
e
-3 0
e
-2 0
e
-1 0
e
0 0
e
1 0
e
2 0
e
3 0
e
4 0
e
5 0
e
6 0
e
7 0
e
8 0
e
