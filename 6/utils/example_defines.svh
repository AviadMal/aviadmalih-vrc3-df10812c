

`ifdef GEN1
parameter G_clk_freq = 50;  
parameter G_RESET_ACTIVE_VALUE=1;
parameter G_START_CONV_POLARITY = 1;
parameter G_CLK_PERIOD_NS    =20;
parameter  G_NUM_OF_INST = 1;

// ----------------------------------------------
`define D_AD7266_GENERICS_DEFINITION \
  parameter	VG_INST_NUM = 0,\
  parameter G_RESET_ACTIVE_VALUE = 1,\
  parameter G_START_CONV_POLARITY = 1,\
  parameter G_CLK_PERIOD_NS    =20,\
  parameter G_clk_freq = 50,\
  parameter       G_NUM_OF_INST = 1


`endif

`ifdef GEN2
parameter G_clk_freq = 150;  
parameter G_RESET_ACTIVE_VALUE=0;
parameter G_START_CONV_POLARITY = 0;
parameter G_CLK_PERIOD_NS    =6;
  parameter       G_NUM_OF_INST = 1;

// ----------------------------------------------
`define D_AD7266_GENERICS_DEFINITION \
  parameter	VG_INST_NUM = 0,\
  parameter G_RESET_ACTIVE_VALUE = 0,\
  parameter G_START_CONV_POLARITY = 0,\
  parameter G_CLK_PERIOD_NS    =6,\
  parameter G_clk_freq = 150,\
  parameter       G_NUM_OF_INST = 1

  
`endif



	//////env_parameter////////////////////
	parameter       VC_data_start = 1;	
	parameter 	    VC_G_data_ratio = 8;
	parameter       VC_data_cycle = 1;
	parameter       VC_twos_comp = 1;
	parameter       VC_BITMAP_WIDTH = 24;
   parameter   VC_ch_mux_with = 3;
   parameter   VC_sample_num_with = 32;
   parameter   VC_DATA_OUT_WIDTH = 16;
  parameter      VG_INST_NUM = 0;


											 
`define D_AD7266_GENERICS_MAPPING \
 .VG_INST_NUM(VG_INST_NUM),.G_RESET_ACTIVE_VALUE (G_RESET_ACTIVE_VALUE ),.G_START_CONV_POLARITY (G_START_CONV_POLARITY),.G_clk_freq(G_clk_freq),.G_CLK_PERIOD_NS(G_CLK_PERIOD_NS),.G_NUM_OF_INST(G_NUM_OF_INST)

//-----------------------------------------------------	

//-----------------------------------------------------
`define D_BUS_START_MAPPING \
 .DATA_WIDTH   (VC_data_start )
//-----------------------------------------------------

//-----------------------------------------------------
`define D_BUS_RATIO_MAPPING \
 .DATA_WIDTH   (VC_G_data_ratio )
//-----------------------------------------------------

//-----------------------------------------------------
`define D_BUS_CYCLE_MAPPING \
 .DATA_WIDTH   (VC_data_cycle )
//-----------------------------------------------------

//-----------------------------------------------------
`define D_BUS_TWOS_COMP_MAPPING \
 .DATA_WIDTH   (VC_twos_comp )
//-----------------------------------------------------
