function changeBodyContent() {
    var bodyDiv = document.querySelector('.body');

    if (!window.originalBodyContent) {
        window.originalBodyContent = bodyDiv.innerHTML;
    }

    if (!document.getElementById('add')) {
        var template = document.getElementById('card-template');
        var card = template.content.cloneNode(true);

        bodyDiv.appendChild(card);

        var opF = document.getElementById('from');
        var opT = document.getElementById('to');
        for (let i = 0; i < 24; i++) {
            var optionT = document.createElement('option');
            let hour = i < 10 ? '0' + i : i;
            optionT.value = optionT.text = `${hour}:00`;
            opF.appendChild(optionT);
            opT.appendChild(optionT.cloneNode(true));
        }

        card.querySelector('.back').addEventListener('click', function (e) {
            e.preventDefault();
            restoreOriginalContent();
        });

    } else {
        document.getElementById('add').style.display = "block";
    }

    
}

function restoreOriginalContent() {
    var overlay = document.querySelector('.card');
    if (overlay) {
        overlay.remove();
    }
}

