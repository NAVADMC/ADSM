set xlabel "Days since first detection of disease in any\nunit in the population"
set xrange [0:27.5]
set ylabel 'p'
set yrange [0:1.1]
set border 1+2
set xtics nomirror
set ytics nomirror
set arrow from 0,1 to 0,1.1 lt -1
set arrow from 25,0 to 27.5,0 lt -1
set label "Baseline before\n1st detection" at 5,0.6 center
set arrow from 2.5,0.48 to 0,0.13 lt -1
set label "1st detection" at 7,0.4 center
set arrow from 4.5,0.35 to 1,0.1 lt -1
plot '-' notitle w p pt 7 lc rgb "green" ps 3,\
 '-' notitle w p pt 7 lc rgb "blue" ps 3,\
 '-' notitle w p pt 7 lc rgb "#FF00FF" ps 3,\
 '-' notitle w l lt 1 lw 4
5 0.1
e
0 0.1
e
15 0.5
e
0 0.1
7 0.1
25 1
27 1
e
