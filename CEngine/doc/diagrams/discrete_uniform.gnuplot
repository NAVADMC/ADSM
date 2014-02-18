set ylabel "P(x)"
set xlabel "x"
set xrange [-3:5]
set yrange [0:0.6]
set border 1+2
set xtics nomirror
set ytics nomirror
# gnuplot doesn't have a built-in combinations or "n choose r" function, so we
# implement it.  gnuplot does have a factorial function, but to avoid overflow
# problems, it's safer to use the fact that gamma(n+1) = n! and do the
# calculation with logs.
choose(n,r) = exp(lgamma(n+1) - lgamma(r+1) - lgamma(n-r+1))
round(x) = floor(x+0.5)
discreteuniform(x,a,b) = ((x < a) || (x > b)) ? 0 : (1.0 / (b - a + 1))
set label "min=-1, max=3" at first -1,0.23 left tc lt 1
set label "min=2, max=4" at first 2,0.36 left tc lt 2
plot discreteuniform(x,-1,3) notitle w histeps lw 3, \
  discreteuniform(x,2,4) notitle w histeps lw 3 

