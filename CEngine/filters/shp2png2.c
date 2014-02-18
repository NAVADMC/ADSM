/** @file shp2png2.c
 *
 * A filter that takes an ArcView file of polygons (output from
 * summary_gis_filter) and creates a picture in PNG format to show the value of
 * one of the polygon attributes.
 *
 * Call it as
 *
 * <code>shp2png ARCVIEW-SHP-FILE ATTRNAME MIN-COLOUR MAX-COLOUR [IMAGE-FILE]</code>
 *
 * The variable name is case-insensitive.  If the given attribute name isn't
 * found in the shapefile or it isn't a numeric attribute, the program will
 * use the first numeric attribute in the attribute list.  If there are no
 * numeric attributes, the program will stop.  The min-color and max-color
 * are given as hex RGB color codes, e.g., 000000 for black, FF0000 for bright
 * red, FFFFFF for white.
 *
 * If the image file name is omitted, the image file will have the name of the
 * ArcView shape file, followed by an underscore, followed by the attribute
 * name, and a ".png" extension.
 *
 * @author Neil Harvey <nharve01@uoguelph.ca><br>
 *   School of Computer Science, University of Guelph<br>
 *   Guelph, ON N1G 2W1<br>
 *   CANADA
 * @date December 2005
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
#define IMAGE_BORDER 20
#define MARKER_SIZE 5
#define EPSILON 0.001



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
 * Converts a color in hex notation to 3 decimal values (red, green, blue)
 * each between 0 and 255.
 */
void
str_to_color (const char *hex, int *r, int *g, int *b)
{
  int len;
  int start;
  int i;
  char c;
  int value[6];
  gboolean invalid_chars;

#if DEBUG
  g_debug ("----- ENTER str_to_color");
#endif

  /* Check that the string is either 6 chars long, or 7 with a # character at
   * the beginning. */
  len = strlen (hex);
  if (len != 6 && !(len == 7 && hex[0] == '#'))
    {
      g_warning
        ("string \"%s\" is not 6 characters long (or 7 with a '#' at the start), returning black",
         hex);
      *r = *g = *b = 0;
      goto end;
    }

  if (hex[0] == '#')
    start = 1;
  else
    start = 0;

  /* Check for invalid characters. */
  invalid_chars = FALSE;
  for (i = start; i < len; i++)
    {
      c = hex[i];
      if (c >= '0' && c <= '9')
        {
          value[i - start] = c - '0';
          continue;
        }
      if (c >= 'A' && c <= 'F')
        {
          value[i - start] = c - 'A' + 10;
          continue;
        }
      if (c >= 'a' && c <= 'f')
        {
          value[i - start] = c - 'a' + 10;
          continue;
        }
      invalid_chars = TRUE;
      break;
    }
  if (invalid_chars == TRUE)
    {
      g_warning ("string \"%s\" must contain only 0-9, a-f, or A-F, returning black", hex);
      *r = *g = *b = 0;
      goto end;
    }

  /* Now that the string has passed all those checks, we can turn it into
   * integer R, G, B values. */
  *r = value[0] * 16 + value[1];
  *g = value[2] * 16 + value[3];
  *b = value[4] * 16 + value[5];

end:
  #if DEBUG
    g_debug ("\"%s\" converted to (%i,%i,%i)", hex, *r, *g, *b);
  #endif

  #if DEBUG
    g_debug ("----- ENTER str_to_color");
  #endif

  return;
}



/**
 * Blends one color into another.
 *
 * @param r1 the red value of the first color (0-255).
 * @param g1 the green value of the first color (0-255).
 * @param b1 the blue value of the first color (0-255).
 * @param r2 the red value of the second color (0-255).
 * @param g2 the green value of the second color (0-255).
 * @param b2 the blue value of the second color (0-255).
 * @param amount the amount of blending.  0 yields the first color, 1 yields
 *   the second color, and intermediate values yield a blend.
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



/**
 * Converts a shape object from Shapelib to one or more arrays of gdPoint
 * objects.  Each "part" or sub-polygon of the shape becomes a separate array
 * of gdPoints.
 *
 * @param shape a Shapelib shape object.
 * @return a GPtrArray in which each item is a GArray of gdPoint objects.
 */
GPtrArray *
shape_to_gdpoints (SHPObject * shape)
{
  GPtrArray *parts;
  GArray *part;
  int nparts, npoints;
  int i, j, start, end;
#if DEBUG
  GString *s;
#endif

#if DEBUG
  g_debug ("----- ENTER shape_to_gdpoints");
#endif

  parts = g_ptr_array_new ();
  if (shape == NULL)
    {
      g_warning ("shape is null, will return zero-length array of gdPoints");
      goto end;
    }

  nparts = shape->nParts;
  if (nparts == 0)
    {
      g_warning ("shape has 0 parts, will return zero-length array of gdPoints");
      goto end;
    }

  #if DEBUG
    g_debug ("shape has %i parts", nparts);
  #endif

  for (i = 0; i < nparts; i++)
    {
      /* Allocate the points for the part. */
      start = shape->panPartStart[i];
      if (i < (nparts - 1))
        end = shape->panPartStart[i + 1];
      else
        end = shape->nVertices;
      npoints = end - start;
      part = g_array_sized_new (FALSE, FALSE, sizeof (gdPoint), npoints);
      g_array_set_size (part, npoints);
      g_ptr_array_add (parts, part);

      /* Copy the vertices. */
      #if DEBUG
        s = g_string_new (NULL);
      #endif
      for (j = start; j < end; j++)
        {
          g_array_index (part, gdPoint, j - start).x = (int) (shape->padfX[j]);
          g_array_index (part, gdPoint, j - start).y = (int) (shape->padfY[j]);
          #if DEBUG
            if (j > start)
              g_string_append_c (s, ',');
            g_string_append_printf (s, "(%i,%i)",
                                    g_array_index (part, gdPoint, j - start).x,
                                    g_array_index (part, gdPoint, j - start).y);
          #endif
        }                       /* end of loop over points */
      #if DEBUG
        g_debug ("part %i (%i points) = %s", i + 1, npoints, s->str);
        g_string_free (s, TRUE);
      #endif
    }                           /* end of loop over parts */

end:
#if DEBUG
  g_debug ("----- EXIT shape_to_gdpoints");
#endif

  return parts;
}



void
convert (const char *shape_file_name, const char *attribute_name,
         double min_attribute_value, double max_attribute_value,
         const char *min_color_hex, const char *max_color_hex, const char *image_file_name)
{
  SHPHandle shape_file = NULL;
  SHPObject *shape = NULL;
  int nshapes;
  int shape_type;
  int shape_index;
  double minbound[4], maxbound[4];
  DBFHandle attribute_file = NULL;
  DBFFieldType field_type;
  int nfields;
  int field_index;
  gboolean numeric_field_found;
  char field_name[12]; /**< buffer to hold a field name; maximum field name
    length in ArcView DBF files is 11 + terminating null char. */
  double field_value;
  double min_attr_value, max_attr_value;
  double shape_w, shape_h;
  double ratio1, ratio2;
  unsigned int image_x, image_y;
  int i; /**< loop counter */
  gdImagePtr im = NULL;
  /* Colourss */
  int white, black;
  int min_color_r, min_color_g, min_color_b;
  int max_color_r, max_color_g, max_color_b;
  int r, g, b, tmp_color;
  GPtrArray *parts;
  int part_index;
  GArray *part;
  FILE *fp = NULL;

#if DEBUG
  g_debug ("----- ENTER convert");
#endif

  /* Open the shape and DBF (attribute) files for reading. */
  #if DEBUG
    g_debug ("opening shape file \"%s\"", shape_file_name);
  #endif
  shape_file = SHPOpen (shape_file_name, "rb");
  if (shape_file == NULL)
    {
      g_warning ("could not open shape file");
      goto end;
    }

  /* Verify that the shape file contains polygons. */
  SHPGetInfo (shape_file, &nshapes, &shape_type, minbound, maxbound);
  if (shape_type != SHPT_POLYGON)
    {
      g_warning ("shape file must contain polygons");
      goto end;
    }
  if (nshapes == 0)
    {
      g_warning ("shape file contains no shapes");
      goto end;
    }

  /* Open the matching attribute file. */
  #if DEBUG
    g_debug ("opening corresponding attribute file");
  #endif
  attribute_file = DBFOpen (shape_file_name, "rb");
  if (attribute_file == NULL)
    {
      g_warning ("could not open attribute (.dbf) file");
      goto end;
    }

  /* Get the index of the desired field. */
  field_index = DBFGetFieldIndex (attribute_file, attribute_name);
  if (field_index == -1)
    {
      g_warning ("there is no attribute named \"%s\"", attribute_name);
    }
  else
    {
      /* Check that the field is of type integer or double. */
      field_type = DBFGetFieldInfo (attribute_file, field_index, field_name, NULL, NULL);
      if (field_type != FTInteger && field_type != FTDouble)
        {
          g_warning ("attribute \"%s\" is not of numeric type", attribute_name);
          field_index = -1;
        }
    }
  /* If we couldn't find the requested field, or it wasn't of numeric type, try
   * to find a suitable numeric field. */
  if (field_index == -1)
    {
      nfields = DBFGetFieldCount (attribute_file);
      numeric_field_found = FALSE;
      for (field_index = 0; field_index < nfields; field_index++)
        {
          field_type = DBFGetFieldInfo (attribute_file, field_index, field_name, NULL, NULL);
          if (field_type == FTInteger || field_type == FTDouble)
            {
              numeric_field_found = TRUE;
              break;
            }
        }
      if (!numeric_field_found)
        {
          g_error ("could not find any numeric fields to color the plot by");
        }
      g_warning ("will use numeric field \"%s\" to color the plot", field_name);
    }

  /* If the user didn't pass in minimum and maximum values for the attribute,
   * find them. */
  if (max_attribute_value > min_attribute_value)
    {
      min_attr_value = min_attribute_value;
      max_attr_value = max_attribute_value;
    }
  else
    {
      #if DEBUG
        g_debug ("finding minimum and maximum values for attribute \"%s\"", field_name);
      #endif
      if (field_type == FTInteger)
        field_value = DBFReadIntegerAttribute (attribute_file, 0, field_index);
      else
        field_value = DBFReadDoubleAttribute (attribute_file, 0, field_index);
      min_attr_value = max_attr_value = field_value;
      for (shape_index = 1; shape_index < nshapes; shape_index++)
        {
          if (field_type == FTInteger)
            field_value = DBFReadIntegerAttribute (attribute_file, shape_index, field_index);
          else
            field_value = DBFReadDoubleAttribute (attribute_file, shape_index, field_index);
          if (field_value < min_attr_value)
            min_attr_value = field_value;
          else if (field_value > max_attr_value)
            max_attr_value = field_value;
        }
    }
  #if DEBUG
    g_debug ("attribute \"%s\" varies between %.2f and %.2f",
             field_name, min_attr_value, max_attr_value);
  #endif
  if (max_attr_value - min_attr_value < EPSILON)
    {
      g_warning ("all values for \"%s\" are the same, all cells will be minimum color",
                 field_name);
      max_attr_value = min_attr_value + 1;
    }

  str_to_color (min_color_hex, &min_color_r, &min_color_g, &min_color_b);
  str_to_color (max_color_hex, &max_color_r, &max_color_g, &max_color_b);

  /* Create a drawing object.  First, decide on a size for it. */
  ratio1 = (double) (MAX_X_SIZE - 2 * IMAGE_BORDER) / (MAX_Y_SIZE - 2 * IMAGE_BORDER);
  #if DEBUG
    g_debug ("max size for output image = %ix%i (ratio %.1f) (%ix%i with borders)",
             MAX_X_SIZE - 2 * IMAGE_BORDER, MAX_Y_SIZE - 2 * IMAGE_BORDER,
             ratio1, MAX_X_SIZE, MAX_Y_SIZE);
  #endif
  shape_w = maxbound[0] - minbound[0];
  shape_h = maxbound[1] - minbound[1];
  ratio2 = shape_w / shape_h;
  #if DEBUG
    g_debug ("shapefile bounds = %.2fx%.2f (ratio %.1f)", shape_w, shape_h, ratio2);
  #endif
  if (ratio2 >= ratio1)
    {
      image_x = MAX_X_SIZE - 2 * IMAGE_BORDER;
      image_y = (unsigned int) round (image_x / ratio2);
      #if DEBUG
        g_debug ("output constrained by x=%i, will be %ix%i (%ix%i with borders)",
                 image_x, image_x, image_y, image_x + 2 * IMAGE_BORDER, image_y + 2 * IMAGE_BORDER);
      #endif
    }
  else
    {
      image_y = MAX_Y_SIZE - 2 * IMAGE_BORDER;
      image_x = (unsigned int) round (image_y * ratio2);
      #if DEBUG
        g_debug ("output constrained by y=%i, will be %ix%i (%ix%i with borders)",
                 image_y, image_x, image_y, image_x + 2 * IMAGE_BORDER, image_y + 2 * IMAGE_BORDER);
      #endif
    }
  im = gdImageCreateTrueColor (image_x + 2 * IMAGE_BORDER, image_y + 2 * IMAGE_BORDER);
  if (im == NULL)
    {
      g_warning ("not enough memory to create %ix%i image",
                 image_x + 2 * IMAGE_BORDER, image_y + 2 * IMAGE_BORDER);
      goto end;
    }
  /* Make the background white. */
  white = gdImageColorAllocate (im, 255, 255, 255);
  gdImageFilledRectangle (im, 0, 0, im->sx - 1, im->sy - 1, white);

  /* Allocate colors. */
  black = gdImageColorAllocate (im, 0, 0, 0);

  /* Draw each polygon, colored according to the attribute value. */
  #if DEBUG
    g_debug ("drawing polygons");
  #endif
  for (shape_index = 0; shape_index < nshapes; shape_index++)
    {
      /* Get the shape, which may have multiple parts. */
      shape = SHPReadObject (shape_file, shape_index);

      /* Convert the lat/lon numbers to image (pixel) coordinates.  We need to
       * do this before converting to gdPoint arrays (the polygon object used
       * by the GD drawing library) because gdPoints contain integers, not
       * doubles, and converting lat/lon values to integers will lose too much
       * precision.
       *
       * Altering the padfX and padfY arrays inside a Shapelib shape object
       * will mess up the bounds stored in the shape object, but we don't care
       * because we're not going to use them.
       *
       * Remember that latitude goes up, and pixel y-coordinates go down!
       */
      for (i = shape->panPartStart[0]; i < shape->nVertices; i++)
        {
          shape->padfX[i] =
            round ((shape->padfX[i] - minbound[0]) / shape_w * image_x + IMAGE_BORDER);
          shape->padfY[i] =
            round (IMAGE_BORDER + image_y - ((shape->padfY[i] - minbound[1]) / shape_h * image_y));
        }

      /* Convert the Shapelib shape object into an array of arrays of gdPoint
       * objects, then discard the shape object. */
      parts = shape_to_gdpoints (shape);
      SHPDestroyObject (shape);

      /* Calculate the fill color. */
      if (field_type == FTInteger)
        field_value = DBFReadIntegerAttribute (attribute_file, shape_index, field_index);
      else
        field_value = DBFReadDoubleAttribute (attribute_file, shape_index, field_index);
      blend (min_color_r, min_color_g, min_color_b,
             max_color_r, max_color_g, max_color_b,
             (field_value - min_attr_value) / (max_attr_value - min_attr_value), &r, &g, &b);
      tmp_color = gdImageColorAllocate (im, r, g, b);

      /* Draw the polygons, outlined in black. */
      for (part_index = 0; part_index < parts->len; part_index++)
        {
          part = (GArray *) g_ptr_array_index (parts, part_index);
          gdImageFilledPolygon (im, &(g_array_index (part, gdPoint, 0)), part->len, tmp_color);
          gdImagePolygon (im, &(g_array_index (part, gdPoint, 0)), part->len, black);
          g_array_free (part, TRUE);
        }
      g_ptr_array_free (parts, TRUE);

    }                           /* end of loop over shapes */

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
  if (im != NULL)
    gdImageDestroy (im);
  if (attribute_file != NULL)
    DBFClose (attribute_file);
  if (shape_file != NULL)
    SHPClose (shape_file);

#if DEBUG
  g_debug ("----- EXIT convert");
#endif

  return;
}



int
main (int argc, char *argv[])
{
  const char *arcview_file_name = NULL; /**< name of the ArcView shapefile */
  const char *attribute_name; /**< name of the attribute in the ArcView
    DBF file */
  double min_attribute_value = 0;
  double max_attribute_value = -1;
  const char *min_color; /**< hex RGB representation of the color to
    assign to the minimum attribute value */
  const char *max_color; /**< hex RGB representation of the color to
    assign to the maximum attribute value */
  char *image_file_name; /**< name of the image file to write */
  char *arcview_base_name;
  int verbosity = 0;
  GError *option_error = NULL;
  GOptionContext *context;
  GOptionEntry options[] = {
    { "verbosity", 'V', 0, G_OPTION_ARG_INT, &verbosity, "Message verbosity level (0 = simulation output only, 1 = all debugging output)", NULL },
    { "min-value", 0, 0, G_OPTION_ARG_DOUBLE, &min_attribute_value, "override minimum attribute value", NULL },
    { "max-value", 0, 0, G_OPTION_ARG_DOUBLE, &max_attribute_value, "override maximum attribute value", NULL },
    { NULL }
  };

  /* Get the command-line options and arguments.  There should be at least four
   * command-line arguments, the name of the ArcView shapefile, the name of the
   * attribute to read, a color for the minimum attribute value, a color for
   * the maximum attribute value, and optionally a fifth argument giving the
   * name of the image file to write. */
  context = g_option_context_new ("");
  g_option_context_add_main_entries (context, options, /* translation = */ NULL);
  if (!g_option_context_parse (context, &argc, &argv, &option_error))
    {
      g_error ("option parsing failed: %s\n", option_error->message);
    }

  /* Set the verbosity level. */
  if (verbosity < 1)
    {
      g_log_set_handler (NULL, G_LOG_LEVEL_DEBUG, silent_log_handler, NULL);
    }
  #if DEBUG
    g_debug ("verbosity = %i", verbosity);
  #endif

  if (argc >= 2)
    arcview_file_name = argv[1];
  else
    {
      g_error ("Need the name of an ArcView shapefile.");
    }

  if (argc >= 3)
    {
      attribute_name = argv[2];
      #if DEBUG
        g_debug ("attribute name = \"%s\"", attribute_name);
      #endif
    }
  else
    {
      attribute_name = NULL;
      g_warning
        ("No attribute name supplied, will use the first numeric attribute found in the ArcView DBF file.");
    }

  if (argc >= 4)
    min_color = argv[3];
  else
    {
      g_warning ("No minimum color given, will use white.");
      min_color = "FFFFFF";
    }
  #if DEBUG
    g_debug ("color for minimum value = #%s", min_color);
  #endif

  if (argc >= 5)
    max_color = argv[4];
  else
    {
      g_warning ("No maximum color given, will use black.");
      max_color = "000000";
    }
  #if DEBUG
    g_debug ("color for maximum value = #%s", max_color);
  #endif

  if (argc >= 6)
    {
      image_file_name = argv[5];
      #if DEBUG
        g_debug ("output file name = \"%s\"", image_file_name);
      #endif
    }
  else
    {
      arcview_base_name = g_strndup (arcview_file_name, strlen (arcview_file_name) - 4);
      image_file_name = g_strdup_printf ("%s_%s.png", arcview_base_name, attribute_name);
      g_free (arcview_base_name);
      #if DEBUG
        g_debug ("No output file name given, will use \"%s\"", image_file_name);
      #endif
    }

  g_option_context_free (context);

  convert (arcview_file_name, attribute_name, min_attribute_value,
           max_attribute_value, min_color, max_color, image_file_name);

  return EXIT_SUCCESS;
}

/* end of file shp2png2.c */
