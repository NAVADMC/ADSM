set xrange [0:4]
set yrange [0:1]
set xlabel "day"
set ylabel "prevalence"
set border 1+2
set xtics nomirror
set ytics nomirror
set arrow from 0.5,0 to 0.5,0.5 nohead lt 0
set arrow from 0.5,0.5 to 0,0.5 nohead lt 0
plot '-' notitle w l lw 3
0 0
1 1
2 0
e
