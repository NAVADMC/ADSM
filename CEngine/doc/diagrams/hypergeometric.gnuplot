set ylabel "P(x)"
set xlabel "x"
set xrange [0:10]
set yrange [0:1.0]
set border 1+2
set xtics nomirror
set ytics nomirror
# gnuplot doesn't have a built-in combinations or "n choose r" function, so we
# implement it.  gnuplot does have a factorial function, but to avoid overflow
# problems, it's safer to use the fact that gamma(n+1) = n! and do the
# calculation with logs.
choose(n,r) = exp(lgamma(n+1) - lgamma(r+1) - lgamma(n-r+1))
round(x) = floor(x+0.5)
# Recall the screwy way that the GSL handles parameters:
# Sample size = n (@Risk) = t (GSL)
# Subpopulation = D (@Risk) = n1 (GSL)
# Total population = M (@Risk) = n2 + n1 (GSL) 
hypergeometric(x,n1,n2,t) = choose(n1, round(x)) * choose(n2, t-round(x)) / choose(n1+n2, t)
# n1=3, n2=5, t=4
set label "M=8, D=3, n=4" at first 2.75,0.25 left tc lt 1
plot hypergeometric(x,3,5,4) notitle w histeps lw 3
