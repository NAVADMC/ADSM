/** @file zone.c
 * Functions for creating, destroying, printing, and manipulating zones.
 *
 * From an implementation point of view, a zone is a polygon, possibly made up
 * of several disjoint sub-polygons, which we will call "contours" (following
 * the General Polygon Clipper library, which is used to implement zones).  A
 * zone is built up by adding "foci", locations of diseased or suspect herds.
 * When a focus is added to a zone, a circle is drawn around the focus and that
 * circle is added to the zone polygon.  The new circle may merge with one or
 * more existing contours.
 *
 * One goal of this library is to make it easy and efficient to track which
 * zone each herd is in.  Since the contours making up a zone can change over
 * time as they merge with other contours, I introduce an intermediate data
 * structure, a "zone fragment".  A fragment <i>is</i> persistent over time,
 * unlike a contour (although the underlying contour that a fragment point to
 * may change).  Once a herd is assigned to a fragment, it needs to be
 * re-assigned <i>only</i> if a fragment of a higher surveillance level zone
 * appears at the herd's location.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @date December 2003
 *
 * Copyright &copy; University of Guelph, 2003-2009
 * 
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 */

#if HAVE_CONFIG_H
#  include <config.h>
#endif

#include "zone.h"
#include "gis.h"

#if STDC_HEADERS
#  include <stdlib.h>
#  include <string.h>
#endif

#if HAVE_MATH_H
#  include <math.h>
#endif

#if HAVE_ERRNO_H
#  include <errno.h>
#endif

#define EPSILON 0.01 /* 10 m */
#define CIRCLE_NSIDES 20        /* must be divisible by 4! */
#define TWOPI 6.28318530717958647692



/**
 * Creates a new zone fragment.  For internal use; to add to a zone, use
 * ZON_zone_add_focus().
 *
 * @param parent a zone.
 * @param contour the contour of <i>poly</i> to which this fragment corresponds.
 * @returns a pointer to a newly-created, initialized ZON_zone_fragment_t
 *   structure.
 */
ZON_zone_fragment_t *
ZON_new_fragment (ZON_zone_t * parent, int contour)
{
  ZON_zone_fragment_t *fragment;
#if DEBUG
  static int current_id = 0;
#endif

  fragment = g_new (ZON_zone_fragment_t, 1);
#if DEBUG
  fragment->id = current_id++;
#endif
  fragment->parent = parent;
  fragment->contour = contour;
  fragment->nests_in = NULL;
  return fragment;
}



/**
 * Deletes a zone fragment structure from memory.
 *
 * @param F a pointer to a ZON_zone_fragment_t structure.
 */
#define ZON_free_fragment(F) g_free(F)



/**
 * Creates a new, empty zone list.
 *
 * @param membership_length the size needed for the membership array.  This
 *   should be the number of herds.
 * @return a pointer to a newly-created, empty ZON_zone_list_t structure.
 */
ZON_zone_list_t *
ZON_new_zone_list (unsigned int membership_length)
{
  ZON_zone_list_t *zones;

  zones = g_new (ZON_zone_list_t, 1);
  zones->list = g_ptr_array_new ();
  zones->membership_length = membership_length;
  if (membership_length == 0)
    zones->membership = NULL;
  else
    zones->membership = g_new0 (ZON_zone_fragment_t *, membership_length);
  zones->membership_length = membership_length;
  zones->pending_foci = g_queue_new ();
  return zones;
}



/**
 * A function to insert a pointer at an arbitrary position in a GLib Pointer
 * Array. GLib 2.40 and higher has such a function (g_ptr_array_insert) but the
 * highest version available for Windows as of this comment is 2.34. */
static void
ptr_array_insert (GPtrArray * array, guint i, gpointer data)
{
  guint old_len;
  guint j;
  gpointer *pdata;

  old_len = array->len;
  g_ptr_array_set_size (array, old_len + 1);
  pdata = array->pdata;
  for (j = old_len; j > i; j--)
    pdata[j] = pdata[j - 1];
  pdata[i] = data;
}



/**
 * Appends a zone to a zone list.  The list is kept ordered by the "level"
 * parameter of the zone, with highest priority (lowest numbers) first.
 *
 * If the <i>radius</i> field of the zone is 0, the zone will treated as the
 * "background" zone.
 *
 * If the <i>level</i> field of the zone is -1, the zone will be given a
 * priority one lower (a level number one greater) than any seen so far.
 *
 * NB: The list retains a pointer to the given zone structure; do not free the
 * zone structure after adding it to a zone list.
 *
 * Side-effects: This function will log a warning if a zone with the same level
 * already exists, or if the radius of a zone with a lower level nubmer exceeds
 * that of an existing zone with a higher level number.
 *
 * @param zones a zone list.
 * @param zone a zone.
 * @return the index at which the new zone was added.
 */
unsigned int
ZON_zone_list_append (ZON_zone_list_t * zones, ZON_zone_t * zone)
{
  int i, j;
  gboolean has_background_zone;
  unsigned int nzones;
  ZON_zone_t *existing_zone;
  ZON_zone_fragment_t *fragment;

#if DEBUG
  g_debug ("----- ENTER ZON_zone_list_append");
#endif

  nzones = ZON_zone_list_length (zones);
  has_background_zone = (nzones > 0);

  if (zone->radius < EPSILON && has_background_zone)
    {
      /* This zone claims to be the "background" zone.  Since a background
       * zone (with no name) is created automatically before any zone
       * parameters are loaded, use this zone's name if the background
       * zone's name is currently blank. */
      existing_zone = ZON_zone_list_get (zones, nzones - 1);
      if (g_utf8_strlen (existing_zone->name, -1) == 0)
        {
          #if DEBUG
            g_debug ("setting name of background zone to \"%s\"", zone->name);
          #endif
          g_free (existing_zone->name);
          existing_zone->name = zone->name;
        }
      else
        {
          #if DEBUG
            g_debug ("there is already a background zone named \"%s\", ignoring zone \"%s\"",
                     existing_zone->name, zone->name);
          #endif
          ;
        }
      i = nzones - 1;
      goto end;
    }

  /* If we are adding the background zone, create a special fragment that
   * doesn't map to a polygon/contour. */
  if (zone->radius < EPSILON)
    {
      fragment = ZON_new_fragment (zone, -1);
      g_queue_push_tail (zone->fragments, fragment);
    }

  /* If the zone's surveillance level is -1, meaning that the parameter was
   * omitted, set the level as one greater (a priority one lower) than any 
   * existing zone. */
  if (zone->level == -1)
    {
      if (nzones > 1)
        zone->level = ZON_zone_list_get (zones, nzones - 2)->level + 1;
      else
        zone->level = 1;
    }

  /* Find the correct spot to insert the zone in the zone list. */
  for (i = 0; i < nzones; i++)
    {
      existing_zone = ZON_zone_list_get (zones, i);
      if (existing_zone->level == zone->level)
        {
          #if DEBUG
            g_debug ("zones \"%s\" and \"%s\" have the same level (%i)",
                     existing_zone->name, zone->name, zone->level);
          #endif
          for (j = i; j < nzones; j++)
            ZON_zone_list_get (zones, j)->level++;
          break;
        }
      else if (existing_zone->level > zone->level)
        break;
    }

  #if DEBUG
    g_debug ("new zone \"%s\" will be inserted into list at position %i", zone->name, i);
  #endif

  ptr_array_insert (zones->list, i, zone);

end:
#if DEBUG
  g_debug ("----- EXIT ZON_zone_list_append");
#endif

  return i;
}



/**
 * Resets all zones in a zone list.  Removes all foci, clears all pending foci,
 * and resets the membership array so that all herds are in the "background"
 * zone.
 */
void
ZON_zone_list_reset (ZON_zone_list_t *zones)
{
  unsigned int nzones, i;
  ZON_zone_fragment_t *background_zone;

#if DEBUG
  g_debug ("----- ENTER ZON_zone_list_reset");
#endif

  if (zones == NULL)
    goto end;

  nzones = ZON_zone_list_length (zones);

  for (i = 0; i < nzones; i++)
    ZON_reset (ZON_zone_list_get (zones, i));

  background_zone = ZON_zone_list_get_background (zones);
  for (i = 0; i < zones->membership_length; i++)
    zones->membership[i] = background_zone;
        
  /* Empty the list of pending zone foci. */
  while (!g_queue_is_empty (zones->pending_foci))
    g_free ((ZON_pending_focus_t *) g_queue_pop_head (zones->pending_foci));

end:
#if DEBUG
  g_debug ("----- EXIT ZON_zone_list_reset");
#endif

  return;
}



/**
 * Adds a new focus to the list of pending foci.
 *
 * @param zones a zone list.
 * @param x the x-coordinate of the focus (corresponds to longitude).
 * @param y the y-coordinate of the focus (corresponds to latitude).
 */
void
ZON_zone_list_add_focus (ZON_zone_list_t * zones, double x, double y)
{
  ZON_pending_focus_t *pending_focus;

#if DEBUG
  g_debug ("----- ENTER ZON_zone_list_add_focus");
#endif

  pending_focus = g_new (ZON_pending_focus_t, 1);
  pending_focus->x = x;
  pending_focus->y = y;
  g_queue_push_tail (zones->pending_foci, pending_focus);

#if DEBUG
  g_debug ("----- EXIT ZON_zone_list_add_focus");
#endif
}



/**
 * Returns a text string containing a zone list.
 *
 * @param zones a zone list.
 * @return a string.
 */
char *
ZON_zone_list_to_string (ZON_zone_list_t * zones)
{
  GString *s;
  char *substring, *chararray;
  unsigned int nzones;
  unsigned int i;               /* loop counter */

  s = g_string_new (NULL);

  nzones = ZON_zone_list_length (zones);
  if (nzones > 0)
    {
      substring = ZON_zone_to_string (ZON_zone_list_get (zones, 0));
      g_string_assign (s, substring);
      g_free (substring);
      for (i = 1; i < nzones; i++)
        {
          substring = ZON_zone_to_string (ZON_zone_list_get (zones, i));
          g_string_append_printf (s, "\n%s", substring);
          g_free (substring);
        }
    }
  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Prints a zone list to a stream.
 *
 * @param stream an output stream to write to.  If NULL, defaults to stdout.
 * @param zones a zone list.
 * @return the number of characters written.
 */
int
ZON_fprintf_zone_list (FILE * stream, ZON_zone_list_t * zones)
{
  char *s;
  int nchars_written;

#if DEBUG
  g_debug ("----- ENTER ZON_fprintf_zone_list");
#endif

  if (!stream)
    stream = stdout;

  s = ZON_zone_list_to_string (zones);
  nchars_written = fprintf (stream, "%s", s);
  free (s);

#if DEBUG
  g_debug ("----- EXIT ZON_fprintf_zone_list");
#endif

  return nchars_written;
}



/**
 * Deletes a zone list from memory.
 *
 * @param zones a zone list.
 */
void
ZON_free_zone_list (ZON_zone_list_t * zones)
{
  ZON_zone_t *zone;
  unsigned int nzones;
  int i;
  ZON_pending_focus_t *pending_focus;

#if DEBUG
  g_debug ("----- ENTER ZON_free_zone_list");
#endif

  if (zones == NULL)
    goto end;

  /* Free the dynamic parts of each zone structure. */
  nzones = ZON_zone_list_length (zones);
  for (i = 0; i < nzones; i++)
    {
      zone = ZON_zone_list_get (zones, i);
      ZON_free_zone (zone);
    }
  g_ptr_array_free (zones->list, TRUE);

  if (zones->membership != NULL)
    g_free (zones->membership);

  while (!g_queue_is_empty (zones->pending_foci))
    {
      pending_focus = (ZON_pending_focus_t *) g_queue_pop_head (zones->pending_foci);
      g_free (pending_focus);
    }
  g_queue_free (zones->pending_foci);

  g_free (zones);

end:
#if DEBUG
  g_debug ("----- EXIT ZON_free_zone_list");
#endif
  return;
}



/**
 * Returns the zone fragment corresponding to the "background" zone.  This is
 * the fragment to which all herds should be initially assigned.
 *
 * @param zones a zone list.
 * @return the fragment corresponding to the background zone.
 */
ZON_zone_fragment_t *
ZON_zone_list_get_background (ZON_zone_list_t * zones)
{
  unsigned int nzones;
  ZON_zone_t *zone;
  ZON_zone_fragment_t *fragment;

  /* Retrieve the last (lowest-priority) zone in the list. */
  nzones = ZON_zone_list_length (zones);
  g_assert (nzones >= 1);
  zone = ZON_zone_list_get (zones, nzones - 1);

  #if DEBUG
    g_debug ("background zone is named \"%s\", has %i fragments",
             zone->name, g_queue_get_length (zone->fragments));
  #endif

  fragment = (ZON_zone_fragment_t *) g_queue_peek_head (zone->fragments);
  g_assert (fragment->parent == zone);

  /* The zone will have just one fragment. */
  return (ZON_zone_fragment_t *) g_queue_peek_head (zone->fragments);
}



/**
 * Creates a new zone.
 *
 * @param name a text label for the zone.  The name is copied and can be freed
 *   after calling this function.
 * @param level the priority level of the zone.  Must be >= 1.  Lower numbers
 *   will probably correspond to a smaller radius and a higher surveillance
 *   level.
 * @param radius the radius of the circle drawn around each new focus.
 * @return a pointer to a newly-created, initialized ZON_zone_t structure.
 */
ZON_zone_t *
ZON_new_zone (char *name, int level, double radius)
{
  ZON_zone_t *z;

#if DEBUG
  g_debug ("----- ENTER ZON_new_zone");
#endif

  z = g_new (ZON_zone_t, 1);
  z->name = g_strdup (name);
  z->level = level;
  z->radius = radius;
  z->radius_sq = radius * radius;
  z->epsilon_sq = (radius + EPSILON) * (radius + EPSILON) - z->radius_sq;
  z->foci = g_array_new (FALSE, FALSE, sizeof (gpc_vertex));
  z->poly = g_new (gpc_polygon, 1);
  z->poly->num_contours = 0;
  z->poly->hole = NULL;
  z->poly->contour = NULL;
  z->fragments = g_queue_new ();
  z->area = 0;
  z->perimeter = 0;
  z->nholes_filled = 0;
#ifdef USE_SC_GUILIB
  z->max_area = 0.0;
  z->max_day = 0;
  z->_unitDays = g_hash_table_new( g_direct_hash, g_direct_equal );
  z->_animalDays = g_hash_table_new( g_direct_hash, g_direct_equal );
#endif

#if DEBUG
  g_debug ("----- EXIT ZON_new_zone");
#endif

  return z;
}



/**
 * Returns a deep copy of a zone.
 *
 * @param zone a zone to be copied.
 * @return a pointer to a newly-created, initialized ZON_zone_t structure.
 */
ZON_zone_t *
ZON_clone_zone (ZON_zone_t * zone)
{
  ZON_zone_t *clone;

#if DEBUG
  g_debug ("----- ENTER ZON_clone_zone");
#endif

  clone = g_new (ZON_zone_t, 1);
  clone->name = g_strdup (zone->name);

#if DEBUG
  g_debug ("----- ENTER ZON_clone_zone");
#endif

  return clone;
}



/**
 * Deletes a zone structure from memory.
 *
 * @param zone a pointer to a ZON_zone_t structure.
 */
void
ZON_free_zone (ZON_zone_t * zone)
{
  if (zone == NULL)
    return;

  g_free (zone->name);
  g_array_free (zone->foci, TRUE);
  gpc_free_polygon (zone->poly);
  g_free (zone->poly);
  while (!g_queue_is_empty (zone->fragments))
    ZON_free_fragment ((ZON_zone_fragment_t *) g_queue_pop_head (zone->fragments));
  g_queue_free (zone->fragments);
  g_free (zone);
}



/**
 * Returns a text representation of a zone.
 *
 * @param zone a zone.
 * @return a string.
 */
char *
ZON_zone_to_string (ZON_zone_t * zone)
{
  GString *s;
  char *chararray;
#if DEBUG
  int i, j;                     /* loop counters */
  gpc_vertex_list *contour;
  gpc_vertex *vertex;
  GList *iter;
  ZON_zone_fragment_t *fragment;
#endif

  s = g_string_new (NULL);
  g_string_printf (s, "<zone \"%s\" level=%i", zone->name, zone->level);

  if (zone->radius > EPSILON)
    g_string_append_printf (s, " radius=%.2g", zone->radius);
  else
    g_string_append_printf (s, " all other areas");

  /* If the library was compiled with debugging information turned on, list the
   * polygon contours and the mapping of fragments to contours.  Otherwise,
   * just output how many separate contours make up the zone. */
#if DEBUG
  g_string_append_printf (s, "\n  contours={");
  for (i = 0; i < zone->poly->num_contours; i++)
    {
      g_string_append_printf (s, "\n    ");
      contour = &(zone->poly->contour[i]);
      for (j = 0; j < contour->num_vertices; j++)
        {
          vertex = &(contour->vertex[j]);
          g_string_append_printf (s, (j > 0) ? ",(%g,%g)" : "(%g,%g)", vertex->x, vertex->y);
        }
    }
  g_string_append_c (s, '}');
#else
  g_string_append_printf (s, "\n  %i separate areas", zone->poly->num_contours);
#endif

#if DEBUG
  g_string_append_printf (s, "\n  fragments={");
  for (iter = zone->fragments->head; iter != NULL; iter = g_list_next (iter))
    {
      fragment = (ZON_zone_fragment_t *) (iter->data);
      g_string_append_printf (s, "\n    %i->contour %i", fragment->id, fragment->contour);
    }
  g_string_append_c (s, '}');
#endif

  g_string_append_c (s, '>');

  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);
  return chararray;
}



/**
 * Returns a gnuplot script for drawing a zone.
 *
 * @param zone a zone.
 * @return a string containing a gnuplot script.
 */
char *
ZON_zone_to_gnuplot (ZON_zone_t * zone)
{
  GString *s;
  char *chararray;
  int i;
  gpc_vertex_list *contour;
  gpc_vertex *vertex;
  int j;

#if DEBUG
  g_debug ("----- ENTER ZON_zone_to_gnuplot");
#endif

  s = g_string_new ("plot ");
  for (i = 0; i < zone->poly->num_contours; i++)
    {
      if (i > 0)
        g_string_append_printf (s, ", ");
      g_string_append_printf (s, "'-' title 'contour %i", i);
      if (zone->poly->hole[i] == 1)
        g_string_append_printf (s, " (hole)");
      g_string_append_printf (s, "' w l lw 3");
    }

  for (i = 0; i < zone->poly->num_contours; i++)
    {
      contour = &(zone->poly->contour[i]);
      for (j = 0; j < contour->num_vertices; j++)
        {
          vertex = &(contour->vertex[j]);
          g_string_append_printf (s, "\n%g %g", vertex->x, vertex->y);
        }
      /* Repeat the first point to close the contour. */
      vertex = &(contour->vertex[0]);
      g_string_append_printf (s, "\n%g %g", vertex->x, vertex->y);
      g_string_append_printf (s, "\ne");
    }

  /* don't return the wrapper object */
  chararray = s->str;
  g_string_free (s, FALSE);

#if DEBUG
  g_debug ("----- EXIT ZON_zone_to_gnuplot");
#endif

  return chararray;
}



/**
 * Prints a zone to a stream.
 *
 * @param stream an output stream to write to.  If NULL, defaults to stdout.
 * @param zone a zone.
 * @return the number of characters written.
 */
int
ZON_fprintf_zone (FILE * stream, ZON_zone_t * zone)
{
  char *s;
  int nchars_written;

  s = ZON_zone_to_string (zone);
  nchars_written = fprintf (stream ? stream : stdout, "%s", s);
  free (s);
  return nchars_written;
}



/**
 * Returns a deep copy of a GPC contour.
 *
 * @param contour a contour.
 * @return a copy of <i>contour</i>
 */
gpc_vertex_list *
gpc_copy_contour (gpc_vertex_list * contour)
{
  int nvertices;
  int i;
  gpc_vertex_list *new_contour;

  nvertices = contour->num_vertices;
  new_contour = g_new (gpc_vertex_list, 1);
  new_contour->num_vertices = nvertices;
  new_contour->vertex = g_new (gpc_vertex, nvertices);
  for (i = 0; i < nvertices; i++)
    new_contour->vertex[i] = contour->vertex[i];

  return new_contour;
}



/**
 * Returns whether two GPC contours are the same.
 *
 * @param contour1 a contour.
 * @param contour2 a contour.
 * @return TRUE if the contours are the same, FALSE otherwise.
 */
gboolean
gpc_contour_equal (gpc_vertex_list * contour1, gpc_vertex_list * contour2)
{
  int i;
  gpc_vertex *v1, *v2;

  if (contour1->num_vertices != contour2->num_vertices)
    return FALSE;

  for (i = 0; i < contour1->num_vertices; i++)
    {
      v1 = &(contour1->vertex[i]);
      v2 = &(contour2->vertex[i]);
      if ((v1->x != v2->x) || (v1->y != v2->y))
        return FALSE;
    }

  return TRUE;
}



/**
 * Adds a new focus to a zone.
 *
 * @param zone a zone.
 * @param x the x-coordinate of the focus.
 * @param y the y-coordinate of the focus.
 * @param holes a location in which to return any "holes" filled in when the
 *   focus was added.  If NULL, the holes will not be returned.
 * @return the fragment (possibly a newly-created one) in which the focus lies.
 */
ZON_zone_fragment_t *
ZON_zone_add_focus (ZON_zone_t * zone, double x, double y, gpc_polygon ** holes)
{
  gpc_vertex_list *contour;
  double angle, step;
  int i, j;                     /* loop counter */
  gpc_polygon *circle, *intermedpoly, *newpoly;
  int nholes, hole_index;
  ZON_zone_fragment_t *fragment, *fragment_containing_focus;
  GList *iter;
#if DEBUG
  char *s;
#endif

#if DEBUG
  g_debug ("----- ENTER ZON_zone_add_focus");
#endif

  /* Eliminate compiler warnings about uninitialized values */
  nholes = INT_MIN;
  fragment_containing_focus = NULL;

  /* If the zone is a "background" zone, simply return the one fragment. */
  if (zone->radius < EPSILON)
    {
      fragment_containing_focus = (ZON_zone_fragment_t *) g_queue_peek_head (zone->fragments);
      goto end;
    }

  /* Create a new contour, a circle around the focus. */
  #if DEBUG
    g_debug ("creating %i-sided polygon to approximate a circle", CIRCLE_NSIDES);
  #endif
  contour = g_new (gpc_vertex_list, 1);
  contour->num_vertices = CIRCLE_NSIDES;
  contour->vertex = g_new (gpc_vertex, CIRCLE_NSIDES);
  step = TWOPI / CIRCLE_NSIDES; /* radians in each segment of the circle */
  for (i = 0, angle = 0; i < CIRCLE_NSIDES; i++, angle += step)
    {
      contour->vertex[i].y = sin (angle) * zone->radius + y;
      contour->vertex[i].x = cos (angle) * zone->radius + x;
    }

  /* Wrap the contour in a polygon object. */
  circle = gpc_new_polygon ();
  gpc_add_contour (circle, contour, 0);

  /* Get the union of the existing polygon and the new circle. */
  intermedpoly = g_new (gpc_polygon, 1);
  gpc_polygon_clip (GPC_UNION, zone->poly, circle, intermedpoly);

  /* Close any holes in the new polygon, in accordance with the no-donuts
   * rule. */
  if (holes != NULL)
    {
      /* The caller requested that a list of the holes be returned.  Prepare a
       * polygon object to hold them. */
      nholes = 0;
      for (i = 0; i < intermedpoly->num_contours; i++)
        if (intermedpoly->hole[i] == TRUE)
          nholes++;

      *holes = gpc_new_polygon ();
      (*holes)->num_contours = nholes;
      (*holes)->hole = (int *) malloc (sizeof(int) * nholes);
      g_assert ((*holes)->hole != NULL);
      for (i = 0; i < nholes; i++)
        (*holes)->hole[i] = 0;
      (*holes)->contour = (gpc_vertex_list *) malloc (sizeof(gpc_vertex_list) * nholes);
      g_assert ((*holes)->contour != NULL);
    }
  hole_index = 0;
  i = 0;
  while (i < intermedpoly->num_contours)
    if (intermedpoly->hole[i] == TRUE)
      {
        #if DEBUG
          g_debug ("removing hole (contour at index %i)", i);
        #endif
        if (holes != NULL)
          {
            /* Copy the vertex list to the list of holes. */
            (*holes)->contour[hole_index++] = intermedpoly->contour[i];
          }
        else
          {
            /* Free the vertex list for the hole. */
            free (intermedpoly->contour[i].vertex);
          }

        /* Move higher-numbered contours down to fill the gap. */
        for (j = i + 1; j < intermedpoly->num_contours; j++)
          {
            intermedpoly->hole[j - 1] = intermedpoly->hole[j];
            intermedpoly->contour[j - 1] = intermedpoly->contour[j];
          }
        intermedpoly->num_contours--;
        zone->nholes_filled++;
      }
    else
      i++;

  /* If there were holes, we need to union the new polygon with itself, so that
   * any contours that were completely inside a hole will be absorbed.  This
   * operation will turn those absorbed contours into holes themselves, so we
   * have to go through the exercise of removing holes again. */
  if (nholes == 0)
    {
      newpoly = intermedpoly;
    }
  else
    {
      newpoly = g_new (gpc_polygon, 1);
      #if DEBUG
        g_debug ("union new polygon with itself");
      #endif
      gpc_polygon_clip (GPC_UNION, intermedpoly, intermedpoly, newpoly);
      gpc_free_polygon (intermedpoly);
      i = 0;
      while (i < newpoly->num_contours)
        {
          if (newpoly->hole[i] == TRUE)
            {
              #if DEBUG
                g_debug ("removing hole (contour at index %i)", i);
              #endif
              /* Free the vertex list for the hole. */
              free (newpoly->contour[i].vertex);

              /* Move higher-numbered contours down to fill the gap. */
              for (j = i + 1; j < newpoly->num_contours; j++)
                {
                  newpoly->hole[j - 1] = newpoly->hole[j];
                  newpoly->contour[j - 1] = newpoly->contour[j];
                }
              newpoly->num_contours--;
            }
          else
            i++;
        }
    }

  /* Now we need to update the zone fragment list.  One of three things may
   * have happened:
   * 1 - The number of contours in the zone polygon increased by one.  This
   *     means that the circle was outside of any previous contours, and a new
   *     fragment is needed.
   * 2 - The number of contours in the zone polygon stayed the same.  This
   *     means that the circle overlapped or was entirely inside an existing
   *     contour, so we need to find out which contour that was.
   * 3 - The number of contours in the zone polygon decreased.  This means that
   *     the circle joined two or more existing contours, so we need to find
   *     out which ones.
   */
  if (newpoly->num_contours > zone->poly->num_contours)
    {
      #if DEBUG
        g_debug ("new circle is disjoint from any existing zone fragment");
      #endif
      /* Find the index of the new contour.  (Assume the rest of the contours
       * remain in order, but with a new contour inserted somewhere). */
      for (i = 0; i < newpoly->num_contours; i++)
        {
          contour = &(newpoly->contour[i]);
          /* We know the new shape is a polygon with CIRCLE_NSIDES sides
           * centered on x,y. */
          #if DEBUG
            g_debug ("contour %i %ith point=(%.2f,%.2f) %ith point=(%.2f,%.2f)",
                     i,
                     CIRCLE_NSIDES / 4 - 1,
                     contour->vertex[CIRCLE_NSIDES / 4 - 1].x,
                     contour->vertex[CIRCLE_NSIDES / 4 - 1].y,
                     CIRCLE_NSIDES / 2 - 1,
                     contour->vertex[CIRCLE_NSIDES - 1].x, contour->vertex[CIRCLE_NSIDES - 1].y);
          #endif
          if (fabs (contour->vertex[CIRCLE_NSIDES / 4 - 1].y - y) < EPSILON
              && fabs (contour->vertex[CIRCLE_NSIDES - 1].x - x) < EPSILON)
            break;
        }
      #if DEBUG
        g_debug ("new contour has index %i", i);
      #endif
      /* The indices of the other contours increase by 1, so update the
       * existing zone fragments. */
      for (iter = zone->fragments->head; iter != NULL; iter = g_list_next (iter))
        {
          fragment = (ZON_zone_fragment_t *) (iter->data);
          if (fragment->contour >= i)
            fragment->contour++;
        }
      /* Now add the new fragment.  Store the new focus as a "sample" point,
       * one that is known to be inside the fragment. */
      fragment = ZON_new_fragment (zone, i);
      fragment->sample.x = x;
      fragment->sample.y = y;
      g_queue_push_tail (zone->fragments, fragment);
      fragment_containing_focus = fragment;

      /* End of case where a new contour is added. */
    }
  else /* newpoly->num_contours <= zone->poly->num_contours */
    {
      #if DEBUG
        if (newpoly->num_contours == zone->poly->num_contours)
          g_debug ("new circle overlapped or was enclosed by existing zone fragment");
        else
          g_debug ("new circle merged two or more existing zone fragments");
      #endif
      /* Use a point-in-polygon test to figure out which contour joined or
       * enclosed the circle. */
      for (i = 0; i < newpoly->num_contours; i++)
        if (GIS_point_in_contour (&(newpoly->contour[i]), x, y))
          break;
      #if DEBUG
        g_debug ("point (%g,%g) is inside contour with index %i", x, y, i);
      #endif
      /* Take the "sample" point stored along with each fragment.  Use a
       * point-in-polygon test to figure out which new contour corresponds to
       * each existing fragment.  At the same time, watch for a fragment that
       * maps to the contour containing the focus.
       *
       * NB: This is done even if the number of contours has not changed,
       * because sometimes GPC shuffles some of the contours around.  Is this
       * overkill - would it work to simply scan to the left & right of the
       * contour containing the new point, stopping upon encountering a contour
       * that has not changed?
       */
      for (iter = zone->fragments->head; iter != NULL; iter = g_list_next (iter))
        {
          fragment = (ZON_zone_fragment_t *) (iter->data);
          for (j = 0; j < newpoly->num_contours; j++)
            if (GIS_point_in_contour
                (&(newpoly->contour[j]), fragment->sample.x, fragment->sample.y))
              {
                fragment->contour = j;
                break;
              }
          #if DEBUG
            g_debug ("fragment %i now maps to contour with index %i", fragment->id, j);
          #endif
          if (j == i)
            fragment_containing_focus = fragment;
        }

      /* End of case where the number of contours stays the same or decreases. */
    }

  /* Discard the old polygon defining the zone and use the new one. */
  gpc_free_polygon (zone->poly);
  zone->poly = newpoly;

#if DEBUG
  s = ZON_zone_to_gnuplot (zone);
  g_debug ("to visualize new zone:\n%s", s);
  g_free (s);
#endif

  /* Clean up. */
  gpc_free_polygon (circle);

end:
#if DEBUG
  g_debug ("----- EXIT ZON_zone_add_focus");
#endif
  return fragment_containing_focus;
}



/**
 * Resets a zone to not covering any areas.
 *
 * @param zone a zone.
 */
void
ZON_reset (ZON_zone_t * zone)
{  
#if DEBUG
  g_debug ("----- ENTER ZON_reset");
#endif

#ifdef USE_SC_GUILIB
  zone->max_area = 0.0;
  zone->max_day = 0;

  if ( zone->_unitDays != NULL )
  {
    g_hash_table_destroy( zone->_unitDays );
    zone->_unitDays = g_hash_table_new( g_direct_hash, g_direct_equal );
  };

  if ( zone->_animalDays != NULL )
  {
    g_hash_table_destroy( zone->_animalDays );
    zone->_animalDays =  g_hash_table_new( g_direct_hash, g_direct_equal );
  };
#endif

/* If this is the "background" zone, there's nothing to do. */
  if (zone->radius < EPSILON)
  {
    #if DEBUG
      g_debug ("----- EXIT ZON_reset, early exit; background zone, no work to perform.");
    #endif
    return;
  }

  /* Empty the list of the foci that built the zone. */
  g_array_set_size (zone->foci, 0);

  /* Erase the polygon and create a new, empty one. */
  gpc_free_polygon (zone->poly);
  zone->poly->num_contours = 0;
  zone->poly->hole = NULL;
  zone->poly->contour = NULL;

  /* Empty the list of zone fragments. */
  while (!g_queue_is_empty (zone->fragments))
    ZON_free_fragment ((ZON_zone_fragment_t *) g_queue_pop_head (zone->fragments));

  /* Reset the area and perimeter. */
  zone->area = zone->perimeter = 0;

  /* Reset the count of holes filled. */
  zone->nholes_filled = 0;
#if DEBUG
  g_debug ("----- EXIT ZON_reset");
#endif  
}



/**
 * Returns whether a zone contains a particular location.
 *
 * @param zone a zone.
 * @param x the x-coordinate of the location.
 * @param y the y-coordinate of the location.
 * @return TRUE if the location is inside the zone, FALSE otherwise.
 */
gboolean
ZON_zone_contains (ZON_zone_t * zone, double x, double y)
{
  return GIS_point_in_polygon (zone->poly, x, y);
}



gboolean
ZON_same_zone (ZON_zone_fragment_t * fragment1, ZON_zone_fragment_t * fragment2)
{
  if (fragment1 == NULL || fragment2 == NULL)
    return FALSE;

  return (fragment1->parent == fragment2->parent);
}



gboolean
ZON_same_fragment (ZON_zone_fragment_t * fragment1, ZON_zone_fragment_t * fragment2)
{
  return ZON_same_zone (fragment1, fragment2) && (fragment1->contour == fragment2->contour);
}



/**
 * Tests whether one zone fragment nests inside another.
 *
 * @param inner a fragment of the higher-level zone (smaller zone circles)
 * @param outer a fragment of the lower-level zone (larger zone circles)
 * @return TRUE if "inner" nests inside "outer", FALSE otherwise.
 */
gboolean
ZON_nests_in (ZON_zone_fragment_t * inner, ZON_zone_fragment_t * outer)
{
  gboolean result;

  /* The level of "inner" must be less than the level of "outer" (e.g., zone
   * circles of level 1 are inside zone circles of level 2). */
  if (ZON_level (inner) >= ZON_level (outer))
    result = FALSE;
  else if (ZON_level (inner) == ZON_level (outer) - 1)
    {
      result = ZON_same_fragment (inner->nests_in, outer);
    }
  else
    {
      /* Recursive call. */
      result = ZON_nests_in (inner->nests_in, outer);
    }

  return result;
}



/**
 * Re-calculates the area of the zone polygon.
 *
 * @param zone a zone.
 * @return the calculated area.
 */
double
ZON_update_area (ZON_zone_t *zone)
{
  double area;
  
  if (zone == NULL)
    area = 0;
  else
    area = zone->area = GIS_polygon_area (zone->poly);

  return area;
}


/**
 * Re-calculates the perimeter of the zone polygon.
 *
 * @param zone a zone.
 * @return the calculated perimeter.
 */
double
ZON_update_perimeter (ZON_zone_t *zone)
{
  double perimeter;
  
  if (zone == NULL)
    perimeter = 0;
  else
    perimeter = zone->perimeter = GIS_polygon_perimeter (zone->poly);

  return perimeter;
}

#ifdef USE_SC_GUILIB
  void addToZoneTotals( unsigned short int _day, ZON_zone_t *_zone, unsigned int _prod_id, unsigned int _herd_size   )
  {
    guint herdCount, animalCount;
    #if DEBUG
      g_debug ("----- ENTER addToZoneTotals");
    #endif  

    #if DEBUG
      g_debug ("----- addToZoneTotals: Checking Unit Days...");
    #endif    

    if ( _zone == NULL )
    {
      g_debug ("----- EXIT addToZoneTotals, premature exit, _zone == NULL !");       
      return;
    };
  
#if DEBUG
  g_debug ("----- addToZoneTotals: Zone unitDays, for zone (%s), hash table size is: %i", ((_zone->name != NULL)? _zone->name:"NONE"),  g_hash_table_size( _zone->_unitDays) );
#endif    

    if ( g_hash_table_size( _zone->_unitDays ) == 0 )
    {  
#if DEBUG
  g_debug ("----- addToZoneTotals: Adding to the herd Count for this produciton type...inserting first one.");
#endif          
  	  herdCount = 1;
      g_hash_table_insert( _zone->_unitDays, GUINT_TO_POINTER(_prod_id), GUINT_TO_POINTER(herdCount) );
    }
    else
    {
	  if ( g_hash_table_lookup( _zone->_unitDays, GUINT_TO_POINTER(_prod_id) ) == NULL )
	  {
#if DEBUG
  g_debug ("----- addToZoneTotals: Adding to the herd Count for this produciton type...inserting.");
#endif            
  	    herdCount = 1;
        g_hash_table_insert( _zone->_unitDays, GUINT_TO_POINTER(_prod_id), GUINT_TO_POINTER(herdCount) );
	  }
	  else
	  {
#if DEBUG
  g_debug ("----- addToZoneTotals: Adding to the herd Count for this produciton type...replacing.");
#endif           
        herdCount =  GPOINTER_TO_UINT(g_hash_table_lookup( _zone->_unitDays, GUINT_TO_POINTER(_prod_id) )) + 1;
        g_hash_table_replace( _zone->_unitDays, GUINT_TO_POINTER(_prod_id), GUINT_TO_POINTER(herdCount) );
	  };
    };

#if DEBUG
  g_debug ("----- addToZoneTotals: Checkig Animal Days...");
#endif   

    if ( g_hash_table_size( _zone->_animalDays ) == 0 ) 
    {   
#if DEBUG
  g_debug ("----- addToZoneTotals: Adding to the animal Count for this produciton type...inserting first one.");
#endif           
      animalCount = _herd_size;      
      g_hash_table_insert( _zone->_animalDays, GUINT_TO_POINTER(_prod_id), GUINT_TO_POINTER(animalCount) );
    }
    else
    {
	  if ( g_hash_table_lookup( _zone->_animalDays, GUINT_TO_POINTER(_prod_id) ) == NULL )
	  {
#if DEBUG
  g_debug ("----- addToZoneTotals: Adding to the animal Count for this produciton type...inserting.");
#endif            
		animalCount = _herd_size;      
        g_hash_table_insert( _zone->_animalDays, GUINT_TO_POINTER(_prod_id), GUINT_TO_POINTER(animalCount) );
	  }
	  else
	  {
#if DEBUG
  g_debug ("----- addToZoneTotals: Adding to the animal Count for this produciton type...replacing.");
#endif           
  	    animalCount =  GPOINTER_TO_UINT( g_hash_table_lookup( _zone->_animalDays, GUINT_TO_POINTER(_prod_id) )) + _herd_size;
        g_hash_table_replace( _zone->_animalDays, GUINT_TO_POINTER(_prod_id), GUINT_TO_POINTER(animalCount) );
	  };
    };    

#if DEBUG
  g_debug ("----- EXIT addToZoneTotals");
#endif 
 
  }
#endif

/* end of file zone.c */
