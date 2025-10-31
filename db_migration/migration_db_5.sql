alter table certificates add column  fingerprintSHA256 text ;
alter table certificates add column  not_before timestamp ;
alter table certificates add column  parent_fingerprintSHA256 text ;
alter table hosts add column  fingerprintSHA256 text ;

