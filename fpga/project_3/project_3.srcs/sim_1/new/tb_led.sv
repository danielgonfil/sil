`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 14.08.2025 13:28:18
// Design Name: 
// Module Name: tb_led
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


module tb_led;
    localparam int N = 4;
    
    logic [N-1:0] SW;
    logic [N-1:0] LED;
    logic [$clog2(N+1)-1:0] l;
    
    led #(.N(N)) u_tb_led (
        .SW(SW),
        .LED(LED),
        .l(l)
    );
    
    initial begin
        $display("Test led");
        
        SW = 4'b0001; #10;
        $display("SW=%b, LED=%b, l=%d", SW, LED, l);
        
        SW = 4'b0010; #10;
        $display("SW=%b, LED=%b, l=%d", SW, LED, l);
        
        SW = 4'b0100; #10;
        $display("SW=%b, LED=%b, l=%d", SW, LED, l);
        
        SW = 4'b1000; #10;
        $display("SW=%b, LED=%b, l=%d", SW, LED, l);
        
        SW = 4'b0101; #10;
        $display("SW=%b, LED=%b, l=%d", SW, LED, l);
        
        SW = 4'b1010; #10;
        $display("SW=%b, LED=%b, l=%d", SW, LED, l);
        
        SW = 4'b1101; #10;
        $display("SW=%b, LED=%b, l=%d", SW, LED, l);
        
        $finish;
    end

endmodule
