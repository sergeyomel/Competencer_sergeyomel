CREATE DATABASE test_db_1
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'ru_RU.UTF-8'
    LC_CTYPE = 'ru_RU.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;


CREATE TABLE locations (
	location_id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	country varchar(100),
	city varchar(100),
	street varchar(100)
);

CREATE TABLE companies (
	company_id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	company_name varchar(150)
);

create table company_locations (
	company_location_id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	company_id int not null,
	location_id int not null,
	CONSTRAINT fk_company_companies FOREIGN KEY (company_id) references companies (company_id),
	CONSTRAINT fk_location_locations FOREIGN KEY (location_id) references locations (location_id)
);

create table resources (
	resource_id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	title varchar(100) not null
);

create table experiences (
	experience_id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	exp_min varchar(5),
	exp_max varchar(5)
);

create table salaries (
	salary_id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	lower_threshold varchar(10),
	upper_threshold varchar(10)
);

create table skills (
	skill_id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	title varchar(100) not null
);

create table responsibilities (
	responsibility_id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	title varchar(250)
);

create table vacancies (
	vacancy_id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	platform_id varchar(50),
	title varchar(150)
);

create table necessary_skills (
	skill_id int not null,
	vacancy_id int not null,
	primary key (skill_id, vacancy_id),
	CONSTRAINT fk_skill_necessary_skill FOREIGN KEY (skill_id) references skills (skill_id),
	CONSTRAINT fk_vacancy_necessary_skill FOREIGN KEY (vacancy_id) references vacancies (vacancy_id)
);

create table extra_skills (
	skill_id int not null,
	vacancy_id int not null,
	primary key (skill_id, vacancy_id),
	CONSTRAINT fk_skill_extra_skill FOREIGN KEY (skill_id) references skills (skill_id),
	CONSTRAINT fk_vacancy_extra_skill FOREIGN KEY (vacancy_id) references vacancies (vacancy_id)
);

create table key_skills (
	skill_id int not null,
	vacancy_id int not null,
	primary key(skill_id, vacancy_id),
	CONSTRAINT fk_skill_key_skill FOREIGN KEY (skill_id) references skills (skill_id),
	CONSTRAINT fk_vacancy_key_skill FOREIGN KEY (vacancy_id) references vacancies (vacancy_id)
);

create table vacancy_responsibilities (
	responsibility_id int not null,
	vacancy_id int not null,
	primary key (responsibility_id, vacancy_id),
	CONSTRAINT fk_responsibility_vacancy_responsibility FOREIGN KEY (responsibility_id) references responsibilities (responsibility_id),
	CONSTRAINT fk_vacancy_key_skill FOREIGN KEY (vacancy_id) references vacancies (vacancy_id)
);

create table company_vacancies (
	company_vacancy_id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	publication_date timestamp not null,
	description varchar(1000),
	company_id int not null,
	experience_id int not null,
	salary_id int not null,
	vacancy_id int not null,
	CONSTRAINT fk_company_company_vacancies FOREIGN KEY (company_id) references companies (company_id),
	CONSTRAINT fk_experience_company_vacancies FOREIGN KEY (experience_id) references experiences (experience_id),
	CONSTRAINT fk_salary_company_vacancies FOREIGN KEY (salary_id) references salaries (salary_id),
	CONSTRAINT fk_vacancy_company_vacancies FOREIGN KEY (vacancy_id) references vacancies (vacancy_id)
);

create table parsings (
	parsing_id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	resource_parsing_id int not null,
	parsing_date timestamp not null,
	company_vacancy_id int not null,
	CONSTRAINT fk_resource_parsing FOREIGN KEY (resource_parsing_id) references resources (resource_id),
	CONSTRAINT fk_company_vacancy FOREIGN KEY (company_vacancy_id) references company_vacancies (company_vacancy_id)
);

insert into resources (title) values ('hh');
insert into resources (title) values ('linkedin');
insert into resources (title) values ('indeed');