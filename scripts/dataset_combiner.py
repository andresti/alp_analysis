from rootpy.io import root_open
from rootpy.plotting.hist import Hist
import rootpy
from ROOT import TDirectoryFile


class Dataset:
  def __init__(self, name, sel_events, gen_events, sel_events_withtrig, xs):
    self.name = name
    self.sel_events = sel_events
    self.gen_events = gen_events
    self.sel_events_withtrig = sel_events_withtrig
    self.xs = float(xs)
    self.calculate_weight_pb()
  
  def calculate_weight_pb(self):
    n = self.xs * 1.e3
    self.weight = n/self.gen_events

  def calculate_lumi_equiv(self, no_trig = True):
    #gen_evs_1fbinv = ds.xs * 1.e3 / ds.gen_events
    #n_fbinvs = (1 / gen_evs_1fbinv) * (ds.sel_events / ds.sel_events_withtrig)
    #v2 = (ds.gen_events / (1000. * ds.xs)) * (ds.sel_events / ds.sel_events_withtrig)
    lumi_eq = (1 / self.weight)
    if no_trig == True:
      lumi_eq *= (float(self.sel_events) / self.sel_events_withtrig)
    return lumi_eq


datasets = [
  #Dataset("QCD_HT200to300", 224, 56328408, 19, 1712000),
  #Dataset("QCD_HT300to500", 1003, 54537904, 498, 347700, ),
  Dataset("QCD_HT500to700", 2795,  49139388, 2323, 32100, ),
  Dataset("QCD_HT700to1000", 4631, 40779996, 3054, 6831, ),
  Dataset("QCD_HT1000to1500", 2066, 10035033, 1742, 1207, ),
  Dataset("QCD_HT1500to2000", 3431, 10872426, 2019, 119.9, ),
  Dataset("QCD_HT2000toInf", 1758, 4891602, 1256, 25.24, ),
]


def get_min_lumi(datasets):
  min_name = ""
  min_lumi = 999.
  for ds in datasets:
    lumi = ds.calculate_lumi_equiv()
    if lumi < min_lumi:
      min_name = ds
      min_lumi = lumi
  return min_lumi, min_name

def calculate_event_counts(datasets):
  n_events = {}
  min_lumi, min_name = get_min_lumi(datasets) 
  for ds in datasets:
    factor = ds.calculate_lumi_equiv() / min_lumi
    n_events[ds.name] = int(round(ds.sel_events / factor))
    print ds.name, ds.calculate_lumi_equiv(), ds.calculate_lumi_equiv(False), n_events[ds.name], ds.sel_events
  return n_events

def copy_file_n_events(n_events, infile_name, outfile_name):
  myfile = root_open(infile_name)
  outfile = root_open(outfile_name, "recreate")

  for path, dirs, objects in myfile.walk():
    for p in dirs:
      if not path == "":
        outpath = getattr(outfile, path)
        outpath.cd()
      mydir = TDirectoryFile(p, p)
      mydir.Write()
    for obj in objects:
      if not path == '': 
        mydir = getattr(outfile, path)
        mydir.cd()        
      if "tree" in obj: #It's a tree, limit to N events
        tree = getattr(getattr(myfile,path), obj)
        mytree = tree.CloneTree(n_events)
        mytree.Write()
      else: #It's a histogram, just copy - TODO, can we do something better?
        if not path == '':
          histo = getattr(getattr(myfile,path), obj)
        else:
          histo = getattr(myfile, obj)
        histo.Write()
  outfile.Close()
  myfile.Close()

if __name__ == "__main__":
  indir = "/lustre/cmswork/hh/alp_moriond_base/def_cmva_notrg/"
  outdir = "/lustre/cmswork/hh/alp_moriond_base/def_cmva_notrg_normalized/"
  event_counts = calculate_event_counts(datasets)
  for ds in datasets:
    infile_name = "%s/%s.root" % (indir, ds.name)
    outfile_name = "%s/%s.root" % (outdir, ds.name)
    print event_counts, ds.name, event_counts[ds.name], infile_name, outfile_name
    copy_file_n_events(event_counts[ds.name], infile_name, outfile_name)
