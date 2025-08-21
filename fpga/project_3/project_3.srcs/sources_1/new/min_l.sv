`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 14.08.2025 14:16:01
// Design Name: 
// Module Name: min_l
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


module min_l
    #(parameter int N = 8) (
    input logic [N-1:0] in1,
    input logic [N-1:0] in2,
    input logic [$clog2(N+1)-1:0] in_l1,
    input logic [$clog2(N+1)-1:0] in_l2,
    output logic [N-1:0] out,
    output logic [$clog2(N+1)-1:0] out_l
    );
    
    assign out = (in1 < in2) ? in1 : in2;
    assign out_l = (in1 < in2) ? in_l1 : in_l2;
    
endmodule
