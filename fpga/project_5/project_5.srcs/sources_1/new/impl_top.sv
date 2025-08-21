
// 
// Module: impl_top
// 
// Notes:
// - Top level module to be used in an implementation.
// - To be used in conjunction with the constraints/defaults.xdc file.
// - Ports can be (un)commented depending on whether they are being used.
// - The constraints file contains a complete list of the available ports
//   including the chipkit/Arduino pins.
//

module impl_top (
    input clk,              // Top level system clock input.
    input wire [4:0] sw,    // Slide switches.
    input wire [4:0] btn,   // Slide switches.
    input wire uart_rxd,    // UART Recieve pin.
    output wire uart_txd,   // UART transmit pin.
    output wire [15:0] led
    );
    
    parameter N = 8; // corresponds to the number of sites in the chain (change only here and NUM_BYTES_RX, NUM_BYTES_TX before programming)
    parameter CLK_HZ = 100000000; // in hertz
    parameter BIT_RATE = 9600; // needs to match the bitrate on pc
    parameter PAYLOAD_BITS = 8; // constant, do not change
    
    wire [PAYLOAD_BITS-1:0]  uart_rx_data;
    wire uart_rx_valid;
    wire uart_rx_break;
    
    wire [PAYLOAD_BITS-1:0]  uart_tx_data;
    wire uart_tx_busy;
    wire uart_tx_en;
    
    reg  [15:0]  led_reg;
    assign led = led_reg; // to be able to change in clock loop
    
    // ------------------------------------------------------------------------- 
    
    localparam NUM_BYTES_RX = (N + PAYLOAD_BITS - 1) / PAYLOAD_BITS; // (N + PAYLOAD_BITS) / PAYLOAD_BITS; // ceil(N / 8) bits needed to receive state
    localparam NUM_BYTES_TX = 1; // only 1 byte is needed to transmit l
    localparam L_WIDTH = $clog2(N+1);  // number of bits needed for l
    localparam PAD_WIDTH = PAYLOAD_BITS - L_WIDTH; // bits to pad when sending l
    
    reg [$clog2(NUM_BYTES_RX)-1:0] rx_count = 0;
    reg [$clog2(NUM_BYTES_TX)-1:0] tx_count = 0;
    
    reg [NUM_BYTES_RX*PAYLOAD_BITS-1:0] rx_buffer = 0;
    reg [NUM_BYTES_TX*PAYLOAD_BITS-1:0] tx_buffer = 0;
    wire [NUM_BYTES_TX*PAYLOAD_BITS-1:0] tx_buffer_wire;
    
    reg [PAYLOAD_BITS-1:0] uart_tx_data_reg;
    reg uart_tx_en_reg = 0;
    reg tx_busy_prev = 0;
    
    assign uart_tx_data = uart_tx_data_reg;
    assign uart_tx_en = uart_tx_en_reg;
    
    wire [N-1:0] r; // representative of the state
    wire [$clog2(N+1)-1:0] l; // number of bits needed to store int from 0 to N
    
    reg state = 0; // 0 for receiving 1 for sending
    
    symmetrization #(.N(N)) i_symmetrization (
        .in(rx_buffer), // use only the N bits that correspond to the state
        .r(r),
        .l(l)
    );
    
    assign led_reg = rx_buffer;
    assign tx_buffer_wire = { {PAD_WIDTH{1'b0}}, l }; // complete with 0 to get a full vyte
        
    // clock loop
    always @(posedge clk) begin
            
        uart_tx_en_reg <= 0;
        
        if (!sw[0]) begin // nothing
            
//            led_reg <= 8'b10101010;         
            state <= 0;
            rx_count <= 0;
            tx_count <= 0;
            rx_buffer <= 0;
            tx_buffer <= 0;
            
        end else if (!state) begin // receiving state
            
            if (uart_rx_valid) begin // receiving sth
            
                rx_buffer[PAYLOAD_BITS*(NUM_BYTES_RX - 1 - rx_count) +: PAYLOAD_BITS] <= uart_rx_data; // add byte to buffer
//                led_reg <= rx_buffer[PAYLOAD_BITS*rx_count +: PAYLOAD_BITS];
                
                if (rx_count == NUM_BYTES_RX - 1) begin
                
                    state <= 1; // change state to sending
                    tx_count <= 0;
                    
                end else begin
                
                    rx_count <= rx_count + 1;
                    
                end
            end
            
        end else if (state) begin // sending state
            
            if (tx_count == 0) begin
                tx_buffer <= tx_buffer_wire; // load send data to buffer. has to be here so that it doesn't miss the last byte sent
            end
            
            if (!uart_tx_busy && tx_busy_prev) begin // can transmit if tx_busy is 0 now and was 1 before
                // ^ this is needed to detect a falling edge of uart_tx_busy. otherwise some bytes don't get sent
            
                // uart_tx_data_reg <= 8'b10101010; 
                uart_tx_data_reg <= tx_buffer[PAYLOAD_BITS*(NUM_BYTES_TX - 1 - tx_count) +: PAYLOAD_BITS];
//                led_reg <= tx_buffer[PAYLOAD_BITS*tx_count +: PAYLOAD_BITS];
                uart_tx_en_reg <= 1; // trigger sending
                tx_busy_prev <= 0;
                    
                if (tx_count == NUM_BYTES_TX - 1) begin
                    
                    state <= 0; // change state to receiving
                    rx_count <= 0;
                    rx_buffer <= 0;
                    tx_buffer <= 0;
                    tx_busy_prev <= 0;
                    
                end else begin
                
                    tx_count <= tx_count + 1;
                    
                end
            end else begin
                tx_busy_prev <= 1;
            end
        end
    end
    
    
    // ------------------------------------------------------------------------- 
    
    //
    // UART RX (Receiver module)
    //
    uart_rx #(
        .BIT_RATE(BIT_RATE),
        .PAYLOAD_BITS(PAYLOAD_BITS),
        .CLK_HZ  (CLK_HZ)
        ) i_uart_rx (
        .clk          (clk          ), // Top level system clock input.
        .resetn       (sw[0]        ), // Asynchronous active low reset.
        .uart_rxd     (uart_rxd     ), // UART Recieve pin.
        .uart_rx_en   (1'b1         ), // Recieve enable
        .uart_rx_break(uart_rx_break), // Did we get a BREAK message?
        .uart_rx_valid(uart_rx_valid), // Valid data received and available.
        .uart_rx_data (uart_rx_data )  // The received data.
    );
    
    //
    // UART TX (Transmitter module)
    //
    uart_tx #(
        .BIT_RATE(BIT_RATE),
        .PAYLOAD_BITS(PAYLOAD_BITS),
        .CLK_HZ  (CLK_HZ)
        ) i_uart_tx (
        .clk          (clk          ),
        .resetn       (sw[0]        ),
        .uart_txd     (uart_txd     ),
        .uart_tx_en   (uart_tx_en   ),
        .uart_tx_busy (uart_tx_busy ),
        .uart_tx_data (uart_tx_data ) 
    );


endmodule