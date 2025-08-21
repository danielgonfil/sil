`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 14.08.2025 15:27:41
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
    #(parameter int N) (
    input wire [N-1:0] in,
    output wire [N-1:0] r, // minimal configuration
    output wire [$clog2(N+1)-1:0] l // number of steps to min cfg
    );
    
    wire [N-1:0] translations [0:N-1];
    assign translations[0] = in;
    
    wire [N-1:0] mins [0:N-1];
    assign mins[0] = in;
    
    localparam LSIZE = $clog2(N+1)-1;
    wire [LSIZE:0] ls [0:N-1];
    assign ls[0] = N;
    
    genvar i;
    generate
        for (i = 1; i < N; i = i + 1) begin : gen_translate_and_min_l
            // translate original state by i states
            assign translations[i] = ((in << i) | (in >> (N - i))) & ((1 << N) - 1);
            
            // check if it's the current minimal state    
            assign mins[i] = (translations[i] < mins[i-1]) ? translations[i] : mins[i-1];
            
            // update the l value if needed
            assign ls[i] =  (translations[i] < mins[i-1]) ? i[LSIZE-1:0] : 
                            (translations[i] == mins[i-1] && i[LSIZE-1:0] < ls[i-1]) ? i[LSIZE-1:0] : 
                            ls[i-1];

        end
    endgenerate
  
    assign r = mins[N-1];
    assign l = ls[N-1];
endmodule
