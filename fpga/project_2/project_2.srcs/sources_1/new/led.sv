`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 13.08.2025 12:54:26
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
    #(parameter int N = 8) (
    input wire [N-1:0] SW,
    output logic [N-1:0] LED
    );

    //min_cfg #(.N(N)) u_min_cfg (
    //    .in(SW),
    //    .out(LED)
    //);
    
    logic [N-1:0] translated;
    
    translate #(.N(N), .STEPS(1)) u_translate (
        .in(SW),
        .out(translated)
    );
    
    assign LED = translated;
        
endmodule
