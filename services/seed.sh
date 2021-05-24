echo "
  PRAGMA foreign_keys = ON;

  DELETE FROM departments;
  DELETE FROM admins;

  INSERT INTO departments (name, country, city, address, department_manager)
  VALUES
    ('first', 'Ukraine', 'Kharkov', 'st.23 August, 33', 'Anton Bodiak'),
    ('second', 'USA', 'New York', '275 7th Ave', 'Thomas Edison'),
    ('third', 'Poland', 'Warszawa', 'Grzybowska, 62', 'Gabriel Fahrenheit'),
    ('fourth', 'Russia', 'Moscow', 'st.9th Radial, 2', 'Yuri Gagarin'),
    ('fifth', 'Denmark', 'Copenhagen', 'Frederiksberggade, 11', 'Ole Kirk Christiansen');

  INSERT INTO employees (department_id, first_name, last_name, gender, age, position, salary)
  VALUES
    (1, 'Anton', 'Bodiak', 'Male', '31', 'Department manager', 5200),
    (1, 'Anna', 'Bodiak', 'Female', '19', 'Designer', 800),
    (2, 'Vladimir', 'Vrublevskiy', 'Male', '19', 'Junior dev', 1600),
    (2, 'Thomas', 'Edison', 'Male', '35', 'Department manager', 11000),
    (3, 'Gabriel', 'Fahrenheit', 'Male', '35', 'Department manager', 5500),
    (3, 'Nadin', 'Freshman', 'Female', '20', 'Middle dev', 1500),
    (3, 'Danil', 'Freshman', 'Male', '26', 'Senior dev', 1200),
    (3, 'Danil', 'Buli', 'Male', '21', 'Security', 400),
    (4, 'Yuri', 'Gagarin', 'Male', '38', 'Department manager', 5000),
    (4, 'Vladislav', 'Kipyatkov', 'Male', '20', 'Junior dev', 800),
    (4, 'Boris', 'Borisov', 'Male', '22', 'Middle developer', 1300),
    (4, 'Zhanna', 'Terpilova', 'Female', '20', 'HR', 600),
    (4, 'Danone', 'Chudo', 'Male', '20', 'Dadnone', 5000),
    (5, 'Ole Kirk', 'Christiansen', 'Male', '42', 'Department manager', 10000);

    INSERT INTO admins (user_id, name, email, profile_pic)
    VALUES
      ('106994613627336821261', 'Вова', 'vrublevskiy.2015@gmail.com', 'https://lh3.googleusercontent.com/a-/AOh14Gh3VL_6WyoakytCtCyTUkg-sechWE8TgH_Q1Z1llQ=s96-c');

" | sqlite3 ../db.db