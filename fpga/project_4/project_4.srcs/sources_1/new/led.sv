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
    output logic [6:0] seg,
    output logic [7:0] an
    );
    
    wire [N-1:0] in = SW;
    
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
            assign ls[i] = (translations[i] < mins[i-1]) ? i[LSIZE-1:0] : ls[i-1];
        end
    endgenerate
  
    assign LED = mins[N-1];   
    
    wire [LSIZE:0] l = ls[N-1];
    assign an = 8'b11111110; // only light up first digit
    assign seg = (l == 4'd0) ? 7'b0000001 :
                 (l == 4'd1) ? 7'b1001111 :
                 (l == 4'd2) ? 7'b0010010 :
                 (l == 4'd3) ? 7'b0000110 :
                 (l == 4'd4) ? 7'b1001100 :
                 (l == 4'd5) ? 7'b0100100 :
                 (l == 4'd6) ? 7'b0100000 :
                 (l == 4'd7) ? 7'b0001111 :
                 (l == 4'd8) ? 7'b0000000 :
                 (l == 4'd9) ? 7'b0001100 :
                 7'b1111111; // default blank 
                 
endmodule
