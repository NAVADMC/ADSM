
#ifndef _MEMOIZATION_H_
#define _MEMOIZATION_H_

#include "spatial_search.h"

#define _IN_
#define _IN_OUT_
#define _OUT_


typedef struct Location Location;

/* location information */

struct Location {
	guint uiID;
	double x;
	double y;
};

typedef struct HerdNode HerdNode;
struct HerdNode {
	guint uiID;
	double distance;
	HerdNode* psNext;
};

typedef struct InProximity InProximity;
struct InProximity {
	double dRadius;
	HerdNode* psHerdList;
	InProximity* psNext;
};

typedef struct {
  guint uiNumHerds;
  Location *pUnsortedList;
  InProximity  **pAllHerds;
} MemoizationTable;

/************************** memoization functions ***********************************/


/*
   Description : This function initializes the memoization table and also 
                  creates sorted lists for circles and squares algorithm.
   Parameters  : Locations

   Usage :     : should be called before any calls are made to "searchWithMemoization" 
                  or "serchWithCirclesAndSquare, 
                  typically after herd list is created in main function "run_sim_main"  
*/
MemoizationTable *initMemoization(double *x, double *y, guint n);

/*
   Description  : search in circles and squares with memoization
   Parameters  : id of the herd for which "herds in proximity is calculated", 
                   "Radius" with which herds are to be found.
		   callback function to be called for a herd in given proximity (same as RTree argument)
		   arguments for callback function
 */
void searchWithMemoization (MemoizationTable *, spatial_search_t *,
                            guint uiID, double dRadius,
                            spatial_search_hit_callback pfCallback, void* pCallbackArgs);

void deleteMemoization (MemoizationTable *);

#endif /* _MEMOIZATION_H_ */
