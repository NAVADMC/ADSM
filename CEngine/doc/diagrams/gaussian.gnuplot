set ylabel "P(x)"
set xlabel "x"
set xrange [-9:9]
set yrange [0:0.5]
set border 1+2
set xtics nomirror
set ytics nomirror
gaussian(x,u,s) = exp(-0.5*(x-u)**2/(s**2)) / (s*sqrt(2*pi))
set label "m" at first 1,0.425 left font "Symbol" tc lt 1
set label "s" at first 2.6,0.425 left font "Symbol" tc lt 1
set label "=0,   =1" at first 1.5,0.425 left tc lt 1
set label "m" at first 4,0.15 left font "Symbol" tc lt 2
set label "s" at first 5.6,0.15 left font "Symbol" tc lt 2
set label "=1,   =3" at first 4.5,0.15 left tc lt 2
plot gaussian(x,0.0,1.0) notitle w l lw 3,\
  gaussian(x,1.0,3.0) notitle w l lw 3
