
#pragma once

#include <algorithm>

#include "TH1.h"
#include "TH2.h"

#include "BaseOperator.h"
#include "Utils.h"

template <class EventClass> class DiJetPlotterOperator : public BaseOperator<EventClass> {

  public:
 
    std::vector<std::string> weights_;
    std::string btagWname = "BTagWeight"; //make it more general?

    TH1D h_H0_mass   {"h_H0_mass",   "leading di-jet mass"    , 300, 0., 900.};
    TH1D h_H0_pt     {"h_H0_pt"  ,   "leading di-jet pt"      , 300, 0., 900.};
    TH1D h_H0_eta    {"h_H0_eta" ,   "leading di-jet eta"     , 100, -4.0, 4.0};
    TH1D h_H0_csthst_a {"h_H0_csthst_a", "leading di-jet |costh*|"  , 100, 0., 1.};
    TH1D h_H0_dr     {"h_H0_dr"   ,  "leading di-jet deltaR"  , 100, 0., 7.};
    TH1D h_H0_deta   {"h_H0_deta" ,  "leading di-jet deltaEta", 100, -4.0, 4.0};
    TH1D h_H0_dphi   {"h_H0_dphi" ,  "leading di-jet deltaPhi", 100, -4.0, 4.0};
    TH1D h_H0_deta_a {"h_H0_deta_a", "leading di-jet deltaEta", 100, 0., 4.0};
    TH1D h_H0_dphi_a {"h_H0_dphi_a", "leading di-jet deltaPhi", 100, 0., 4.0};

    TH1D h_H1_mass   {"h_H1_mass",   "trailing di-jet mass"    ,300, 0., 900.};
    TH1D h_H1_pt     {"h_H1_pt"  ,   "trailing di-jet pt"      ,300, 0., 900.};
    TH1D h_H1_eta    {"h_H1_eta" ,   "trailing di-jet eta"     ,100, -4.0, 4.0};
    TH1D h_H1_csthst_a {"h_H1_csthst_a", "trailing di-jet |costh*|"  ,100, 0., 1.};
    TH1D h_H1_dr     {"h_H1_dr"   ,  "trailing di-jet deltaR"  ,100, 0., 7.};
    TH1D h_H1_deta   {"h_H1_deta" ,  "trailing di-jet deltaEta",100, -4.0, 4.0};
    TH1D h_H1_dphi   {"h_H1_dphi" ,  "trailing di-jet deltaPhi",100, -4.0, 4.0};
    TH1D h_H1_deta_a {"h_H1_deta_a", "trailing di-jet deltaEta",100, 0., 4.0};
    TH1D h_H1_dphi_a {"h_H1_dphi_a", "trailing di-jet deltaPhi",100, 0., 4.0};

    TH1D h_H0H1_mass {"h_H0H1_mass", "four-body mass"    , 300, 0., 900.};
    TH1D h_H0H1_pt   {"h_H0H1_pt"  , "four-body pt"      , 300, 0., 900.};
    TH1D h_H0H1_eta  {"h_H0H1_eta" , "four-body eta"     , 100, -6.0, 6.0};
    TH1D h_H0H1_dr   {"h_H0H1_dr"  , "four-body deltaR"  , 100, 0., 7.};
    TH1D h_H0H1_deta {"h_H0H1_deta", "four-body deltaEta", 100, -4.0, 4.0};
    TH1D h_H0H1_dphi {"h_H0H1_dphi", "four-body deltaPhi", 100, -4.0, 4.0};
    TH1D h_H0H1_deta_a {"h_H0H1_deta_a", "four-body deltaEta", 100, 0., 4.0};
    TH1D h_H0H1_dphi_a {"h_H0H1_dphi_a", "four-body deltaPhi", 100, 0., 4.0};

    TH2D h_H0_H1_mass {"h_H0_H1_mass","", 300, 0., 600., 300, 0., 600.};  

     DiJetPlotterOperator(const std::vector<std::string> & weights = {}) :
      weights_(weights) {}
    virtual ~DiJetPlotterOperator() {}

    virtual void init(TDirectory * tdir) {

      h_H0_mass.SetDirectory(tdir);
      h_H0_pt.SetDirectory(tdir);
      h_H0_eta.SetDirectory(tdir);
      h_H0_csthst_a.SetDirectory(tdir);
      h_H0_dr.SetDirectory(tdir);
      h_H0_deta.SetDirectory(tdir);
      h_H0_dphi.SetDirectory(tdir);
      h_H0_deta_a.SetDirectory(tdir);
      h_H0_dphi_a.SetDirectory(tdir);
      h_H1_mass.SetDirectory(tdir);
      h_H1_pt.SetDirectory(tdir);
      h_H1_eta.SetDirectory(tdir);
      h_H1_csthst_a.SetDirectory(tdir);
      h_H1_dr.SetDirectory(tdir);
      h_H1_deta.SetDirectory(tdir);
      h_H1_dphi.SetDirectory(tdir);
      h_H1_deta_a.SetDirectory(tdir);
      h_H1_dphi_a.SetDirectory(tdir);
      h_H0H1_mass.SetDirectory(tdir);
      h_H0H1_pt.SetDirectory(tdir);
      h_H0H1_eta.SetDirectory(tdir);
      h_H0H1_dr.SetDirectory(tdir);
      h_H0H1_deta.SetDirectory(tdir);
      h_H0H1_dphi.SetDirectory(tdir);
      h_H0H1_deta_a.SetDirectory(tdir);
      h_H0H1_dphi_a.SetDirectory(tdir);
      h_H0_H1_mass.SetDirectory(tdir);
      h_H0_mass.Sumw2();
      h_H0_pt.Sumw2();
      h_H0_eta.Sumw2();
      h_H0_csthst_a.Sumw2();
      h_H0_dr.Sumw2();
      h_H0_deta.Sumw2();
      h_H0_dphi.Sumw2();
      h_H0_deta_a.Sumw2();
      h_H0_dphi_a.Sumw2();
      h_H1_mass.Sumw2();
      h_H1_pt.Sumw2();
      h_H1_eta.Sumw2();
      h_H1_csthst_a.Sumw2();
      h_H1_dr.Sumw2();
      h_H1_deta.Sumw2();
      h_H1_dphi.Sumw2();
      h_H1_deta_a.Sumw2();
      h_H1_dphi_a.Sumw2();
      h_H0H1_mass.Sumw2();
      h_H0H1_pt.Sumw2();
      h_H0H1_eta.Sumw2();
      h_H0H1_dr.Sumw2();
      h_H0H1_deta.Sumw2();
      h_H0H1_dphi.Sumw2();
      h_H0H1_deta_a.Sumw2();
      h_H0H1_dphi_a.Sumw2();

      h_H0_H1_mass.Sumw2();
   }


    virtual bool process( EventClass & ev ) {

      float w = 1.0;
      w*=ev.eventInfo_.eventWeight(weights_);
      if (ev.eventInfo_.hasWeight(btagWname)) {
        w*=ev.eventInfo_.getWeight(btagWname);
      }   
     // debug - jets already sorted accordingly to pairing
      h_H0_mass.Fill(ev.dijets_.at(0).mass(), w);
      h_H0_pt.Fill(ev.dijets_.at(0).pt(), w);
      h_H0_eta.Fill(ev.dijets_.at(0).eta(), w);
      h_H0_csthst_a.Fill(get_absCosThetaStar(ev.dijets_.at(0),ev.dijets_.at(0)+ev.dijets_.at(1)), w);
      h_H0_dr.Fill(ROOT::Math::VectorUtil::DeltaR(ev.jets_.at(2).p4_, ev.jets_.at(3).p4_), w);
      h_H0_deta.Fill(ev.jets_.at(0).eta()-ev.jets_.at(1).eta(), w);
      h_H0_dphi.Fill(ROOT::Math::VectorUtil::DeltaPhi(ev.jets_.at(0).p4_, ev.jets_.at(1).p4_), w);
      h_H0_deta_a.Fill(std::abs(ev.jets_.at(0).eta()-ev.jets_.at(1).eta()), w);
      h_H0_dphi_a.Fill(get_dj_dPhiabs(ev.jets_.at(0),ev.jets_.at(1)), w); //std::abs(ROOT::Math::VectorUtil::DeltaR(ev.jets_.at(0).p4_, ev.jets_.at(1).p4_))

      h_H1_mass.Fill(ev.dijets_.at(1).mass(), w);
      h_H1_pt.Fill(ev.dijets_.at(1).pt(), w);
      h_H1_eta.Fill(ev.dijets_.at(1).eta(), w);
      h_H1_csthst_a.Fill(get_absCosThetaStar(ev.dijets_.at(1),ev.dijets_.at(0)+ev.dijets_.at(1)), w);
      h_H1_dr.Fill(ROOT::Math::VectorUtil::DeltaR(ev.jets_.at(2).p4_, ev.jets_.at(3).p4_), w);
      h_H1_deta.Fill(ev.jets_.at(2).eta()-ev.jets_.at(3).eta(), w);
      h_H1_dphi.Fill(ROOT::Math::VectorUtil::DeltaPhi(ev.jets_.at(2).p4_, ev.jets_.at(3).p4_), w);
      h_H1_deta_a.Fill(std::abs(ev.jets_.at(2).eta()-ev.jets_.at(3).eta()), w);
      h_H1_dphi_a.Fill(get_dj_dPhiabs(ev.jets_.at(2),ev.jets_.at(3)), w); //std::abs(ROOT::Math::VectorUtil::DeltaR(ev.jets_.at(2).p4_, ev.jets_.at(3).p4_))

      h_H0H1_mass.Fill((ev.dijets_.at(0)+ev.dijets_.at(1)).mass(), w);
      h_H0H1_pt.Fill((ev.dijets_.at(0)+ev.dijets_.at(1)).pt(), w);
      h_H0H1_eta.Fill((ev.dijets_.at(0)+ev.dijets_.at(1)).eta(), w);
      h_H0H1_dr.Fill(ROOT::Math::VectorUtil::DeltaR(ev.dijets_.at(0), ev.dijets_.at(1)), w);
      h_H0H1_deta.Fill(ev.dijets_.at(0).eta()-ev.dijets_.at(1).eta(), w);
      h_H0H1_dphi.Fill(ROOT::Math::VectorUtil::DeltaPhi(ev.dijets_.at(0), ev.dijets_.at(1)), w);
      h_H0H1_deta_a.Fill(std::abs(ev.dijets_.at(0).eta()-ev.dijets_.at(1).eta()), w);
      h_H0H1_dphi_a.Fill(get_ddj_dPhiabs(ev.dijets_.at(0), ev.dijets_.at(1)), w);//std::abs(ROOT::Math::VectorUtil::DeltaR(ev.dijets_.at(0), ev.dijets_.at(1)))

      h_H0_H1_mass.Fill(ev.dijets_.at(0).mass(), ev.dijets_.at(1).mass(), w);

      return true;
    }

    virtual bool output( TFile * tfile) {

      return true;

    }

};
