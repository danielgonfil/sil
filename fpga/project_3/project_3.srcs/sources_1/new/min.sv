`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 14.08.2025 13:43:22
// Design Name: 
// Module Name: min
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


module min
    #(parameter int N = 8) (
    input logic [N-1:0] in1,
    input logic [N-1:0] in2,
    output logic [N-1:0] out
    );
    
    assign out = (in1 < in2) ? in1 : in2;
endmodule
