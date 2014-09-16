/**
 * Changes to files provided by V. Basupalli on Mar 22 2010:
 *
 * - Removed dependency on ADSM unit.h. Now just stores location associated
 *   with an integer ID.
 * - Wrapped formerly global variables in a struct named MemoizationTable.
 * - Removed code for converting between lat-long and x-y.  Now works entirely 
 *   in x-y.
 * - Removed Circles-&-Squares code.  The code now calls on an underlying
 *   spatial_search_t object, which may use the Circles-&-Squares algorithm or
 *   something else.
 * - addToList2 no longer keeps the list in sorted order.
 */

#if HAVE_CONFIG_H
#  include <config.h>
#endif

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "gis.h"

#include "memoization.h"


gboolean addToMemoization2 (int id, gpointer user_data);

gboolean insertHerd (_IN_OUT_ Location* psHerdList,
		    _IN_ double x,
		    _IN_ double y,
		    _IN_ guint uiID) {

  gboolean ret_val = FALSE;

  if (NULL != psHerdList) {
    psHerdList[uiID].x = x;
    psHerdList[uiID].y = y;
    psHerdList[uiID].uiID = uiID;

    ret_val = TRUE;
  }

  return ret_val;
}




MemoizationTable *initMemoization (double *x, double *y, guint nherds) {

  MemoizationTable *memo;
  guint i;

  memo = g_new (MemoizationTable, 1);
  memo->uiNumHerds = nherds;

  memo->pAllHerds = g_new0 (InProximity *, nherds);
  memo->pUnsortedList = g_new0 (Location, nherds);

  for (i = 0; i < nherds; i++) {
    insertHerd(memo->pUnsortedList, x[i], y[i], i);
  }

  return memo;
}


InProximity* createNewProxmityList(double dRadius) {
  InProximity* new_dist = NULL;

  new_dist = g_new (InProximity, 1);
  new_dist->dRadius = dRadius;
  new_dist->locations =
    g_array_new (/* zero_terminated = */ FALSE,
                 /* clear = */ FALSE,
                 sizeof(HerdNode));
  new_dist->is_sorted = FALSE;

  return new_dist;
}

void deleteProximityList(InProximity* pDistances) {
  if (pDistances != NULL) {
    g_array_free (pDistances->locations, /* free_segment = */ TRUE);
    g_free(pDistances);
  }
}

void deleteMemoization(MemoizationTable *memo) {
  #if DEBUG
    GString *s;
  #endif

  if (memo != NULL)
    {
      guint i;
      
      #if DEBUG
        g_debug ("Memoization table final state:");
        s = g_string_new (NULL);
      #endif
      for (i = 0; i < memo->uiNumHerds; i++) {
        if (NULL != memo->pAllHerds[i]) {
          #if DEBUG
            guint n, j;
            g_string_printf (s, "unit with index %u", i);
            if (memo->pAllHerds[i]->is_sorted == FALSE)
              {
                g_string_append_printf (s, " (unsorted)");
              }
            g_string_append_printf (s, ": ");
            n = memo->pAllHerds[i]->locations->len;
            for (j = 0; j < n; j++)
              {
                HerdNode *node;
                node = &g_array_index (memo->pAllHerds[i]->locations, HerdNode, j);
                if (j > 0)
                  g_string_append_c (s, ',');
                g_string_append_printf (s, "u%u=%gkm", node->uiID, node->distance);
              }
            g_debug ("%s", s->str);
          #endif
          deleteProximityList(memo->pAllHerds[i]);
        }
      }
      g_free (memo->pAllHerds);
      g_free (memo);
      #if DEBUG
        g_string_free (s, TRUE);
      #endif
    }
  return;
}


/************************** 10 search with memoization  **************************/

/**
 * Call the given callback function for each location in the list. Optionally,
 * stop past a given distance.
 *
 * @param locations a GArray of HerdNode structs.
 * @param upToDistance call the callback function for locations up to and
 *   including this distance. Use -1 to indicate no maximum distance.
 */
void
processHerdList2 (GArray *locations, double upToDistance,
                  spatial_search_hit_callback pfCallback,
		          void* pCallbackArgs)
{
  guint n, i;
  HerdNode *location;

  n = locations->len;
  if (upToDistance < 0)
    {
      /* Process the whole list. */
      for (i = 0; i < n; i++)
        {
          location = &g_array_index (locations, HerdNode, i);
          pfCallback(location->uiID, pCallbackArgs);
        }
    }
  else
    {
      /* Process the list just up to and including upToDistance. */
      for (i = 0; i < n; i++)
        {
          location = &g_array_index (locations, HerdNode, i);
          if (location->distance <= upToDistance)
            pfCallback(location->uiID, pCallbackArgs);
          else
            break;
        }      
    }
  return;
}



/**
 * Comparison function for sorting the list of HerdNode objects in an
 * inProximity object.
 */
static
int compare_distance (const void *a, const void *b)
{
  double distance_a, distance_b;
  
  distance_a = ((HerdNode *)a)->distance;
  distance_b = ((HerdNode *)b)->distance;
  if (distance_a > distance_b)
    return 1;
  else if (distance_b > distance_a)
    return -1;
  else
    return 0;  
}



/**
 * A structure used to hold callback arguments in inMemoization2 below.
 */
typedef struct {
  Location *pUnsortedList;
  Location *pS_Herd;
  double dRadius;
  InProximity *pTargetList;
  double dLastRadius;
} addToMemoization2_args_t;



gboolean inMemoization2(MemoizationTable *memo,
              spatial_search_t *searcher,
		      Location* pHerd, InProximity* pSrcHerds,
		      double dRadius, spatial_search_hit_callback pfCallback,
		      void* pCallbackArgs)  {
  gboolean ret_val = FALSE;

  /* If the requested radius is smaller than the cached search circle, make
   * sure the cached list is sorted, then return all the locations up to and
   * including the requested radius. */
  if (dRadius < pSrcHerds->dRadius)
    {
      if (pSrcHerds->is_sorted == FALSE)
        {
          qsort (pSrcHerds->locations->data, pSrcHerds->locations->len,
                 sizeof(HerdNode), compare_distance);
          pSrcHerds->is_sorted = TRUE;
        }
      processHerdList2(pSrcHerds->locations, dRadius, pfCallback, pCallbackArgs);      
    }
  else if (dRadius > pSrcHerds->dRadius)
    {
      /* The requested radius is greater than the cached search circle. Do a
       * search to get the additional locations outside the cached search
       * circle, add those to the cache, then return all locations from the
       * cache. */
      addToMemoization2_args_t args;
      guint old_len;
      guint new_len;

      args.pUnsortedList = memo->pUnsortedList;
      args.pS_Herd = pHerd;
      args.dRadius = dRadius;
      args.pTargetList = pSrcHerds;
      args.dLastRadius = pSrcHerds->dRadius;
      old_len = pSrcHerds->locations->len;
      spatial_search_circle_by_xy (searcher,
                                   pHerd->x, pHerd->y, dRadius,
                                   addToMemoization2, &args);
      /* If the previous cached locations were sorted, we should sort the new
       * ones we just added to the end, so that the is_sorted property remains
       * TRUE. */
      new_len = pSrcHerds->locations->len;
      if (pSrcHerds->is_sorted && new_len > old_len)
        {
          qsort (pSrcHerds->locations->data + old_len * sizeof(HerdNode),
                 new_len - old_len,
                 sizeof(HerdNode), compare_distance);
        }      
      pSrcHerds->dRadius = dRadius;
      processHerdList2(pSrcHerds->locations, -1, pfCallback, pCallbackArgs);
    }
  else
    {
      /* The requested radius is exactly the same as the cached search circle.
       * Return all locations from the cache. It doesn't matter whether the
       * cache is sorted or not. */
      processHerdList2(pSrcHerds->locations, -1, pfCallback, pCallbackArgs);      
    }

  return ret_val;
}

/* search with memoization */
void
searchWithMemoization (MemoizationTable *memo,
                       spatial_search_t *searcher,
                       guint uiID, double dRadius,
                       spatial_search_hit_callback pfCallback, void* pCallbackArgs)
{
  Location *herd;

  herd = &(memo->pUnsortedList[uiID]);
  pfCallback(uiID, pCallbackArgs);

  if (NULL == memo->pAllHerds[uiID])
  {
    /* In the original implementation, this function called searchInProximity2,
     * which in turn called addToMemoization2 for all herds that it found. Here
     * we are replacing searchInProximity2 by an arbitrary spatial_search_t
     * object, which must also call addToMemoization2 for all herds that it
     * finds. */
    addToMemoization2_args_t args;

    memo->pAllHerds[uiID] = createNewProxmityList(dRadius);

    /* These callback arguments correspond to the arguments to the old function
     * searchInProximity2. */
    args.pUnsortedList = memo->pUnsortedList;
	args.pS_Herd = herd;
    args.dRadius = dRadius;
    args.pTargetList = memo->pAllHerds[uiID];
    args.dLastRadius = -1;
    spatial_search_circle_by_xy (searcher,
                                 herd->x, herd->y, dRadius,
                                 addToMemoization2, &args);

    processHerdList2(memo->pAllHerds[uiID]->locations, -1, 
		     pfCallback, pCallbackArgs);
  }else {
    inMemoization2(memo, searcher, herd, memo->pAllHerds[uiID], dRadius,  
		   pfCallback, pCallbackArgs);
  }

  return;
}



/**
 * Binary search a sorted GArray. Based on the glibc bsearch code, but returns
 * the index of the location where the search stopped. The caller must check
 * whether the element at that index contains the exact value searched for. */
size_t
g_array_bsearch (const void *key, GArray *arr, size_t width,
                 int (*compar) (const void *, const void *))
{
  size_t l, u, mid;
  gchar *base;
  const void *p;
  int comparison;

  l = 0;
  u = arr->len;
  base = arr->data;
  while (l < u)
    {
      mid = l + (u - l) / 2; /* integer division */
      p = base + mid * width;
      comparison = (*compar) (key, p);
      if (comparison < 0)
        u = mid;
      else if (comparison > 0)
        l = mid + 1;
      else
        return mid;
    }
  return l;
}



/* search with memoization */
void
searchClosestToDistanceWithMemoization (MemoizationTable *memo,
                                        spatial_search_t *searcher,
                                        guint uiID, double desired_distance,
                                        spatial_search_hit_callback pfCallback,
                                        void* pCallbackArgs)
{
  Location *herd;
  double desired_distance_x2;
  InProximity *proximity_list;
  guint low, high;
  gboolean keep_going, no_more_low, no_more_high;
  HerdNode key;

  #if DEBUG
    g_debug ("----- ENTER searchClosestToDistanceWithMemoization");
  #endif

  herd = &(memo->pUnsortedList[uiID]);
  desired_distance_x2 = 2.0 * desired_distance;

  proximity_list = memo->pAllHerds[uiID];
  if (proximity_list == NULL)
    {
      /* Create a new proximity list around the point. */
      addToMemoization2_args_t args;

      #if DEBUG
        g_debug ("creating a new proximity list around location ID %u", uiID);
      #endif
      memo->pAllHerds[uiID] = proximity_list = createNewProxmityList(desired_distance_x2);

      args.pUnsortedList = memo->pUnsortedList;
      args.pS_Herd = herd;
      args.dRadius = desired_distance_x2;
      args.pTargetList = proximity_list;
      args.dLastRadius = -1;
      spatial_search_circle_by_xy (searcher,
                                   herd->x, herd->y, desired_distance_x2,
                                   addToMemoization2, &args);
      #if DEBUG
        g_debug ("new proximity list contains %u locations",
                 proximity_list->locations->len);
      #endif
    }
  else if (proximity_list->dRadius < desired_distance_x2)
    {
      /* Expand the existing proximity list around the point. */
      addToMemoization2_args_t args;
      guint old_len;
      guint new_len;

      args.pUnsortedList = memo->pUnsortedList;
      args.pS_Herd = herd;
      args.dRadius = desired_distance_x2;
      args.pTargetList = proximity_list;
      args.dLastRadius = proximity_list->dRadius;
      old_len = proximity_list->locations->len;
      spatial_search_circle_by_xy (searcher,
                                   herd->x, herd->y, desired_distance_x2,
                                   addToMemoization2, &args);
      /* If the previous cached locations were sorted, we should sort the new
       * ones we just added to the end, so that the is_sorted property remains
       * TRUE. */
      new_len = proximity_list->locations->len;
      if (proximity_list->is_sorted && new_len > old_len)
        {
          qsort (proximity_list->locations->data + old_len * sizeof(HerdNode),
                 new_len - old_len,
                 sizeof(HerdNode), compare_distance);
        }      
      proximity_list->dRadius = desired_distance_x2;
    }

  /* Make sure the list is sorted. */
  if (proximity_list->is_sorted == FALSE)
    {
      qsort (proximity_list->locations->data, proximity_list->locations->len,
             sizeof(HerdNode), compare_distance);
      proximity_list->is_sorted = TRUE;
    }

  #if DEBUG
  {
    /* Verify that the list is sorted. */
    HerdNode *curr, *prev;
    guint i;
    if (proximity_list->locations->len > 1)
      {
        for (i = 1; i < proximity_list->locations->len; i++)
          {
            curr = &g_array_index (proximity_list->locations, HerdNode, i);
            prev = &g_array_index (proximity_list->locations, HerdNode, i-1);
            g_assert (prev->distance <= curr->distance);
          }
      }
  } 
  #endif

  if (proximity_list->locations->len >= 1)
    {
      /* Search for the place in the list where a point exactly the given distance
       * from the starting point would be. */
      key.uiID = 0;
      key.distance = desired_distance;
      high = g_array_bsearch (&key, proximity_list->locations,
                             sizeof(HerdNode), compare_distance);
      #if DEBUG
        g_debug ("binary search returns index %u (distance %g)",
                 high,
                 g_array_index (proximity_list->locations, HerdNode, high).distance); 
      #endif
      /* Now "high" is the index at which there is a point exactly the given
       * distance from the starting point, or a greater distance from the starting
       * point. Or, high may be one higher than the highest index of any point in
       * the list. */
      no_more_high = (high == proximity_list->locations->len);
      if (high > 0)
        {
          low = high - 1;
          no_more_low = FALSE;
        }
      else
        no_more_low = TRUE;

      keep_going = TRUE;    
      while (keep_going && !(no_more_low && no_more_high))
        {
          if (no_more_high)
            {
              HerdNode *location = &g_array_index (proximity_list->locations, HerdNode, low);
              keep_going = pfCallback(location->uiID, pCallbackArgs);
              if (low == 0)
                no_more_low = TRUE;
              else
                low--;
            }
          else if (no_more_low)
            {
              HerdNode *location = &g_array_index (proximity_list->locations, HerdNode, high);
              keep_going = pfCallback(location->uiID, pCallbackArgs);
              high++;
              if (high == proximity_list->locations->len)
                no_more_high = TRUE;
            }      
          else
            {
              HerdNode *location_low, *location_high;
              double dlow, dhigh;
              location_low = &g_array_index (proximity_list->locations, HerdNode, low);
              location_high = &g_array_index (proximity_list->locations, HerdNode, high);
              dlow = fabs(desired_distance - location_low->distance);
              dhigh = fabs(desired_distance - location_high->distance);
              if (dlow < dhigh)
                {
                  keep_going = pfCallback(location_low->uiID, pCallbackArgs);
                  if (low == 0)
                    no_more_low = TRUE;
                  else
                    low--;
                }
              else
                {
                  keep_going = pfCallback(location_high->uiID, pCallbackArgs);
                  high++;
                  if (high == proximity_list->locations->len)
                    no_more_high = TRUE;
                }
            }
          #if DEBUG
            g_debug ("return value from callback indicates %s",
                     keep_going ? "keep going" : "stop"); 
          #endif
        }
    } /* end of if proximity list not empty */
    
  #if DEBUG
    g_debug ("----- EXIT searchClosestToDistanceWithMemoization");
  #endif

  return;
}


gboolean addToMemoization2 (int id, gpointer user_data) {
  addToMemoization2_args_t *args;
  Location *pS_Herd, *pT_Herd;
  double distance;

  args = (addToMemoization2_args_t *) user_data;
  pS_Herd = args->pS_Herd;
  pT_Herd = &(args->pUnsortedList[id]);

  if (pS_Herd != pT_Herd)
    {
      /* calculate weather the herd is within radius */
      distance = GIS_distance(pS_Herd->x, pS_Herd->y, 
	    			pT_Herd->x, pT_Herd->y);
  
      if (distance <= args->dRadius
          && distance > args->dLastRadius)
        {
          /* Append to the list. */
          HerdNode new_node;
          new_node.uiID = pT_Herd->uiID;
          new_node.distance = distance;
          g_array_append_val (args->pTargetList->locations, new_node);
        }
    }

  return TRUE; /* A return value of FALSE would stop the spatial search early,
    which we don't want to do. */
}



