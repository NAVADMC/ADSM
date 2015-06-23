set xrange [0:4]
set yrange [0:1]
set xlabel "day"
set ylabel "prevalence"
set border 1+2
set xtics nomirror
set ytics nomirror
set arrow from 0.5,0 to 0.5,0.25 nohead lt 0
set arrow from 0.5,0.25 to 0,0.25 nohead lt 0
set arrow from 1.5,0 to 1.5,0.75 nohead lt 0
set arrow from 1.5,0.75 to 0,0.75 nohead lt 0
plot '-' notitle w l lw 3
0 0
2 1
4 0
e
