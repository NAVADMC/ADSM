
#ifndef _MEMOIZATION_H_
#define _MEMOIZATION_H_

#include "spatial_search.h"

#define _IN_
#define _IN_OUT_
#define _OUT_


#ifndef TRUE
#define TRUE           (1)
#endif

#ifndef FALSE
#define FALSE          (0)
#endif


typedef unsigned int 	uint;
typedef unsigned short 	ushort;
typedef unsigned long 	ulong;
typedef uint 	boolean;


typedef struct Location Location;

/* location information */

struct Location {
	uint uiID;
	double x;
	double y;
};

typedef struct HerdNode HerdNode;
struct HerdNode {
	Location* psHerd;
	HerdNode* psNext;
};

typedef struct InProximity InProximity;
struct InProximity {
	double dRadius;
	HerdNode* psHerdList;
	InProximity* psNext;
};

typedef struct {
  uint uiNumHerds;
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
MemoizationTable *initMemoization(double *x, double *y, uint n);

/*
   Description  : search in circles and squares with memoization
   Parameters  : id of the herd for which "herds in proximity is calculated", 
                   "Radius" with which herds are to be found.
		   callback function to be called for a herd in given proximity (same as RTree argument)
		   arguments for callback function
 */
boolean searchWithMemoization (MemoizationTable *, spatial_search_t *,
                               uint uiID, double dRadius,
                               spatial_search_hit_callback pfCallback, void* pCallbackArgs);

void deleteMemoization (MemoizationTable *);

#endif /* _MEMOIZATION_H_ */
