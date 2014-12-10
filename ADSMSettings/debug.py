import sys
import os
import re
import tempfile
import StringIO
import hotshot
import hotshot.stats
import cProfile
import pstats
from cStringIO import StringIO as cStringIO

from django.conf import settings


words_re = re.compile(r'\s+')

group_prefix_re = [
    re.compile("^.*/django/[^/]+"),
    re.compile("^(.*)/[^/]+$"), # extract module path
    re.compile(".*"), # catch strange entries
]

# Displays hotshot profiling. Add ?hotshotProf to url.
# Note: hotshot is not thread safe.
class HotshotProfileMiddleware(object):
    def process_request(self, request):
        if (settings.DEBUG or request.user.is_superuser) and 'hotshotProf' in request.GET:
            self.tmpfile = tempfile.mktemp()
            self.hotshotProf = hotshot.Profile(self.tmpfile)

    def process_view(self, request, callback, callback_args, callback_kwargs):
        if (settings.DEBUG or request.user.is_superuser) and 'hotshotProf' in request.GET:
            return self.hotshotProf.runcall(callback, request, *callback_args, **callback_kwargs)

    def get_group(self, file):
        for g in group_prefix_re:
            name = g.findall(file)
            if name:
                return name[0]

    def get_summary(self, results_dict, sum):
        list = [(item[1], item[0]) for item in results_dict.items()]
        list.sort(reverse=True)
        list = list[:40]

        res = "      tottime\n"
        for item in list:
            res += "%4.1f%% %7.3f %s\n" % ( 100 * item[0] / sum if sum else 0, item[0], item[1] )

        return res

    def summary_for_files(self, stats_str):
        stats_str = stats_str.split("\n")[5:]

        mystats = {}
        mygroups = {}

        sum = 0

        for s in stats_str:
            fields = words_re.split(s)
            if len(fields) == 7:
                time = float(fields[2])
                sum += time
                file = fields[6].split(":")[0]

                if not file in mystats:
                    mystats[file] = 0
                mystats[file] += time

                group = self.get_group(file)
                if not group in mygroups:
                    mygroups[group] = 0
                mygroups[group] += time

        return "<pre>" + \
               " ---- By file ----\n\n" + self.get_summary(mystats, sum) + "\n" + \
               " ---- By group ---\n\n" + self.get_summary(mygroups, sum) + \
               "</pre>"

    def process_response(self, request, response):
        if (settings.DEBUG or request.user.is_superuser) and 'hotshotProf' in request.GET:
            self.hotshotProf.close()

            out = StringIO.StringIO()
            old_stdout = sys.stdout
            sys.stdout = out

            stats = hotshot.stats.load(self.tmpfile)
            stats.sort_stats('time', 'calls')
            stats.print_stats()

            sys.stdout = old_stdout
            stats_str = out.getvalue()

            if response and response.content and stats_str:
                response.content = "<pre>" + stats_str + "</pre>"

            response.content = "\n".join(response.content.split("\n")[:40])

            response.content += self.summary_for_files(stats_str)

            os.unlink(self.tmpfile)

        return response


class cProfileMiddleware(object):
    def process_view(self, request, callback, callback_args, callback_kwargs):
        if settings.DEBUG and 'prof' in request.GET:
            self.profiler = cProfile.Profile()
            args = (request,) + callback_args
            return self.profiler.runcall(callback, *args, **callback_kwargs)

    def process_response(self, request, response):
        if settings.DEBUG and 'prof' in request.GET:
            self.profiler.create_stats()
            io = cStringIO()
            stats = pstats.Stats(self.profiler, stream=io)
            stats.strip_dirs().sort_stats(request.GET.get('sort', 'time'))
            stats.print_stats(int(request.GET.get('count', 10000)))
            response.content = '<pre>%s</pre>' % io.getvalue()
        return response

#------------------------------------------------------------------------------------------
def startDebug():
    import pdb

    print("\n\nIn DEBUG mode! Type name of variable to print it, 's' steps into functions, 'n' steps over functions, 'r' continue until this function returns, 'c' continue until new breakpoint, 'b' [[filename:]lineno] set break points, 'q' quit the program...\n")
    pdb.set_trace()