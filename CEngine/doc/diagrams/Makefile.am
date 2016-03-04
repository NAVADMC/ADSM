## Makefile.am -- Process this file with automake to produce Makefile.in

%.gnuplot: $(top_srcdir)/modules/test/%.xml
	python units2gnuplot.py < $< > $@

.dia.eps:
	dia -e $@ $<

.dia.svg:
	dia -e $@ $<

.gnuplot.svg:
	(echo set term svg enhanced mouse && echo set output \'$@\' && cat $<) | gnuplot

.gnuplot.eps:
	(echo set terminal postscript eps color 24 && echo set output \'$@\' && cat $<) | gnuplot

.eps.png:
	convert -density 72x72 $< $@
	convert -geometry "640x1024>" $@ $@

.dot.png:
	dot -T png $< > $@

dist_noinst_DATA = state-transition.png \
  uniform.png \
  triangular.png \
  piecewise.png \
  piecewise_flat.png \
  gaussian.png \
  beta.png \
  betapert.png \
  gamma.png \
  weibull.png \
  exponential.png \
  logistic.png \
  loglogistic.png \
  lognormal.png \
  pearson.png \
  poisson.png \
  negbinomial.png \
  pareto.png pareto_log.png \
  binomial.png \
  bernoulli.png \
  discrete_uniform.png \
  hypergeometric.png \
  inverse_gaussian.png \
  rel_chart.png \
  airborne.png \
  directions.png \
  building_blocks.png \
  events.png \
  events_flowchart.png \
  priority_queues.png \
  1unit.png \
  1unit_start_infectious.png \
  1unit_start_infectious_1dayleft.png \
  1unit_start_infectious_2daysleft.png \
  1unit_start_subclinical.png \
  1unit_1dayleft.png \
  1unit_3daysleft.png \
  2units.png \
  2units_xy.png \
  2units_pigs_cattle_pigs_infected.png \
  2units_pigs_cattle_all_infected.png \
  2targets_same_dist_same_size.png \
  2targets_same_dist_diff_size.png \
  2units_1_start_destroyed.png \
  2units_1_start_nimmune.png \
  2units_1_start_nimmune_2daysleft.png \
  2units_1_start_nimmune_3daysleft.png \
  2units_1_start_vimmune.png \
  2units_1_start_vimmune_1dayleft.png \
  2units_1_start_vimmune_2daysleft.png \
  2units_ascii.png 2units_iso88591.png 2units_utf8.png 2units_utf8_no_bom.png \
  2units_utf16_big_endian.png 2units_utf16_big_endian_no_bom.png \
  2units_utf16_little_endian.png 2units_utf16_little_endian_no_bom.png \
  3units.png \
  3units_2_at_same_loc.png \
  3units_pigs_2cattle_pigs_infected.png \
  3units_pigs_cattle_sheep_sheep_infected.png \
  3units_pigs_cattle_sheep_pigs_sheep_infected.png \
  3units_pigs_cattle_sheep_all_infected.png \
  3units_1_start_vimmune.png \
  3units_1_start_destroyed.png \
  3targets_same_dist_same_size.png \
  4units_line.png \
  4units_line_xy.png \
  4units_all_infected.png \
  4units_line_2.png \
  4units_line_3.png \
  4units_line_4.png \
  4units_2.png \
  4units_2_reversed.png \
  5units.png \
  5units_2.png \
  5units_very_close.png \
  6units.png \
  6units_2.png \
  7units.png \
  8units_all_infected.png \
  8units_all_infected_diff_types.png \
  8units_2rows.png \
  8units_2rows_2.png \
  8units_2rows_3.png \
  8units_2rows_4.png \
  9units.png \
  9units_2_zone_holes.png \
  10units_2cols.png \
  12units_2rings_largesmall_plus2infected.png \
  14units_2rings_overlap.png \
  15units_line.png \
  15units_2rings.png \
  units_circle.png \
  units_circle2.png \
  16units_square.png \
  16units_2rings.png \
  20units_2rings.png \
  21units_3rings_overlap.png \
  24units_2rings_plus2infected.png \
  no_rtree_lat0.png \
  rtree_lat0.png \
  no_rtree_lat45.png \
  no_rtree_lat45_xy.png \
  rtree_lat45.png \
  rtree_lat45_xy.png \
  no_rtree_lat_minus45.png \
  rtree_lat_minus45.png \
  no_rtree_contact_spread.png \
  rtree_contact_spread.png \
  1000units_line.png \
  speedup.png \
  uncontrolled_example.png \
  rtree_benefit.png \
  contact_problem.png \
  contact_proof.png \
  extend_array_1.png \
  extend_array_2.png \
  surv_levels.png \
  basic_circle.png \
  ordered_circles.png \
  adjacent_zones.png \
  enclosure.png \
  enclosure2.png \
  split_zones.png \
  movement_inside.png \
  lower_to_higher.png \
  detour.png \
  1_zone_1_focus.png \
  2_zones_1_focus.png \
  1_zone_2_foci.png \
  1_zone_2_foci_merge.png \
  1_zone_2_foci_merge_w_triangle.png \
  2_zones_2_foci.png \
  2_zones_2_foci_merge1.png \
  2_zones_2_foci_merge2.png \
  3_foci_merge.png \
  1_zone_13_foci.png \
  1_zone_13_foci_merge.png \
  zones_trace_cattle.png \
  zones_trace_pigs.png \
  zones_trace_both.png \
  zones_trace_both_merge.png \
  2foci_separate.png \
  2foci_joined.png \
  3foci.png \
  donut_0.png \
  donut_1.png \
  2_zone_levels.png \
  2targets_1_in_zone.png \
  prevalence_1.png \
  prevalence_2.png \
  prevalence_triangle_6days.png \
  air_prevalence.png \
  air_prevalence_incr.png \
  prevalence_day2.png \
  prevalence_day4.png \
  16units_1_zone.png \
  16units_2_zones.png \
  7units_w_ring.png \
  6units_2_w_ring.png \
  6units_2_w_ring2.png \
  6units_2_w_rings.png \
  16units_square_w_ring_radius_0.png \
  16units_square_w_ring_radius_0.5.png \
  16units_square_w_ring_radius_1.png \
  16units_square_w_ring_radius_2.5.png \
  3units_cycle.png \
  direct_indirect_in_out.png \
  albers.gif \
  trace_rfc_example_1a.png \
  trace_rfc_example_2.png \
  trace_rfc_example_7.png \
  4units_line_5_zones_not_merged.png \
  4units_line_5_zones_merged.png \
  4units_line_5_zones_not_merged_2.png \
  4units_line_5_zones_merged_2.png \
  4units_line_5_zones_merged_3.png \
  vaccpriority_1ring.png \
  vaccpriority_2rings.png \
  vaccpriority_2cols_rings_same_size.png \
  vaccpriority_2cols_rings_size_5_3.png \
  vaccpriority_2cols_rings_size_2-5_1-3.png \
  14units_2rings_overlap_thin_rings.png \
  14units_2rings_overlap_1thin_1thick.png \
  15units_1ring_s_p.png \
  15units_2rings_s_p_overlap.png \
  21units_3rings_overlap_thin_rings.png \
  clock_24_hour.png

state_transition_png_SOURCES = state-transition.dia

uniform_png_SOURCES = uniform.gnuplot

triangular_png_SOURCES = triangular.gnuplot

piecewise_png_SOURCES = piecewise.gnuplot

piecewise_flat_png_SOURCES = piecewise_flat.gnuplot

gaussian_png_SOURCES = gaussian.gnuplot

beta_png_SOURCES = beta.gnuplot

betapert_png_SOURCES = betapert.gnuplot

gamma_png_SOURCES = gamma.gnuplot

weibull_png_SOURCES = weibull.gnuplot

exponential_png_SOURCES = exponential.gnuplot

logistic_png_SOURCES = logistic.gnuplot

loglogistic_png_SOURCES = loglogistic.gnuplot

lognormal_png_SOURCES = lognormal.gnuplot

pearson_png_SOURCES = pearson.gnuplot

poisson_png_SOURCES = poisson.gnuplot

negbinomial_png_SOURCES = negbinomial.gnuplot

pareto_png_SOURCES = pareto.gnuplot
pareto_log_png_SOURCES = pareto_log.gnuplot

rel_chart_png_SOURCES = rel_chart.gnuplot

airborne_png_SOURCES = airborne.dia

directions_png_SOURCES = directions.dia

building_blocks_png_SOURCES = building_blocks.dia bluetongue.jpg stormy_sky.jpg vaccine.jpg guillotine.jpg cow.jpg sherlock_items.jpg farm_truck.jpg

events_png_SOURCES = events.dia ear.gif siren.gif cow.png pig.png

events_flowchart_png_SOURCES = events_flowchart.dia

priority_queues_png_SOURCES = priority_queues.dia

1unit_png_SOURCES = $(top_srcdir)/models/test/1unit.xml

1unit_start_infectious_png_SOURCES = $(top_srcdir)/models/test/1unit_start_infectious.xml

1unit_start_infectious_1dayleft_png_SOURCES = $(top_srcdir)/models/test/1unit_start_infectious_1dayleft.xml

1unit_start_infectious_2daysleft_png_SOURCES = $(top_srcdir)/models/test/1unit_start_infectious_2daysleft.xml

1unit_start_subclinical_png_SOURCES = $(top_srcdir)/models/test/1unit_start_subclinical.xml

1unit_1dayleft_png_SOURCES = $(top_srcdir)/models/test/1unit_1dayleft.xml

1unit_3daysleft_png_SOURCES = $(top_srcdir)/models/test/1unit_3daysleft.xml

2units_png_SOURCES = $(top_srcdir)/models/test/2units.xml

2units_pigs_cattle_pigs_infected_png_SOURCES = $(top_srcdir)/models/test/2units_pigs_cattle_pigs_infected.xml

2units_pigs_cattle_all_infected_png_SOURCES = $(top_srcdir)/models/test/2units_pigs_cattle_all_infected.xml

2targets_same_dist_same_size_png_SOURCES = $(top_srcdir)/models/test/2targets_same_dist_same_size.xml

2targets_same_dist_diff_size_png_SOURCES = $(top_srcdir)/models/test/2targets_same_dist_diff_size.xml

2units_1_start_destroyed_png_SOURCES = $(top_srcdir)/models/test/2units_1_start_destroyed.xml

2units_1_start_nimmune_png_SOURCES = $(top_srcdir)/models/test/2units_1_start_nimmune.xml

2units_1_start_nimmune_2daysleft_png_SOURCES = $(top_srcdir)/models/test/2units_1_start_2daysleft_nimmune.xml

2units_1_start_nimmune_3daysleft_png_SOURCES = $(top_srcdir)/models/test/2units_1_start_3daysleft_nimmune.xml

2units_1_start_vimmune_png_SOURCES = $(top_srcdir)/models/test/2units_1_start_vimmune.xml

2units_1_start_vimmune_1dayleft_png_SOURCES = $(top_srcdir)/models/test/2units_1_start_1dayleft_vimmune.xml

2units_1_start_vimmune_2daysleft_png_SOURCES = $(top_srcdir)/models/test/2units_1_start_2daysleft_vimmune.xml

2units_ascii_png_SOURCES = $(top_srcdir)/models/test/2units_ascii.xml

2units_iso88591_png_SOURCES = $(top_srcdir)/models/test/2units_iso88591.xml

2units_utf8_png_SOURCES = $(top_srcdir)/models/test/2units_utf8.xml

2units_utf8_no_bom_png_SOURCES = $(top_srcdir)/models/test/2units_utf8_no_bom.xml

2units_utf16_big_endian_png_SOURCES = $(top_srcdir)/models/test/2units_utf16_big_endian.xml

2units_utf16_big_endian_no_bom_png_SOURCES = $(top_srcdir)/models/test/2units_utf16_big_endian_no_bom.xml

2units_utf16_little_endian_png_SOURCES = $(top_srcdir)/models/test/2units_utf16_little_endian.xml

2units_utf16_little_endian_no_bom_png_SOURCES = $(top_srcdir)/models/test/2units_utf16_little_endian_no_bom.xml

3units_png_SOURCES = $(top_srcdir)/models/test/3units.xml

3units_2_at_same_loc_png_SOURCES = $(top_srcdir)/models/test/3units_2_at_same_loc.xml

3units_pigs_2cattle_pigs_infected_png_SOURCES = $(top_srcdir)/models/test/3units_pigs_2cattle_pigs_infected.xml

3units_pigs_cattle_sheep_pigs_sheep_infected_png_SOURCES = $(top_srcdir)/models/test/3units_pigs_cattle_sheep_pigs_sheep_infected.xml

3targets_same_dist_same_size_png_SOURCES = $(top_srcdir)/models/test/3targets_same_dist_same_size.xml

4units_line_png_SOURCES = $(top_srcdir)/models/test/4units_line.xml

4units_all_infected_png_SOURCES = $(top_srcdir)/models/test/4units_all_infected.xml

5units_png_SOURCES = $(top_srcdir)/models/test/5units.xml

5units_2_png_SOURCES = $(top_srcdir)/models/test/5units_2.xml

5units_very_close_png_SOURCES = $(top_srcdir)/models/test/5units_very_close.xml

6units_png_SOURCES = $(top_srcdir)/models/test/6units.xml

6units_2_png_SOURCES = $(top_srcdir)/models/test/6units_2.xml

7units_png_SOURCES = $(top_srcdir)/models/test/7units.xml

8units_all_infected_png_SOURCES = $(top_srcdir)/models/test/8units_all_infected.xml

8units_all_infected_diff_types_png_SOURCES = $(top_srcdir)/models/test/8units_all_infected_diff_types.xml

8units_2rows_png_SOURCES = $(top_srcdir)/models/test/8units_2rows.xml

8units_2rows_2_png_SOURCES = $(top_srcdir)/models/test/8units_2rows_2.xml

8units_2rows_3_png_SOURCES = $(top_srcdir)/models/test/8units_2rows_3.xml

8units_2rows_4_png_SOURCES = $(top_srcdir)/models/test/8units_2rows_4.xml

9units_png_SOURCES = $(top_srcdir)/models/test/9units.xml

10units_2cols_png_SOURCES = $(top_srcdir)/models/test/10units_2cols.xml

12units_2rings_largesmall_plus2infected_png_SOURCES = $(top_srcdir)/modules/test/12units_2rings_largesmall_plus2infected.xml

14units_2rings_overlap_png_SOURCES = $(top_srcdir)/models/test/14units_2rings_overlap.xml

15units_line_png_SOURCES = $(top_srcdir)/models/test/15units_line.xml

15units_2rings_png_SOURCES = $(top_srcdir)/models/test/15units_2rings.xml

units_circle_png_SOURCES = $(top_srcdir)/models/test/units_circle.xml

units_circle2_png_SOURCES = $(top_srcdir)/models/test/units_circle2.xml

16units_square_png_SOURCES = $(top_srcdir)/models/test/16units_square.xml

16units_2rings_png_SOURCES = $(top_srcdir)/models/test/16units_2rings.xml

20units_2rings_png_SOURCES = $(top_srcdir)/models/test/20units_2rings.xml

21units_3rings_overlap_png_SOURCES = $(top_srcdir)/models/test/21units_3rings_overlap.xml

24units_2rings_plus2infected_png_SOURCES = $(top_srcdir)/models/test/24units_2rings_plus2infected.xml

no_rtree_lat0_png_SOURCES = $(top_srcdir)/models/test/no_rtree_lat0.xml

rtree_lat0_png_SOURCES = $(top_srcdir)/models/test/rtree_lat0.xml

no_rtree_lat45_png_SOURCES = $(top_srcdir)/models/test/no_rtree_lat45.xml

rtree_lat45_png_SOURCES = $(top_srcdir)/models/test/rtree_lat45.xml

no_rtree_contact_spread_png_SOURCES = $(top_srcdir)/models/test/no_rtree_contact_spread.xml

rtree_contact_spread_png_SOURCES = $(top_srcdir)/models/test/rtree_contact_spread.xml

1000units_line_png_SOURCES = $(top_srcdir)/models/test/1000units_line.xml

speedup_png_SOURCES = speedup.gnuplot

uncontrolled_example_png_SOURCES = uncontrolled_example.eps

rtree_benefit_png_SOURCES = rtree_benefit.gnuplot

contact_problem_png_SOURCES = contact_problem.dia

contact_proof_png_SOURCES = contact_proof.dia

extend_array_1_png_SOURCES = extend_array_1.dia

extend_array_2_png_SOURCES = extend_array_2.dia

surv_levels_png_SOURCES = surv_levels.dia

basic_circle_png_SOURCES = basic_circle.dia

ordered_circles_png_SOURCES = ordered_circles.dia

adjacent_zones_png_SOURCES = adjacent_zones.dia

enclosure_png_SOURCES = enclosure.dia

enclosure2_png_SOURCES = enclosure2.dia

split_zones_png_SOURCES = split_zones.dia

movement_inside_png_SOURCES = movement_inside.dia

lower_to_higher_png_SOURCES = lower_to_higher.dia

detour_png_SOURCES = detour.dia

1_zone_1_focus_png_SOURCES = 1_zone_1_focus.gnuplot

2_zones_1_focus_png_SOURCES = 2_zones_1_focus.gnuplot

1_zone_2_foci_png_SOURCES = 1_zone_2_foci.gnuplot

1_zone_2_foci_merge_png_SOURCES = 1_zone_2_foci_merge.gnuplot

1_zone_2_foci_merge_w_triangle_png_SOURCES = 1_zone_2_foci_merge_w_triangle.gnuplot

2_zones_2_foci_png_SOURCES = 2_zones_2_foci.gnuplot

2_zones_2_foci_merge1_png_SOURCES = 2_zones_2_foci_merge1.gnuplot

2_zones_2_foci_merge2_png_SOURCES = 2_zones_2_foci_merge2.gnuplot

3_foci_merge_png_SOURCES = 3_foci_merge.gnuplot

1_zone_13_foci_png_SOURCES = 1_zone_13_foci.gnuplot

1_zone_13_foci_merge_png_SOURCES = 1_zone_13_foci_merge.gnuplot

zones_trace_cattle_png_SOURCES = zones_trace_cattle.gnuplot

zones_trace_pigs_png_SOURCES = zones_trace_pigs.gnuplot

zones_trace_both_png_SOURCES = zones_trace_both.gnuplot

zones_trace_both_merge_png_SOURCES = zones_trace_both_merge.gnuplot

2foci_separate_png_SOURCES = 2foci_separate.gnuplot

2foci_joined_png_SOURCES = 2foci_joined.gnuplot

3foci_png_SOURCES = 3foci.gnuplot

donut_0_png_SOURCES = donut_0.gnuplot

donut_1_png_SOURCES = donut_1.gnuplot

2_zone_levels_png_SOURCES = 2_zone_levels.gnuplot

2targets_1_in_zone_png_SOURCES = 2targets_1_in_zone.gnuplot

prevalence_1_png_SOURCES = prevalence_1.gnuplot

prevalence_2_png_SOURCES = prevalence_2.gnuplot

prevalence_triangle_6days_png_SOURCES = prevalence_triangle_6days.gnuplot

air_prevalence_png_SOURCES = air_prevalence.gnuplot

air_prevalence_incr_png_SOURCES = air_prevalence_incr.gnuplot

prevalence_day2_png_SOURCES = prevalence_day2.gnuplot

prevalence_day4_png_SOURCES = prevalence_day4.gnuplot

16units_1_zone_png_SOURCES = 16units_1_zone.gnuplot

16units_2_zones_png_SOURCES = 16units_2_zones.gnuplot

7units_w_ring_png_SOURCES = 7units_w_ring.gnuplot

3units_cycle_png_SOURCES = 3units_cycle.gnuplot

direct_indirect_in_out_png_SOURCES = direct_indirect_in_out.gnuplot

vaccpriority_1ring_png_SOURCES = vaccpriority_1ring.gnuplot

vaccpriority_2rings_png_SOURCES = vaccpriority_2rings.gnuplot

vaccpriority_2cols_rings_same_size_png_SOURCES = vaccpriority_2cols_rings_same_size.gnuplot

vaccpriority_2cols_rings_size_5_3_png_SOURCES = vaccpriority_2cols_rings_size_5_3.gnuplot

vaccpriority_2cols_rings_size_2_5_1_3_png_SOURCES = vaccpriority_2cols_rings_size_2-5_1-3.gnuplot

14units_2rings_overlap_thin_rings_png_SOURCES = 14units_2rings_overlap_thin_rings.gnuplot

14units_2rings_overlap_1thin_1thick_png_SOURCES = 14units_2rings_overlap_1thin_1thick.gnuplot

15units_1ring_s_p_png_SOURCES = 15units_1ring_s_p.gnuplot

15units_2rings_s_p_overlap_png_SOURCES = 15units_2rings_s_p_overlap.gnuplot

21units_3rings_overlap_thin_rings_png_SOURCES = 21units_3rings_overlap_thin_rings.gnuplot

clock_24_hour_png_SOURCES = clock_24_hour.dia
