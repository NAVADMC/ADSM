set ylabel "P(x)"
set xlabel "x"
set xrange [0:]
set yrange [0:1]
set border 1+2
set xtics nomirror
set ytics nomirror
weibull(x,a,b) = a / (b**a) * (x**(a-1)) * exp (-(x/b)**a)
set label "a" at first 0.4,0.9 left font "Symbol" tc lt 1
set label "b" at first 1.4,0.9 left font "Symbol" tc lt 1
set label "=1,   =1" at first 0.7,0.9 left tc lt 1
set label "a" at first 2.5,0.5 left font "Symbol" tc lt 2
set label "b" at first 3.5,0.5 left font "Symbol" tc lt 2
set label "=3,   =2" at first 2.8,0.5 left tc lt 2
set label "a" at first 4,0.2 left font "Symbol" tc lt 3
set label "b" at first 5,0.2 left font "Symbol" tc lt 3
set label "=2,   =3" at first 4.3,0.2 left tc lt 3
plot weibull(x,1.0,1.0) notitle w l lw 3,\
  weibull(x,3.0,2.0) notitle w l lw 3,\
  weibull(x,2.0,3.0) notitle w l lw 3
