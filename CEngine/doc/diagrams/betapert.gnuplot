set ylabel "P(x)"
set xlabel "x"
set xrange [0:3]
set yrange [0:3]
set border 1+2
set xtics nomirror
set ytics nomirror
beta(x,a,b,l,s) = gamma(a+b) / (gamma(a) * gamma(b) * (s-l)**(a+b-1)) * ((x-l)**(a-1)) * ((s-x)**(b-1))
set label "min=0,\nmode=0.5,\nmax=1" at first 0.3,2.7 left tc lt 1
set label "min=0.5,\nmode=2,\nmax=2.5" at first 2.3,1.3 left tc lt 2
set label "min=0,\nmode=0.33,\nmax=2.5" at first 0.85,1.15 left tc lt 3
plot beta(x,4.0,4.0,0.0,1.0) notitle w l lw 3,\
  beta(x,4.67,2.33,0.5,2.5) notitle w l lw 3,\
  beta(x,1.49,4.35,0,2.5) notitle w l lw 3
