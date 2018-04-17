$(document).ready(function() {
  setUpDatepicker();
});

function getDateString() {
  return $('#datepicker').datepicker('getDate').toJSON().substr(0,10);
}

function setUpDatepicker() {
  $("#datepicker").datepicker({
    onSelect: setUpClassButtons
  }).datepicker("setDate", new Date());

  setUpClassButtons();
}

function setUpClassButtons() {
  $.get('http://0.0.0.0:5000/classes',
    {date: getDateString()},
    function(data) {
      const buttonDiv = document.getElementById('classes');
      buttonDiv.innerHTML = '';

      for (let d of data) {
        buttonDiv.appendChild(createButton(d));
      }
    }
  );
}

function createButton(data) {
  let button = document.createElement('button');
  button.innerHTML = data.name;
  button.className = 'class-button nav-button';
  button.dataset.key = data.key;
  button.onclick = setUpRoster;

  return button;
}

function setUpRoster() {
  const date = getDateString();
  const classKey = this.getAttribute("data-key");
  $.get('http://0.0.0.0:5000/roster',
    {date: date, class: classKey},
    function(data) {
      const main = document.getElementById('main');
      main.innerHTML = '';
      main.appendChild(createTable(data));
    }
  );
}

function createTable(data) {
  const table = document.createElement('table');
  const headerRow = document.createElement('tr');
  headerRow.innerHTML = '<td>Student Name</td><td>Sign In</td><td>Sign Out</td>'
  table.appendChild(headerRow);

  for (let d of data) {
    let row = document.createElement('tr');
    
    let tdName = document.createElement('td');
    tdName.innerHTML = d.name;
    
    let tdIn = document.createElement('td');
    tdIn.innerHTML = d.in;

    let tdOut = document.createElement('td');
    tdOut.innerHTML = d.out;

    row.appendChild(tdName);
    row.appendChild(tdIn);
    row.appendChild(tdOut);

    table.appendChild(row);
  }

  return table;
}
