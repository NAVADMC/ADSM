set ylabel "P(x)"
set xlabel "x"
set xrange [0:6]
set border 1+2
set xtics nomirror
set ytics nomirror
gammapdf(x,a,b) = ((x/b)**(a-1)) * exp (-x/b) / (b * gamma(a))
set label "a" at first 0.75,0.55 left font "Symbol" tc lt 1
set label "b" at first 1.35,0.55 left font "Symbol" tc lt 1
set label "=1,   =1" at first 0.95,0.55 left tc lt 1
set label "a" at first 2.25,0.3 left font "Symbol" tc lt 2
set label "b" at first 2.85,0.3 left font "Symbol" tc lt 2
set label "=2,   =1" at first 2.45,0.3 left tc lt 2
plot gammapdf(x,1.0,1.0) notitle w l lw 3,\
  gammapdf(x,2.0,1.0) notitle w l lw 3
