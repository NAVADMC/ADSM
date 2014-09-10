
#ifndef _MEMOIZATION_H_
#define _MEMOIZATION_H_

#include "unit.h"

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


typedef struct HerdLocation HerdLocation;

/* location information of the a herd */

struct HerdLocation {
	uint uiID;    /* this is the id of this herd in the main herd list */
	float fLat;	/* can be latitude or longitude */
	float fLon;	/* can be longitude or latitude */
};

typedef struct HerdNode HerdNode;
struct HerdNode {
	HerdLocation* psHerd;
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
  uint uiSize;
  HerdLocation *pLatitudeList;
  HerdLocation *pLongitudeList;
  HerdLocation *pUnsortedList;
  InProximity  **pAllHerds;
} MemoizationTable;

/************************** memoization functions ***********************************/


/*
   Description : This function initializes the memoization table and also 
                  creates sorted herd lists for circles and squares algorithm.
   Parameters  :  pointer to the herd list

   Usage :     : should be called before any calls are made to "searchWithMemoization" 
                  or "serchWithCirclesAndSquare, 
                  typically after herd list is created in main function "run_sim_main"  
*/
MemoizationTable *initMemoization(UNT_unit_list_t* herds);

typedef int (*SearchHitCallback)(int id, void* arg);
/*
   Description  : search in circles and squares with memoization
   Parameters  : pointer to the herd for which "herds in proximity is calculated", 
                   "Radius" with which herds are to be found.
		   callback function to be called for a herd in given proximity (same as RTree argument)
		   arguments for callback function
 */
boolean searchWithMemoization (MemoizationTable *,
			      UNT_unit_t* pHerd, double dRadius,
			      SearchHitCallback pfCallback, void* pCallbackArgs);

/*
   Description  : search in circles and squares without memoization
   Parameters  : pointer to the herd for which "herds in proximity is calculated", 
                   "Radius" with which herds are to be found.
		   callback function to be called for a herd in given proximity (same as RTree argument)
		   arguments for callback function (same as RTree argument)
 */
boolean searchWithCirclesAndSquares (MemoizationTable *,
				     UNT_unit_t* pHerd, double dRadius,
				     SearchHitCallback pfCallback, void* pCallbackArgs);

void deleteMemoization (MemoizationTable *);

#endif /* _MEMOIZATION_H_ */
