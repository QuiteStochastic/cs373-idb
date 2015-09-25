delete from membership *;
delete from participant *;
delete from party *;
delete from visitor *;
delete from organization *;
delete from character *;
delete from event *;
delete from location *;
delete from episode *;

copy character from '/code/raw_data/character.csv' delimiter ',' csv;
copy location from '/code/raw_data/location.csv' delimiter ',' csv;
copy organization from '/code/raw_data/organization.csv' delimiter ',' csv;
copy episode from '/code/raw_data/episode.csv' delimiter ',' csv;
copy event from '/code/raw_data/event.csv' delimiter ',' csv;
copy membership from '/code/raw_data/member.csv' delimiter ',' csv;
copy participant from '/code/raw_data/participant.csv' delimiter ',' csv;
copy party from '/code/raw_data/party.csv' delimiter ',' csv;
copy visitor from '/code/raw_data/visitor.csv' delimiter ',' csv;

