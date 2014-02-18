/** @file shp2png.c
 *
 * A filter that takes an ArcView file of units (output from xml2shp or
 * weekly_gis_filter) and optionally an Arcview file of zones (output from
 * weekly_gis_zones_filter) and creates a picture in PNG format to show the
 * status of each unit and the extent of the zones.
 *
 * Call it as
 *
 * <code>shp2png [-z ZONE-SHP-FILE] POPULATION-SHP-FILE [IMAGE-FILE]</code>
 *
 * If the image file name is omitted, the image file will have the same name as
 * the ArcView unit file, but with a ".png" extension instead of ".shp".
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @date November 2005
 *
 * Copyright &copy; University of Guelph, 2005-2006
 * 
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 */

#if HAVE_CONFIG_H
#  include <config.h>
#endif

#include <stdio.h>
#include <glib.h>
#include <shapefil.h>
#include <gd.h>

#if STDC_HEADERS
#  include <stdlib.h>
#  include <string.h>
#elif HAVE_STRINGS_H
#  include <strings.h>
#endif

#if !HAVE_ROUND && HAVE_RINT
#  define round rint
#endif

/* Temporary fix -- "round" and "rint" are in the math library on Red Hat 7.3,
 * but they're #defined so AC_CHECK_FUNCS doesn't find them. */
double round (double x);



#define MAX_X_SIZE 640
#define MAX_Y_SIZE 480
#define MIN_RATIO 0.5
#define MAX_RATIO 2.0
#define IMAGE_BORDER 20
#define MARKER_SIZE 5
/* One hundred metres */
#define EPSILON 0.000898315



/**
 * A log handler that simply discards messages.
 */
void
silent_log_handler (const gchar * log_domain, GLogLevelFlags log_level,
                    const gchar * message, gpointer user_data)
{
  ;
}



/**
 * Blends one colour into another.
 *
 * @param r1 the red value of the first colour (0-255).
 * @param g1 the green value of the first colour (0-255).
 * @param b1 the blue value of the first colour (0-255).
 * @param r2 the red value of the second colour (0-255).
 * @param g2 the green value of the second colour (0-255).
 * @param b2 the blue value of the second colour (0-255).
 * @param amount the amount of blending.  0 yields the first colour, 1 yields
 *   the second colour, and intermediate values yield a blend.
 * @param r a location in which to store the result red value.
 * @param g a location in which to store the result green value.
 * @param b a location in which to store the result blue value.
 */
void
blend (int r1, int g1, int b1, int r2, int g2, int b2, double amount, int *r, int *g, int *b)
{
  *r = (int) round ((r2 - r1) * amount + r1);
  *g = (int) round ((g2 - g1) * amount + g1);
  *b = (int) round ((b2 - b1) * amount + b1);
}



void
draw_zones (SHPHandle shape_file, int nzones, gdImagePtr im,
            double min_x, double width, double min_y, double height,
            unsigned int image_x, unsigned int image_y)
{
  int black;
  int hr, hg, hb;               /* colour for the highest-level zone */
  int lr, lg, lb;               /* colour for the lowest-level zone */
  int *colour;
  double blend_amount;
  int r, g, b;                  /* blended colour */
  unsigned int i, j, n;
  int shape_index;
  SHPObject *shape;
  int part;
  int partStart, partEnd;
  gdPoint *points;

#if DEBUG
  g_debug ("----- ENTER draw_zones");
#endif

  black = gdImageColorAllocate (im, 0, 0, 0);
  /* For the highest-level zone, use a paler version of the red used for
   * Infectious Clinical units.  For the lowest-level zone, use a paler version
   * of the yellow used for Latent units.  (If there is only one zone, use the
   * red.)  Use the blending function to get colours for zones in between. */
  hr = 204;
  hg = 0;
  hb = 0;
  blend (hr, hg, hb, 255, 255, 255, 0.5, &hr, &hg, &hb);
  lr = 229;
  lg = 229;
  lb = 0;
  blend (lr, lg, lb, 255, 255, 255, 0.5, &lr, &lg, &lb);
  colour = g_new (int, nzones);
  for (i = 0; i < nzones; i++)
    {
      if (nzones == 1)
        blend_amount = 1.0;
      else
        blend_amount = 1.0 * i / (nzones - 1);
      blend (lr, lg, lb, hr, hg, hb, blend_amount, &r, &g, &b);
      colour[i] = gdImageColorAllocate (im, r, g, b);
    }

  /* Draw each zone as a polygon. */
  for (shape_index = 0; shape_index < nzones; shape_index++)
    {
      #if DEBUG
        g_debug ("drawing zone %i", shape_index);
      #endif
      shape = SHPReadObject (shape_file, shape_index);

      /* A shape may contain several "parts", corresponding to disconnected
       * areas of the same zone.  Copy each part to an array of gdPoints, as
       * required by the polygon drawing function. */
      #if DEBUG
        g_debug ("zone %i has %i parts", shape_index, shape->nParts);
      #endif
      partStart = 0;
      for (part = 0; part < shape->nParts; part++)
        {
          if (part < (shape->nParts - 1))
            partEnd = shape->panPartStart[part + 1];
          else
            partEnd = shape->nVertices;
          n = partEnd - partStart;
          #if DEBUG
            g_debug ("part %i has %i points (indexes %i-%i)", part, n, partStart, partEnd - 1);
          #endif

          points = g_new (gdPoint, n);
          for (i = partStart, j = 0; i < partEnd; i++, j++)
            {
              points[j].x =
                (int) round ((shape->padfX[i] - min_x) / width * image_x + IMAGE_BORDER);
              /* Remember that latitude goes up, and pixel y-coordinates go down. */
              points[j].y =
                (int) round (IMAGE_BORDER + image_y -
                             ((shape->padfY[i] - min_y) / height * image_y));
            }

          gdImageFilledPolygon (im, points, n, colour[shape_index]);
          gdImagePolygon (im, points, n, black);

          g_free (points);
          partStart = partEnd;
        }

      SHPDestroyObject (shape);
    }

  g_free (colour);

#if DEBUG
  g_debug ("----- EXIT draw_zones");
#endif

  return;
}



void
draw_units (SHPHandle shape_file, DBFHandle attribute_file, int nunits, gdImagePtr im,
            double min_x, double width, double min_y, double height,
            unsigned int image_x, unsigned int image_y)
{
  /* Color indexes */
  int white, grey, yellow, orange, red, green, blue, black;
  int field_index;
  DBFFieldType field_type;
  int shape_index;
  SHPObject *shape;
  double unit_x, unit_y;
  double point_x, point_y;
  const char *field_value;
  int color;

#if DEBUG
  g_debug ("----- ENTER draw_units");
#endif

  /* Allocate colours. */
  white = gdImageColorAllocate (im, 255, 255, 255);
  grey = gdImageColorAllocate (im, 200, 200, 200);
  yellow = gdImageColorAllocate (im, 229, 229, 0);
  orange = gdImageColorAllocate (im, 229, 153, 0);
  red = gdImageColorAllocate (im, 204, 0, 0);
  green = gdImageColorAllocate (im, 0, 168, 0);
  blue = gdImageColorAllocate (im, 0, 0, 168);
  black = gdImageColorAllocate (im, 0, 0, 0);

  /* Get the index of the status field in the attribute file.  If there is no
   * attribute file, or no status field, or the field isn't of type text, we
   * will just colour all units white. */
  if (attribute_file == NULL)
    field_index = -1;
  else
    {
      field_index = DBFGetFieldIndex (attribute_file, "status");
      if (field_index == -1)
        {
          g_warning ("there is no attribute named \"status\"");
        }
      else
        {
          /* Check that the field is of type text. */
          field_type = DBFGetFieldInfo (attribute_file, field_index, NULL, NULL, NULL);
          if (field_type != FTString)
            {
              g_warning ("attribute \"status\" must be of text type");
              field_index = -1;
            }
        }
    }

  /* Draw a coloured circle representing each unit. */
  #if DEBUG
    g_debug ("drawing units");
  #endif
  for (shape_index = 0; shape_index < nunits; shape_index++)
    {
      shape = SHPReadObject (shape_file, shape_index);
      unit_x = shape->padfX[0];
      point_x = round ((unit_x - min_x) / width * image_x + IMAGE_BORDER);
      /* Remember that latitude goes up, and pixel y-coordinates go down. */
      unit_y = shape->padfY[0];
      point_y = round (IMAGE_BORDER + image_y - ((unit_y - min_y) / height * image_y));

      if (field_index == -1)
        color = white;
      else
        {
          field_value = DBFReadStringAttribute (attribute_file, shape_index, field_index);
          if (field_value == NULL)
            {
              g_warning ("no status for unit %i", shape_index);
              color = white;
            }
          else if (strcmp (field_value, "Susc") == 0)
            color = white;
          else if (strcmp (field_value, "Lat") == 0)
            color = yellow;
          else if (strcmp (field_value, "Subc") == 0)
            color = orange;
          else if (strcmp (field_value, "Clin") == 0)
            color = red;
          else if (strcmp (field_value, "NImm") == 0)
            color = green;
          else if (strcmp (field_value, "VImm") == 0)
            color = blue;
          else if (strcmp (field_value, "Dest") == 0)
            color = black;

          /* Note that we don't free field_value; it is a pointer to an
           * internal buffer in shapelib. */
        }
      if (color == white)
        {
          gdImageFilledEllipse (im, (int) point_x, (int) point_y, MARKER_SIZE, MARKER_SIZE, white);
          gdImageArc (im, (int) point_x, (int) point_y, MARKER_SIZE, MARKER_SIZE, 0, 360, grey);
        }
      else
        {
          gdImageFilledEllipse (im, (int) point_x, (int) point_y,
                                MARKER_SIZE, MARKER_SIZE, color);
        }
      SHPDestroyObject (shape);
    }

  #if DEBUG
    g_debug ("----- EXIT draw_units");
  #endif

  return;
}



void
convert (const char *unit_shapefile_name, const char *zone_shapefile_name,
         const char *image_file_name)
{
  SHPHandle unit_shape_file = NULL;
  int nunits;
  int shape_type;
  double minbound[4], maxbound[4];
  DBFHandle unit_attribute_file = NULL;
  double width, height, center;
  double ratio1, ratio2;
  double min_x, min_y;
  unsigned int image_x, image_y;
  gdImagePtr im = NULL;
  SHPHandle zone_shape_file = NULL;
  int nzones;
  FILE *fp = NULL;

#if DEBUG
  g_debug ("----- ENTER convert");
#endif

  /* Open the unit shape and DBF (attribute) files for reading. */
  #if DEBUG
    g_debug ("opening unit shape file \"%s\"", unit_shapefile_name);
  #endif
  unit_shape_file = SHPOpen (unit_shapefile_name, "rb");
  if (unit_shape_file == NULL)
    {
      g_warning ("could not open unit shape file");
      goto end;
    }

  /* Verify that the unit shape file contains points. */
  SHPGetInfo (unit_shape_file, &nunits, &shape_type, minbound, maxbound);
  if (shape_type != SHPT_POINT)
    {
      g_warning ("unit shape file must contain points");
      goto end;
    }
  #if DEBUG
    g_debug ("unit shape file contains %i units", nunits);
    g_debug ("bounds: top left lat=%g,lon=%g, bottom right lat=%g,lon=%g",
             maxbound[1], minbound[0], minbound[1], maxbound[0]);
  #endif

  /* Open the unit attribute file. */
  #if DEBUG
    g_debug ("opening unit attribute file");
  #endif
  unit_attribute_file = DBFOpen (unit_shapefile_name, "rb");
  if (unit_attribute_file == NULL)
    {
      g_warning ("could not open unit attribute (.dbf) file");
    }

  /* Get the dimensions of the population file.  In the special case where there is
   * just 1 unit, we want the unit centered, with some space around it.  Also,
   * if the population file is excessively long and thin, pad it with some space so
   * that it won't look silly. */
  if (nunits == 1)
    {
      width = EPSILON;
      height = EPSILON;
      min_x = minbound[0] - EPSILON / 2;
      min_y = minbound[1] - EPSILON / 2;
      ratio1 = 1.0;
    }
  else
    {
      width = maxbound[0] - minbound[0];
      min_x = minbound[0];
      height = maxbound[1] - minbound[1];
      if (height < EPSILON)
        ratio1 = MAX_RATIO + 1; /* force height to be expanded, below */
      else
        {
          min_y = minbound[1];
          ratio1 = width / height;
        }
      /* Constrain the ratio, because excessively long and thin diagrams look
       * silly. */
      if (ratio1 < MIN_RATIO)
        {
          /* Expand the width of the diagram. */
          #if DEBUG
            g_debug ("rectangle too narrow, expanding width");
          #endif
          center = (minbound[0] + maxbound[0]) / 2;
          width = height * MIN_RATIO;
          min_x = center - 0.5 * width;
          ratio1 = MIN_RATIO;
        }
      else if (ratio1 > MAX_RATIO)
        {
          /* Expand the height of the diagram. */
          #if DEBUG
            g_debug ("rectangle too narrow, expanding height");
          #endif
          center = (minbound[1] + maxbound[1]) / 2;
          height = width / MAX_RATIO;
          min_y = center - 0.5 * height;
          ratio1 = MAX_RATIO;
        }
    }
  #if DEBUG
    g_debug ("shapefile bounds = %.2fx%.2f (ratio %.1f)", width, height, ratio1);
  #endif

  /* Create a drawing object.  First, decide on a resolution for it. */
  ratio2 = (double) (MAX_X_SIZE - 2 * IMAGE_BORDER) / (MAX_Y_SIZE - 2 * IMAGE_BORDER);
  #if DEBUG
    g_debug ("max size for output image = %ix%i (ratio %.1f) (%ix%i with borders)",
             MAX_X_SIZE - 2 * IMAGE_BORDER, MAX_Y_SIZE - 2 * IMAGE_BORDER,
             ratio2, MAX_X_SIZE, MAX_Y_SIZE);
  #endif

  if (ratio1 >= ratio2)
    {
      image_x = MAX_X_SIZE - 2 * IMAGE_BORDER;
      image_y = (unsigned int) round (image_x / ratio1);
      #if DEBUG
        g_debug ("output constrained by x=%i, will be %ix%i (%ix%i with borders)",
                 image_x, image_x, image_y, image_x + 2 * IMAGE_BORDER, image_y + 2 * IMAGE_BORDER);
      #endif
    }
  else
    {
      image_y = MAX_Y_SIZE - 2 * IMAGE_BORDER;
      image_x = (unsigned int) round (image_y * ratio1);
      #if DEBUG
        g_debug ("output constrained by y=%i, will be %ix%i (%ix%i with borders)",
                 image_y, image_x, image_y, image_x + 2 * IMAGE_BORDER, image_y + 2 * IMAGE_BORDER);
      #endif
    }
  im = gdImageCreate (image_x + 2 * IMAGE_BORDER, image_y + 2 * IMAGE_BORDER);
  if (im == NULL)
    {
      g_warning ("not enough memory to create %ix%i image",
                 image_x + 2 * IMAGE_BORDER, image_y + 2 * IMAGE_BORDER);
      goto end;
    }
  /* Set the background colour to white. */
  gdImageColorAllocate (im, 255, 255, 255);

  /* Open the zone shape file for reading. */
  if (zone_shapefile_name != NULL)
    {
      #if DEBUG
        g_debug ("opening zone shape file \"%s\"", zone_shapefile_name);
      #endif
      zone_shape_file = SHPOpen (zone_shapefile_name, "rb");
      if (zone_shape_file == NULL)
        {
          g_warning ("could not open zone shape file");
        }
      else
        {
          /* Verify that the zone shape file contains polygons. */
          SHPGetInfo (zone_shape_file, &nzones, &shape_type, minbound, maxbound);
          if (shape_type != SHPT_POLYGON)
            {
              g_warning ("zone shape file must contain polygons");
              SHPClose (zone_shape_file);
              zone_shape_file = NULL;
            }
          else
            {
              #if DEBUG
                g_debug ("zone shape file contains %i zones", nzones);
              #endif
              ;
            }
        }
    }

  /* Draw the zones first so that they will appear behind the units. */
  if (zone_shape_file != NULL)
    draw_zones (zone_shape_file, nzones, im, min_x, width, min_y, height,
                image_x, image_y);
  draw_units (unit_shape_file, unit_attribute_file, nunits, im, min_x, width, min_y, height,
              image_x, image_y);

  /* Write the image to the file. */
  #if DEBUG
    g_debug ("creating image file \"%s\"", image_file_name);
  #endif
  fp = fopen (image_file_name, "wbx"); /* Flawfinder: ignore */
  if (fp == NULL)
    {
      g_warning ("could not open file \"%s\" for writing", image_file_name);
      goto end;
    }
  gdImagePng (im, fp);

end:
  /* Clean up. */
  if (fp != NULL)
    fclose (fp);
  if (zone_shape_file != NULL)
    SHPClose (zone_shape_file);
  if (im != NULL)
    gdImageDestroy (im);
  if (unit_attribute_file != NULL)
    DBFClose (unit_attribute_file);
  if (unit_shape_file != NULL)
    SHPClose (unit_shape_file);

  #if DEBUG
    g_debug ("----- EXIT convert");
  #endif

  return;
}



int
main (int argc, char *argv[])
{
  const char *unit_shapefile_name = NULL;       /* name of the unit shapefile */
  const char *zone_shapefile_name = NULL;       /* name of the zone shapefile */
  char *image_file_name; /* name of the image file to write. */
  char *base_name;
  int verbosity = 0;
  GError *option_error = NULL;
  GOptionContext *context;
  GOptionEntry options[] = {
    { "verbosity", 'V', 0, G_OPTION_ARG_INT, &verbosity, "Message verbosity level (0 = simulation output only, 1 = all debugging output)", NULL },
    { "zones", 'z', 0, G_OPTION_ARG_FILENAME, &zone_shapefile_name, "Zone shape file", NULL },
    { NULL }
  };

  /* Get the command-line options and arguments.  There should be at least one
   * command-line argument, the name of the unit shapefile, and optionally a
   * second argument giving the name of the image file to write. */
  context = g_option_context_new ("");
  g_option_context_add_main_entries (context, options, /* translation = */ NULL);
  if (!g_option_context_parse (context, &argc, &argv, &option_error))
    {
      g_error ("option parsing failed: %s\n", option_error->message);
    }
  if (argc >= 2)
    unit_shapefile_name = argv[1];
  else
    {
      g_error ("Need the name of an ArcView file of units.");
    }

  if (argc >= 3)
    image_file_name = argv[2];
  else
    image_file_name = NULL;
  g_option_context_free (context);

  /* Set the verbosity level. */
  if (verbosity < 1)
    {
      g_log_set_handler (NULL, G_LOG_LEVEL_DEBUG, silent_log_handler, NULL);
    }
  #if DEBUG
    g_debug ("verbosity = %i", verbosity);
  #endif

  if (image_file_name == NULL)
    {
      base_name = g_strndup (unit_shapefile_name, strlen (unit_shapefile_name) - 4);
      image_file_name = g_strdup_printf ("%s.png", base_name);
      g_free (base_name);
      #if DEBUG
        g_debug ("will output to \"%s\"", image_file_name);
      #endif
    }

  convert (unit_shapefile_name, zone_shapefile_name, image_file_name);

  return EXIT_SUCCESS;
}

/* end of file shp2png.c */
