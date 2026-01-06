// admin-produto-images.js
// Show + buttons to reveal imagem_2 and imagem_3 fields in Django admin product form
(function() {
    function qs(name) { return document.querySelector(name); }

    function findFieldRowByInputName(name) {
        const input = document.querySelector('[name="' + name + '"]');
        if (!input) return null;
        // admin wraps inputs in .form-row or .field-<name> depending on version
        let row = input.closest('.form-row');
        if (!row) row = input.closest('.field-' + name);
        return row;
    }

    function init() {
        const mainRow = findFieldRowByInputName('imagem');
        const row2 = findFieldRowByInputName('imagem_2');
        const row3 = findFieldRowByInputName('imagem_3');
        if (!mainRow) return; // nothing to do

        // hide rows 2 and 3 initially if empty
        if (row2) {
            const input2 = row2.querySelector('input[type="file"]');
            if (input2 && !input2.value) row2.style.display = 'none';
        }
        if (row3) {
            const input3 = row3.querySelector('input[type="file"]');
            if (input3 && !input3.value) row3.style.display = 'none';
        }

        // create + button element
        const addBtn = document.createElement('button');
        addBtn.setAttribute('type', 'button');
        addBtn.setAttribute('aria-label', 'Adicionar mais imagens');
        addBtn.className = 'add-image-btn';
        addBtn.style.marginLeft = '8px';
        addBtn.style.padding = '4px 8px';
        addBtn.style.borderRadius = '4px';
        addBtn.style.border = '1px solid #ccc';
        addBtn.style.background = '#fff';
        addBtn.style.cursor = 'pointer';
        addBtn.textContent = '+';

        // place button after the input or label in mainRow
        const reference = mainRow.querySelector('input[type="file"]') || mainRow.querySelector('label');
        if (reference && reference.parentNode) {
            reference.parentNode.insertBefore(addBtn, reference.nextSibling);
        } else {
            mainRow.appendChild(addBtn);
        }

        function revealNext() {
            if (row2 && row2.style.display === 'none') {
                row2.style.display = '';
                // focus the file input
                const in2 = row2.querySelector('input[type="file"]');
                if (in2) in2.focus();
                return;
            }
            if (row3 && row3.style.display === 'none') {
                row3.style.display = '';
                const in3 = row3.querySelector('input[type="file"]');
                if (in3) in3.focus();
                return;
            }
            // reached max (3) -> disable button
            addBtn.disabled = true;
            addBtn.style.opacity = '0.6';
            addBtn.title = 'Máximo de 3 imagens atingido';
        }

        addBtn.addEventListener('click', function(e) {
            e.preventDefault();
            revealNext();
        });

        // If file inputs are filled (e.g., editing existing product), ensure button state
        function updateButtonState() {
            const visibleCount = [mainRow, row2, row3].filter(r => r && r.style.display !== 'none').length;
            if (visibleCount >= 3) {
                addBtn.disabled = true;
                addBtn.style.opacity = '0.6';
            } else {
                addBtn.disabled = false;
                addBtn.style.opacity = '1';
            }
        }

        // Watch for changes in inputs (in case user clears or fills them)
        [row2, row3].forEach(r => {
            if (!r) return;
            const input = r.querySelector('input[type="file"]');
            if (!input) return;
            input.addEventListener('change', updateButtonState);
        });

        updateButtonState();
    }

    // Run when admin form is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
