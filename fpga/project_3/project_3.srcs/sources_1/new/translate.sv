`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 14.08.2025 11:58:19
// Design Name: 
// Module Name: translate
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


module translate
    #(parameter int N = 8, int STEPS = 1) (
    input logic [N-1:0] in,
    output logic [N-1:0] out
    );
    
    assign out = ((in << STEPS) | (in >> (N - STEPS))) & ((1 << N) - 1);
    
endmodule
