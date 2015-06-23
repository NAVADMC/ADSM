set ylabel "P(x)"
set xlabel "x"
set xrange [1:5]
set yrange [0:2]
set border 1+2
set xtics nomirror
set ytics nomirror
#Names for parameters given here follow @Risk and Vose, _Quantitative Risk Analysis_.
#Note that GSL parameter names are different:
#theta (@Risk) = a (GSL)
#a (@Risk) = b (GSL)
pareto(x,theta,a) = (theta/a)/((x/a)**(theta+1))
set label "theta=1,\na=1" at first 3.6,0.3 left tc lt 1
set label "theta=4,\na=1" at first 1.4,1.6 left tc lt 2
set label "theta=0.5,\na=1" at first 2,0.5 left tc lt 3
plot pareto(x,1.0,1.0) notitle w l lw 3 lt 1,\
  pareto(x,4.0,1.0) notitle w l lw 3 lt 2,\
  pareto(x,0.5,1.0) notitle w l lw 3 lt 3
