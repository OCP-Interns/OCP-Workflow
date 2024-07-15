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
            let nextH = parseInt(hour) + 1;
            if(hour < 9) {
                nextH = '0' + nextH;
            }
            optionT.value = optionT.text = `${hour}:${nextH}`;
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

document.addEventListener("DOMContentLoaded", function() {
    fetch('http://localhost:5000/SelectTable')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            console.log('Data fetched successfully:', data);
            const timetable = data.timetable;
            timetable.forEach(entry => {
                const day = entry.day;
                const from = entry.from;
                const to = entry.to;

                const [fromH1, fromH2] = from.split(':').map(Number);
                const [toH1, toH2] = to.split(':').map(Number);

                let currentHour = fromH1;
                let currentHour2 = fromH2;

                while (currentHour < toH1 || (currentHour === toH1 && currentHour2 < toH2)) {
                    const time = `${currentHour < 10 ? '0' : ''}${currentHour}:${currentHour2 < 10 ? '0' : ''}${currentHour2}`;
                    const cellId = `${day}-${time}`;
                    const cell = document.getElementById(cellId);

                    console.log(`Looking for cell with ID: ${cellId}`);

                    if (cell) {
                        cell.style.backgroundColor = 'black';
                        console.log('Updated cell:', cell);
                    } else {
                        console.error(`No cell found for ID: ${cellId}`);
                    }

                    currentHour2++;
                    if (currentHour2 === 60) {
                        currentHour2 = 0;
                        currentHour++;
                    }
                }
            });
        })
        .catch(error => console.error('Error fetching timetable:', error));
});

