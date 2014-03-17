/** @file zone.h
 *
 * Zones are areas of differing surveillance and control policies.  The text
 * below gives the rules for how zones work; for notes on how they are
 * implemented in code, see zone.c.
 *
 * There can be an arbitrary number of zones, each with a name.
 *
 * @image html surv_levels.png
 *
 * The basic form of a zone is a circle around a unit.  Areas outside the
 * circle also constitute a zone, with the lowest surveillance level.
 *
 * @image html basic_circle.png
 *
 * Higher levels of surveillance correspond to smaller zones.
 *
 * @image html ordered_circles.png
 *
 * Overlapping foci of the same zone merge.
 *
 * @image html adjacent_zones.png
 *
 * Zones with lower surveillance levels are absorbed when enclosed by a zone of
 * a higher surveillance level.  (The "no donuts" rule.)
 *
 * @image html enclosure.png
 *
 * Note that adding a focus can join existing physically separated areas of the
 * same zone and create more than one donut-hole.
 *
 * @image html enclosure2.png
 *
 * If a focus is removed from a zone, the zone takes the shape it would have
 * had were that focus never included.  (The "no bites out of Mickey's head"
 * rule.)
 *
 * @image html split_zones.png
 *
 * @section movement-and-zones Movement and zones
 *
 * Movement inside a zone may be allowed, but movement between physically
 * separated foci of the same zone is not.
 *
 * @image html movement_inside.png
 *
 * Movement from a zone to an adjacent zone of a higher surveillance level is
 * allowed, but not vice-versa.
 *
 * @image html lower_to_higher.png
 *
 * Movement that would cross a zone of a higher surveillance level "as the crow
 * flies" but where a "detour" exists, is allowed.
 *
 * @image html detour.png
 *
 * Symbols from this module begin with ZON_.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @date October 2004
 *
 * Copyright &copy; University of Guelph, 2004-2009
 * 
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 */

#ifndef ZONE_H
#define ZONE_H

#include <stdio.h>
#include <gpcl/gpc.h>

#include <glib.h>



/** A zone. */
/* NOTE: When this struct is altered, the record type ZON_zone_t in
 * the Delphi user interface also needs to be updated. */
typedef struct
{
  GString *name;
  int level;
  double radius;
  double radius_sq; /* Comparing distance^2 to radius^2 saves us taking a
    square root. */
  double epsilon_sq; /* The leeway when comparing distance^2 to radius^2. */
  GArray *foci; /**< Unordered array of foci.  Each focus is a gpc_vertex
    structure. */
  gpc_polygon *poly; /**< the (possibly multi-contour) polygon */
  GQueue *fragments; /**< The fragments (contours) making up the zone.  It is
    safe to keep a pointer to a particular fragment since fragments will not
    disappear during a simulation.  If one fragment merges with another, both
    fragments will continue to exist, and will simply point to the same contour
    in <i>poly</i>.  You should use ZON_same_zone() and ZON_same_fragment() to
    safely compare zone fragments. */
  double area;
  double perimeter;
  unsigned int nholes_filled;
#ifdef USE_SC_GUILIB  
  double max_area;
  unsigned short int max_day;
  GHashTable *_unitDays;
  GHashTable *_animalDays;
#endif  
}
ZON_zone_t;



/** A zone "fragment". */
typedef struct _ZON_zone_fragment_t ZON_zone_fragment_t;
struct _ZON_zone_fragment_t
{
#if DEBUG
  int id; /**< a numeric identifier for debugging purposes */
#endif
  ZON_zone_t *parent; /**< the zone this fragment is part of */
  int contour; /**< the index of the sub-polygon in the parent structure */
  gpc_vertex sample; /**< a point (any point) that is known to be inside the
    fragment.  Used to tell which post-merge contour corresponds to which
    pre-merge contour. */
  ZON_zone_fragment_t *nests_in; /**< If there are multiple levels of zones,
    this points to the fragment of the next larger zone inside which this
    fragment nests. */
};



typedef struct
{
  double x, y;
}
ZON_pending_focus_t;



/** A list of zones. */
typedef struct
{
  GPtrArray *list;
  ZON_zone_fragment_t **membership; /**< A list with 1 item per herd.  Each
    item is a pointer to the zone fragment that herd is in.  The pointers are
    never null, because even herds that are not inside a zone focus count as
    being in the "background" zone. */
  unsigned int membership_length; /**< Length of the membership array. */
  gboolean use_rtree_index;
  GQueue *pending_foci; /**< A list of foci that have yet to be added.  Each
    item in the queue will be a ZON_pending_focus struct.  Because the events
    in one simulation day should be considered to happen simultaneously,
    changes to a zone are not processed mid-day; instead, they are stored and
    applied all at once later. */
}
ZON_zone_list_t;



/* Prototypes. */

/* Functions for lists of zone objects. */

ZON_zone_list_t *ZON_new_zone_list (unsigned int membership_length);
unsigned int ZON_zone_list_append (ZON_zone_list_t *, ZON_zone_t *);

/**
 * Returns the number of zones in a zone list.
 *
 * @param Z a zone list.
 * @return the number of zones in the list.
 */
#define ZON_zone_list_length(Z) (Z->list->len)

/**
 * Returns the ith zone in a zone list.
 *
 * @param Z a zone list.
 * @param I the index of the zone to retrieve.
 * @return the ith zone.
 */
#define ZON_zone_list_get(Z,I) ((ZON_zone_t*)g_ptr_array_index(Z->list,I))

void ZON_zone_list_reset (ZON_zone_list_t *);
void ZON_zone_list_add_focus (ZON_zone_list_t *, double x, double y);

ZON_zone_fragment_t *ZON_zone_list_get_background (ZON_zone_list_t *);

char *ZON_zone_list_to_string (ZON_zone_list_t *);
int ZON_fprintf_zone_list (FILE *, ZON_zone_list_t *);

#define ZON_printf_zone_list(Z) ZON_fprintf_zone_list(stdout,Z)

void ZON_free_zone_list (ZON_zone_list_t *);

/* Functions for zone objects. */

ZON_zone_t *ZON_new_zone (char *, int level, double radius);
void ZON_free_zone (ZON_zone_t *);
char *ZON_zone_to_string (ZON_zone_t *);
int ZON_fprintf_zone (FILE *, ZON_zone_t *);

#define ZON_printf_zone(Z) ZON_fprintf_zone(stdout,Z)

void ZON_reset (ZON_zone_t *);
ZON_zone_fragment_t *ZON_zone_add_focus (ZON_zone_t *, double x, double y, gpc_polygon ** holes);
gboolean ZON_zone_contains (ZON_zone_t *, double x, double y);
gboolean ZON_same_zone (ZON_zone_fragment_t *, ZON_zone_fragment_t *);
gboolean ZON_same_fragment (ZON_zone_fragment_t *, ZON_zone_fragment_t *);
gboolean ZON_nests_in (ZON_zone_fragment_t * inner, ZON_zone_fragment_t * outer);
double ZON_update_area (ZON_zone_t *);
double ZON_update_perimeter (ZON_zone_t *);

#define ZON_level(F) (F->parent->level)

#ifdef USE_SC_GUILIB
  void addToZoneTotals( unsigned short int _day, ZON_zone_t *_zone, unsigned int _prod_id, unsigned int _herd_size   );
#endif

#endif /* !ZONE_H */
