set xrange [0:6.5]
set yrange [0:1.1]
set xlabel "day"
set ylabel "prevalence"
set border 1+2
set xtics nomirror
set ytics nomirror
#
set arrow from 0,0.6 to 3.5,0.6 nohead lt 0 lw 4
set arrow from 3.5,0.6 to 3.5,0 nohead lt 0 lw 4
set label 'day 4' at 0.3,0.56 left
#
set arrow from 0,0.75 to 4.5,0.75 nohead lt 0 lw 4
set arrow from 4.5,0.75 to 4.5,0 nohead lt 0 lw 4
set label 'day 5' at 0.5,0.71 left
#
set arrow from 0,1 to 5.5,1 nohead lt 0 lw 4
set arrow from 5.5,1 to 5.5,0 nohead lt 0 lw 4
set label 'day 6' at 0.7,0.96 left
#
plot '-' notitle w l lw 6
0 0.1
1.5 0.1
3.5 0.6
4.5 0.76
5.5 1.0
6 0
e
