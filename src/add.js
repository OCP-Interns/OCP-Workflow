function changeBodyContent() {
    var bodyDiv = document.querySelector('.body');
    
    if (!window.originalBodyContent) {
        window.originalBodyContent = bodyDiv.innerHTML;
    }
    
    // Check if the card already exists
    if (!document.getElementById('add')) {
        // Get the card template
        var template = document.getElementById('card-template');
        var card = template.content.cloneNode(true);

        bodyDiv.appendChild(card);

        // Populate the "from" and "to" select elements
        var opF = document.getElementById('from');
        var opT = document.getElementById('to');
        for (let i = 0; i < 24; i++) {
            var optionT = document.createElement('option');
            let hour = i < 10 ? '0' + i : i;
            optionT.value = optionT.text = `${hour}:00`;
            opF.appendChild(optionT);
            opT.appendChild(optionT.cloneNode(true));
        }
    } else {
        // If the card exists, just make it visible
        document.getElementById('add').style.display = "block";
    }
}

document.addEventListener('DOMContentLoaded', function () {
    // Initial population of select elements if needed
    let options = '';
    for (let i = 0; i < 24; i++) {
        let hour = i < 10 ? '0' + i : i;
        options += `<option value="${hour}:00">${hour}:00</option>`;
    }
    document.querySelectorAll('.from, .to').forEach(select => {
        select.innerHTML = options;
    });
});

function restoreOriginalContent() {
    var overlay = document.querySelector('.card');
    if (overlay) {
        overlay.remove();
    }
}
