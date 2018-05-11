const url = 'http://0.0.0.0:5000/';

function start() {
  setupDatepickerAndClasses();
  setupPeopleTable('whois-button', 'whoshere', "Who's here?");
  setupPeopleTable('directory-button', 'directory', 'All Students');
  setupSearchBar();
};

start();

function getDateString(id) {
  /* return the data as a string from the dakerpicker with the specified id */
  return $('#' + id).datepicker('getDate').toJSON().substr(0,10);
}

function createButton(name, key, className, text, clickFcn) {
  /* creates a button with the specified properties */
  const btn = document.createElement('button');
  btn.className = className;
  btn.dataset.key = key;
  btn.dataset.name = name;
  btn.innerHTML = text;
  btn.onclick = clickFcn;
  return btn;
}

function createNode(kind, id, className, inner) {
  /* creates an element with the specified properties */
  const node = document.createElement(kind);
  if (id) node.id = id;
  if (className) node.className = className;
  if (inner) node.innerHTML = inner;
  return node;
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
  const date = getDateString('datepicker');
  $.get(url + 'classes',
    {date: date},
    function(data) {
      const buttonDiv = document.getElementById('classes');
      buttonDiv.innerHTML = '';

      for (let d of data) {
        const btn = createButton(d.name, d.key,
          'class-button nav-button', d.name, setupRoster);
        btn.dataset.date = date;
        buttonDiv.appendChild(btn);
      }
    }
  );
}

function setupSearchBar() {
  $.get(url + 'directory',
    function(data) {
      let tags = [];
      for (var d of data) {
        let name = d.firstName + ' ' + d.lastName;
        tags.push({label: name, value: d.key});
      }

      $('.search').autocomplete({
        source: tags,
        select: function (e, ui) {
          $('.search').val(ui.item.label);
          setupStudentPage(ui.item.value);
          return false;
        }
      });
    });
}

function setupPeopleTable(className, path, header) {
  /* when the user clicks the who's here or all student buttons,
   * then create the appropriate page */
  const btn = document.getElementsByClassName(className)[0];

  btn.onclick = function() {
    $.get(url + path,
      function(data) {
        const main = document.getElementById('main');
        const cont = document.createElement('div');
        const h1 = document.createElement('h1');
        h1.innerHTML = header;
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
  const date = this.getAttribute("data-date");
  const dateSplit = date.split('-');
  const classKey = this.getAttribute("data-key");
  const className = this.getAttribute("data-name");
  // use the api to get the class info for this day
  $.get(url + 'roster',
    {date: date, class: classKey},
    function(data) {
      const main = document.getElementById('main');
      const cont = document.createElement('div');
      const h1 = document.createElement('h1');
      const h3 = document.createElement('h3');
      
      main.innerHTML = '';
      cont.className = 'table-container';
      h1.innerHTML = className;
      h3.innerHTML = dateSplit[1] + '/' + dateSplit[2] + '/' + dateSplit[0];

      main.appendChild(cont);
      cont.appendChild(h1);
      const btn = createButton(className, classKey, 'go-to-rate',
        'Attendance Rate Info', setupAttendanceRatePage);
      btn.dataset.date = date;
      cont.appendChild(btn);
      cont.appendChild(h3);

      if (className === 'Tutoring') {
        cont.appendChild(createTutorRosterTable(data));
      } else {
        cont.appendChild(createRosterTable(data));
      }
    }
  );
}

function setupAttendanceRatePage() {
  /* set up page to allow user to calculate attendance statistics */
  const name = this.getAttribute('data-name');
  const key = this.getAttribute('data-key');
  const date = this.getAttribute('data-date');
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
  const btn = createButton(name, key, 'back-to-roster',
    'Back to Roster', setupRoster);
  btn.dataset.date = date;
  cont.appendChild(btn);
  
  $('#date-start-picker').datepicker()
    .datepicker("setDate", $.datepicker.parseDate("yy-mm-dd", date));
  $('#date-end-picker').datepicker()
    .datepicker("setDate", $.datepicker.parseDate("yy-mm-dd", date));
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

  form.appendChild(createButton(name, key, 'calc-button',
    'Calculate Attendance Rate', getAttendanceStatistic));

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
    table.appendChild(createStudentRow(d, false));
  }

  return table;
}

function createStudentRow(d, forTutorTable) {
  /* create table row for a student */
  let row = document.createElement('tr');

  let tdName = document.createElement('td');
  tdName.appendChild(createStudentLink(d));

  let tdIn = document.createElement('td');
  tdIn.appendChild(createRosterCheckbox(d.in, "in", d.key));

  let tdOut = document.createElement('td');
  tdOut.appendChild(createRosterCheckbox(d.out, "out", d.key));

  if (forTutorTable)
    row.appendChild(document.createElement('tr'));

  row.appendChild(tdName);
  row.appendChild(tdIn);
  row.appendChild(tdOut);

  return row;
}

function createTutorRosterTable(data) {
  /* create table for class page */
  const table = document.createElement('table');
  table.className = 'tutor-table';
  const headRow = document.createElement('tr');
  headRow.innerHTML = '<th></th><th>Name</th><th>Sign In</th><th>Sign Out</th>'
  headRow.firstChild.appendChild(createButton('', '', 'expand-all', '+', function() {
      this.innerHTML = this.innerHTML === '+' ? '-' : '+';
      const btsn = document.getElementsByClassName('expand-button');
      for (let b of btsn) {
        if (b.innerHTML !== this.innerHTML) {
          b.click();
        }
      }
    }));
  table.appendChild(headRow);

  for (let d of data) {
    let row = document.createElement('tr');

    let tdExpand = document.createElement('td');
    tdExpand.className = 'expand-cell';
    let expandBtn = createButton('', '', 'expand-button', '+', function(){
      this.innerHTML = this.innerHTML === '+' ? '-' : '+';
      const color = $(this).parent().parent().css('background-color');
      $(this).parent().parent().nextUntil('tr.tutor-row')
        .css('display', function() {
          return this.style.display === 'table-row' ? 'none' : 'table-row';
        })
        .css('background-color', color);
    });
    tdExpand.appendChild(expandBtn);

    let tdName = document.createElement('td');
    tdName.appendChild(createTutorLink(d));

    let tdIn = document.createElement('td');
    tdIn.appendChild(createRosterCheckbox(d.in, "in", d.key));

    let tdOut = document.createElement('td');

    row.appendChild(tdExpand);
    row.appendChild(tdName);
    row.appendChild(tdIn);
    row.appendChild(tdOut);
    row.className = 'tutor-row';

    table.appendChild(row);

    for (let s of d.students) {
      let r = createStudentRow(s, true);
      r.className = 'student-row';
      table.appendChild(r);
    }
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
  link.innerHTML = data.firstName + ' ' + data.lastName;
  link.className = 'link';
  link.dataset.key = data.key;
  link.onclick = function() {
    setupStudentPage(data.key);
  };
  return link;
}

function createTutorLink(data) {
  /* create link to tutor profile */
  const link = document.createElement('a');
  link.innerHTML = data.firstName + ' ' + data.lastName;
  link.className = 'link';
  link.dataset.key = data.key;
  link.onclick = function() {
    setupTutorPage(data.key);
  };
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
  console.log('sign in ' + this.getAttribute('data-key') + ' ' + this.checked);
}

function signStudentOut() {
  /* use API to update student sign out */
  console.log('sign out ' + this.getAttribute('data-key') + ' ' + this.checked);
}

function setupStudentPage(key) {
  /* set up student profile page */
  $.get(url + 'student',
    {student: key},
    function(data) {
      const main = document.getElementById('main');
      main.innerHTML = '';
      main.appendChild(createProfile(data, true));
    }
  );
}

function setupTutorPage(key) {
  /* set up tutor profile page */
  $.get(url + 'tutor',
    {tutor: key},
    function(data) {
      const main = document.getElementById('main');
      main.innerHTML = '';
      main.appendChild(createProfile(data, false));
    }
  );
}

function createProfile(data, isStudent) {
  /* create divs for student or tutor profile */
  const cont = createNode('div', '', 'profile-container', '');

  cont.appendChild(createBasicInfo(data, isStudent)); 
  cont.appendChild(createOtherInfo(data, isStudent));

  return cont;
}

function createBasicInfo(data, isStudent) {
  /* create image, name, and date of birth */

  const basic = createNode('div', '', 'basic-info', '');
  const nameAge = createNode('div', '', 'name-age', '');

  if (data.firstName === 'Tanya')
    basic.innerHTML = '<img src=' + 'images/tanya.jpg' + '>';
  else if (data.firstName === 'Doug')
    basic.innerHTML = '<img src=' + 'images/doug.jpg' + '>';
  else
    basic.innerHTML = '<img src=' + 'images/kelly.jpeg' + '>';

  const nameHead = createNode('h1', '', '',
    data.firstName + ' ' + data.lastName);
  nameAge.appendChild(nameHead);

  if (isStudent) {
    const dob = createNode('p', '', '', 'Date of Birth: ' + data.dob);
    nameAge.appendChild(dob);
  }

  basic.appendChild(nameAge);

  return basic;
}

function createOtherInfo(data, isStudent) {
  /* create enrolled classes, sign out info, and emergency info for students
   * create students, tutoring days, and contact information for tutors */
  const other = createNode('div', '', 'other-info', '');

  const first = createNode('div', '', 'profile-other-card', '');
  const second = createNode('div', '', 'profile-other-card', '');
  const third = createNode('div', '', 'profile-other-card', '');

  const firstHead = createNode('div', '', 'profile-other-header',
    isStudent ? 'Enrolled Classes' : 'Tutor Days');
  const firstInfo = createNode('div', '', 'profile-other-info',
    isStudent ? data.classes.join('<br>') : data.days.join('<br>'));
  first.appendChild(firstHead);
  first.appendChild(firstInfo);

  const secondHead = createNode('div', '', 'profile-other-header',
    isStudent ? 'Sign Out Information' : 'Students');
  const secondInfo = createNode('div', '', 'profile-other-info', '');
  if (isStudent) {
    secondInfo.innerHTML = data.signout.join('<br>');
  } else {
    for (let s of data.students) {
      secondInfo.appendChild(createStudentLink(s));
      secondInfo.appendChild(createNode('br', '', '', ''));
    }
  }
  second.appendChild(secondHead);
  second.appendChild(secondInfo);

  const thirdHead = createNode('div', '', 'profile-other-header',
    isStudent ? 'Emergency Contacts' : 'Contact');

  let info = [];
  if (isStudent) {
    info = data.emergency.map((d) => d.name + ': ' +  d.number);
  } else {
    info = ['Email: ' + data.email, 'Phone: ' + data.phone];
  }
  const thirdInfo = createNode('div', '',
    'profile-other-info', info.join('<br>'));
  third.appendChild(thirdHead);
  third.appendChild(thirdInfo);

  other.appendChild(third);
  other.appendChild(second);
  other.appendChild(first);

  return other;
}
