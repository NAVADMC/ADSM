set ylabel "P(x)"
set xlabel "x"
set xrange [0:3.5]
set yrange [0:1.4]
set border 1+2
set xtics nomirror
set ytics nomirror
invgaussian(x,u,l) = ((l/(2*pi*x*x*x))**0.5) * exp(-l*((x-u)**2)/(2*u*u*x))
set label "m" at first 0.4,1.15 left font "Symbol" tc lt 1
set label "l" at first 0.74,1.15 left font "Symbol" tc lt 1
set label "=1,   =0.2" at first 0.5,1.15 left tc lt 1
set label "m" at first 1.4,0.48 left font "Symbol" tc lt 2
set label "l" at first 1.74,0.48 left font "Symbol" tc lt 2
set label "=1,   =3" at first 1.5,0.48 left tc lt 2
plot invgaussian(x,1.0,0.2) notitle w l lw 3,\
  invgaussian(x,1.0,3.0) notitle w l lw 3
