CREATE DATABASE jobexploresdb
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Russian_Russia.1251'
    LC_CTYPE = 'Russian_Russia.1251'
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
	title varchar(150),
	location_company int NOT NULL DEFAULT 1,
	CONSTRAINT fk_location_company FOREIGN KEY (location_company) references locations (location_id)
);

create table resources (
	resource_id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	title varchar(100) not null
);

create table parsings (
	parsing_id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	resource_parsing int not null,
	parsing_date timestamp not null,
	CONSTRAINT fk_resource_parsing FOREIGN KEY (resource_parsing) references resources (resource_id)
);

create table experiences (
	experience_id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	experience int not null CHECK (experience >= 0)
);

create table salaries (
	salary_id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	lower_threshold int CHECK (lower_threshold >= 0),
	upper_threshold int CHECK (upper_threshold >= 0)
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
	title varchar(150)
);

create table necessary_skills (
	skill int not null,
	vacancy int not null,
	primary key (skill, vacancy),
	CONSTRAINT fk_skill_necessary_skill FOREIGN KEY (skill) references skills (skill_id),
	CONSTRAINT fk_vacancy_necessary_skill FOREIGN KEY (vacancy) references vacancies (vacancy_id)
);

create table extra_skills (
	skill int not null,
	vacancy int not null,
	primary key (skill, vacancy),
	CONSTRAINT fk_skill_extra_skill FOREIGN KEY (skill) references skills (skill_id),
	CONSTRAINT fk_vacancy_extra_skill FOREIGN KEY (vacancy) references vacancies (vacancy_id)
);

create table key_skills (
	skill int not null,
	vacancy int not null,
	primary key(skill, vacancy),
	CONSTRAINT fk_skill_key_skill FOREIGN KEY (skill) references skills (skill_id),
	CONSTRAINT fk_vacancy_key_skill FOREIGN KEY (vacancy) references vacancies (vacancy_id)
);

create table vacancy_responsibilities (
	responsibility int not null,
	vacancy int not null,
	primary key (responsibility, vacancy),
	CONSTRAINT fk_responsibility_vacancy_responsibility FOREIGN KEY (responsibility) references responsibilities (responsibility_id),
	CONSTRAINT fk_vacancy_key_skill FOREIGN KEY (vacancy) references vacancies (vacancy_id)
);

create table company_vacancies (
	company_vacanci_id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	publication_date timestamp not null,
	description varchar(1000),
	company int not null,
	experience int not null,
	salary int not null,
	vacancy int not null,
	CONSTRAINT fk_company_company_vacancies FOREIGN KEY (company) references companies (company_id),
	CONSTRAINT fk_experience_company_vacancies FOREIGN KEY (experience) references experiences (experience_id),
	CONSTRAINT fk_salary_company_vacancies FOREIGN KEY (salary) references salaries (salary_id),
	CONSTRAINT fk_vacancy_company_vacancies FOREIGN KEY (vacancy) references vacancies (vacancy_id)
);











