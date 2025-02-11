/**
 * Shopping cart quantity management functionality.
 * 
 * Features:
 * - Quantity input validation (1-99 range)
 * - Increment/decrement buttons with proper disabling
 * - Custom input styling to remove browser spinners
 * - Real-time quantity updates
 * - Form submission handling
 * 
 * Dependencies:
 * - jQuery for DOM manipulation and event handling
 * - Bootstrap for input group styling
 */

$(document).ready(function() {
    
    // Disable +/- buttons outside 1-99 range and validate input
    function handleEnableDisable(itemId) {
        var currentValue = parseInt($(`#id_qty_${itemId}`).val());
        
        // Validate and correct the input value
        if (isNaN(currentValue) || currentValue < 1) {
            currentValue = 1;
        } else if (currentValue > 99) {
            currentValue = 99;
        }
        
        // Update the input value if it was corrected
        $(`#id_qty_${itemId}`).val(currentValue);
        
        var minusDisabled = currentValue < 2;
        var plusDisabled = currentValue > 98;
        $(`#decrement-btn_${itemId}`).prop('disabled', minusDisabled);
        $(`#increment-btn_${itemId}`).prop('disabled', plusDisabled);
    }

    // Ensure proper enabling/disabling of all inputs on page load
    var allQtyInputs = $('.qty_input');
    
    // Apply styles and attributes to disable browser spinners
    allQtyInputs.css({
        '-webkit-appearance': 'textfield',
        '-moz-appearance': 'textfield',
        'appearance': 'textfield'
    });
    
    allQtyInputs.attr({
        'type': 'number',
        'min': '1',
        'max': '99',
        'pattern': '[1-9][0-9]?'
    });
    
    for(var i = 0; i < allQtyInputs.length; i++){
        var itemId = $(allQtyInputs[i]).data('item_id');
        handleEnableDisable(itemId);
    }

    // Check enable/disable every time the input is changed
    $('.qty_input').on('input change', function() {
        var itemId = $(this).data('item_id');
        handleEnableDisable(itemId);
    });

    // Increment quantity
    $('.increment-btn').click(function(e) {
       e.preventDefault();
       var closestInput = $(this).closest('.input-group').find('.qty_input');
       var currentValue = parseInt(closestInput.val());
       closestInput.val(currentValue + 1).change();
       var itemId = $(this).data('item_id');
       handleEnableDisable(itemId);
    });

    // Decrement quantity
    $('.decrement-btn').click(function(e) {
       e.preventDefault();
       var closestInput = $(this).closest('.input-group').find('.qty_input');
       var currentValue = parseInt(closestInput.val());
       closestInput.val(currentValue - 1).change();
       var itemId = $(this).data('item_id');
       handleEnableDisable(itemId);
    });

    // Update quantity on click
    $('.update-link').click(function(e) {
        var form = $(this).prev('.update-form');
        form.submit();
    })
})