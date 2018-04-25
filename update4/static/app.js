const url = 'http://0.0.0.0:5000/';

function start() {
  setupDatepickerAndClasses();
  setupWhosHere();
};

start();

function getDateString(id) {
  /* return the data as a string from the dakerpicker with the specified id */
  return $('#' + id).datepicker('getDate').toJSON().substr(0,10);
}

function createButton(name, key, className, text, clickFcn) {
  const btn = document.createElement('button');
  btn.className = className;
  btn.dataset.key = key;
  btn.dataset.name = name;
  btn.innerHTML = text;
  btn.onclick = clickFcn;
  return btn;
}

function createNode(kind, id, className, inner) {
  const node = document.createElement(kind);
  if (id) node.id = id;
  if (className) node.className = className;
  if (inner) node.innerHTML = inner;
  return node;
}

function createDiv(id, className) {
  return createNode('div', id, className, '');
}

function setupDatepickerAndClasses() {
  /* create the classes datepicker and then set up the class buttons */
  $("#datepicker").datepicker({
    onSelect: setupClassButtons
  }).datepicker("setDate", new Date());

  setupClassButtons();
}

function setupClassButtons() {
  /* use the api to get the classes for the day and create the buttons */
  $.get(url + 'classes',
    {date: getDateString('datepicker')},
    function(data) {
      const buttonDiv = document.getElementById('classes');
      buttonDiv.innerHTML = '';

      for (let d of data) {
        buttonDiv.appendChild(createButton(d.name, d.key, 'class-button nav-button', d.name, setupRoster));
      }
    }
  );
}

function setupWhosHere() {
  /* when the user clicks the who's here button, create the who's here page */
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

function setupRoster() {
  /* when a class button is clicked, setup the class roster */
  const date = getDateString('datepicker');
  const classKey = this.getAttribute("data-key");
  const className = this.getAttribute("data-name");
  // use the api to get the class info for this day
  $.get(url + 'roster',
    {date: date, class: classKey},
    function(data) {
      const main = document.getElementById('main');
      const cont = document.createElement('div');
      const h1 = document.createElement('h1');
      h1.innerHTML = className;
      cont.className = 'table-container';
      main.innerHTML = '';
      main.appendChild(cont);
      cont.appendChild(h1);
      cont.appendChild(createButton(className, classKey, 'go-to-rate', 'Attendance Rate Info', setupAttendanceRatePage));
      cont.appendChild(createRosterTable(data));
    }
  );
}

function setupAttendanceRatePage() {
  /* set up page to allow user to calculate attendance statistics */
  const name = this.getAttribute('data-name');
  const key = this.getAttribute('data-key');
  const main = document.getElementById('main');
  const cont = document.createElement('div');
  const form = createAttendanceRateForm(name, key);
  
  main.innerHTML = '';
  cont.className = 'rate-container';
  
  main.appendChild(cont);
  
  const h1 = document.createElement('h1');
  h1.id = 'rate-header';
  h1.innerHTML = name + ' Attendance Rate';
    
  const stat = document.createElement('h1');
  stat.id = 'stat';
  stat.innerHTML = '';
  
  cont.appendChild(h1);
  cont.appendChild(form);
  cont.appendChild(stat);
  cont.appendChild(createButton(name, key, 'back-to-roster', 'Back to Roster', setupRoster));
  
  $('#date-start-picker').datepicker().datepicker("setDate", new Date());
  $('#date-end-picker').datepicker().datepicker("setDate", new Date());
}


function createAttendanceRateForm(name, key) {
  /* create day of week and date range options for attendance stats */
  const form = document.createElement('div');
  form.className = 'rate-form';
  
  const daysTitle = document.createElement('div');
  daysTitle.className = 'days-title';
  daysTitle.innerHTML = 'Select Days of the Week:';
  const daysGroup = document.createElement('div');
  daysGroup.className = 'days';
  const dayNames = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'];

  for (let d of dayNames) {
    const check = document.createElement('input');
    check.type = "checkbox";
    check.checked = false;
    check.id = 'check-' + d;
    const label = document.createElement('label');
    label.htmlFor = check.id;
    label.innerHTML = d;

    daysGroup.appendChild(check);
    daysGroup.appendChild(label);
  }

  form.appendChild(daysTitle);
  form.appendChild(daysGroup);
  
  const datesTitle = document.createElement('div');
  datesTitle.className = 'dates-title';
  datesTitle.innerHTML = 'Choose Date Range:';
  const datesPickers = document.createElement('div');
  datesPickers.className = 'dates-pickers';
  datesPickers.appendChild(createDatepicker('date-start'));
  const pTo = document.createElement('div');
  pTo.id = "dates-to";
  pTo.innerHTML = 'to';
  datesPickers.appendChild(pTo);
  datesPickers.appendChild(createDatepicker('date-end'));

  form.appendChild(datesTitle);
  form.appendChild(datesPickers);

  form.appendChild(createButton(name, key, 'calc-button', 'Calculate', getAttendanceStatistic));

  return form;
}

function getAttendanceStatistic() {
  /* get the attendance rate from the api based on the selections */
  const statHeader = document.getElementById('stat');

  const days = document.getElementsByClassName('days')[0];
  var dayStr = '';

  for (let node of days.childNodes) {
    if (node.nodeName === 'INPUT') {
      dayStr += node.checked ? '1' : '0';
    }
  }

  const data = {
    start: getDateString('date-start-picker'),
    end: getDateString('date-end-picker'),
    class: this.getAttribute('data-key'),
    days: dayStr
  };

  $.get(url + 'rate',
    data,
    function(response) {
      statHeader.innerHTML = response.rate + '\%';
    }
  );
}

function createDatepicker(id) {
  /* create datepicker with given id*/
  const div = document.createElement('div');
  div.id = id;
  const datepicker = document.createElement('input');
  datepicker.type = 'text';
  datepicker.id = id + '-picker';
  const label = document.createElement('label');
  label.htmlFor = id + '-picker';
  label.innerHTML = '<i class="material-icons">date_range</i>';

  div.appendChild(datepicker);
  div.appendChild(label);

  return div;
}

function createRosterTable(data) {
  /* create table for class page */
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
    tdIn.appendChild(createRosterCheckbox(d.in, "in", d.key));

    let tdOut = document.createElement('td');
    tdOut.appendChild(createRosterCheckbox(d.out, "out", d.key));

    row.appendChild(tdName);
    row.appendChild(tdIn);
    row.appendChild(tdOut);

    table.appendChild(row);
  }

  return table;
}

function createWhosHereTable(data) {
  /* create table for who's here page */
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
  /* create link to student profile */
  const link = document.createElement('a');
  link.innerHTML = data.name;
  link.className = 'link';
  link.dataset.key = data.key;
  link.onclick = setupStudentPage;
  return link;
}

function createRosterCheckbox(checked, inOrOut, key) {
  /* create sign in and sign out checkboxes */
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

function signStudentIn() {
  /* use API to update student sign in */
  console.log('sign in - ' + this.getAttribute('data-key') + ' - ' + this.checked);
}

function signStudentOut() {
  /* use API to update student sign out */
  console.log('sign out - ' + this.getAttribute('data-key') + ' - ' + this.checked);
}

function setupStudentPage() {
  /* set up student profile page */
  const key = this.getAttribute('data-key');
  $.get(url + 'student',
    {student: key},
    function(data) {
      const main = document.getElementById('main');
      main.innerHTML = '';
      main.appendChild(createStudentProfile(data));
    }
  );
}

function createStudentProfile(data) {
  /* create divs for student profile */
  const cont = createDiv('', 'student-container');

  cont.appendChild(createBasicInfo(data)); 
  cont.appendChild(createOtherInfo(data));

  return cont;
}

function createBasicInfo(data) {
  /* create image, name, and date of birth */
  console.log(data);

  const basic = createDiv('', 'basic-info');
  const nameAge = createDiv('', 'name-age');

  basic.innerHTML = '<img src=' + 'kelly.jpeg' + '>';

  const nameHead = createNode('h1', '', '', data.name);
  const dob = createNode('p', '', '', 'Date of Birth: ' + data.dob);
  nameAge.appendChild(nameHead);
  nameAge.appendChild(dob);

  basic.appendChild(nameAge);

  return basic;
}

function createOtherInfo(data) {
  /* create enrolled classes, sign out info, and emergency info */
  const other = createDiv('', 'other-info');
  
  const classes = createDiv('enrolled-classes', 'student-other-card');
  const signOut = createDiv('sign-out-rules', 'student-other-card');
  const emergency = createDiv('emergency-info', 'student-other-card');

  const classesHead = createNode('div', '', 'student-other-header', 'Enrolled Classes');
  const classesInfo = createNode('div', '', 'student-other-info', data.classes.join('<br>'));
  classes.appendChild(classesHead);
  classes.appendChild(classesInfo);

  const signoutHead = createNode('div', '', 'student-other-header', 'Sign Out Information');
  const signoutInfo = createNode('div', '', 'student-other-info', data.signout.join('<br>'));
  signOut.appendChild(signoutHead);
  signOut.appendChild(signoutInfo);
  
  const emergencyHead = createNode('div', '', 'student-other-header', 'Emergency Contacts');
  const info = data.emergency.map((d) => d.name + ': ' +  d.number);
  const emergencyInfo = createNode('div', '', 'student-other-info', info.join('<br>'));
  emergency.appendChild(emergencyHead);
  emergency.appendChild(emergencyInfo);

  other.appendChild(emergency);
  other.appendChild(signOut);
  other.appendChild(classes);

  return other;
}
