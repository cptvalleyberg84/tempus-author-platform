/**
 * Shopping cart quantity management functionality.
 *
 * Features:
 * - Real-time quantity input validation (1-99 range)
 * - Increment/decrement button handlers
 * - Input validation on manual entry
 * - Consistent behavior across all products
 *
 * Implementation:
 * - Uses vanilla JavaScript for DOM manipulation
 * - Event delegation for dynamic elements
 * - No external dependencies required
 */

document.addEventListener('DOMContentLoaded', function() {
    // Get all quantity inputs
    const qtyInputs = document.querySelectorAll('.qty_input');
    
    // Add event listeners to each input
    qtyInputs.forEach(input => {
        // Validate on input
        input.addEventListener('input', function() {
            let value = parseInt(this.value);
            if (isNaN(value) || value < 1) {
                this.value = 1;
            } else if (value > 99) {
                this.value = 99;
            }
        });
    });

    // Handle increment buttons
    document.querySelectorAll('.increment-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const input = this.closest('.input-group').querySelector('.qty_input');
            let value = parseInt(input.value);
            if (value < 99) {
                input.value = value + 1;
            }
        });
    });

    // Handle decrement buttons
    document.querySelectorAll('.decrement-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const input = this.closest('.input-group').querySelector('.qty_input');
            let value = parseInt(input.value);
            if (value > 1) {
                input.value = value - 1;
            }
        });
    });
});