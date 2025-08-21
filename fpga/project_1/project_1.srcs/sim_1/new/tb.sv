`timescale 1ns / 100ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 13.08.2025 10:35:21
// Design Name: 
// Module Name: tb
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


module tb;
    logic [1:0] SW;
    logic [3:0] LED;
    //logic_ex u_logic_ex (.*);
    logic_ex u_logic_ex (.SW, .LED);
    //logic_ex u_logic_ex (.SW(switch_sig), .LED(led_sig));
    //logic_ex u_logic_ex (.*, .LED(led_sig));
    
    // Stimulus
    initial begin
        $printtimescale(tb);
        SW = '0;
        for (int i = 0; i < 4; i++) begin
            $display("Setting switches to %2b", i[1:0]);
            SW = i[1:0];
            #100;
        end
        
        $display("PASS: logic_ex test PASSED!");
        $stop;
    end
    
    always @(SW, LED) begin
        if (!SW[0] !== LED[0]) begin
            $display("FAIL: NOT Gate mismatch");
            $stop;
        end
        if (&SW[1:0] !== LED[1]) begin
            $display("FAIL: AND Gate mismatch");
            $stop;
        end
        if (|SW[1:0] !== LED[2]) begin
            $display("FAIL: OR Gate mismatch");
            $stop;
        end
        if (^SW[1:0] !== LED[3]) begin
            $display("FAIL: XOR Gate mismatch");
            $stop;
        end
    end
endmodule