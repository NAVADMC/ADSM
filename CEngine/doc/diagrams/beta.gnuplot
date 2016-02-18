set ylabel "P(x)"
set xlabel "x"
set xrange [0:2]
set yrange [0:3]
set border 1+2
set xtics nomirror
set ytics nomirror
beta(x,a,b,l,s) = gamma(a+b) / (gamma(a) * gamma(b) * (s-l)**(a+b-1)) * ((x-l)**(a-1)) * ((s-x)**(b-1))
set label "a" at first 0.12,1.9 left font "Symbol" tc lt 1
set label "b" at first 0.22,1.9 left font "Symbol" tc lt 1
set label "=1,   =1" at first 0.15,1.9 left tc lt 1
set label "a" at first 0.37,1.65 left font "Symbol" tc lt 2
set label "b" at first 0.47,1.65 left font "Symbol" tc lt 2
set label "=2,   =2" at first 0.4,1.65 left tc lt 2
set label "a" at first 0.71,1.4 left font "Symbol" tc lt 3
set label "b" at first 0.81,1.4 left font "Symbol" tc lt 3
set label "=4,   =2" at first 0.74,1.4 left tc lt 3
plot beta(x,1.0,2.0,0,1) notitle w l lw 3,\
  beta(x,2.0,2.0,0,1) notitle w l lw 3,\
  beta(x,4.0,2.0,0,1) notitle w l lw 3,\
  beta(x,4.0,2.0,0.5,1.5) notitle w l lw 3
