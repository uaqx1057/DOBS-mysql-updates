
COPY public."user" (id, username, password, role, name, designation, branch_city, email) FROM stdin;
10	kashif	$2a$06$eSxuy4p.DMRE.guvhOpCT.8Xi2UyQIYAedU0dwKSpwIY2ag/dfM6W	FleetManager	kashif	fleat manager	Dammam	kashif@gmail.com
11	asif	$2a$06$wOVks9c9j2ODfsk6UleTieBys9t9VACxT.nLaJbkf34PIQq4ECSB2	FinanceManager	asif	asif	Dammam	asif@gmail.com
7	usama	pbkdf2:sha256:260000$GG9mqCnKBNmlhGkQ$1693ae1fcdef1daac935cb0a60026a7deb8b5ebed4039c5725355543bdb5131f	HR	usama	IT manager	Dammam	usama@gmail.com
12	usman	pbkdf2:sha256:260000$yS3J1fi2gsssSZYA$15c16cc5d066c421e13cb1d8f930e8ee20651e7acd220876e28e93e0366dbae2	OpsManager	usman	dev	Dammam	usman@gmail.com
9	ahmed	pbkdf2:sha256:260000$QqGuFEEmEminBavH$c259730afd154fe1632f75238dffe09fca24ebce5b1da9b17a77c1ed08c3cf27	OpsSupervisor	ahmed	dummy	Dammam	ahmed@gmail.com
1	superadmin	pbkdf2:sha256:260000$yYKP6YbqwW5xduZo$32780dacf73b1330c5cbd335240e7b8ab6324e9e452c73e24eab3db6f0a10cba	SuperAdmin	\N	\N	\N	dobsykjq_admin@example.com
\.

