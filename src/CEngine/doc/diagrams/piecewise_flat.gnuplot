set ylabel "P(x)"
set xlabel "x"
set border 1+2
set xtics nomirror 2
set mxtics 2
set ytics nomirror
set xrange [0:7]
set yrange [0:1]
set arrow from 2,0 to 2,0.5 nohead lt 0 lw 3
set arrow from 5,0 to 5,0.5 nohead lt 0 lw 3
set arrow from 10,0 to 10,5 nohead lt 0 lw 3
set arrow from 0,0 to 7,0 lt -1
set arrow from 0,0 to 0,1 lt -1
plot '-' notitle w l lw 3
1 0
2 0.5
3 0
4 0
5 0.5
6 0
e
