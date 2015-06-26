set ylabel "P(x)"
set xlabel "x"
set border 1+2
set noxtics
set noytics
set xrange [0:5]
set yrange [0:2.5]
set label "a" at 1,-0.1 center
set label "b" at 4,-0.1 center
set arrow from 4,0 to 5,0 lt -1
set arrow from 0,2 to 0,2.5 lt -1
plot '-' notitle w l lw 3
1 0
1 2
4 2
4 0
e
