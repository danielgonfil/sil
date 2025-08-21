`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 14.08.2025 12:26:08
// Design Name: 
// Module Name: tb_translate
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


module tb_translate;
    
    localparam int N = 4;
    
    logic [N-1:0] in;
    logic [N-1:0] out;
    
    translate #(.N(N)) u_tb_translate (
        .in(in),
        .out(out)
    );
    
    initial begin
        $display("Test translate (N=%0d)", N);
        
        in = 4'b0001; #10;
        $display("in=%b, out=%b", in, out);
        
        $finish;
    end
endmodule