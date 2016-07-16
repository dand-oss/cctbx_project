from __future__ import division

'''
Author      : Young, I.D.
Created     : 07/14/2016
Last Changed: 07/14/2016
Description : XFEL UI plot real-time run stats
'''

from libtbx.phil import parse
from libtbx.utils import Sorry
from xfel.ui import db_phil_str
from xfel.ui.db.xfel_db import xfel_db_application
from xfel.ui.db.stats import HitrateStats
from xfel.ui.components.run_stats_plotter import plot_multirun_stats
import sys

phil_str = """
  run = None
    .type = int
    .multiple = True
  trial = None
    .type = int
  rungroup = None
    .type = int
  hit_cutoff = 30
    .type = int
    .help = Number of reflections to consider an image a hit. Estimate by looking at plot of strong reflections/image.
"""
phil_scope = parse(phil_str + db_phil_str)

def run(args):
  user_phil = []
  for arg in args:
    try:
      user_phil.append(parse(arg))
    except Exception, e:
      raise Sorry("Unrecognized argument %s"%arg)
  params = phil_scope.fetch(sources=user_phil).extract()

  app = xfel_db_application(params)
  all_results = []
  for run_no in params.run:
    all_results.append(HitrateStats(app, run_no, params.trial, params.rungroup)())
  plot_multirun_stats(all_results)

if __name__ == "__main__":
  run(sys.argv[1:])