set encoding iso_8859_1
set xrange [-3:3]
set yrange [-3:3]
set size square
set xlabel "km (E-W)"
set ylabel "km (N-S)"
set arrow from -3,0 to 3,0 nohead lt 0
set arrow from 0,-3 to 0,3 nohead lt 0
set label "0" at -0.8,0.8 left
set label "1" at -1.8,-0.2 left
set label "2" at -0.8,-1.2 left
set label "3" at 1.2,0.8 left
set label "4" at 2.2,-0.2 left
set label "5" at 1.2,-1.2 left
set label "6" at 0.2,-0.2 left
set label "7" at -0.8,-0.2 left
set label "8" at 1.2,-0.2 left
set label "added after\nothers" at 0,2.5 center
set arrow from 0,1.9 to 0,0.8 lt -1
set parametric
plot [0:2*pi] 0.75*sin(t)-1, 0.75*cos(t)+1 notitle w l lt 1 lw 3,\
  0.75*sin(t)-2, 0.75*cos(t) notitle w l lt 1 lw 3,\
  0.75*sin(t)-1, 0.75*cos(t)-1 notitle w l lt 1 lw 3,\
  0.75*sin(t)+1, 0.75*cos(t)+1 notitle w l lt 1 lw 3,\
  0.75*sin(t)+2, 0.75*cos(t) notitle w l lt 1 lw 3,\
  0.75*sin(t)+1, 0.75*cos(t)-1 notitle w l lt 1 lw 3,\
  0.75*sin(t), 0.75*cos(t) notitle w l lt 2 lc 1 lw 3,\
  '-' notitle w p lt 6 pt 7 ps 2, \
  '-' notitle w p lt 6 pt 7 ps 2, \
  '-' notitle w p lt 6 pt 7 ps 2, \
  '-' notitle w p lt 6 pt 7 ps 2, \
  '-' notitle w p lt 6 pt 7 ps 2, \
  '-' notitle w p lt 6 pt 7 ps 2, \
  '-' notitle w p lt 6 pt 7 ps 2, \
  '-' notitle w p lt 6 pt 7 ps 2, \
  '-' notitle w p lt 7 pt 71 ps 2
-1 1
e
-2 0
e
-1 -1
e
1 1
e
2 0
e
1 -1
e
0 0
e
-1 0
e
1 0
e
