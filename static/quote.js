$(document).ready(function () {
    $('#lookupButton').click(function () {
        const symbol = $('#stockSymbolInput').val();
                // Check if the symbol is not empty
                if (symbol.trim() === '') {
                    $('#stockSymbolResult').html('<p>Please enter a stock symbol.</p>');
                    return;
                }

                // Fetch the stock price using your Flask route
                $.ajax({
                    url: '/quote/' + symbol,  // Use your Flask route for fetching the price
                    type: 'GET',
                    dataType: 'json',
                    success: function (data) {
                        if (data.current_price !== undefined) {
                            $('#stockSymbolResult').html('<p>Price: $' + data.current_price + '</p>');
                        } else {
                            $('#stockSymbolResult').html('<p>Symbol not found.</p>');
                        }
                    },
                    error: function () {
                        $('#stockSymbolResult').html('<p>Lookup failed. Please try again later.</p>');
                    }
                });
            });
        });