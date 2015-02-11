set ylabel "P(x)"
set xlabel "x"
set xrange [0:8]
set border 1+2
set xtics nomirror
set ytics nomirror
loglogistic(x,A,B,C) = (x <= A) ? 0 :(C/B) * (((x-A)/B)**(C-1)) / ((1+((x-A)/B)**C)**2)
set label "location=0,scale=1,shape=2" at first 1.1,0.55 left tc lt 1
set label "location=1,scale=2,shape=3" at first 3.5,0.33 left tc lt 2
plot loglogistic(x,0.0,1.0,2.0) notitle w l lw 3,\
  loglogistic(x,1.0,2.0,3.0) notitle w l lw 3
