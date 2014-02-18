df(d,m)=(m-d)/(m-1.0)
air(d,m,p)=p*df(d,m)
set yrange [0:1.1]
set xrange [0:27]
set xlabel 'distance from source (km)'
set ylabel 'probability of spread'
set arrow from 1,0 to 1,0.5 nohead lt 0
set arrow from 5,0 to 5,0.5 nohead lt 0
set arrow from 10,0 to 10,0.5 nohead lt 0
plot 0.5 notitle w l lt 0,\
  air(x,25,0.9) title 'p at 1 km=0.9, prev=1.0' lt 1,\
  air(x,25,0.9*0.75) title 'prev=0.75' lt 2,\
  air(x,25,0.9*0.6) title 'prev=0.6' lt 3
