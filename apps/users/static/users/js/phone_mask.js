jQuery(document).ready(function ($) {
    var phoneInput = $('input[name="phone"]');

    phoneInput.inputmask({
        "mask": "+\\9\\98 (99) 999-99-99",
        "placeholder": "_",
        "clearIncomplete": true
    });

    $('form').on('submit', function() {
        var clean = phoneInput.val().replace(/^\+998|\D/g, '');
        phoneInput.val(clean);
    });
});
