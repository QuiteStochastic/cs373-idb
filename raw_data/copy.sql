delete from membership *;
delete from participant *;
delete from party *;
delete from visitor *;
delete from organization *;
delete from character *;
delete from event *;
delete from location *;
delete from episode *;

copy character from '/home/ubuntu/cs373-idb/raw_data/character.csv' delimiter ',' csv;
copy location from '/home/ubuntu/cs373-idb/raw_data/location.csv' delimiter ',' csv;
copy organization from '/home/ubuntu/cs373-idb/raw_data/organization.csv' delimiter ',' csv;
copy episode from '/home/ubuntu/cs373-idb/raw_data/episode.csv' delimiter ',' csv;
copy event from '/home/ubuntu/cs373-idb/raw_data/event.csv' delimiter ',' csv;
copy membership from '/home/ubuntu/cs373-idb/raw_data/member.csv' delimiter ',' csv;
copy participant from '/home/ubuntu/cs373-idb/raw_data/participant.csv' delimiter ',' csv;
copy party from '/home/ubuntu/cs373-idb/raw_data/party.csv' delimiter ',' csv;
copy visitor from '/home/ubuntu/cs373-idb/raw_data/visitor.csv' delimiter ',' csv;

