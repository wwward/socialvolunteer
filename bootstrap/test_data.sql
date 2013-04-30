INSERT INTO Volunteer VALUES ('1', 'Bob Smith', '(111)111-1111', 'New York, NY', '', 111, 1, 'bob1');
INSERT INTO Volunteer VALUES ('2', 'Jane Doe', '(222)222-2222', 'New York, NY', '', 222, 1, 'jane2');
INSERT INTO Volunteer VALUES ('3', 'Jim Brown', '(333)333-3333', 'Philadelphia, PA', '', 333, 1, 'jim3');
INSERT INTO Volunteer VALUES ('4', 'Jill Hill', '(444)444-4444', 'San Diego, CA', '',444, 1, 'jill44');
INSERT INTO Volunteer VALUES ('5', 'Santa Claus', '(555)555-5555', 'North Pole, NP', '', 555, 1, 'santa5');
INSERT INTO Friends VALUES ('1', '2');
INSERT INTO Friends VALUES ('2', '1');
INSERT INTO Friends VALUES ('1', '5');
INSERT INTO Friends VALUES ('2', '5');
INSERT INTO Friends VALUES ('3', '5');
INSERT INTO Friends VALUES ('4', '5');
INSERT INTO Friends VALUES ('4', '3');
INSERT INTO Friends VALUES ('5', '3');
INSERT INTO Organization VALUES ('11', 'Good Deeds & Co.', '(111)100-1000', 'New York, NY', 1, 'We do all sorts of good stuff');
INSERT INTO Organization VALUES ('22', 'Kittens R\' US', '(222)200-2000', 'New York, NY', 1, 'All kittens are final sale!');
INSERT INTO Organization VALUES ('33', 'ShamCo.', '(333)300-3000', 'Philadelphia, PA', 1, 'This is not a scam.');
INSERT INTO Job VALUES ('100', '11', '2013-5-04', '18:00:00', 120, 120, 'Crosswalk guard! Help grandmothers cross the street after bingo', 'Elderly', 1);
INSERT INTO Job VALUES ('101', '11', '2013-4-14', '01:00:00', 30, 30, 'Feed Grandpa', 'Elderly', 0);
INSERT INTO Job VALUES ('102', '11', '2013-5-11', '12:00:00', 60, 60, 'Change litter boxes at animal shelter', 'Animals', 1);
INSERT INTO Job VALUES ('103', '11', '2013-5-01', '00:00:00', 60, 60, 'Hand out water at a race at the local park', 'Fitness', 1);
INSERT INTO Job VALUES ('200', '22', '2013-5-21', '07:30:00', 120, 60, 'Pet the kittens', 'Animals', 1);
INSERT INTO Job VALUES ('201', '22', '2013-4-13', '16:00:00', 60, 60, 'Feed the kittens', 'Animals', 0);
INSERT INTO Job VALUES ('202', '22', '2013-5-03', '20:10:00', 30, 60, 'Walk the kittens', 'Animals', 1);
INSERT INTO Job VALUES ('300', '33', '2013-5-07', '19:45:00', 60, 60, 'Sell kidneys on the street corner! These are legit kidneys. Seriously. Totally legit.', 'Elderly', 1);
INSERT INTO Job VALUES ('301', '33', '2013-5-18', '02:00:00', 30, 60, 'Borrow gems from the jewelry store. Then run like hell.', 'Fitness', 0);
INSERT INTO Job VALUES ('302', '33', '2013-4-24', '06:00:00', 60, 60, 'Boxing match with local police force! Help keep our boys in blue in top shape!', 'Fitness', 1);
INSERT INTO Job VALUES ('303', '33', '2013-5-03', '19:00:00', 60, 60, 'So this guy I know, he owes us some money. And like, we need you to convince him that we need our money back.', 'Community', 1);
INSERT INTO Keyword VALUES ('grandparent', '100');
INSERT INTO Keyword VALUES ('grandpa', '100');
INSERT INTO Keyword VALUES ('crosswalk', '100');
INSERT INTO Keyword VALUES ('grandparent', '101');
INSERT INTO Keyword VALUES ('grandpa', '101');
INSERT INTO Keyword VALUES ('food', '101');
INSERT INTO Keyword VALUES ('feeding', '101');
INSERT INTO Keyword VALUES ('animals', '102');
INSERT INTO Keyword VALUES ('kittens', '102');
INSERT INTO Keyword VALUES ('litterbox', '102');
INSERT INTO Keyword VALUES ('shelter', '102');
INSERT INTO Keyword VALUES ('cleaning', '102');
INSERT INTO Keyword VALUES ('water', '103');
INSERT INTO Keyword VALUES ('running', '103');
INSERT INTO Keyword VALUES ('race', '103');
INSERT INTO Keyword VALUES ('kittens', '200');
INSERT INTO Keyword VALUES ('pet', '200');
INSERT INTO Keyword VALUES ('kittens', '201');
INSERT INTO Keyword VALUES ('feeding', '201');
INSERT INTO Keyword VALUES ('food', '201');
INSERT INTO Keyword VALUES ('kittens', '202');
INSERT INTO Keyword VALUES ('walk', '202');
INSERT INTO Keyword VALUES ('sales', '300');
INSERT INTO Keyword VALUES ('kidney', '300');
INSERT INTO Keyword VALUES ('crosswalk', '300');
INSERT INTO Keyword VALUES ('legit', '300');
INSERT INTO Keyword VALUES ('legit', '301');
INSERT INTO Keyword VALUES ('gems', '301');
INSERT INTO Keyword VALUES ('jewelry', '301');
INSERT INTO Keyword VALUES ('running', '301');
INSERT INTO Keyword VALUES ('borrow', '301');
INSERT INTO Keyword VALUES ('legit', '302');
INSERT INTO Keyword VALUES ('boxing', '302');
INSERT INTO Keyword VALUES ('police', '302');
INSERT INTO Keyword VALUES ('legit', '303');
INSERT INTO Keyword VALUES ('money', '303');
INSERT INTO Keyword VALUES ('boxing', '303');
INSERT INTO Keyword VALUES ('collection', '303');
INSERT INTO Keyword VALUES ('community', '303');
INSERT INTO Job_volunteer VALUES ('100', '1', 1, 0, 0, 0);
INSERT INTO Job_volunteer VALUES ('201', '1', 1, 0, 1, 0);
INSERT INTO Job_volunteer VALUES ('202', '1', 1, 1, 1, 1);
INSERT INTO Job_volunteer VALUES ('200', '2', 1, 1, 1, 1);
INSERT INTO Job_volunteer VALUES ('201', '2', 1, 1, 1, 1);
INSERT INTO Job_volunteer VALUES ('202', '2', 1, 1, 1, 1);
INSERT INTO Job_volunteer VALUES ('300', '2', 1, 0, 1, 0);
INSERT INTO Job_volunteer VALUES ('300', '3', 1, 0, 0, 0);
INSERT INTO Job_volunteer VALUES ('301', '3', 1, 0, 0, 0);
INSERT INTO Job_volunteer VALUES ('302', '3', 1, 0, 0, 0);
INSERT INTO Job_volunteer VALUES ('303', '3', 1, 0, 0, 0);
INSERT INTO Job_volunteer VALUES ('303', '4', 1, 0, 1, 0);
INSERT INTO Job_volunteer VALUES ('301', '4', 1, 1, 1, 1);
INSERT INTO Job_volunteer VALUES ('201', '4', 1, 0, 0, 0);
INSERT INTO Job_volunteer VALUES ('100', '5', 1, 1, 1, 1);
INSERT INTO Job_volunteer VALUES ('101', '5', 1, 1, 1, 1);
INSERT INTO Job_volunteer VALUES ('102', '5', 1, 1, 1, 1);
INSERT INTO Job_volunteer VALUES ('103', '5', 1, 1, 1, 1);
INSERT INTO Job_volunteer VALUES ('201', '5', 1, 0, 1, 0);







