set ylabel "P(x)"
set xlabel "x"
set xrange [0.0001:6]
set border 1+2
set xtics nomirror
set ytics nomirror
lognormal(x,z,s) = exp (-0.5 * ((log(x)-z)/s)**2) / (x * s * sqrt(2*pi))
set label "z" at first 1.5,0.35 left font "Symbol" tc lt 1
set label "s" at first 2.05,0.35 left font "Symbol" tc lt 1
set label "=0,   =1" at first 1.65,0.35 left tc lt 1
set label "z" at first 0.28,0.75 left font "Symbol" tc lt 2
set label "s" at first 1.05,0.75 left font "Symbol" tc lt 2
set label "=0.5,   =2" at first 0.43,0.75 left tc lt 2
plot lognormal(x,0.0,1.0) notitle w l lw 3,\
  lognormal(x,0.5,2.0) notitle w l lw 3
