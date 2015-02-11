set ylabel "P(x)"
set xlabel "x"
set border 1+2
set xtics nomirror 5
set mxtics 5
set ytics nomirror
set xrange [0:15]
set yrange [0:0.25]
set arrow from 5,0 to 5,0.072 nohead lt 0 lw 3
set arrow from 7.5,0 to 7.5,0.072 nohead lt 0 lw 3
set arrow from 10,0 to 10,0.18 nohead lt 0 lw 3
set arrow from 0,0 to 15,0 lt -1
set arrow from 0,0 to 0,0.25 lt -1
plot '-' notitle w l lw 3
1 0
5 0.072
7.5 0.072
10 0.18
14 0
e
