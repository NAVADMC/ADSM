set xlabel "# Processors"
set xrange [1:]
set x2label "# Trials per processor"
set x2range [100:5]
set x2tics
set ylabel "Speedup (x)"
set yrange [1:]
plot x title 'Ideal' w l lw 3, '-' title 'Actual' w l lw 3
1 1
2 2.2
4 4.05
8 6.84
12 9.95
16 11.72
20 13.06
e
