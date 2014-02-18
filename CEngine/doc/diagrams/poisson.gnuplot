set ylabel "P(x)"
set xlabel "x"
set xrange [0:12]
set yrange [0:0.5]
set border 1+2
set xtics nomirror
set ytics nomirror
# To avoid possible overflow problems with the exponent and factorial in the
# poisson formula, we do the calculation with logs.
round(x) = floor(x+0.5)
poisson(x,mu) = exp(round(x)*log(mu) - mu - lgamma(round(x)+1))
set label "m" at first 3.7,0.2 left font "Symbol" tc lt 1
set label "=3" at first 4,0.2 left tc lt 1
set label "m" at first 0.7,0.4 left font "Symbol" tc lt 2
set label "=0.75" at first 1,0.4 left tc lt 2
plot poisson(x,3.0) notitle w histeps lw 3,\
  poisson(x,0.75) notitle w histeps lw 3
