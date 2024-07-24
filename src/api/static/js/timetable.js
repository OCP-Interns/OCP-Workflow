//function showEditForm() {
//    document.getElementById('edit-employee-form').style.display = 'flex';
//    document.getElementById('timetable').style.display = 'none';
//}

//function showTimetable() {
//    document.getElementById('edit-employee-form').style.display = 'none';
//    document.getElementById('timetable').style.display = 'block';
//}

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

    const timetable = {
        day: day,
        from: from,
        to: to
    };

    console.log(timetable);
    document.getElementById('timetable_json').value = JSON.stringify(timetable);
    //!event.target.submit();
}

document.addEventListener('DOMContentLoaded', () => {

    console.log(`matricule: ${employeeNum}`);
    fetch(`http://localhost:5000/edit-employee-timetable/json/${employeeNum}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not okay ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            console.log('Data fetched successfully: ', data);
			
			//* HERE
			// Convert the timetable JSON string to an object
			const timetable = JSON.parse(data.timetable);
			console.log('Timetable: ', timetable);

			// Iterate over the timetable entries
			for (const day in timetable) {
				// Get the entries (intervals) for the current day
				const entries = timetable[day];
				// Iterate over the entries and add the `filled` class to the cells
				entries.forEach(entry => {
					const from = entry.from;
					const to = entry.to;
					
					// Add the class `filled` to the cells that are occupied (including the cells in between)
					const fromH = parseInt(from.split(':')[0]);
					const toH = parseInt(to.split(':')[0]);
					var cells = [];
					// Iterate over the hours in the interval
					for (let i = fromH; i < toH; i++) {
						// Select cells by their ID (composed of the day and the hour)
						const cellID = `${day}-${i < 10 ? '0' + i : i % 24}`;
						const cell = document.getElementById(cellID);
						if (cell) {
							cell.classList.add('filled');
							cells.push(cell);
						} else {
							console.error(`No cell found for ID: ${cellID}`);
						}
					}
				});
			}

			//?{
            //const timetable = data.timetable;
            //timetable.forEach(entry => {
            //    const day = entry.day;
            //    const from = entry.from;
            //    const to = entry.to;

            //    let [fromH, fromM] = from.split(':').map(Number);
            //    let [toH, toM] = to.split(':').map(Number);

            //    let firstHour = fromH;
            //    let lastHour = toH

            //    const time1 = `${firstHour < 10 ? '0' : ''}${firstHour}:00`;
            //    const cellID1 = `${day}-${time1}`;
            //    const cell1 = document.getElementById(cellID1);
            //    const time2 = `${lastHour < 10 ? '0' : ''}${lastHour}:00`;
            //    const cellID2 = `${day}-${time2}`
            //    const cell2 = document.getElementById(cellID2)

            //    console.log(cellID1);

            //    if (cell1 || cell2) {
            //        console.log('OK')
            //        cell1.style.backgroundColor = 'black';
            //        cell2.style.backgroundColor = 'black';
            //    } else {
            //        console.error(`No cell found for ID: ${cellID1}`);
            //    }

            //});
			//?}
        })
        .catch(error => console.error('Error fetching timetable: ', error));
});
    
