function handleADD_show() {
    document.getElementById('card').style.display = 'block';

    var opF = document.getElementById('from');
    var opT = document.getElementById('to');
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

function addTimeTableToJson(event) {
    event.preventDefault();

    const dayElement = document.getElementById('day');
    const fromElement = document.getElementById('from');
    const toElement = document.getElementById('to'); 

    if (!dayElement || !fromElement || !toElement) {
        console.error('One or more elements not found');
        return;
    }

    const day = dayElement.value;
    const from = fromElement.value;
    const to = toElement.value;

    const fromHour = parseInt(from.split(':')[0]);
    const toHour = parseInt(to.split(':')[0]);

    const timetableEntries = [];

    function getNextDay(currentDay) {
        const daysOfWeek = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
        const currentIndex = daysOfWeek.indexOf(currentDay);
        const nextIndex = (currentIndex + 1) % daysOfWeek.length;
        return daysOfWeek[nextIndex];
    }

    if (fromHour >= toHour) {
        for (let hour = fromHour; hour < 24; hour++) {
            const entry = {
                day: day,
                from: `${hour < 10 ? '0' + hour : hour}:00`,
                to: `${hour + 1 < 10 ? '0' + (hour + 1) : hour + 1}:00`
            };
            timetableEntries.push(entry);
        }
        
        const nextDay = getNextDay(day);
        for (let hour = 0; hour < toHour; hour++) {
            const entry = {
                day: nextDay,
                from: `${hour < 10 ? '0' + hour : hour}:00`,
                to: `${hour + 1 < 10 ? '0' + (hour + 1) : hour + 1}:00`
            };
            timetableEntries.push(entry);
        }
    } else {
        for (let hour = fromHour; hour < toHour; hour++) {
            const entry = {
                day: day,
                from: `${hour < 10 ? '0' + hour : hour}:00`,
                to: `${hour + 1 < 10 ? '0' + (hour + 1) : hour + 1}:00`
            };
            timetableEntries.push(entry);
        }
    }

    console.log('timetable list: ', timetableEntries);
    document.getElementById('timetable_json').value = JSON.stringify(timetableEntries);
}

document.addEventListener('DOMContentLoaded', () => {
    console.log(`matricule: ${employeeNum}`);
    fetch(`/timetable/json/${employeeNum}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not okay ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            console.log('Data fetched successfully: ', data);
            
            const timetable = JSON.parse(data.timetable || '{}');
            console.log('Timetable: ', timetable);

            for (const day in timetable) {
                const entries = timetable[day];
                entries.forEach(entry => {
                    const from = entry.from;
                    const to = entry.to;
                    
                    const fromH = parseInt(from.split(':')[0]);
                    const toH = parseInt(to.split(':')[0]);

                    for (let i = fromH; i < toH; i++) {
                        const cellID = `${day}-${i < 10 ? '0' + i : i}`;
                        const cell = document.getElementById(cellID);
                        if (cell) {
                            cell.classList.add('filled');
                            cell.style.backgroundColor = 'black';  

                            if (!cell.querySelector('button')) {
                                const button = document.createElement('button');
                                button.className = 'trash'
                                button.addEventListener('click', () => handleDelete(employeeNum, day, from));
                                cell.appendChild(button);
                            }
                        } else {
                            console.error(`No cell found for ID: ${cellID}`);
                        }
                    }
                });
            }
        })
        .catch(error => console.error('Error fetching timetable: ', error));
});


function handleDelete(personnelRegNum, day, fromTime) {
    console.log(`id: ${personnelRegNum}, day: ${day}, time: ${fromTime}`)
    fetch(`/delete-timetable-entry/${personnelRegNum}`, {
        method: 'POST',
        body: new URLSearchParams({
            'day': day,
            'from': fromTime
        })
    })
    .then(response => {
        console.log()
        if (!response.ok) {
            throw new Error('Network response was not okay');
        }
        return response.json();
    })
    .then(data => {
        window.location.href = `/edit-employee-timetable/${employeeNum}`;
        console.log('Success:', data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

