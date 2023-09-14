$(document).ready(function () {
    console.log("Doc Ready")
    const stockInput = $('#stockInput');
    const searchResults = $('#searchResults');

    stockInput.on('input', function () {
        const searchTerm = $(this).val();
        if (searchTerm) {
            console.log("Search Working")
            fetchSearchResults(searchTerm);
        } else {
            searchResults.empty();
        }
    });

    function fetchSearchResults(searchTerm) {
        const apiKey = "N1K9PC5HBHHQJPCM";
        const url = `https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=${searchTerm}&apikey=${apiKey}`;

        $.getJSON(url, function (data) {
            searchResults.empty();

            if (data.bestMatches) {
                data.bestMatches.forEach(function (match) {
                    const listItem = `<li><a href="#" data-symbol="${match['1. symbol']}">${match['2. name']} (${match['1. symbol']})</a></li>`;
                    searchResults.append(listItem);
                });
            }
        });
    }

    searchResults.on('click', 'a', function (event) {
        event.preventDefault();
        const symbol = $(this).data('symbol');
        stockInput.val(symbol); // Set the input value to the selected symbol
        searchResults.empty(); // Clear the autocomplete suggestions

        // Load the form template using jQuery's AJAX
        $.get('/get-add-stock-form/' + symbol, function (response) {
            $('body').append(response);

            // Handle form submission
            $('#stockForm').submit(function (event) {
                event.preventDefault();
                const transactionType = $("#transactionType").val();
                const shareQuantity = parseFloat($('#shareQuantity').val());
                const purchasePrice = parseFloat($('#purchasePrice').val());
                const date = $('#date').val();

                const stockData = {
                    symbol: symbol,
                    name: symbol,
                    purchasePrice: purchasePrice,
                    quantity: shareQuantity,
                    date: date,
                    transactionType: transactionType
                };

                if (transactionType === 'buy') {
                    $.ajax({
                        method: 'POST',
                        url: '/add-stock',
                        contentType: 'application/json',
                        data: JSON.stringify(stockData),
                        success: function (response) {
                            console.log(response.message);
                            $('#stockForm').remove(); // Remove the form after submission
                        },
                        error: function (error) {
                            console.error('Error:', error);
                        },
                    });
                }
                else if (transactionType==='sell'){
               $.ajax({
                        method: 'POST',
                        url: '/sell-stock',
                        contentType: 'application/json',
                        data: JSON.stringify(stockData),
                        success: function (response) {
                            console.log(response.message);
                            $('#stockForm').remove(); // Remove the form after submission
                        },
                        error: function (error) {
                            console.error('Error:', error);
                        },
                    });
                }
            });
        });
    });
});