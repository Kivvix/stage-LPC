/**
 * @file hist.cpp
 * @package compare
 * @author J. Massot
 * @date 2014-06-16
 * 
 * @brief Display histograms
 */


#include "hist.hpp"

void hCoord( std::vector< std::vector<float> > &data , std::string run )
{
	// nom des fichiers de sortie
	std::string deltaCoord_eps   = PATH_OUTPUT + "/delaCoord-"  + run + ".eps";
	std::string deltaCoord_root  = PATH_OUTPUT + "/delaCoord-"  + run + ".root";
	
	
	TCanvas *c1 = new TCanvas("c1", "c1",900,900);
	
	// Create the three pads
	TPad *center_pad = new TPad("center_pad", "center_pad",0.0,0.0,0.6,0.6);
	center_pad->Draw();

	TPad *right_pad = new TPad("right_pad", "right_pad",0.55,0.0,1.0,0.6);
	right_pad->Draw(); right_pad->SetLogx();

	TPad *top_pad = new TPad("top_pad", "top_pad",0.0,0.55,0.6,1.0);
	top_pad->Draw(); top_pad->SetLogy();

	// Create, fill and project a 2D histogram.
	TH2F *h2 = new TH2F("h2","",40,-2,2,40,-2,2);
	
	Double_t x, y;
	for ( int i = 0 ; i < data.size() ; i++ ) {
		x = data[i][0]; y = data[i][1];
		h2->Fill( x , y );
	}
	TH1D * projh2X = h2->ProjectionX();
	TH1D * projh2Y = h2->ProjectionY();

	// Drawing
	center_pad->cd();
	h2->Draw("COL");

	top_pad->cd();
	projh2X->SetFillColor(kBlue+1);
	projh2X->Draw("bar");

	right_pad->cd();
	projh2Y->SetFillColor(kBlue-2);
	projh2Y->Draw("hbar");
	
	c1->cd();
	TLatex *t = new TLatex();
	t->SetTextFont(42);
	t->SetTextSize(0.02);
	t->DrawLatex(0.6,0.88,"This example demonstrate how to display");
	t->DrawLatex(0.6,0.85,"a histogram and its two projections.");
	
	c1->Update();
	c1->Print( deltaCoord_eps.c_str()  , "Landscape" );
	c1->Print( deltaCoord_root.c_str() , "RECREATE"  );
}

void hMag( std::vector< std::vector<float> > &data , std::string run )
{
	
	std::string deltaMag_eps   = PATH_OUTPUT + "/delaMag-"  + run + ".eps";
	std::string deltaMag_root  = PATH_OUTPUT + "/delaMag-"  + run + ".root";
	
	// on dessine un canvas
	TCanvas * cDeltaMag = new TCanvas( "cDeltaMag" , "Delta Mag" , 900 , 700 );
	// on y inclut un pad
	TPad *pDeltaMag = new TPad("pDeltaMag" , "Delta Mag" , 0.05,0.05,0.95,0.95,0.6 );
	pDeltaMag->Draw(); pDeltaMag->SetLogy();
	// on crée notre histogramme
	TH1F *hDeltaMag = new TH1F("delta_Mag" , "delta_Mag_density" , 500,-0.2,0.2 );
	
	for ( int i = 0 ; i < data.size() ; i++ ) {
		std::cout << data[i][2] << std::endl;
		hDeltaMag->Fill( data[i][2] );
	}
	pDeltaMag->cd();
	hDeltaMag->Draw();
	cDeltaMag->cd();
	cDeltaMag->Update();
	cDeltaMag->Print( deltaMag_eps.c_str()  , "Landscape" );
	cDeltaMag->Print( deltaMag_root.c_str() , "RECREATE"  );
}