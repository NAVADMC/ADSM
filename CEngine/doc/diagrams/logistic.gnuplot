set ylabel "P(x)"
set xlabel "x"
set border 1+2
set xtics nomirror
set ytics nomirror
logistic(x,a,b) = exp ((x-a)/b) / ((1 + exp ((x-a)/b))**2) / b
set label "location=0,\nscale=1" at first -6.5,0.15 left tc lt 1
set label "location=3,\nscale=0.6" at first 5,0.25 left tc lt 2
plot logistic(x,0.0,1.0) notitle w l lw 3,\
  logistic(x,3.0,0.6) notitle w l lw 3
