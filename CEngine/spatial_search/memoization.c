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
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "gis.h"

#include "memoization.h"


#define EPSILON			(0.001)


void addToMemoization2 (int id, gpointer user_data);

boolean insertHerd (_IN_OUT_ HerdLocation* psHerdList,
		    _IN_ double x,
		    _IN_ double y,
		    _IN_ uint uiID) {

  boolean ret_val = FALSE;

  if (NULL != psHerdList) {
    psHerdList[uiID].x = x;
    psHerdList[uiID].y = y;
    psHerdList[uiID].uiID = uiID;

    ret_val = TRUE;
  }

  return ret_val;
}




MemoizationTable *initMemoization (double *x, double *y, uint nherds) {

  MemoizationTable *memo;
  uint i;

  memo = g_new (MemoizationTable, 1);
  memo->uiNumHerds = nherds;

  memo->pAllHerds = g_new0 (InProximity *, nherds);
  memo->pUnsortedList = g_new0 (HerdLocation, nherds);

  for (i = 0; i < nherds; i++) {
    insertHerd(memo->pUnsortedList, x[i], y[i], i);
  }

  return memo;
}


InProximity* createNewProxmityList(double dRadius) {
  InProximity* new_dist = NULL;

  new_dist = (InProximity*)malloc(sizeof(InProximity));

  if (NULL != new_dist) {
    new_dist->dRadius = dRadius;
    new_dist->psHerdList = NULL;
    new_dist->psNext = NULL;
  }

  return new_dist;
}

HerdNode* createNewHerdNode(HerdLocation* pHerd) {
  HerdNode* new_node = (HerdNode*)malloc(sizeof(HerdNode));
  new_node->psHerd = pHerd;
  new_node->psNext = NULL;

  return new_node;
}


void deleteHerdList (HerdNode* pHerd) {
  HerdNode* temp_herd;

  while (NULL != pHerd) {
    temp_herd = pHerd;
    pHerd = pHerd->psNext;
    free(temp_herd);
  }
}

void deleteProximityList(InProximity* pDistances) {
  InProximity* temp_dist;

  while (NULL != pDistances) {
    deleteHerdList(pDistances->psHerdList);
    temp_dist = pDistances;
    pDistances = pDistances->psNext;
    free(temp_dist);
  }
}

void deleteMemoization(MemoizationTable *memo) {
  if (memo != NULL)
    {
      uint i;
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


boolean withInRadius(HerdLocation* pX_Herd, HerdLocation* pY_Herd, double dRadius) {
  boolean ret_val = FALSE;
  double distance;

  /* calculate weather the herd is within radius */
  distance = GIS_distance(pX_Herd->x, pX_Herd->y, pY_Herd->x, pY_Herd->y);

  if ((distance - dRadius) <= EPSILON) {
    ret_val = TRUE;
  }

  return ret_val;
}

void processHerd (HerdLocation* pS_Herd, HerdLocation* pT_Herd, 
		     double dRadius, boolean bSureIn, 
		     spatial_search_hit_callback pfCallback, void* pCallbackArgs) {

  if (!bSureIn) {
    if(withInRadius(pS_Herd, pT_Herd, dRadius)) {
      pfCallback(pT_Herd->uiID, pCallbackArgs);      
    }
  }else {
      pfCallback(pT_Herd->uiID, pCallbackArgs);
  }
}


/************************** 10 search with memoization  **************************/

void processHerdList2(HerdNode* pHerdList, spatial_search_hit_callback pfCallback,
		     void* pCallbackArgs) {
  while (NULL != pHerdList) {
    /* call the function which processes the list */
    pfCallback(pHerdList->psHerd->uiID, pCallbackArgs);
    pHerdList = pHerdList->psNext;
  }
}

void splitHerdList2(HerdLocation* pHerd, InProximity* pDistList, double dRadius) {
  HerdNode* src_list = pDistList->psNext->psHerdList;
  HerdNode* next_list = NULL;
  HerdNode* prev_list = NULL;

  pDistList->psHerdList = NULL;
  pDistList->psNext->psHerdList =  NULL;     

  while (NULL != src_list) {
    if (TRUE == withInRadius(pHerd, src_list->psHerd, dRadius)) {
      if (NULL == pDistList->psHerdList) {
	prev_list = src_list;
	pDistList->psHerdList = prev_list;
      }else {
	prev_list->psNext = src_list;
	prev_list = prev_list->psNext;
      }
      src_list = src_list->psNext;
      prev_list->psNext = NULL;

    }else {
      if (NULL == pDistList->psNext->psHerdList) {
	next_list = src_list;
	pDistList->psNext->psHerdList =  src_list;     	
      }else {
	next_list->psNext = src_list;
	next_list = next_list->psNext;	
      }
      src_list = src_list->psNext;
      next_list->psNext = NULL;
    }
  }
}


/**
 * A structure used to hold callback arguments in inMemoization2 below.
 */
typedef struct {
  HerdLocation *pUnsortedList;
  HerdLocation *pS_Herd;
  double dRadius;
  InProximity *pTargetList;
  double dLastRadius;
} addToMemoization2_args_t;



boolean inMemoization2(MemoizationTable *memo,
              spatial_search_t *searcher,
		      HerdLocation* pHerd, InProximity** pSrcHerds,
		      double dRadius, spatial_search_hit_callback pfCallback,
		      void* pCallbackArgs)  {
  InProximity* src_list = *pSrcHerds;
  InProximity* prev_list = NULL;
  InProximity* temp_list = NULL;
  boolean ret_val = FALSE;

  while (NULL != src_list) {
    
    if (fabs(src_list->dRadius - dRadius) <= EPSILON){
      /* process the herds */
      processHerdList2(src_list->psHerdList, pfCallback, pCallbackArgs);
      ret_val = TRUE;
      break;
    }else if (src_list->dRadius > dRadius) {
      /* split list */
      if (NULL == prev_list) {
	temp_list = createNewProxmityList(dRadius);
	temp_list->psNext = src_list;
	*pSrcHerds = temp_list;
      }else{
	temp_list = prev_list;
	temp_list->psNext = createNewProxmityList(dRadius);
	temp_list = temp_list->psNext;
	temp_list->psNext = src_list;
      }
      splitHerdList2(pHerd, temp_list, dRadius);
      processHerdList2(temp_list->psHerdList, pfCallback, pCallbackArgs);
      ret_val = TRUE;
      break;
    }else if (src_list->dRadius < dRadius) {
      /* process the herds */
      processHerdList2(src_list->psHerdList, pfCallback, pCallbackArgs);
    }
    prev_list = src_list;
    src_list = src_list->psNext;
  }

  if (FALSE == ret_val) {		/* create new distance list */
    addToMemoization2_args_t args;

    temp_list = createNewProxmityList(dRadius);
    /* These callback arguments correspond to the arguments to the old function
     * searchInProximity2. */
    args.pUnsortedList = memo->pUnsortedList;
	args.pS_Herd = pHerd;
    args.dRadius = dRadius;
    args.pTargetList = temp_list;
    args.dLastRadius = prev_list->dRadius;
    spatial_search_circle_by_xy (searcher,
                                 pHerd->x, pHerd->y, dRadius,
                                 addToMemoization2, &args);
    processHerdList2(temp_list->psHerdList, pfCallback, pCallbackArgs);
    prev_list->psNext = temp_list;
  }

  return ret_val;
}

/* search in circles and squares with memoization */
boolean
searchWithMemoization (MemoizationTable *memo,
                       spatial_search_t *searcher,
                       uint uiID, double dRadius,
                       spatial_search_hit_callback pfCallback, void* pCallbackArgs)
{
  boolean ret_val = FALSE;
  HerdLocation *herd;

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
    args.dLastRadius = 0,0;
    spatial_search_circle_by_xy (searcher,
                                 herd->x, herd->y, dRadius,
                                 addToMemoization2, &args);

    processHerdList2(memo->pAllHerds[uiID]->psHerdList, 
		     pfCallback, pCallbackArgs);
  }else {
    inMemoization2(memo, searcher, herd, &(memo->pAllHerds[uiID]), dRadius,  
		   pfCallback, pCallbackArgs);
  }

  return ret_val;
}


boolean searchInHerdList2 (InProximity* pSearchList, HerdLocation* pHerd) {
  boolean ret_val = FALSE;
  HerdNode* herd;

  while (NULL != pSearchList) {
    herd = pSearchList->psHerdList;

    while(NULL != herd){
      if (herd->psHerd->uiID == pHerd->uiID) {
	ret_val = TRUE;
	break;
      }
      herd = herd->psNext;
    }

    if (TRUE == ret_val) {
      break;
    }else {
      pSearchList = pSearchList->psNext;
    }
  }

  return ret_val;
}

void addToList2 (InProximity* pTargetList, HerdLocation* pHerd) {
  HerdNode* new_node = createNewHerdNode(pHerd);

  if (NULL != pTargetList->psHerdList) {
    HerdNode* curr_node = pTargetList->psHerdList;
    HerdNode* prev_node = NULL;

    while ((NULL != curr_node->psNext)
	   && (curr_node->psHerd->uiID < pHerd->uiID)) {
      prev_node = curr_node;
      curr_node = curr_node->psNext;
    }

    if (curr_node->psHerd->uiID > pHerd->uiID) {
      if (NULL == prev_node) {
	pTargetList->psHerdList = new_node;
      }else {
	prev_node->psNext = new_node;
      }
      new_node->psNext = curr_node;
    }else {
      curr_node->psNext = new_node;
    }

  }else {
    pTargetList->psHerdList = new_node;
  }

}

void addToHerdList2 (InProximity* pTargetList, InProximity* pSearchList, 
		     HerdLocation* pHerd) {
  if (FALSE == searchInHerdList2 (pSearchList, pHerd)){
    addToList2(pTargetList, pHerd);
  }
}


void addToMemoization2 (int id, gpointer user_data) {
  addToMemoization2_args_t *args;
  HerdLocation *pS_Herd, *pT_Herd;
  double distance;

  args = (addToMemoization2_args_t *) user_data;
  pS_Herd = args->pS_Herd;
  pT_Herd = &(args->pUnsortedList[id]);

  /* calculate weather the herd is within radius */
  distance = GIS_distance(pS_Herd->x, pS_Herd->y, 
				pT_Herd->x, pT_Herd->y);
  
  if ((distance - args->dRadius) <= EPSILON) {
    if ((distance - args->dLastRadius) > EPSILON) {
          addToList2(args->pTargetList, pT_Herd);
    }
  }

  return;
}



