dnl Configure path for MPI (Message Passing Interface) library
dnl Neil Harvey <nharve01@uoguelph.ca>, August 2003

dnl AM_PATH_MPI([ACTION-IF-FOUND [, ACTION-IF-NOT-FOUND]])
dnl Test for MPI, and define MPI_CFLAGS and MPI_LIBS.
dnl
AC_DEFUN(AM_PATH_MPI,[
  AC_ARG_WITH([mpi],
    AC_HELP_STRING([--with-mpi], [MPI installation prefix]),
    [ac_cv_with_mpi_root=${with_mpi}],
    AC_CACHE_CHECK([whether with-mpi was specified], ac_cv_with_mpi_root,
      ac_cv_with_mpi_root=no)
  ) # end of AC_ARG_WITH mpi

  AC_ARG_WITH([mpi-cflags],
    AC_HELP_STRING([--with-mpi-cflags], [MPI compile flags]),
    [ac_cv_with_mpi_cflags=${with_mpi_cflags}],
    AC_CACHE_CHECK([whether with-mpi-cflags was specified], ac_cv_with_mpi_cflags,
      ac_cv_with_mpi_cflags=no)
  ) # end of AC_ARG_WITH mpi-cflags

  AC_ARG_WITH([mpi-libs],
    AC_HELP_STRING([--with-mpi-libs], [MPI link command arguments]),
    [ac_cv_with_mpi_libs=${with_mpi_libs}],
    AC_CACHE_CHECK([whether with-mpi-libs was specified], ac_cv_with_mpi_libs,
      ac_cv_with_mpi_libs=no)
  ) # end of AC_ARG_WITH mpi-libs

  case "X${ac_cv_with_mpi_cflags}" in
  Xyes|Xno|X )
    case "X${ac_cv_with_mpi_root}" in
    Xyes|Xno|X ) ac_cv_with_mpi_cflags=no ;;
    * )        ac_cv_with_mpi_cflags=-I${ac_cv_with_mpi_root}/include ;;
    esac
  esac
  case "X${ac_cv_with_mpi_libs}" in
  Xyes|Xno|X )
    case "X${ac_cv_with_mpi_root}" in
    Xyes|Xno|X ) ac_cv_with_mpi_libs=no ;;
    * )        ac_cv_with_mpi_libs="-L${ac_cv_with_mpi_root}/lib -lmpi";;
    esac
  esac
  ac_save_CPPFLAGS="${CPPFLAGS}"
  ac_save_LIBS="${LIBS}"
  ac_save_DEFS="${DEFS}"

  AC_ARG_ENABLE([mpi-test],
    AC_HELP_STRING([--disable-mpitest], [Do not try to compile and run a test MPI program]),
    [ac_cv_with_mpi_test=${with_mpi_test}],
    AC_CACHE_CHECK([whether disable-mpitest was specified], ac_cv_with_mpi_test,
      ac_cv_with_mpi_test=no)
  ) # end of AC_ARG_WITH libmpi

  case "X${ac_cv_with_mpi_cflags}" in
  Xyes|Xno|X )
    ac_cv_with_mpi_cflags="" ;;
  * )
    MPI_CFLAGS="${ac_cv_with_mpi_cflags}"
    CPPFLAGS="${CPPFLAGS} ${MPI_CFLAGS}" ;;
  esac
  case "X${ac_cv_with_mpi_libs}" in
  Xyes|Xno|X )
    ac_cv_with_mpi_libs="" ;;
  * )
    MPI_LIBS="${ac_cv_with_mpi_libs}"
    LIBS="${LIBS} ${MPI_LIBS}" ;;
  esac

  dnl
  dnl At this point the MPI header file and library information have been
  dnl appended to the CPPFLAGS and LIBS variables.
  dnl 
  dnl Now try to compile and link a program that uses MPI.
  dnl

  AC_CACHE_CHECK([for MPI],[ac_cv_with_mpi],[
  AC_LANG_PUSH(C)
  AC_LINK_IFELSE([[
#include <stdio.h>

#include <mpi.h>



int
main (int argc, char *argv[])
{
  if (MPI_Init (&argc, &argv) != MPI_SUCCESS)
    return 1;
  MPI_Finalize ();
  return 0;
}
]],
    [ac_cv_with_mpi=yes],
    [ac_cv_with_mpi=no]) # end of AC_LINK_IFELSE 
  AC_LANG_POP(C)
  ]) # end of AC_CACHE_CHECK for ac_cv_with_mpi

  if test "X${ac_cv_with_mpi}" != Xno
  then
    AC_DEFINE([HAVE_MPI],[1],
        [Define this if the link test succeeded])
    ifelse([$1], , :, [$1])
  else
    MPI_CFLAGS=""
    MPI_LIBS=""
    ifelse([$2], , :, [$2])
  fi
  CPPFLAGS="${ac_save_CPPFLAGS}"
  LIBS="${ac_save_LIBS}"
  AC_SUBST([MPI_CFLAGS])
  AC_SUBST([MPI_LIBS])
  
]) # end of AC_DEFUN of AC_WITHLIB_MPI
dnl
dnl mpi.m4 ends here
