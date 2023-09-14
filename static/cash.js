$(document).ready(function () {
    $('#cashForm').submit(function (event) {
        event.preventDefault(); // Prevent the form from submitting via HTTP
        const transactionType = $("#cashTransactionType").val();
        const amount = parseFloat($('#cashAmount').val());
        const memo = $('#memo').val();

        // Create a JavaScript object with form data
        const formData = {
            transactionType: transactionType,
            amount: amount,
            memo: memo
        };

        if (transactionType === 'deposit') {
            $.ajax({
                type: 'POST',
                url: '/deposit-cash', // Replace with your actual endpoint URL
                data: JSON.stringify(formData),
                contentType: 'application/json',
                success: function (response) {
                    console.log(response); // Handle the server response here
                    window.location.href = '/';
                },
                error: function (error) {
                    console.error('Error:', error);
                },
            });
        }
        else if (transactionType === 'withdraw') {
            $.ajax({
                type: 'POST',
                url: '/withdraw-cash', // Replace with your actual endpoint URL
                data: JSON.stringify(formData),
                contentType: 'application/json',
                success: function (response) {
                    console.log(response); // Handle the server response here
                    window.location.href = '/';
                },
                error: function (error) {
                    console.error('Error:', error);
                },
            });
        }
    });
});
