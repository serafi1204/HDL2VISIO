/******************************************************************************
Copyright (c) 2022 SoC Design Laboratory, Konkuk University, South Korea
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met: redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer;
redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution;
neither the name of the copyright holders nor the names of its
contributors may be used to endorse or promote products derived from
this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Authors: Uyong Lee (uyonglee@konkuk.ac.kr)

Revision History
2022.11.17: Started by Uyong Lee
*******************************************************************************/
module controller(
        input 		    clk, nrst, in_vld, out_rdy,
        output wire 	in_rdy, out_vld,
	    output wire	    sel_input,
	    output wire 	sel_res,
        output wire 	sel_mem,
        output wire 	we_AMEM, we_BMEM, we_OMEM,
        output wire 	[3:0] addr_AMEM,
        output wire 	[3:0] addr_BMEM,
        output wire 	[3:0] addr_OMEM,
        output wire 	[2:0] addr_CROM,
        output wire 	en_REG_A,
	    output reg	    en_REG_B, en_REG_C
);

/////////////////////////////////////
/////////// Edit code below!!////////

reg [4:0] cnt;
reg [2:0] cstate, nstate;

localparam
	IDLE	= 1'b0,
	RUN		= 1'b1;

always@(posedge clk) begin
	if(!nrst) begin
		cnt <= 0;
	end	
	else begin
		if(in_vld == 1'b0 || out_rdy == 1'b0) begin
			cnt <= 0;
		end
		else if(cnt == 18) begin
			cnt <= 0;
		end
		else begin
			cnt <= cnt + 1;
		end
	end
end

always @(posedge clk)
begin
    if(!nrst) begin
       cstate <= IDLE;
    end
    else begin
       cstate <= nstate;
    end
end

always @(*) begin
    case(cstate)
	        IDLE : begin
	            if(in_vld) begin
	               nstate <= RUN;
	            end
	            else begin
	               nstate <= IDLE;
	            end
	        end
			RUN : begin
				if(cnt == 18 && in_vld == 1) begin
					nstate <= IDLE;	
				end
				else begin
					nstate <= RUN;
				end
			end
			default : nstate <= IDLE;
	endcase
end

assign en_REG_A = cnt[0];

always @(posedge clk) 
begin
	if(!nrst) begin
		en_REG_B <=0;
		en_REG_C <=0;
	end
    	else if(cstate != IDLE) begin
		en_REG_B <= cnt[1];
		en_REG_C <= cnt[2];
	end
	else begin
		en_REG_B <= en_REG_B;
		en_REG_C <= en_REG_C;
	end 
end

assign addr_CROM = {cnt[2], cnt[1], cnt[0]};


assign out_vld = cnt[0];
assign in_rdy = cnt[1];				
assign sel_input = in_rdy;


assign we_AMEM 	= cnt[0];
assign we_BMEM 	= cnt[1];
assign we_OMEM 	= cnt[2];


assign sel_res = cnt[0];  
assign sel_mem  = cnt[1];

assign addr_AMEM = {cnt[0], cnt[1], cnt[2], cnt[3]};		
assign addr_BMEM = {cnt[0], cnt[1], cnt[2], cnt[3]};
assign addr_OMEM = {cnt[0], cnt[1], cnt[2], cnt[3]};
		
//////////Edit code above!!/////////
////////////////////////////////////		
		
endmodule
