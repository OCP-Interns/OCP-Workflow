function showEditForm() {
    document.getElementById('edit-form').style.display = 'block';
    document.getElementById('timetable').style.display = 'none';
}

function showTimetable() {
    document.getElementById('edit-form').style.display = 'none';
    document.getElementById('timetable').style.display = 'block';
}

function handleADD_show() {
    document.getElementById('card').style.display = 'block';

    var opF = document.getElementById('from');
    var opT = document.getElementById('To');
    for (let i = 0; i < 24; i++) {
        var optionT = document.createElement('option');
        let hour = i < 10 ? '0' + i : i;
        optionT.value = optionT.text = `${hour}:00`;
        opF.appendChild(optionT);
        opT.appendChild(optionT.cloneNode(true));
    }

}

function handleADD_hide() {
    document.getElementById('card').style.display = 'none';
}

function addTableTimeTonJson(event) {
    event.preventDefault();

    const dayElement = document.getElementById('day');
    const fromElement = document.getElementById('from');
    const toElement = document.getElementById('To'); 

    if (!dayElement || !fromElement || !toElement) {
        console.error('One or more elements not found');
        return;
    }

    const day = dayElement.value;
    const from = fromElement.value;
    const to = toElement.value;

    const timetable = {
        day: day,
        from: from,
        to: to
    };

    console.log(timetable);

    document.getElementById('timetable_json').value = JSON.stringify(timetable);

    event.target.submit();
}

document.addEventListener('DOMContentLoaded', () => {
    console.log(`matricule: ${employeeNum}`);
    fetch(`http://localhost:5000/timetable/${employeeNum}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not okay ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            console.log('Data fetched successfully: ', data);
            const timetable = data.timetable;
            timetable.forEach(entry => {
                const day = entry.day;
                const from = entry.from;
                const to = entry.to;

                let [fromH, fromM] = from.split(':').map(Number);
                let [toH, toM] = to.split(':').map(Number);

                let firstHour = fromH;
                let lastHour = toH

                const time1 = `${firstHour < 10 ? '0' : ''}${firstHour}:00`;
                const cellID1 = `${day}-${time1}`;
                const cell1 = document.getElementById(cellID1);
                const time2 = `${lastHour < 10 ? '0' : ''}${lastHour}:00`;
                const cellID2 = `${day}-${time2}`
                const cell2 = document.getElementById(cellID2)

                console.log(cellID1);

                if (cell1 || cell2) {
                    console.log('OK')
                    cell1.style.backgroundColor = 'black';
                    const btn = document.createElement('button');
                    btn.classList.add('deleteBtn');
                    btn.addEventListener('click', () => HandleEvent_Delete(day, time1));
                    cell1.appendChild(btn);
                    cell2.style.backgroundColor = 'black';
                } else {
                    console.error(`No cell found for ID: ${cellID1}`);
                }

            });
        })
        .catch(error => console.error('Error fetching timetable: ', error));
});
    
function HandleEvent_Delete (day, time) {
    const params = new URLSearchParams({
        day: day,
        time: time
    });

    console.log('params in js: ', params)

    fetch(`http://localhost:5000/deleteTableTime/${regNum}?${params.toString()}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('deleted successfully: ', data);
    })
    .catch(error => console.error('Error: ', error));
}