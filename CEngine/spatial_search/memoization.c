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
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "gis.h"

#include "memoization.h"
#include "timsort.h"


void addToMemoization2 (int id, gpointer user_data);

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
  if (memo != NULL)
    {
      guint i;
      for (i = 0; i < memo->uiNumHerds; i++) {
        if (NULL != memo->pAllHerds[i]) {
          deleteProximityList(memo->pAllHerds[i]);
        }
      }
      g_free (memo->pAllHerds);
      g_free (memo);
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
int compare_node (const void *a, const void *b)
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
          timsort (pSrcHerds->locations->data, pSrcHerds->locations->len,
                   sizeof(HerdNode), compare_node);
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
          timsort (pSrcHerds->locations->data + old_len * sizeof(HerdNode),
                   new_len - old_len,
                   sizeof(HerdNode), compare_node);
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

/* search in circles and squares with memoization */
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


void addToMemoization2 (int id, gpointer user_data) {
  addToMemoization2_args_t *args;
  Location *pS_Herd, *pT_Herd;
  double distance;

  args = (addToMemoization2_args_t *) user_data;
  pS_Herd = args->pS_Herd;
  pT_Herd = &(args->pUnsortedList[id]);

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

  return;
}



