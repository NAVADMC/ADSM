set xrange [0:6]
set yrange [0:1]
set xlabel "day"
set ylabel "prevalence"
set border 1+2
set xtics nomirror
set ytics nomirror
set arrow from 0.5,0 to 0.5,0.16667 nohead lt 0
set arrow from 0.5,0.16667 to 0,0.16667 nohead lt 0
set arrow from 1.5,0 to 1.5,0.5 nohead lt 0
set arrow from 1.5,0.5 to 0,0.5 nohead lt 0
set arrow from 2.5,0 to 2.5,0.83333 nohead lt 0
set arrow from 2.5,0.83333 to 0,0.83333 nohead lt 0
plot '-' notitle w l lw 3
0 0
3 1
6 0
e
