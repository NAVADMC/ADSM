dnl Process this file with autoconf to produce a configure script.
AC_INIT(adsm, 3.3.0)
AC_CONFIG_SRCDIR(main_loop/main_loop.c)
AM_INIT_AUTOMAKE
AC_CONFIG_HEADERS(config.h)
AC_PROG_RANLIB

dnl Adds command-line options.

 AC_DEFINE(DEBUG,0,[Define to 1 to provide an option for debug output.])

AC_ARG_ENABLE([debug],
  AC_HELP_STRING([--enable-debug], [provide an option for debug output]),
  [ac_cv_enable_debug=${enable_debug}],
  AC_CACHE_CHECK([whether enable-debug was specified], ac_cv_enable_debug,
    ac_cv_enable_debug=yes)
) # end of AC_ARG_ENABLE debug
case "X${ac_cv_enable_debug}" in
  Xyes|X )
    AC_DEFINE(DEBUG,1,[Define to 1 to provide an option for debug output.]) ;;
  * )
    ;;
  esac

ac_cv_enable_sc_guilib=no

AC_ARG_ENABLE([sc_guilib],
  AC_HELP_STRING([--enable-sc-guilib], [provide for MySQL database SQL output statements]),
  [ac_cv_enable_sc_guilib=${enable_sc_guilib}],
  AC_CACHE_CHECK([whether enable-sc-guilib was specified], ac_cv_enable_sc_guilib,
    ac_cv_enable_sc_guilib=yes)
) # end of AC_ARG_ENABLE sc_guilib  
case "X${ac_cv_enable_sc_guilib}" in
  Xyes|X )
{
    AC_DEFINE(USE_SC_GUILIB,1,[Define to 1 to provide an option for SQL output.])
    AC_DEFINE(SILENT_MODE,1,[Define to 1 to remove standard output result data, other than SQL statements.])} ;;
  * )
    ;;
  esac

AM_CONDITIONAL(USE_SC_GUILIB, test "X${ac_cv_enable_sc_guilib}" != Xno)

dnl Checks for programs.
AC_PROG_CC
AC_C_CONST

AM_PROG_LEX
AC_PROG_YACC
case "X${YACC}" in
  Xyacc )
  {
    AC_DEFINE( USE_PLAIN_YACC, 1, [Set this to 1 if no byacc or bison are available])
  };;
  esac

dnl Checks for libraries.

AC_CHECK_PROG(have_pkgconfig, pkg-config, yes)

dnl Work around the fact that pkg-config is not available on MinGW. If
dnl pkg-config is not present, we define stub versions of its macros just to
dnl avoid syntax errors further on.
dnl Workaround found here: http://osdir.com/ml/automake-gnu/2011-03/msg00007.html

m4_define_default([PKG_PROG_PKG_CONFIG],
[AC_MSG_CHECKING([pkg-config])
AC_MSG_RESULT([no])])
PKG_PROG_PKG_CONFIG

m4_define_default([PKG_CHECK_MODULES],
[AC_MSG_CHECKING([$1])
AC_MSG_RESULT([no])
$4])

dnl g_option_context_new was introduced in version 2.6, so checking for that
dnl function is equivalent to checking version >= 2.6.

if test "X${have_pkgconfig}" = Xyes
then
  PKG_CHECK_MODULES([GLIB], [glib >= 2.6],,try_glib_20=yes)
  if test "X${try_glib_20}" = Xyes
  then
    PKG_CHECK_MODULES([GLIB], [glib-2.0 >= 2.6],,AC_MSG_ERROR(cannot continue without glib))
  fi
  AC_SUBST(GLIB_CFLAGS)
  AC_SUBST(GLIB_LIBS)
else
  AC_CHECK_LIB(glib,g_option_context_new,,try_glib_20=yes)
  if test "X${try_glib_20}" = Xyes
  then
    AC_CHECK_LIB(glib-2.0,g_option_context_new,,AC_MSG_ERROR(cannot continue without glib))
  fi
fi

if test "X${have_pkgconfig}" = Xyes
then
  PKG_CHECK_MODULES([JSON_GLIB], [json-glib-1.0 >= 1.0], ,AC_MSG_ERROR(cannot continue without JSON-GLIB))
  AC_SUBST(JSON_GLIB_CFLAGS)
  AC_SUBST(JSON_GLIB_LIBS)
else
  AC_CHECK_LIB(json-glib-1.0,json_object_new,,AC_MSG_ERROR(cannot continue without JSON-GLIB))
fi

AM_PATH_GSL(1.4,[have_gsl=true],AC_MSG_ERROR(cannot continue without GSL))
AC_SUBST(GSL_CFLAGS)
AC_SUBST(GSL_LIBS)

if test "X${have_pkgconfig}" = Xyes
then
  PKG_CHECK_MODULES([SQLITE], [sqlite3 >= 3], ,AC_MSG_ERROR(cannot continue without SQLite3))
  AC_SUBST(SQLITE_CFLAGS)
  AC_SUBST(SQLITE_LIBS)
else
  AC_CHECK_LIB(sqlite3,sqlite3_open,,AC_MSG_ERROR(cannot continue without SQLite3))
fi

AC_CHECK_LIB(m,pow,,AC_MSG_ERROR(cannot continue without math library))

AC_CHECK_LIB(shp,SHPCreate,,AC_MSG_ERROR(cannot continue without Shapefile library))

AC_CHECK_LIB(gpcl,gpc_polygon_clip,,AC_MSG_ERROR(cannot continue without General Polygon Clipping (GPC) library))

AC_CHECK_LIB(gd,gdImageCreate,,AC_MSG_ERROR(cannot continue without GD graphics drawing library))

AC_CHECK_LIB(proj,pj_init,,AC_MSG_ERROR(cannot continue without PROJ.4 Cartographic Projections library))

dnl Checks for header files.
AC_HEADER_STDC
AC_CHECK_HEADERS(errno.h math.h unistd.h limits.h regex.h ctype.h)

dnl Checks for typedefs, structures, and compiler characteristics.
AC_C_CONST
AC_TYPE_SIZE_T

dnl Checks for library functions.
AC_CHECK_FUNCS(getstr getdelim getline strtoi)

AC_OUTPUT(Makefile \
  wml/Makefile \
  wml/test/Makefile \
  unit/Makefile \
  unit/test/Makefile \
  prob_dist/Makefile \
  prob_dist/test/Makefile \
  rel_chart/Makefile \
  rel_chart/test/Makefile \
  gis/Makefile \
  gis/test/Makefile \
  reporting/Makefile \
  reporting/test/Makefile \
  main_loop/Makefile \
  modules/Makefile \
  modules/test/Makefile \
  modules/test/module.disease/Makefile \
  modules/test/module.direct_contact_spread/Makefile \
  modules/test/module.indirect_contact_spread/Makefile \
  modules/test/module.airborne_spread/Makefile \
  modules/test/module.detection/Makefile \
  modules/test/module.control_measures/Makefile \
  modules/test/module.ring_destruction/Makefile \
  modules/test/module.ring_vaccination/Makefile \
  modules/test/module.zones/Makefile \
  modules/test/module.economic/Makefile \
  dll/Makefile \
  doc/Makefile \
  doc/diagrams/Makefile)
