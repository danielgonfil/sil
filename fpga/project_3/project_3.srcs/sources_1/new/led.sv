`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 14.08.2025 11:58:19
// Design Name: 
// Module Name: led
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


module led 
    #(parameter int N = 4) (
    input wire [N-1:0] SW,
    output logic [N-1:0] LED,
    output logic [$clog2(N+1)-1:0] l
    );
    
    symmetrization #(.N(N)) u_symmetrization (
        .in(SW),
        .r(LED),
        .l(l) // not used rn
    );
    
    // assign LED = ((SW << 1) | (SW >> 3)) & 4'b1111;
    
endmodule
