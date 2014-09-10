#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include "gis.h"

#include "memoization.h"


#define EPSILON			(0.001)


typedef struct GeoSquare GeoSquare;
struct GeoSquare {
	float fLeftLongitude;
	float fRightLongitude;
	float fTopLatitude;
	float fBottomLatitude;
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


typedef float (*GetLatLong) (HerdLocation* psList);
HerdLocation getHerdLocation(UNT_unit_t* pHerd);
boolean getLatLong (_IN_ char *sString, _OUT_ float *pfLatitude, _OUT_ float *pfLongitude);
float getLatitude(HerdLocation* psList);
float getLongitude(HerdLocation* psList);
int findPosition(HerdLocation* psList, int uiStart, int uiEnd, float fLocation,
		 boolean bIsUpperBound, GetLatLong fpGetPoint);
boolean getGeoSquare(_IN_ HerdLocation sHerd, double dRadius, GeoSquare* pSquare);
void searchInProximity(HerdLocation* psLatList, HerdLocation* psLonList,
		       uint uiSize, HerdLocation* psHerd, double dRadius, 
		       SearchHitCallback pfCallback, void* pCallbackArgs);

void searchInProximity2 (HerdLocation* psLatList, HerdLocation* psLonList,
			uint uiSize, HerdLocation* psHerd, double dRadius,
			 InProximity* pTargetList, double dLastRadius);

int callbackNew(int id, void* args);

/************************** quick sort functions *************************************/
typedef boolean (*CompareLatLon) (_IN_ HerdLocation*, _IN_ HerdLocation*);
void swap(_IN_OUT_ HerdLocation* psHerd1, _IN_OUT_ HerdLocation* psHerd2);
boolean compareLat (_IN_ HerdLocation* psHerd1, _IN_ HerdLocation* psHerd2);
boolean compareLon(_IN_ HerdLocation* psHerd1, _IN_ HerdLocation* psHerd2);
int partition(_IN_OUT_ HerdLocation* psList, _IN_ int iFirst,
					_IN_ int iLast, _IN_ CompareLatLon fpCompare);
void quickSort(_IN_OUT_ HerdLocation* psList, _IN_ int iFirst,
					_IN_ int iLast, _IN_ CompareLatLon fpCompare);

/*************************** global variables ***************************************/

static HerdLocation* g_pLatitudeList = NULL;
static HerdLocation* g_pLongitudeList = NULL;
static HerdLocation* g_pUnsortedList = NULL;

static uint g_uiSize = 0;
static InProximity** g_pAllHerds = NULL;

static double cos0;
static double cos180;
static double cos270;
static double cos90;
static double cos315;
static double cos225;

static double deg_to_rad270;
static double deg_to_rad90;
static double deg_to_rad315;
static double deg_to_rad225;
static double deg_to_rad45;
static double deg_to_rad135;

/************************** quick sort functions *************************/

void swap(_IN_OUT_ HerdLocation* psHerd1, _IN_OUT_ HerdLocation* psHerd2) {
  HerdLocation temp;

  temp = *psHerd1;
  *psHerd1 = *psHerd2;
  *psHerd2 = temp;
}


boolean compareLat (_IN_ HerdLocation* psHerd1, _IN_ HerdLocation* psHerd2) {
  boolean ret_val = FALSE;
  if (NULL != psHerd1) {
    ret_val = ((psHerd1->fLat <= psHerd2->fLat) ? TRUE : FALSE);
  }

  return ret_val;
}

boolean compareLon(_IN_ HerdLocation* psHerd1, _IN_ HerdLocation* psHerd2) {
  boolean ret_val = FALSE;
  if (NULL != psHerd1) {
    ret_val = ((psHerd1->fLon <= psHerd2->fLon) ? TRUE : FALSE);
  }

  return ret_val;
}

int partition(_IN_OUT_ HerdLocation* psList, _IN_ int iFirst, _IN_ int iLast, _IN_ CompareLatLon fpCompare) {
  int i, j;

  i = iFirst-1;

  for (j = iFirst; j<= iLast-1; j++) {
    if (TRUE == fpCompare(&psList[j], &psList[iLast])) {
      i++;
      swap(&psList[i], &psList[j]);
    }
  }
  swap(&psList[i+1], &psList[iLast]);

  return i+1;
}


void quickSort(_IN_OUT_ HerdLocation* psList, _IN_ int iFirst, _IN_ int iLast, _IN_ CompareLatLon fpCompare) {

  if (iFirst < iLast) {
    int pivot;

    pivot = partition(psList, iFirst, iLast, fpCompare);
    quickSort(psList, iFirst, pivot-1, fpCompare);
    quickSort(psList, pivot+1, iLast, fpCompare);
  }
}



void Math_functions() {

  cos0 = cos(DEG_TO_RAD*0);
  cos180 = cos(DEG_TO_RAD*180);
  cos270 = cos(DEG_TO_RAD*270);
  cos90 = cos(DEG_TO_RAD*90);
  cos315 = cos(DEG_TO_RAD*315);
  cos225 = cos(DEG_TO_RAD*225);

  deg_to_rad270 = DEG_TO_RAD*270;
  deg_to_rad90 = DEG_TO_RAD*90;
  deg_to_rad315 = DEG_TO_RAD*315;
  deg_to_rad225 = DEG_TO_RAD*225;
  deg_to_rad45 = DEG_TO_RAD*45;
  deg_to_rad135 = DEG_TO_RAD*135;
}


float getLatitude(HerdLocation* psList) {
  return psList->fLat;
}

float getLongitude(HerdLocation* psList) {
  return psList->fLon;
}

boolean getLatLong (_IN_ char *pcString, _OUT_ float *pfLatitude, _OUT_ float *pfLongitude) {
  boolean ret_val = FALSE;

  if ((NULL != pcString) && (NULL != pfLatitude) && (NULL != pfLongitude)) {
    sscanf(pcString, "%f,%f", pfLatitude, pfLongitude);
    ret_val = TRUE;
  }

  return ret_val;
}

void printList (_IN_ HerdLocation* psList, _IN_ uint uiSize){
  if (NULL != psList) {
    uint i;
    for (i = 1; i <= uiSize; i++) {
      printf("%f,%f,%u\n", psList[i].fLat, psList[i].fLon, psList[i].uiID);
    }
  }
}

HerdLocation getHerdLocation(UNT_unit_t* pHerd) {
   HerdLocation herd;

   herd.uiID = atoi(pHerd->official_id);
   herd.fLat = pHerd->latitude;
   herd.fLon = pHerd->longitude;

   return herd;
}

boolean insertHerd (_IN_OUT_ HerdLocation* psHerdList,
		    _IN_ float fLat,
		    _IN_ float fLon,
		    _IN_ uint uiID) {

  boolean ret_val = FALSE;

  if (NULL != psHerdList) {
    psHerdList[uiID].fLat = fLat;
    psHerdList[uiID].fLon = fLon;
    psHerdList[uiID].uiID = uiID;

    ret_val = TRUE;
  }

  return ret_val;
}




int findPosition(HerdLocation* psList, int uiStart, int uiEnd,
		 float fLocation, boolean bIsUpperBound, GetLatLong fpGetPoint) {
  int position;
  float temp;

  if (uiEnd - uiStart > 0) {

    int i = (uiEnd + uiStart) / 2;

    temp = fpGetPoint(&psList[i]);
    if (fLocation < temp) {
      position = findPosition(psList, uiStart, i -1, fLocation, bIsUpperBound, fpGetPoint);
    }else {
      position = findPosition(psList, i + 1, uiEnd, fLocation, bIsUpperBound, fpGetPoint);
    }
  }else
    {
      position = uiEnd;
      if(TRUE == bIsUpperBound) {
	if((fpGetPoint(&psList[position]) - fLocation) > EPSILON){
	  position--;
	}
      }else {
	if((fpGetPoint(&psList[position]) - fLocation) < EPSILON) {
	  position++;
	}
      }
    }

  return position;
}


boolean initMemoization(uint uiNumHerds) {

  boolean ret_val = FALSE;

  if (NULL == g_pAllHerds) {
    g_pAllHerds = (InProximity**)malloc(uiNumHerds * sizeof(InProximity*));
    memset(g_pAllHerds, 0, uiNumHerds * sizeof(InProximity*));
  }

  return ret_val;
}

void initCirclesAndSquaresList(UNT_unit_list_t* herds) {

  int nherds = UNT_unit_list_length(herds);
  HerdLocation herd;
  int i;
  UNT_unit_t* herd_t;
  uint herd_id;

  /* for id 0, coz official id's start from 1 */ 

  initMemoization(nherds+1);

  g_pLatitudeList = (HerdLocation *)malloc(sizeof(HerdLocation) * (nherds+1));
  g_pLongitudeList = (HerdLocation *)malloc(sizeof(HerdLocation) * (nherds+1));
  g_pUnsortedList = (HerdLocation *)malloc(sizeof(HerdLocation) * (nherds+1));

  g_uiSize = nherds+1;

  for (i = 0; i < nherds; i++) {
    herd_t = (UNT_unit_t*)UNT_unit_list_get(herds, i);       
    herd = getHerdLocation(herd_t);

    herd_id = atoi(herd_t->official_id);
    insertHerd(g_pLatitudeList, herd.fLat, herd.fLon, herd_id);
    insertHerd(g_pLongitudeList, herd.fLat, herd.fLon, herd_id);
    insertHerd(g_pUnsortedList, herd.fLat, herd.fLon, herd_id);
  }

  /* start with index 1, because herd ids start with 1 */
  quickSort(g_pLatitudeList + 1, 0, nherds-1, compareLat);
  quickSort(g_pLongitudeList + 1, 0, nherds-1, compareLon);

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

boolean deleteMemoization(uint uiNumHerds) {
  boolean ret_val = FALSE;

  if (NULL != g_pAllHerds) {
    uint i;

    for (i = 0; i < uiNumHerds; i++) {
      if (NULL != g_pAllHerds[i]) {
	deleteProximityList(g_pAllHerds[i]);
	g_pAllHerds[i] = NULL;
      }
    }

    free(g_pAllHerds);
    g_pAllHerds = NULL;
  }
  return ret_val;
}


boolean withInRadius(HerdLocation* pX_Herd, HerdLocation* pY_Herd, double dRadius) {
  boolean ret_val = FALSE;
  double distance;

  /* calculate weather the herd is within radius */
  distance = GIS_distance(pX_Herd->fLat, pX_Herd->fLon, pY_Herd->fLat, pY_Herd->fLon);

  if ((distance - dRadius) <= EPSILON) {
    ret_val = TRUE;
  }

  return ret_val;
}

/**************************** square calculations **********************************/
boolean getGeoSquareBig(_IN_ HerdLocation sHerd, float uiRadius, GeoSquare* pSquare) {

    float temp_lat;
    float temp1, temp2;
    float lon_top;
    float lon_bottom;
    float lon_0;
    float which_lat;

    /* degrees to radians */
    sHerd.fLat *= DEG_TO_RAD;
    sHerd.fLon *= DEG_TO_RAD;

    /* north side */
    pSquare->fTopLatitude =  asin(sin(sHerd.fLat)*cos(uiRadius/GIS_EARTH_RADIUS)
				  + cos(sHerd.fLat)*sin(uiRadius/GIS_EARTH_RADIUS)*cos0);
    /* south-side */
    pSquare->fBottomLatitude = asin(sin(sHerd.fLat)*cos(uiRadius/GIS_EARTH_RADIUS)
				    + cos(sHerd.fLat)*sin(uiRadius/GIS_EARTH_RADIUS)*cos180);
    /* left side, 270 degree */
    temp_lat =  asin(sin(sHerd.fLat)*cos(uiRadius/GIS_EARTH_RADIUS)
		     + cos(sHerd.fLat)*sin(uiRadius/GIS_EARTH_RADIUS)*cos270);

    temp1 = sin(deg_to_rad270)*sin(uiRadius/GIS_EARTH_RADIUS)*cos(sHerd.fLat);
    temp2 = cos(uiRadius/GIS_EARTH_RADIUS) - (sin(sHerd.fLat) * sin(temp_lat));
    lon_0 = (sHerd.fLon + atan2(temp1, temp2));

    pSquare->fLeftLongitude = lon_0;
    which_lat = sHerd.fLat;

    /*  left side at 270, at top */
    temp_lat =  asin(sin(pSquare->fTopLatitude)*cos(uiRadius/GIS_EARTH_RADIUS)
		     + cos(pSquare->fTopLatitude)*sin(uiRadius/GIS_EARTH_RADIUS)*cos270);

    temp1 = sin(deg_to_rad270)*sin(uiRadius/GIS_EARTH_RADIUS)*cos(sHerd.fLat);
    temp2 = cos(uiRadius/GIS_EARTH_RADIUS) - (sin(pSquare->fTopLatitude) * sin(temp_lat));
    lon_top = (sHerd.fLon + atan2(temp1, temp2));

    if (lon_top < pSquare->fLeftLongitude) {
      pSquare->fLeftLongitude = lon_top;
      which_lat = pSquare->fTopLatitude;
    }

    /*  left side at 270, at bottom */
    temp_lat =  asin(sin(pSquare->fBottomLatitude)*cos(uiRadius/GIS_EARTH_RADIUS)
		     + cos(pSquare->fBottomLatitude)*sin(uiRadius/GIS_EARTH_RADIUS)*cos270);

    temp1 = sin(deg_to_rad270)*sin(uiRadius/GIS_EARTH_RADIUS)*cos(sHerd.fLat);
    temp2 = cos(uiRadius/GIS_EARTH_RADIUS) - (sin(pSquare->fBottomLatitude) * sin(temp_lat));
    lon_bottom = (sHerd.fLon + atan2(temp1, temp2));

    if (lon_bottom < pSquare->fLeftLongitude) {
      pSquare->fLeftLongitude = lon_bottom;
      which_lat = pSquare->fBottomLatitude;
    }

    temp_lat =  asin(sin(which_lat)*cos(uiRadius/GIS_EARTH_RADIUS)
		     + cos(which_lat)*sin(uiRadius/GIS_EARTH_RADIUS)*cos90);

    temp1 = sin(deg_to_rad90)*sin(uiRadius/GIS_EARTH_RADIUS)*cos(which_lat);
    temp2 = cos(uiRadius/GIS_EARTH_RADIUS) - (sin(which_lat) * sin(temp_lat));
    pSquare->fRightLongitude = (sHerd.fLon + atan2(temp1, temp2));


    /* convert back to degrees */
    pSquare->fTopLatitude = RAD_TO_DEG * (pSquare->fTopLatitude);
    pSquare->fBottomLatitude = RAD_TO_DEG * (pSquare->fBottomLatitude);

    /* convert back to degrees */
    pSquare->fLeftLongitude = RAD_TO_DEG * (pSquare->fLeftLongitude);
    pSquare->fRightLongitude = RAD_TO_DEG * (pSquare->fRightLongitude);;

#ifdef DEBUG
    printf ("Top, Left is %f, %f\n", pSquare->fTopLatitude, pSquare->fLeftLongitude);
    printf ("Bottom, Right is %f, %f\n", pSquare->fBottomLatitude, pSquare->fRightLongitude);
#endif
    return TRUE;
}

boolean getGeoSquareSmall(_IN_ HerdLocation sHerd, float uiRadius, GeoSquare* pSquare) {

  float temp1, temp2;
  float lon_bottom;

  /* degrees to radians */
  sHerd.fLat *= DEG_TO_RAD;
  sHerd.fLon *= DEG_TO_RAD;

  /* left, north side */
  pSquare->fTopLatitude =  asin(sin(sHerd.fLat)*cos(uiRadius/GIS_EARTH_RADIUS)
				+ cos(sHerd.fLat)*sin(uiRadius/GIS_EARTH_RADIUS)*cos315);

  temp1 = sin(deg_to_rad315)*sin(uiRadius/GIS_EARTH_RADIUS)*cos(sHerd.fLat);
  temp2 = cos(uiRadius/GIS_EARTH_RADIUS) - (sin(sHerd.fLat) * sin(pSquare->fTopLatitude));
  pSquare->fLeftLongitude = (sHerd.fLon + atan2(temp1, temp2));

  /* left, south-side */
  pSquare->fBottomLatitude = asin(sin(sHerd.fLat)*cos(uiRadius/GIS_EARTH_RADIUS)
				  + cos(sHerd.fLat)*sin(uiRadius/GIS_EARTH_RADIUS)*cos225);
  temp1 = sin(deg_to_rad225)*sin(uiRadius/GIS_EARTH_RADIUS)*cos(sHerd.fLat);
  temp2 = cos(uiRadius/GIS_EARTH_RADIUS) - (sin(sHerd.fLat) * sin(pSquare->fBottomLatitude));
  lon_bottom = (sHerd.fLon + atan2(temp1, temp2));

  if (pSquare->fLeftLongitude > lon_bottom) {
    pSquare->fLeftLongitude = lon_bottom;
  }

  temp1 = sin(deg_to_rad45)*sin(uiRadius/GIS_EARTH_RADIUS)*cos(sHerd.fLat);
  temp2 = cos(uiRadius/GIS_EARTH_RADIUS) - (sin(sHerd.fLat) * sin(pSquare->fTopLatitude));
  pSquare->fRightLongitude = (sHerd.fLon + atan2(temp1, temp2));

  temp1 = sin(deg_to_rad135)*sin(uiRadius/GIS_EARTH_RADIUS)*cos(sHerd.fLat);
  temp2 = cos(uiRadius/GIS_EARTH_RADIUS) - (sin(sHerd.fLat) * sin(pSquare->fBottomLatitude));
  lon_bottom = (sHerd.fLon + atan2(temp1, temp2));

  if (pSquare->fRightLongitude > lon_bottom) {
    pSquare->fRightLongitude = lon_bottom;
  }

  /* convert back to degrees */
  pSquare->fTopLatitude = RAD_TO_DEG * (pSquare->fTopLatitude);
  pSquare->fBottomLatitude = RAD_TO_DEG * (pSquare->fBottomLatitude);

  /* convert back to degrees */
  pSquare->fLeftLongitude = RAD_TO_DEG * (pSquare->fLeftLongitude);
  pSquare->fRightLongitude = RAD_TO_DEG * (pSquare->fRightLongitude);

#ifdef DEBUG
  printf ("Top, Left is %f, %f\n", pSquare->fTopLatitude, pSquare->fLeftLongitude);
  printf ("Bottom, Right is %f, %f\n", pSquare->fBottomLatitude, pSquare->fRightLongitude);
#endif
  return TRUE;
}

/***************** functions of 01, only squares and circles *************/
boolean searchWithCirclesAndSquares (UNT_unit_t* pHerd, double dRadius,
			     SearchHitCallback pfCallback, void* pCallbackArgs) {
  boolean ret_val = FALSE;
  HerdLocation herd = getHerdLocation(pHerd);

  searchInProximity (g_pLatitudeList, g_pLongitudeList, g_uiSize, 
		     &herd, dRadius, pfCallback, pCallbackArgs);

  return ret_val;
}

void processHerd (HerdLocation* pS_Herd, HerdLocation* pT_Herd, 
		     double dRadius, boolean bSureIn, 
		     SearchHitCallback pfCallback, void* pCallbackArgs) {

  if (!bSureIn) {
    if(withInRadius(pS_Herd, pT_Herd, dRadius)) {
      pfCallback(pT_Herd->uiID, pCallbackArgs);      
    }
  }else {
      pfCallback(pT_Herd->uiID, pCallbackArgs);
  }
}


void searchInProximity (HerdLocation* psLatList, HerdLocation* psLonList,
			uint uiSize, HerdLocation* psHerd, double dRadius, 
			SearchHitCallback pfCallback, void* pCallbackArgs) {

  GeoSquare big_square;
  GeoSquare small_square;
  HerdLocation* list;
  int bottom_most;
  int top_most;
  int left_most;
  int right_most;
  int start_pos;
  int end_pos;
  int i;


  getGeoSquareBig(*psHerd, dRadius * 1.1, &big_square);
  getGeoSquareSmall(*psHerd, dRadius*0.99, &small_square);

  /* find latitude and longitudes at the end of the given radius */
  bottom_most = findPosition(psLatList, 1, uiSize, big_square.fBottomLatitude, FALSE, getLatitude);
  top_most = findPosition(psLatList, bottom_most, uiSize, big_square.fTopLatitude, TRUE, getLatitude);
  left_most = findPosition(psLonList, 1, uiSize, big_square.fLeftLongitude, FALSE, getLongitude);
  right_most = findPosition(psLonList, left_most, uiSize, big_square.fRightLongitude, TRUE, getLongitude);

  if ((top_most - bottom_most) > (right_most - left_most)) {
    list = psLonList;
    start_pos = left_most;
    end_pos = right_most;

    for (i = start_pos; i <= end_pos; i++) {
  
      if ((list[i].fLat >= big_square.fBottomLatitude) && (list[i].fLat <= big_square.fTopLatitude)) {

	if ((list[i].fLon > small_square.fLeftLongitude) && (list[i].fLon < small_square.fRightLongitude)
	    && (list[i].fLat > small_square.fBottomLatitude) && (list[i].fLat < small_square.fTopLatitude)){

	  if (list[i].uiID != psHerd->uiID) {
	    processHerd(psHerd, &list[i], dRadius, TRUE, pfCallback, pCallbackArgs);
	  }
	}else{   
	  processHerd(psHerd, &list[i], dRadius, FALSE, pfCallback, pCallbackArgs);
	}
      }
    
    }/* for (i = start_pos; i <= end_pos; i++) */

  }else {
    list = psLatList;
    start_pos = bottom_most;
    end_pos = top_most;

    for (i = start_pos; i <= end_pos; i++) {
	
      if ((list[i].fLon >= big_square.fLeftLongitude) && (list[i].fLon <= big_square.fRightLongitude)){

	if ((list[i].fLon > small_square.fLeftLongitude) && (list[i].fLon < small_square.fRightLongitude)
	    && (list[i].fLat > small_square.fBottomLatitude) && (list[i].fLat < small_square.fTopLatitude)){

	  if (list[i].uiID != psHerd->uiID) {
	    processHerd(psHerd, &list[i], dRadius, TRUE, pfCallback, pCallbackArgs);
	  }
	}else{
	  processHerd(psHerd, &list[i], dRadius, FALSE, pfCallback, pCallbackArgs);
	}
      }    
    }/* for (i = start_pos; i <= end_pos; i++) */
  }

}


/************************** 10 search with memoization  **************************/

void processHerdList2(HerdNode* pHerdList, SearchHitCallback pfCallback,
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


boolean inMemoization2(HerdLocation* pHerd, InProximity** pSrcHerds,
		      double dRadius, SearchHitCallback pfCallback,
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
    temp_list = createNewProxmityList(dRadius);
    searchInProximity2 (g_pLatitudeList, g_pLongitudeList, 
			g_uiSize, pHerd, dRadius, temp_list, 
			prev_list->dRadius);
    processHerdList2(temp_list->psHerdList, pfCallback, pCallbackArgs);
    prev_list->psNext = temp_list;
  }

  return ret_val;
}

/* search in circles and squares with memoization */
boolean searchWithMemoization (UNT_unit_t* pHerd, double dRadius,
			             SearchHitCallback pfCallback, void* pCallbackArgs) {

  boolean ret_val = FALSE;
  HerdLocation herd = getHerdLocation(pHerd);

  if (NULL == g_pAllHerds[herd.uiID]) {
    g_pAllHerds[herd.uiID] = createNewProxmityList(dRadius);

    searchInProximity2 (g_pLatitudeList, g_pLongitudeList, g_uiSize,
			&herd, dRadius, g_pAllHerds[herd.uiID], (double)0.0);

    processHerdList2(g_pAllHerds[herd.uiID]->psHerdList, 
		     pfCallback, pCallbackArgs);
  }else {
    inMemoization2(&herd, &g_pAllHerds[herd.uiID], dRadius,  
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


boolean addToMemoization2 (HerdLocation* pS_Herd, HerdLocation* pT_Herd, 
			   double dRadius, InProximity* pTargetList, 
			   double dLastRadius) {
  boolean ret_val = FALSE;
  double distance;

  /* calculate weather the herd is within radius */
  distance = GIS_distance(pS_Herd->fLat, pS_Herd->fLon, 
				pT_Herd->fLat, pT_Herd->fLon);
  
  if ((distance - dRadius) <= EPSILON) {
    if ((distance - dLastRadius) > EPSILON) {
          addToList2(pTargetList, pT_Herd);
    }
  }

  return ret_val;
}


void searchInProximity2 (HerdLocation* psLatList, HerdLocation* psLonList,
			uint uiSize, HerdLocation* psHerd, double dRadius,
			InProximity* pTargetList, double dLastRadius) {


  GeoSquare big_square;
  GeoSquare small_square;
  HerdLocation* list;
  int bottom_most;
  int top_most;
  int left_most;
  int right_most;
  int start_pos;
  int end_pos;
  int i;


  getGeoSquareBig(*psHerd, (dRadius * 1.1), &big_square);
  getGeoSquareSmall(*psHerd, (dRadius * 0.99), &small_square);

  /* find latitude and longitudes at the end of the given radius */
  bottom_most = findPosition(psLatList, 1, uiSize, big_square.fBottomLatitude, FALSE, getLatitude);
  top_most = findPosition(psLatList, bottom_most, uiSize, big_square.fTopLatitude, TRUE, getLatitude);
  left_most = findPosition(psLonList, 1, uiSize, big_square.fLeftLongitude, FALSE, getLongitude);
  right_most = findPosition(psLonList, left_most, uiSize, big_square.fRightLongitude, TRUE, getLongitude);

  if ((top_most - bottom_most) > (right_most - left_most)) {
    list = psLonList;
    start_pos = left_most;
    end_pos = right_most;

    for (i = start_pos; i <= end_pos; i++) {
  
      if ((list[i].fLat >= big_square.fBottomLatitude) && (list[i].fLat <= big_square.fTopLatitude)) {

	if ((list[i].fLon > small_square.fLeftLongitude) && (list[i].fLon < small_square.fRightLongitude)
	    && (list[i].fLat > small_square.fBottomLatitude) && (list[i].fLat < small_square.fTopLatitude)){

	  if (list[i].uiID != psHerd->uiID) {
	    addToMemoization2(psHerd, &list[i], dRadius, pTargetList, dLastRadius);
	  }
	}else{   
	  addToMemoization2(psHerd, &list[i], dRadius, pTargetList, dLastRadius);	  
	}
      }
    
    }/* for (i = start_pos; i <= end_pos; i++) */

  }else {
    list = psLatList;
    start_pos = bottom_most;
    end_pos = top_most;

    for (i = start_pos; i <= end_pos; i++) {
	
      if ((list[i].fLon >= big_square.fLeftLongitude) && (list[i].fLon <= big_square.fRightLongitude)){

	if ((list[i].fLon > small_square.fLeftLongitude) && (list[i].fLon < small_square.fRightLongitude)
	    && (list[i].fLat > small_square.fBottomLatitude) && (list[i].fLat < small_square.fTopLatitude)){

	  if (list[i].uiID != psHerd->uiID) {
	    addToMemoization2(psHerd, &list[i], dRadius, pTargetList, dLastRadius);	  
	  }
	}else{
	  addToMemoization2(psHerd, &list[i], dRadius, pTargetList, dLastRadius);	  
	}
      }    
    }/* for (i = start_pos; i <= end_pos; i++) */
  }

}



