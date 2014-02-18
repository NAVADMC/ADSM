#ifndef SC_DATABASE_H
#define SC_DATABASE_H

#include <production_type_data.h>

void write_production_type_list_results_SQL( GPtrArray *_production_type_list, unsigned int _run );
void write_outIteration_SQL( guint _run );
void update_outIteration_SQL( guint _run );
void write_outIterationByZone_SQL( guint _run, ZON_zone_list_t *_zones );
void write_outIterationByZoneAndProductiontype_SQL( guint _run, ZON_zone_list_t *_zones );
void write_outIterationByHerd_SQL( guint _run, UNT_unit_list_t *_units );
void write_scenario_SQL( void );
void write_job_SQL();
void write_production_types_SQL( GPtrArray *production_types );
void write_zones_SQL( ZON_zone_list_t *zones );
void write_epi_curve_daily_data_SQL( GPtrArray *_production_types, guint _run, guint _day );
void write_out_daily_by_production_type_SQL( guint _day, guint _run, GPtrArray *_production_types );
void write_outDailyByZone_SQL( guint _day, guint _run, ZON_zone_list_t *_zones );
void write_units_ever_infected_SQL( UNT_unit_list_t *_units );
void write_dyn_unit_SQL( UNT_unit_list_t *_units );
void update_dyn_unit_SQL( UNT_unit_list_t *_units );
#endif
