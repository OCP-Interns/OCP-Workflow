function changeBodyContent_add() {
    var bodyDiv = document.querySelector('.body');
    if (!window.originalBodyContent) {
        window.originalBodyContent = bodyDiv.innerHTML;
    }

    if (!document.getElementById('add')) {
        var template = document.getElementById('card-template_add');
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

    document.getElementById('timeWorkForm').addEventListener('submit', e => {
        e.preventDefault();
        const forme = new FormData(e.currentTarget)
        console.log(forme)

        fetch('http://localhost:5000/addTime', {
            method: 'POST',
            headers: {
                'Content-Type':'application/json'
            },
            // index=> python ///// get(htmlName)
            body: JSON.stringify({
                day: forme.get('day'),
                from: forme.get('from'),
                to: forme.get('to')
            })
        })
        .then(response => {
            restoreOriginalContent();
            return response.json();
        })
    })
    
};

function restoreOriginalContent() {
    var overlay = document.querySelector('.card');
    if (overlay) {
        overlay.remove();
    }
};

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

                let [fromH1, fromH2] = from.split(':').map(Number);
                let [toH1, toH2] = to.split(':').map(Number);

                let currentHour = fromH1;
                let currentHour2 = fromH2;

               
                const time = `${currentHour < 10 ? '0' : ''}${currentHour}:${currentHour2 < 10 ? '0' : ''}${currentHour2}`;
                const cellId = `${day}-${time}`;
                const cell = document.getElementById(cellId);

                console.log(`Looking for cell with ID: ${cellId}`);

                if (cell) {                        
                    cell.style.backgroundColor = 'black';
                    const btn = document.createElement('button');
                    btn.classList.add('deletebtn');
                    btn.addEventListener('click', () => HandleEvent(day, time));
                    cell.appendChild(btn);
                    console.log('Updated cell:', cell);
                } else {
                    console.error(`No cell found for ID: ${cellId}`);
                }

                    
            });
        })
        .catch(error => console.error('Error fetching timetable:', error));

});

function HandleEvent(day, from) {
    fetch('http://localhost:5000/DeleteWork', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `day=${encodeURIComponent(day)}&from=${encodeURIComponent(from)}`
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        console.log('Delete successful:', data);
    })
    .catch(error => console.error('Error deleting entry:', error));
}




