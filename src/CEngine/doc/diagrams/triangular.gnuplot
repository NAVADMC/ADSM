set ylabel "P(x)"
set xlabel "x"
set border 1+2
set noytics
set noxtics
set xrange [0.5:4.5]
set yrange [0:2.5]
set label "a" at 1,-0.1 center
set label "b" at 4,-0.1 center
set label "c" at 2,-0.1 center
set label "d" at 0.4,2 right
set arrow from 2,0 to 2,2 nohead lt 0 lw 3
set arrow from 0.5,2 to 2,2 nohead lt 0 lw 3
set arrow from 4,0 to 4.5,0 lt -1
set arrow from 0.5,2 to 0.5,2.5 lt -1
plot '-' notitle w l lw 3
1 0
2 2
4 0
e
