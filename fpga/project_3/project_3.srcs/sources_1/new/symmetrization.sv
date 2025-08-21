`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 14.08.2025 13:34:25
// Design Name: 
// Module Name: symmetrization
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


module symmetrization
    #(parameter int N = 8) (
    input logic [N-1:0] in,
    output logic [N-1:0] r, // minimal configuration
    output logic [$clog2(N+1)-1:0] l // number of steps to min cfg
    );
    
    wire [N-1:0] mins [0:N-1];
    assign mins[0] = in;
    
    wire [N-1:0] translations [0:N-1];
    assign translations[0] = in;
    
    localparam int LSIZE = $clog2(N+1);
    wire [LSIZE-1:0] ls [0:N-1];
    assign ls[0] = N;
    
    wire [LSIZE-1:0] count = 1;
    
    genvar i;
    generate
        for (i = 1; i < N; i = i + 1) begin : gen_translate_and_min_l
            translate #(.N(N), .STEPS(i)) u_translate_gen[i] (
                .in(in),
                .out(translations[i])
            );
            
            min_l #(.N(N)) u_min_l_gen[i] (
                .in1(mins[i-1]),
                .in2(translations[i]),
                .in_l1(ls[i-1]),
                .in_l2(count),
                .out(mins[i]),
                .out_l(ls[i])
            );
            
            assign count = count + 1;
        end
    endgenerate

    assign r = mins[N-1];
    assign l = ls[N-1];
    
endmodule
