`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 13.08.2025 13:24:52
// Design Name: 
// Module Name: min_cfg
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module min_cfg
    #(parameter int N = 8) (
    input logic [N-1:0] in,
    output logic [N-1:0] out
    );
    
    logic [N-1:0] temp_min [0:N];
    assign temp_min[0] = in;
    
    genvar i;
    generate 
        for (i = 0; i < N; i++) begin : gen_translate_and_min 
            logic [N-1:0] translated;
    
            translate #(.N(N), .STEPS(i)) u_translate (
                .in(in),
                .out(translated)
            );
            
            min u_min (
                .in1(translated),
                .in2(temp_min[i]),
                .out(temp_min[i+1])
            );
    
        end
    
   endgenerate 
endmodule
