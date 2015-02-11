set xrange [0:1]
set xlabel "Ratio diameter : short side of study area"
set ylabel "Speedup (x)"
plot '-' title 'Swiss data' w l lw 3,\
 '-' title 'UK data' w l lw 3,\
 '-' title 'Ontario data' w l lw 3,\
 '-' title 'Iowa data' w l lw 3,\
 1 notitle w l lt 0
0.028 43.3
0.046 23.4
0.093  9.7
0.139  5.1
0.232  2.3
0.463 -1.2
0.927 -2.5
e
0.036  9.8
0.073  7.4
0.109  4.8
0.182  3.2
0.365  1.7
0.547  1.3
0.911  1.0
e
0.008 57.4
0.013 37.5
0.026 16.5
0.040  8.5
0.066  4.0
0.132  1.6
0.265 -1.1
0.397 -1.4
0.662 -1.6
e
0.019 17.5
0.031 12.2
0.062  5.7
0.093  3.8
0.155  2.1
0.309  1.3
0.618  1.0
0.927  1.0
e
