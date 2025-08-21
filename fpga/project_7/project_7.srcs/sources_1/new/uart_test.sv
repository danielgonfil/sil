module uart_test #(
    parameter CLKS_PER_BIT = 868  // For 100 MHz clock and 115200 baud
)(
    input  wire CLK100MHZ,       // System clock
    input  wire UART_TXD_IN,   // UART RX line from PC
    output wire UART_RXD_OUT    // UART TX line to PC
);

    // RX signals
    wire      w_Rx_DV;
    wire [7:0] w_Rx_Byte;

    // TX signals
    reg       r_Tx_DV   = 0;
    reg [7:0] r_Tx_Byte = 0;
    wire      w_Tx_Done;
    wire      w_Tx_Active;

    // UART Receiver
    uart_rx #(.CLKS_PER_BIT(CLKS_PER_BIT)) uart_rx_inst (
        .i_Clock    (CLK100MHZ),
        .i_Rx_Serial(UART_RXD_OUT),
        .o_Rx_DV    (w_Rx_DV),
        .o_Rx_Byte  (w_Rx_Byte)
    );

    // UART Transmitter
    uart_tx #(.CLKS_PER_BIT(CLKS_PER_BIT)) uart_tx_inst (
        .i_Clock    (CLK100MHZ),
        .i_Tx_DV    (r_Tx_DV),
        .i_Tx_Byte  (r_Tx_Byte),
        .o_Tx_Active(w_Tx_Active),
        .o_Tx_Serial(UART_TXD_IN),
        .o_Tx_Done  (w_Tx_Done)
    );

    // Echo logic
    always @(posedge CLK100MHZ) begin
        r_Tx_DV <= 1'b0; // default no send

        // When a byte is received and TX is idle
        if (w_Rx_DV && !w_Tx_Active) begin
            r_Tx_Byte <= w_Rx_Byte;
            r_Tx_DV   <= 1'b1; // trigger send
        end
    end

endmodule
