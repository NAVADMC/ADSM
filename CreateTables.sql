------------------------------------------------------------------
-- input tables
-- schoenbaum
-- 2/19/14 - scripted for django
--
-- note:  any relid or pdfid will not display with a label.
--          relid's and pdfid are displayed in the function form
----------------------------------------------------------------

create table dbschemaversion (
version_number		text	primary key 	not null,
version_application	text			not null,
version_date		text			not null,
version_info_url	text,		
version_id		int
);	

create table dynaherd	(
herd_id			int	primary key 	not null,
productiontypeid	int			not null,
latitude		real			not null,
longitude		real			not null,
initial_state_code	text			not null,
days_in_initial_state	int			not null,
days_left_in_initial_state	int			not null,
initial_size		int 			not null,
final_state_code		text,	
final_control_state_code	text,	
final_detection_state_code	text,	
cum_infected		int ,		
cum_detected		int ,		
cum_destroyed		int ,		
cum_vaccinated		int 
);		


create table dynablob	(
dynblob_id		text 	primary key 	not null,
zone_perimeters		text
);

create table readallcodes (
code_id			int	primary key 	not null,
code			text			not null,
code_type		text			not null,
code_description		text			not null
);

create table readallcodetypes	(
code_type_id		int	primary key 	not null,
code_type		text			not null,
code_description	text			not null
);

----constrain this?
---- ms 2/19 names not modified do not display on form
create table inchart (
chartid		int		primary key 	not null,
fieldname	text,	
chart_name	text				not null,
ispdf		int				not null,
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
dmin		int,		
dmax		int,		
theta		real,		
a		real,		
s		int,		
x_axis_units	text,	
y_axis_units	text,	
notes		text
);


create table inchartdetail (
chartid		int		not null, -- discuss pk needed here
pointorder	int		not null,
x		real		not null,
y		real		not null
);

create table incontrolsglobal 	(
controlsglobalid		text		not null, -- uses that text pk
include_detection		int		not null default 0,
include_tracing			int		not null default 0,
include_tracing_herd_exam		int		not null default 0,
include_tracing_testing		int		not null default 0,
include_destruction		int		not null default 0,
destruction_delay		int,		
destrcapacityrelid		int,		
destruction_priority_order			text,		
destrucion_reason_order				text,		
include_vaccination				int		not null default 0,
vaccincation_detected_units_before_start	int,		
vacccapacityrelid				int,		
vaccination_priority_order			text,		
include_zones					int		not null default 0,
vaccination_retrospective_days			int,		
vacccapacitystartrelid		int,		
vacccapacityrestartrelid	int
);	

-- custom outputs removed

create table indiseasespread (
productiontypepairid		int	primary key 	not null,
spreadmethodcode		text,
latent_can_infect			int,
subclinical_can_infect		int,
mean_contact_rate			real,
use_fixed_contact_rate		int,
fixed_contact_rate		real,
infection_probability		real,
distancepdfid			int,
movementcontrolrelid		int,
transportdelaypdfid		int,
probairbornespread1km		real,
maxdistairbornespread		real,
wind_direction_start		int,
wind_direction_end		int
);


create table	ingeneral (
ingeneralid			text,  ----pk
language varchar(12) not null default 'English'
    check (language in ('English', 'Spanish')),
-- language			text,
Frequency varchar(200)
  CONSTRAINT chk_Frequency CHECK (Frequency IN ('Daily', 'Weekly', 'Monthly', 'Yearly')),
scenario_description			text,
iterations			int,
days				int,
simstopreason			text,
includecontactspread		int,  -- these present in a radio button now
includeairbornespread		int,
use_airborne_exponential_decay	int,
use_within_herd_prevalence		int,
cost_track_destruction		int,
cost_track_vaccination		int,
cost_track_zone_surveillance	int,
use_fixed_random_seed		int,
randomseed			int,
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
production_type_id			int 	primary key 	not null,
production_type_name				text			not null,
use_disease_transition			int,
dislatentperiodpdfid			int,
dissubclinicalperiodpdfid		int,
disclinicalperiodpdfid			int,
disimmuneperiodpdfid			int,
disprevalencerelid			int,
use_detection				int,
detprobobsvstimeclinicalrelid		int,
detprobreportvsfirstdetectionrelid	int,
trace_direct_forward			int,
trace_direct_back				int,
trace_direct_success			real,
trace_direct_trace_period			int,
trace_indirect_forward			int,
trace_indirect_back			int,
trace_indirect_success			real,
trace_indirect_trace_period		int,
tracedelaypdfid				int,
use_destruction			int,
destruction_is_ring_trigger			int,
destruction_ring_radius				real,
destruction_is_ring_target			int,
destroy_direct_forward_traces		int,
destroy_indirect_forward_traces		int,
destroy_direct_back_traces			int,
destroy_indirect_back_traces			int,
destruction_priority				int,
use_vaccination				int,
vacc_min_time_between_vaccinations		int,
vacc_vaccinate_detected			int,
vacc_days_to_immunity			int,
vaccimmuneperiodpdfid			int,
vacc_ring				int,
vacc_ring_radius				real,
vacc_priority				int,
cost_destr_appraisal_per_unit		real,
cost_destr_cleaning_per_unit		real,
cost_destr_euthanasia_per_animal		real,
cost_destr_indemnification_per_animal	real,
cost_destr_disposal_per_animal		real,
cost_vacc_setup_per_unit			real,
cost_vacc_threshold			int,
cost_vacc_baseline_per_animal		real,
cost_vacc_additional_per_animal		real,
zone_detection_is_trigger			int,
zone_direct_trace_is_trigger		int,
zone_indirect_trace_is_trigger		int,
exam_direct_forward			int,
exam_direct_forward_multiplier		real,
exam_indirect_forward			int,
exam_indirect_forward_multiplier		real,
exam_direc_tback				int,
exam_direct_back_multiplier		real,
exam_indirect_back			int,
exam_indirect_back_multiplier		real,
test_direct_forward			int,
test_indirect_forward			int,
test_direct_back				int,
test_indirect_back			int,
test_specificity				real,
test_sensitivity				real,
testdelaypdfid				int,
vacc_restrospective_days			int
);

create table inproductiontypepair (

productiontypepairid	int		int 	primary key 	not null,
sourceproductiontypeid	int		not null,
destproductiontypeid	int		not null,
use_direct_contact	int		not null default 0,
directcontactspreadid	int,		
use_indirect_contact	int		not null default 0,
indirectcontactspreadid	int,		
use_airborne_spread	int		not null default 0,
airbornecontactspreadid	int		
);


create table inzone (
zoneid		int		primary key 	not null,
zone_description	text		not null,
zone_radius	real		not null
);

create table inzoneproductiontypepair (
inzoneproductiontypepairid	int	primary key 	not null,
zoneid				int			not null,
productiontypeid		int			not null,
use_directmovement_control	int			not null default 0,
zonedirectmovementrelid		int,		
use_indirect_movement_control	int			not null default 0,
zoneindirectmovementrelid	int,		
use_detection_multiplier		int			not null default 0,
zone_detection_multiplier		real,		
cost_surv_per_animal_day		real	
); 	

-- conceptually, if you are making this group, you should know all data
create table ingroup (
-- this is v3.3
groupid			int	primary key 	not null,
subgroupid		int			not null,
groupproductiontypes	text			not null  -- check how this looks
);

create table intrigger (
triggerid		int	primary key 	not null,
triggercode		int			not null,
trigger_days		int
trigger_rate		int  	-- not sure on this datatype
triggerproductiontypes	text  -- check how this looks
);
-----------------------------------------
-- outputs
-- not going to constrain outputs at all
-----------------------------------------

create table outdailybyproductiontype (
iteration		int,
productiontypeid	int,
day			int,
tsdususc		int,
tsdasusc		int,
tsdulat			int,
tsdalat			int,
tsdusubc		int,
tsdasubc		int,
tsduclin		int,
tsdaclin		int,
tsdunimm		int,
tsdanimm		int,
tsduvimm		int,
tsdavimm		int,
tsdudest		int,
tsdadest		int,
tscususc		int,
tscasusc		int,
tsculat			int,
tscalat			int,
tscusubc		int,
tscasubc		int,
tscuclin		int,
tscaclin		int,
tscunimm		int,
tscanimm		int,
tscuvimm		int,
tscavimm		int,
tscudest		int,
tscadest		int,
infnuair		int,
infnaair		int,
infnudir		int,
infnadir		int,
infnuind		int,
infnaind		int,
infcuini		int,
infcaini		int,
infcuair		int,
infcaair		int,
infcudir		int,
infcadir		int,
infcuind		int,
infcaind		int,
expcudir		int,
expcadir		int,
expcuind		int,
expcaind		int,
trcudirfwd		int,
trcadirfwd		int,
trcuindfwd		int,
trcaindfwd		int,
trcudirpfwd		int,
trcadirpfwd		int,
trcuindpfwd		int,
trcaindpfwd		int,
tocudirfwd		int,
tocuindfwd		int,
tocudirback		int,
tocuindback		int,
trnudirfwd		int,
trnadirfwd		int,
trnuindfwd		int,
trnaindfwd		int,
trcudirback		int,
trcadirback		int,
trcuindback		int,
trcaindback		int,
trcudirpback		int,
trcadirpback		int,
trcuindpback		int,
trcaindpback		int,
trnudirback		int,
trnadirback		int,
trnuindback		int,
trnaindback		int,
tonudirfwd		int,
tonuindfwd		int,
tonudirback		int,
tonuindback		int,
exmcudirfwd		int,
exmcadirfwd		int,
exmcuindfwd		int,
exmcaindfwd		int,
exmcudirback		int,
exmcadirback		int,
exmcuindback		int,
exmcaindback		int,
exmnuall		int,
exmnaall		int,
tstcudirfwd		int,
tstcadirfwd		int,
tstcuindfwd		int,
tstcaindfwd		int,
tstcudirback		int,
tstcadirback		int,
tstcuindback		int,
tstcaindback		int,
tstcutruepos		int,
tstcatruepos		int,
tstnutruepos		int,
tstnatruepos		int,
tstcutrueneg		int,
tstcatrueneg		int,
tstnutrueneg		int,
tstnatrueneg		int,
tstcufalsepos		int,
tstcafalsepos		int,
tstnufalsepos		int,
tstnafalsepos		int,
tstcufalseneg		int,
tstcafalseneg		int,
tstnufalseneg		int,
tstnafalseneg		int,
detnuclin		int,
detnaclin		int,
detcuclin		int,
detcaclin		int,
detnutest		int,
detnatest		int,
detcutest		int,
detcatest		int,
descuini		int,
descaini		int,
descudet		int,
descadet		int,
descudirfwd		int,
descadirfwd		int,
descuindfwd		int,
descaindfwd		int,
descudirback		int,
descadirback		int,
descuindback		int,
descaindback		int,
descuring		int,
descaring		int,
desnuall		int,
desnaall		int,
deswuall		int,
deswaall		int,
vaccuini		int,
vaccaini		int,
vaccuring		int,
vaccaring		int,
vacnuall		int,
vacnaall		int,
vacwuall		int,
vacwaall		int,
zonnfoci		int,
zoncfoci		int,
appduinfectious		int
);

create table outdailybyzone (
iteration	int,
day		int,
zoneid		int,
zonearea	real,
zoneperimeter	real
);

create table outdailybyzoneandproductiontype  (
iteration		int,
day			int,
zoneid			int,
productiontypeid	int,
unitdaysinzone		int,
animaldaysinzone	int,
unitsinzone		int,
animalsinzone		int
);

create table outdailyevents (

iteration	int,
day		int,
event		int,
herdid		int,
zoneid		int,
eventcode	text,
newstatecode	text,
testresultcode	text
);

create table outdailyexposures (
iteration		int,
day			int,
exposure		int,
initiatedday		int,
exposedherdid		int,
exposedzoneid		int,
exposingherdid		int,
exposingzoneid		int,
spreadmethodcode	text,
isadequate		int,
exposingherdstatuscode	text,
exposedherdstatuscode	text
);

create table outepidemiccurves (
iteration		int,
day			int,
productiontypeid	int,
infectedunits		int,
infectedanimals		int,
detectedunits		int,
detectedanimals		int,
infectiousunits		int,
apparentinfectiousunits	int
);

create table outgeneral (
outgeneralid		text, -- yuck is this that versionapplication thing
simulationstarttime	text,
simulationendtime	text,
completediterations	int,
version			text
);

create table outiteration (
iteration	int,
diseaseended	int,
diseaseendday	int,
outbreakended	int,
outbreakendday	int,
zonefocicreated	int,
deswumax	int,
deswumaxday	int,
deswamax	real,
deswamaxday	int,
deswutimemax	int,
deswutimeavg	real,
vacwumax	int,
vacwumaxday	int,
vacwamax	real,
vacwamaxday	int,
vacwutimemax	int,
vacwutimeavg	real
);


create table outiterationbyherd (
iteration		int,
herdid			int,
laststatuscode		text,
laststatusday		int,
lastcontrolstatecode	text,
lastcontrolstateday	int
);



create table outiterationbyproductiontype (

iteration		int,
productiontypeid	int,
tscususc		int,
tscasusc		int,
tsculat			int,
tscalat			int,
tscusubc		int,
tscasubc		int,
tscuclin		int,
tscaclin		int,
tscunimm		int,
tscanimm		int,
tscuvimm		int,
tscavimm		int,
tscudest		int,
tscadest		int,
infcuini		int,
infcaini		int,
infcuair		int,
infcaair		int,
infcudir		int,
infcadir		int,
infcuind		int,
infcaind		int,
expcudir		int,
expcadir		int,
expcuind		int,
expcaind		int,
trcudirfwd		int,
trcadirfwd		int,
trcuindfwd		int,
trcaindfwd		int,
trcudirpfwd		int,
trcadirpfwd		int,
trcuindpfwd		int,
trcaindpfwd		int,
trcudirback		int,
trcadirback		int,
trcuindback		int,
trcaindback		int,
trcudirpback		int,
trcadirpback		int,
trcuindpback		int,
trcaindpback		int,
tocudirfwd		int,
tocuindfwd		int,
tocudirback		int,
tocuindback		int,
exmcudirfwd		int,
exmcadirfwd		int,
exmcuindfwd		int,
exmcaindfwd		int,
exmcudirback		int,
exmcadirback		int,
exmcuindback		int,
exmcaindback		int,
tstcudirfwd		int,
tstcadirfwd		int,
tstcuindfwd		int,
tstcaindfwd		int,
tstcudirback		int,
tstcadirback		int,
tstcuindback		int,
tstcaindback		int,
tstcutruepos		int,
tstcatruepos		int,
tstcutrueneg		int,
tstcatrueneg		int,
tstcufalsepos		int,
tstcafalsepos		int,
tstcufalseneg		int,
tstcafalseneg		int,
detcuclin		int,
detcaclin		int,
detcutest		int,
detcatest		int,
descuini		int,
descaini		int,
descudet		int,
descadet		int,
descudirfwd		int,
descadirfwd		int,
descuindfwd		int,
descaindfwd		int,
descudirback		int,
descadirback		int,
descuindback		int,
descaindback		int,
descuring		int,
descaring		int,
deswumax		int,
deswamax		real
deswumaxday		int,
deswamaxday		int,
deswutimemax		int,
deswutimeavg		real
deswudaysinqueue	real
deswadaysinqueue	real
vaccuini		int,
vaccaini		int,
vaccuring		int,
vaccaring		int,
vacwumax		int,
vacwamax		real
vacwumaxday		int,
vacwamaxday		int,
vacwutimemax		real
vacwutimeavg		int,
zoncfoci		int,
firstdetection		int,
firstdetuinf		int,
firstdetainf		int,
firstdestruction	int,
firstvaccination	int,
lastdetection		int
);

create table outiterationbyzone (
iteration		int,
zoneid			int,
maxzonearea		real,
maxzoneareaday		int,
finalzonearea		real,
maxzoneperimeter	real,
maxzoneperimeterday	int,
finalzoneperimeter	real
);

create table outiterationbyzoneandproductiontype (
iteration		int,
zoneid			int,
productiontypeid	int,
unitdaysinzone		int,
animaldaysinzone	int,
costsurveillance	real
);

create table outiterationcosts (
iteration		int,
productiontypeid	int,
destrappraisal		real,
destrcleaning		real,
destreuthanasia		real,
destrindemnification	real,
destrdisposal		real,
vaccsetup		real,
vaccvaccination		real
);
