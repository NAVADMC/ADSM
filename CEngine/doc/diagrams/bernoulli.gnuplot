set ylabel "P(x)"
set xlabel "x"
set xrange [-1:2]
set samples 4
set yrange [0:0.8]
set border 1+2
set xtics nomirror
set ytics nomirror
bernoulli(x,p) = x<0? 0 : x>1 ? 0 : (p**x) * ((1-p)**(1-x))
set label "p=0.7" at first 1,0.75 center tc lt 1
set label "p=0.2" at first 4.75,0.125 left tc lt 2
plot bernoulli(x,0.7) notitle w histeps lw 3
