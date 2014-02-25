------------------------------------------------------------------
-- input tables
-- schoenbaum
-- 2/24/14 - scripted for django
-- post xml, with new buckets to support population/disease/control
-- note:  any relid or pdfid will not display with a label.
--          relid's and pdfid are displayed in the function form
--  underscore useds on names that should not display
----------------------------------------------------------------


create table dbschemaversion (
version_number		text	primary key 	not null,
version_application	text			not null,
version_date		text			not null,
version_info_url	text,		
version_id		int
);

create table dynaherd	(
latitude		real			not null,
longitude		real			not null,
initial_state_code	text			not null,
days_in_initial_state	int			not null,
days_left_in_initial_state	int		not null,
initial_size		int 			not null,
_final_state_code	text,	
_final_control_state_code	text,	
_final_detection_state_code	text,	
_cum_infected		int ,		
_cum_detected		int ,		
_cum_destroyed		int ,		
_cum_vaccinated		int ,
user_defined_1		text,  -- the user defineds are based on 
user_defined_2		text,  -- the conversation with shaun about 
user_defined_3		text,  -- about keeping original identifer 
user_defined_4		text
);



create table dynablob	(
zone_perimeters		text
);

-- the code tables are lookups, not provided to user
create table readallcodes (
_code			text			not null,
_code_type		text			not null,
_code_description	text			not null
);

create table readallcodetypes	(
_code_type		text			not null,
_code_type_description	text			not null
);

create table inchart (
--_chartid	int		primary key 	not null,
fieldname	text,
chart_name	text				not null,
_ispdf		int				not null,
chart_type	text,		
mean		real,		
std_dev		real,		
min		real,		
mode		real,		
max		real,		
alpha		real,		
alpha2		real,		
beta		real,		
location	real,		
scale		real,		
shape		real,		
n		int,		
p		real,		
m		int,		
d		int,		
dmin		int, -- don't know what function uses this		
dmax		int, -- don't know what function uses this	
theta		real,		
a		real,		
s		int,		
x_axis_units	text,	
y_axis_units	text,	
_notes		text
);

-- these display within the pdf, no labels
create table inchartdetail (
_chartid		int	not null, -- 
_pointorder	int		not null,
_x		real		not null,
_y		real		not null
);

create table	ingeneral (
--_ingeneralid			text,  ----pk
language			text,
scenario_description			text,
iterations			int,
days				int,
sim_stop_reason			text,
include_contact_spread		int,  -- these present in a radio button now
include_airborne_spread		int,
use_airborne_exponential_decay	int,
use_within_herd_prevalence		int,
cost_track_destruction		int,
cost_track_vaccination		int,
cost_track_zone_surveillance	int,
use_fixed_random_seed		int,
random_seed			int,
save_all_daily_outputs		int,
save_daily_outputs_for_iterations	int,
write_daily_states_file		int,
daily_states_filename		text,
save_daily_events			int,
save_daily_exposures		int,
save_iteration_outputs_for_herds	int,
--usecustomoutputs		int,  no custom outputs
write_map_output		int,
map_directory		text
);

create table inproductiontype (
--production_type_id	int 	primary key 	not null,
production_type_name	text	not null,
production_type_description	text
production_type_group	text
);

create table inproductiontypepair (

--_productiontypepairid	int		int 	primary key 	not null,  -- django should do
_sourceproductiontypeid	int		not null,
_destproductiontypeid	int		not null,
use_direct_contact	int		not null default 0,
_directcontactspreadid	int,		
use_indirect_contact	int		not null default 0,
_indirectcontactspreadid	int,		
use_airborne_spread	int		not null default 0,
_airbornecontactspreadid	int		
);



create table indiseaseglobal (
--_diseaseid	int, -- django should do autoincrement
disease_name    text,
disease_description	text
);

create table indiseaseproductiontype (
-- no autoincrement
_production_type_id		int,
use_disease_transition		int,
_dislatentperiodpdfid		int,
_dissubclinicalperiodpdfid	int,
_disclinicalperiodpdfid		int,
_disimmuneperiodpdfid		int,
_disprevalencerelid		int
);


create table indiseasespread (
_productiontypepairid		int	primary key 	not null,
spread_method_code		text,
latent_can_infect		int,
subclinical_can_infect		int,
mean_contact_rate		real,
use_fixed_contact_rate		int,
fixed_contact_rate		real,
infection_probability		real,
_distancepdfid			int,
_movementcontrolrelid		int,
_transportdelaypdfid		int,
probability_airborne_spread_1km		real,
max_distance_airborne_spread		real,
wind_direction_start		int,
wind_direction_end		int
);


create table inzone (
zone_description	text	not null,
zone_radius		real	not null
);


create table inzoneproductiontypepair (
--inzoneproductiontypepairid	int	primary key 	not null,
_zoneid				int			not null,
_production_type_id		int			not null,
use_directmovement_control	int			not null default 0,
_zonedirectmovementrelid	int,		
use_indirect_movement_control	int			not null default 0,
_zoneindirectmovementrelid	int,		
use_detection_multiplier	int			not null default 0,
zone_detection_multiplier	real,		
cost_surv_per_animal_day	real	
); 

create table incontrolplan (
control_plan_name		text not null,
control_plan_description	text,
control_plan_group		text
);


create table incontrolglobal 	(
--controlsglobalid		text		not null, -- uses that text pk
include_detection		int		not null default 0,
include_tracing			int		not null default 0,
include_tracing_herd_exam	int		not null default 0,
include_tracing_testing		int		not null default 0,
include_destruction		int		not null default 0,
destruction_delay		int,		
_destrcapacityrelid		int,		
destruction_priority_order	text,		
destrucion_reason_order		text,		
include_vaccination		int		not null default 0,
vaccincation_detected_units_before_start	int,		
_vacccapacityrelid		int,		
vaccination_priority_order	text,		
include_zones			int		not null default 0,
vaccination_retrospective_days	int,		
_vacccapacitystartrelid		int,		
_vacccapacityrestartrelid	int
);

create table incontrolsproductiontype (
production_type_id			int 	primary key 	not null,
use_disease_transition			int,
use_detection				int,
_detprobobsvstimeclinicalrelid		int,
_detprobreportvsfirstdetectionrelid	int,
trace_direct_forward			int,
trace_direct_back			int,
trace_direct_success			real,
trace_direct_trace_period		int,
trace_indirect_forward			int,
trace_indirect_back			int,
trace_indirect_success			real,
trace_indirect_trace_period		int,
_tracedelaypdfid			int,
use_destruction				int,
destruction_is_ring_trigger		int,
destruction_ring_radius			real,
destruction_is_ring_target		int,
destroy_direct_forward_traces		int,
destroy_indirect_forward_traces		int,
destroy_direct_back_traces		int,
destroy_indirect_back_traces		int,
destruction_priority			int,
use_vaccination				int,
vaccination_min_time_between		int,
vaccinate_detected			int,
days_to_immunity			int,
_vaccimmuneperiodpdfid			int,
vaccinate_ring				int,
vaccinate_ring_radius			real,
vaccination_priority			int,
cost_destroy_appraisal_per_unit		real,
cost_destroy_cleaning_per_unit		real,
cost_destroy_euthanasia_per_animal	real,
cost_destroy_indemnification_per_animal	real,
cost_destroy_disposal_per_animal	real,
cost_vaccinate_setup_per_unit		real,
cost_vaccinate_threshold		int,
cost_vaccinate_baseline_per_animal	real,
cost_vaccinate_additional_per_animal	real,
zone_detection_is_trigger		int,
zone_direct_trace_is_trigger		int,
zone_indirect_trace_is_trigger		int,
exam_direct_forward			int,
exam_direct_forward_multiplier		real,
exam_indirect_forward			int,
exam_indirect_forward_multiplier	real,
exam_direc_tback			int,
exam_direct_back_multiplier		real,
exam_indirect_back			int,
exam_indirect_back_multiplier		real,
test_direct_forward			int,
test_indirect_forward			int,
test_direct_back			int,
test_indirect_back			int,
test_specificity			real,
test_sensitivity			real,
_testdelaypdfid				int,
vaccinate_restrospective_days		int
);



-- missy note to self - v33 group and trigger tables removed




