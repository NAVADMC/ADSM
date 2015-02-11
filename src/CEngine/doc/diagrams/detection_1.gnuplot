set xlabel "Days that the unit has been showing\nclinical signs"
set xrange [1:8.5]
set ylabel 'p'
set yrange [0:1.1]
set border 1+2
set xtics nomirror
set ytics nomirror
set arrow from 1,1 to 1,1.1 lt -1
set arrow from 8,0 to 8.5,0 lt -1
plot '-' notitle w p pt 7 lc rgb "green" ps 3,\
 '-' notitle w p pt 7 lc rgb "blue" ps 3,\
 '-' notitle w p pt 7 lc rgb "#FF00FF" ps 3,\
 '-' notitle w l lt 1 lw 4
6 1.0
e
2 0.4
e
3 0.6
e
1 0.2
5 1
8 1
e
