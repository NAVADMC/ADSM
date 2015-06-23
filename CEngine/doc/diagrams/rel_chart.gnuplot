set ylabel "y"
set xlabel "x"
set border 1+2
set xtics nomirror 2
set mxtics 2
set ytics nomirror 1
set xrange [-3:6]
set yrange [-3:3]
set arrow from -3,1 to -1,1 nohead lt 0 lw 3
set arrow from 4,0 to 6,0 nohead lt 0 lw 3
set arrow from -3,-3 to 6,-3 lt -1
set arrow from -3,-3 to -3,3 lt -1
plot '-' notitle w l lw 3
-1 1
0 2
1 2
1.5 1.5
2.5 -1.5
3 -2
4 0
e
