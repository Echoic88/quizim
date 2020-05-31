$(document).ready(function () {
    // Set your publishable key: remember to change this to your live publishable key in production
    // See your keys here: https://dashboard.stripe.com/account/apikeys

    let pyData = JSON.parse(document.getElementById("stripe_context").textContent);
    let clientSecret = pyData.client_secret;
    let publishable_key = pyData.publishable;


    var stripe = Stripe(publishable_key);
    var elements = stripe.elements();

    // Set up Stripe.js and Elements to use in checkout form
    var style = {
        base: {
            color: "#32325d",
        }
    };

    //Create and mount card elements
    var cardNumber = elements.create("cardNumber", {
        style: style
    });
    var cardExpiry = elements.create("cardExpiry", {
        style: style
    });
    var cardCvc = elements.create("cardCvc", {
        style: style
    });

    cardNumber.mount("#cardNumber");
    cardExpiry.mount("#cardExpiry");
    cardCvc.mount("#cardCvc");


    // extract billing details from Payment Details form
    // the carholder and address details will prepoulate based on 
    // User and Profile models however if a user wants to enter
    // a different address or cardholder the getBillingDetails
    // function will extract information that a user has entered
    // 
    function getBillingDetails() {
        let formData = $("#paymentDetailsForm").serializeArray();
        let cardHolder = formData[0].value;
        let address = {
            "line1": formData[1].value,
            "line2": formData[2].value,
            "city": formData[3].value,
            "postal_code": formData[4].value,
        };
        let billingDetails = {
            "name": cardHolder,
            "address": address
        };
        return billingDetails;
    }

    //accept payment on paymentForm submit
    let form = document.getElementById("paymentForm");

    form.addEventListener("submit", function (ev) {
        ev.preventDefault();
        $(".stripe-spinner").show();
        $("#paymentButton").hide();
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                type: "card",
                card: cardNumber,
                billing_details: getBillingDetails()
            }
        }).then(function (result) {
            $(".stripe-spinner").hide();
            if (result.error) {
                $("#stripe-error-message").text(result.error.message);
                $("#credit-card-errors").show();
                $("#paymentButton").show();
            } else {
                // The payment has been processed!
                if (result.paymentIntent.status === "succeeded") {
                    form.submit();
                }
            }
        });
    });
});