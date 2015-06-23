set ylabel "P(x)"
set xlabel "x"
set xrange [0:]
set yrange [0:1]
set border 1+2
set xtics nomirror
set ytics nomirror
exponential(x,mu) = exp (-x/mu) / mu
set label "mean=1" at first 0.75,0.6 left tc lt 1
set label "mean=2" at first 2.5,0.2 left tc lt 2
plot exponential(x,1.0) notitle w l lw 3,\
  exponential(x,2.0) notitle w l lw 3
