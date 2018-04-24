const url = 'http://0.0.0.0:5000/';

function start() {
  setupDatepicker();
  setupWhosHere();
};

start();

function getDateString() {
  return $('#datepicker').datepicker('getDate').toJSON().substr(0,10);
}

function setupDatepicker() {
  $("#datepicker").datepicker({
    onSelect: setupClassButtons
  }).datepicker("setDate", new Date());

  setupClassButtons();
}

function setupClassButtons() {
  $.get(url + 'classes',
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

function setupWhosHere() {
  const whoshere = document.getElementsByClassName('whois-button')[0];

  whoshere.onclick = function() {
    $.get(url + 'whoshere',
      function(data) {
        const main = document.getElementById('main');
        const cont = document.createElement('div');
        const h1 = document.createElement('h1');
        h1.innerHTML = "Who's here?";
        cont.className = 'table-container';
        main.innerHTML = '';
        main.appendChild(cont);
        cont.appendChild(h1);
        cont.appendChild(createWhosHereTable(data));
      }
    );
  }
}

function createButton(data) {
  let button = document.createElement('button');
  button.innerHTML = data.name;
  button.className = 'class-button nav-button';
  button.dataset.key = data.key;
  button.onclick = setupRoster;

  return button;
}

function setupRoster() {
  const date = getDateString();
  const classKey = this.getAttribute("data-key");
  const className = this.innerHTML;
  $.get(url + 'roster',
    {date: date, class: classKey},
    function(data) {
      const main = document.getElementById('main');
      const cont = document.createElement('div');
      const h1 = document.createElement('h1');
      h1.innerHTML = className;
      cont.appendChild(h1);
      cont.className = 'table-container';
      main.innerHTML = '';
      main.appendChild(cont);
      cont.appendChild(createRosterTable(data));
    }
  );
}

function createRosterTable(data) {
  const table = document.createElement('table');
  table.className = 'student-table';
  const headerRow = document.createElement('tr');
  headerRow.innerHTML = '<th>Student Name</th><th>Sign In</th><th>Sign Out</th>'
  table.appendChild(headerRow);

  for (let d of data) {
    let row = document.createElement('tr');
    
    let tdName = document.createElement('td');
    tdName.appendChild(createStudentLink(d));
    
    let tdIn = document.createElement('td');
    tdIn.appendChild(createCheckbox(d.in, "in", d.key));

    let tdOut = document.createElement('td');
    tdOut.appendChild(createCheckbox(d.out, "out", d.key));

    row.appendChild(tdName);
    row.appendChild(tdIn);
    row.appendChild(tdOut);

    table.appendChild(row);
  }

  return table;
}

function createWhosHereTable(data) {
  const table = document.createElement('table');
  table.className = 'student-table';
  const headerRow = document.createElement('tr');
  headerRow.innerHTML = '<th>Name</th>'
  table.appendChild(headerRow);

  for (let d of data) {
    let row = document.createElement('tr');
    
    let tdName = document.createElement('td');
    tdName.appendChild(createStudentLink(d));
    
    row.appendChild(tdName);
    table.appendChild(row);
  }

  return table;
}


function createStudentLink(data) {
  const link = document.createElement('a');
  link.innerHTML = data.name;
  link.className = 'link';
  link.dataset.key = data.key;
  link.onclick = setupStudentPage;
  return link;
}

function createCheckbox(checked, inOrOut, key) {
  const checkId = inOrOut + key;
  const cont = document.createElement("div");
  const check = document.createElement("input");
  const label = document.createElement("label");

  check.type = "checkbox";
  check.checked = checked;
  check.className = "sign";
  check.id = checkId;
  check.dataset.key = key;
  
  if (inOrOut === 'in') {
    check.onclick = signStudentIn;
  } else {
    check.onclick = signStudentOut;
  }


  label.htmlFor = checkId;
  
  cont.appendChild(check);
  cont.appendChild(label);

  return cont;
}

function setupStudentPage() {
  const key = this.getAttribute('data-key');
  $.get(url + 'student',
    {student: key},
    function(data) {
      const main = document.getElementById('main');
      const cont = document.createElement('div');
      cont.className = 'main-container';
      main.innerHTML = '';
      main.appendChild(cont);
      cont.innerHTML = data;
    }
  );
}

function signStudentIn() {
  alert('sign in - ' + this.getAttribute('data-key') + ' - ' + this.checked);
}

function signStudentOut() {
  alert('sign out - ' + this.getAttribute('data-key') + ' - ' + this.checked);
}
