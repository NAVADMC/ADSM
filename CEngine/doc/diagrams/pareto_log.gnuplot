set ylabel "P(x)"
set xlabel "x"
set xrange [1:20]
set logscale x
set yrange [10e-4:1]
set logscale y
set border 1+2
set xtics nomirror
set ytics nomirror
#Names for parameters given here follow @Risk and Vose, _Quantitative Risk Analysis_.
#Note that GSL parameter names are different:
#theta (@Risk) = a (GSL)
#a (@Risk) = b (GSL)
pareto(x,theta,a) = (theta/a)/((x/a)**(theta+1))
set label "theta=1,\na=1" at first 5,0.01 left tc lt 1
set label "theta=4,\na=1" at first 1.9,0.006 left tc lt 2
set label "theta=0.5,\na=1" at first 8,0.05 left tc lt 3
plot pareto(x,1.0,1.0) notitle w l lw 3 lt 1,\
  pareto(x,4.0,1.0) notitle w l lw 3 lt 2,\
  pareto(x,0.5,1.0) notitle w l lw 3 lt 3
